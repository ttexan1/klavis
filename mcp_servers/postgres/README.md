# PostgreSQL MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a Model Context Protocol (MCP) server designed to provide read-only access to PostgreSQL databases. It enables Large Language Models (LLMs) and other compatible clients to interact with your database by inspecting schemas and executing safe, read-only SQL queries.

This server is based on the reference implementation from [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres).

## License

This MCP server is licensed under the **MIT License**. You are free to use, modify, and distribute the software under the terms of this license.

## Components

### Tools

*   **`query`**
    *   **Description:** Executes a read-only SQL query against the connected PostgreSQL database.
    *   **Input:** `{"sql": "SELECT * FROM your_table LIMIT 10;"}` (A JSON object containing the SQL query string).
    *   **Output:** A JSON array containing the query results.
    *   **Note:** All queries are automatically wrapped in a `BEGIN TRANSACTION READ ONLY` block to ensure no data modification occurs.

### Resources

The server exposes the schema of publicly accessible tables as resources:

*   **Table Schemas:** (`postgres://<host>/<database>/<table>/schema`)
    *   Provides JSON schema information for each table in the `public` schema of the connected database.
    *   Includes column names and their corresponding data types.
    *   Automatically discovered from database metadata (`information_schema`).

## Prerequisites

*   **Node.js and npm:** Required for running locally without Docker (v18+ recommended).
*   **Docker:** (Optional, Recommended) For containerized deployment.
*   **PostgreSQL Database:** An accessible PostgreSQL database instance.

## Setup

1.  **Clone the Repository:** If you haven't already, clone the main Klavis AI repository.
2.  **Configure Environment Variables:**
    *   This server requires the connection string for your PostgreSQL database.
    *   Navigate to the `mcp_servers/postgres` directory.
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit the `.env` file and set the `DATABASE_URL` variable to your PostgreSQL connection string.
        ```env
        # .env
        DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database_name>
        ```
        Replace `<user>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your actual database credentials and details.

## Running the Server

You can run the server using Docker (recommended) or directly with Node.js/npm.

### Using Docker (Recommended)

1.  **Build the Docker Image:**
    *   Navigate to the **root directory** of the Klavis AI repository (the one containing the `mcp_servers` folder).
    *   Run the build command:
        ```bash
        docker build -t klavis-ai/mcp-server-postgres -f mcp_servers/postgres/Dockerfile .
        ```
        *   `-t klavis-ai/mcp-server-postgres`: Tags the image with a descriptive name.
        *   `-f mcp_servers/postgres/Dockerfile`: Specifies the path to the Dockerfile.
        *   `.`: Specifies the build context (the root directory).

2.  **Run the Docker Container:**
    *   Use the `DATABASE_URL` you configured in the `.env` file.
    *   Run the container, exposing port 5000:
        ```bash
        # Make sure to replace the example URL with your actual DATABASE_URL
        docker run -p 5000:5000 -e DATABASE_URL="postgresql://user:password@host:port/db" --rm klavis-ai/mcp-server-postgres
        ```
        *   `-p 5000:5000`: Maps port 5000 on your host to port 5000 in the container.
        *   `-e DATABASE_URL="..."`: Passes the database connection string as an environment variable *directly* to the container. Ensure this is properly quoted.
        *   `--rm`: Removes the container when it stops.
        *   `klavis-ai/mcp-server-postgres`: The name of the image you built.

    The server should now be running and accessible at `http://localhost:5000`.

### Using NPM (Manual / Development)

1.  **Navigate to the Server Directory:**
    ```bash
    cd mcp_servers/postgres
    ```
2.  **Install Dependencies:**
    ```bash
    npm install
    ```
3.  **Ensure `.env` is Configured:** Make sure you have created and configured the `.env` file as described in the Setup section. The `npm start` script will automatically load it using `dotenv`.
4.  **Start the Server:**
    ```bash
    npm start
    ```
    This command first compiles the TypeScript code (`tsc`) and then runs the server (`node dist/index.js`).

    The server should now be running and accessible at `http://localhost:5000`.

## Usage with MCP Clients

Once the server is running, you can connect to it using any MCP-compatible client. The specific configuration will depend on the client, but it generally involves pointing the client to the server's address (e.g., `http://localhost:5000` if running locally). The client can then list available resources/tools and interact with the `query` tool or read schema resources. 