# Supabase MCP Server (Klavis Fork)

This directory contains a Model Context Protocol (MCP) server designed to allow LLM to interact with your Supabase projects. It is based on the official [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) server but may include modifications specific to the Klavis project.

This server acts as a bridge, exposing Supabase functionalities (like database querying, project management, log fetching) as tools that MCP-compatible AI clients can utilize.

## License

This specific implementation is licensed under the MIT License.

## Prerequisites

*   **Node.js:** Version 22.x or higher is recommended (check with `node -v`). Download from [nodejs.org](https://nodejs.org/).
*   **Docker:** Required for the recommended setup method. Download from [docker.com](https://www.docker.com/).
*   **Supabase Account:** You need a Supabase account.
*   **Supabase Personal Access Token (PAT):**
    1.  Go to your Supabase Account Settings -> Access Tokens.
    2.  Generate a new token. Give it a descriptive name (e.g., "Klavis MCP Server").
    3.  **Important:** Copy the token immediately. You won't be able to see it again.

## Setup

1.  **Environment Variables:**
    *   Navigate to the `mcp_servers/supabase` directory in your terminal.
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit the newly created `.env` file and add your Supabase Personal Access Token:
        ```env
        SUPABASE_AUTH_TOKEN=your_supabase_personal_access_token_here
        # Add any other required environment variables if needed
        ```

## Running the Server Locally

You can run the server using Docker (recommended) or directly with Node.js.

### Method 1: Docker (Recommended)

This method isolates the server environment and simplifies dependency management.

1.  **Build the Docker Image:**
    *   Make sure you are in the root directory of the `klavis` project (the parent directory of `mcp_servers`).
    *   Run the build command:
        ```bash
        docker build -t klavis-supabase-mcp -f mcp_servers/supabase/Dockerfile .
        ```
    *   This command builds an image named `klavis-supabase-mcp` using the specific `Dockerfile` for the Supabase MCP server. The `.` indicates the build context is the current directory (`klavis`).

2.  **Run the Docker Container:**
    *   Execute the following command:
        ```bash
        docker run --rm -p 5000:5000 --env-file mcp_servers/supabase/.env klavis-supabase-mcp
        ```
    *   `--rm`: Automatically removes the container when it exits.
    *   `-p 5000:5000`: Maps port 5000 on your host machine to port 5000 inside the container (the port the server listens on).
    *   `--env-file mcp_servers/supabase/.env`: Loads the environment variables (including your `SUPABASE_AUTH_TOKEN`) from the specified `.env` file into the container.
    *   `klavis-supabase-mcp`: The name of the image to run.

The server should now be running and accessible at `http://localhost:5000`.

### Method 2: Node.js (Alternative)

This method runs the server directly on your machine using your local Node.js installation.

1.  **Navigate to the Directory:**
    ```bash
    cd mcp_servers/supabase
    ```

2.  **Install Dependencies:**
    *   Make sure you have created and configured the `.env` file in this directory as described in the Setup section.
    ```bash
    npm install
    ```

3.  **Build the Server Code:**
    *   This compiles the TypeScript source code into JavaScript.
    ```bash
    npm run build
    ```

4.  **Run the Server:**
    ```bash
    node dist/sse.js
    ```

The server should now be running and accessible at `http://localhost:5000`.

## Configuring Your MCP Client (e.g., Cursor)

To allow your AI assistant to use this server, you need to configure it in the client's settings. MCP clients usually expect a URL where the server's Server-Sent Events (SSE) endpoint is available.

For this server running locally, the endpoint is:

`http://localhost:5000/sse`

Consult your specific MCP client's documentation on how to add a custom MCP server. You will typically need to provide this URL. Unlike the original `npx` approach from the community repository, this server runs independently, and the client connects directly to its URL.

*Note:* Ensure the `SUPABASE_AUTH_TOKEN` is correctly set in the `.env` file used by the server (either via `--env-file` for Docker or by being present in the directory for the Node.js method). The server uses this token to authenticate with Supabase on your behalf.
