# Firecrawl MCP Server

This directory contains a Model Context Protocol (MCP) server for integrating [Firecrawl](https://firecrawl.dev/) capabilities into applications like Klavis, Cursor, Claude, and other LLM clients. It allows leveraging Firecrawl's powerful web scraping, crawling, and data extraction features through a standardized protocol.

This server is based on the official [mendableai/firecrawl-mcp-server](https://github.com/mendableai/firecrawl-mcp-server) and is provided under the MIT license.

## Features

This server exposes the following Firecrawl functionalities as tools:

*   `firecrawl_scrape`: Scrape content from a single URL with advanced options (formats, selectors, main content extraction, JS rendering, etc.).
*   `firecrawl_map`: Discover URLs starting from a given URL using sitemaps and link crawling.
*   `firecrawl_crawl`: Perform an asynchronous crawl starting from a URL, collecting data from multiple pages.
*   `firecrawl_batch_scrape`: Scrape multiple URLs efficiently in parallel.
*   `firecrawl_check_batch_status`: Check the status of an ongoing batch scrape or crawl operation.
*   `firecrawl_search`: Perform a web search using Firecrawl's search capabilities and optionally scrape results.
*   `firecrawl_extract`: Extract structured data from web pages using LLMs based on a provided schema and prompt.
*   `firecrawl_generate_llmstxt`: Generate `llms.txt` and `llms-full.txt` files for a domain to guide LLM interactions.

## Prerequisites

*   **Node.js:** Version 18.0.0 or higher.
*   **npm:** Node Package Manager (usually comes with Node.js).
*   **Docker:** (Recommended) For containerized deployment.
*   **Firecrawl API Key:** Obtainable from [Firecrawl.dev](https://firecrawl.dev/).

## Environment Setup

Before running the server, you need to configure your Firecrawl API credentials.

1.  Copy the example environment file:
    ```bash
    cp mcp_servers/firecrawl/.env.example mcp_servers/firecrawl/.env
    ```
2.  Edit `mcp_servers/firecrawl/.env` and add your Firecrawl API key:
    ```dotenv
    # Firecrawl API credentials
    FIRECRAWL_API_KEY=your-actual-api-key-here

    # --- Optional: For self-hosted Firecrawl instances --- 
    # Uncomment and set if you are NOT using the cloud service
    # FIRECRAWL_API_URL=https://your-self-hosted-firecrawl-url.com 
    # ------

    # --- Optional: Retry configuration --- 
    # You can adjust these values if needed
    # FIRECRAWL_RETRY_MAX_ATTEMPTS=3
    # FIRECRAWL_RETRY_INITIAL_DELAY=1000
    # FIRECRAWL_RETRY_MAX_DELAY=10000
    # FIRECRAWL_RETRY_BACKOFF_FACTOR=2 
    # ------
    ```

*   `FIRECRAWL_API_KEY` (Required): Your API key for the Firecrawl service.
*   `FIRECRAWL_API_URL` (Optional): The URL of your self-hosted Firecrawl instance. Only needed if you are not using the default cloud service.
*   Retry variables (Optional): Control how the server retries requests upon encountering rate limits or transient errors.

*(Note: When using Docker, the `.env` file is automatically copied into the image during the build process as specified in the `Dockerfile`.)*

## Running Locally

There are two primary ways to run the server locally:

### 1. Using Docker (Recommended)

This method packages the server and its dependencies into a container.

1.  **Build the Docker Image:**
    *   Navigate to the root directory of the `klavis` project.
    *   Run the build command:
        ```bash
        # Replace 'firecrawl-mcp-server' with your desired tag
        docker build -t firecrawl-mcp-server -f mcp_servers/firecrawl/Dockerfile .
        ```

2.  **Run the Docker Container:**
    ```bash
    # This runs the server on port 5000
    docker run -p 5000:5000 --env-file mcp_servers/firecrawl/.env firecrawl-mcp-server 
    ```
    *   `-p 5000:5000`: Maps port 5000 on your host machine to port 5000 inside the container.
    *   `--env-file mcp_servers/firecrawl/.env`: Passes the environment variables from your `.env` file to the container.

The server will start, and you should see log output indicating it's running, typically listening on `http://localhost:5000`.

### 2. Using Node.js / npm

This method runs the server directly using your local Node.js environment.

1.  **Navigate to the Server Directory:**
    ```bash
    cd mcp_servers/firecrawl
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Build the Server Code:**
    (This compiles the TypeScript code to JavaScript)
    ```bash
    npm run build
    ```

4.  **Start the Server:**
    ```bash
    npm start
    ```

The server will start using the environment variables defined in `mcp_servers/firecrawl/.env` and listen on port 5000 (or the port specified by the `PORT` environment variable, if set).

## Development

*   **Linting:** `npm run lint` (check code style), `npm run lint:fix` (automatically fix issues)
*   **Formatting:** `npm run format` (using Prettier)
*   **Testing:** `npm test` (runs Jest tests)

## Contributing

Contributions are welcome! Please follow standard GitHub practices (fork, branch, pull request).