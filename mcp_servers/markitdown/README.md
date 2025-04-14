# MarkItDown MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project provides a Model Context Protocol (MCP) server that utilizes the `markitdown` library to convert various document types hosted at a given URL into Markdown format.

## Features

*   Accepts a URL (HTTP/HTTPS) pointing to a document.
*   Supports conversion for:
    *   PDF
    *   Microsoft Office Documents (Word, PowerPoint, Excel)
    *   HTML
    *   Text-based formats (CSV, JSON, XML)
    *   ZIP archives (extracts and converts contents)
    *   EPub files
*   Handles optional authentication tokens for accessing protected resources.

## Running Locally

There are two recommended ways to run this server locally: using Docker (recommended) or using a Python virtual environment.

### Using Docker (Recommended)

This is the easiest way to get the server running without managing dependencies manually.

1.  **Ensure Docker is installed** on your system.
2.  **Navigate to the root directory** of the `klavis` project in your terminal.
3.  **Build the Docker image:**
    ```bash
    docker build -t markitdown-mcp -f mcp_servers/markitdown/Dockerfile .
    ```
    *(You can replace `markitdown-mcp` with any tag you prefer)*
4.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 markitdown-mcp
    ```
    This command maps port 5000 on your host machine to port 5000 inside the container, where the server listens.

The server should now be running and accessible at `http://localhost:5000`.

### Using Python Virtual Environment

This method requires Python 3.12 and `pip` to be installed.

1.  **Navigate to this directory** (`mcp_servers/markitdown`) in your terminal.
2.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv .venv
    ```
3.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the server:**
    ```bash
    python server.py
    ```

The server should now be running and accessible at `http://localhost:5000`.

6.  **Deactivate the virtual environment** when you are finished:
    ```bash
    deactivate
    ``` 