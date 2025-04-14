# Firecrawl Deep Research MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a Model Context Protocol (MCP) server specifically designed to provide Firecrawl's powerful Deep Research capabilities to compatible Large Language Model (LLM) clients like Cursor, Claude, and others. It is a specialized version adapted from the official [mendableai/firecrawl-mcp-server](https://github.com/mendableai/firecrawl-mcp-server).

This server allows LLMs to perform in-depth web research on a given query by intelligently crawling, searching, and analyzing web content.

## Features

*   Provides the `firecrawl_deep_research` tool via MCP.
*   Leverages Firecrawl's API for sophisticated web crawling and data extraction.
*   Handles asynchronous research tasks.
*   Configurable retry logic for API calls.
*   Easy deployment via Docker or local Node.js setup.

## Prerequisites

*   **Node.js:** Version 18.0.0 or higher.
*   **npm:** (Comes with Node.js) or an alternative package manager like pnpm.
*   **Docker:** (Optional, but recommended for ease of deployment).
*   **Firecrawl API Key:** You need an API key from [Firecrawl.dev](https://firecrawl.dev).

## Environment Variables

Before running the server, you need to configure the necessary environment variables. Create a `.env` file in the `mcp_servers/firecrawl_deep_research` directory by copying `.env.example`:

```bash
cp mcp_servers/firecrawl_deep_research/.env.example mcp_servers/firecrawl_deep_research/.env
```

Then, edit the `.env` file and add your credentials:

*   `FIRECRAWL_API_KEY` (Required): Your Firecrawl API key.
*   `FIRECRAWL_API_URL` (Optional): If you are using a self-hosted Firecrawl instance, uncomment this line and provide the URL. Otherwise, leave it commented to use the default cloud service.
*   `FIRECRAWL_RETRY_MAX_ATTEMPTS` (Optional, Default: 3): Number of retry attempts for rate-limited requests.
*   `FIRECRAWL_RETRY_INITIAL_DELAY` (Optional, Default: 1000): Initial delay before first retry (in milliseconds).
*   `FIRECRAWL_RETRY_MAX_DELAY` (Optional, Default: 10000): Maximum delay between retries (in milliseconds).
*   `FIRECRAWL_RETRY_BACKOFF_FACTOR` (Optional, Default: 2): Multiplier for exponential backoff.

## Running the Server

There are two primary ways to run the server:

### 1. Using Docker (Recommended)

This method encapsulates the application and its dependencies in a container.

1.  **Create `.env` file:** Ensure you have created and configured the `.env` file inside the `mcp_servers/firecrawl_deep_research` directory as described above. The Docker build process will copy this file into the image.
2.  **Build the Docker Image:** Navigate to the **root** directory of the `klavis` project (the parent directory of `mcp_servers`) and run the build command:
    ```bash
    docker build -t firecrawl-deep-research-mcp -f mcp_servers/firecrawl_deep_research/Dockerfile .
    ```
    *   `-t firecrawl-deep-research-mcp`: Tags the image with the name `firecrawl-deep-research-mcp`.
    *   `-f mcp_servers/firecrawl_deep_research/Dockerfile`: Specifies the path to the Dockerfile relative to the build context.
    *   `.`: Specifies the build context (the `klavis` root directory).

3.  **Run the Docker Container:**
    ```bash
    docker run -p 5000:5000 --name firecrawl-server firecrawl-deep-research-mcp
    ```
    *   `-p 5000:5000`: Maps port 5000 on your host machine to port 5000 inside the container (where the server listens).
    *   `--name firecrawl-server`: Assigns a name to the running container for easier management.
    *   `firecrawl-deep-research-mcp`: The name of the image to run.

The server should now be running and accessible on `http://localhost:5000`.

### 2. Using Node.js (Local Development)

This method is suitable for development or environments where Docker is not available.

1.  **Navigate to the Server Directory:**
    ```bash
    cd mcp_servers/firecrawl_deep_research
    ```
2.  **Create `.env` file:** Ensure you have created and configured the `.env` file in this directory as described in the "Environment Variables" section.
3.  **Install Dependencies:**
    ```bash
    npm install
    ```
4.  **Build the TypeScript Code:**
    ```bash
    npm run build
    ```
5.  **Start the Server:**
    ```bash
    npm start
    ```

The server should now be running and accessible on `http://localhost:5000`.

## Usage

Once the server is running (either via Docker or Node.js), LLM clients configured to use MCP can connect to it at `http://localhost:5000` (or the appropriate host/port if deployed elsewhere).

The server exposes the `firecrawl_deep_research` tool. An LLM can invoke this tool with the following arguments:

```json
{
  "name": "firecrawl_deep_research",
  "arguments": {
    "query": "Research question or topic",
    "maxDepth": 3, // Optional: Max crawl/search depth (default: 3)
    "timeLimit": 120, // Optional: Time limit in seconds (default: 120)
    "maxUrls": 50 // Optional: Max URLs to analyze (default: 50)
  }
}
```

The server will then initiate the deep research process using the Firecrawl API and return the final analysis generated by Firecrawl's LLM based on the gathered information.

## Contributing

Contributions are welcome! Please follow standard GitHub practices (fork, branch, submit a pull request). Ensure code quality by running linting and formatting checks:

```bash
# Run linter
npm run lint

# Automatically fix linting issues
npm run lint:fix

# Format code
npm run format
```