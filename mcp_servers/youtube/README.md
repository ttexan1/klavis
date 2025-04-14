# YouTube MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that retrieves transcripts/subtitles for a given YouTube video and converts them into Markdown format.

This server utilizes the `FastMCP` framework for handling MCP requests and `MarkItDown` for processing the YouTube video content.

## Features

*   Provides a simple MCP endpoint to get YouTube video transcripts.
*   Accepts a YouTube video URL as input.
*   Returns the transcript/subtitles in Markdown format.
*   Built with Python using `FastMCP` and `MarkItDown`.
*   Can be run easily using Docker or a standard Python environment.

## Running Locally

You can run this server locally using either Docker (recommended) or a Python virtual environment. The instructions assume you are in the root directory of the `klavis` project (the parent directory of `mcp_servers`).

### Prerequisites

*   **Docker:** If using the Docker method.
*   **Python:** Python 3.11+ if using the virtual environment method.
*   **`.env` File:** Create a file named `.env` in the root of the `klavis` project directory. While the current server code doesn't explicitly require environment variables, the underlying libraries (like `MarkItDown`) might need API keys or configurations in the future. The Docker setup copies this file, and it's good practice to have it for the virtual environment setup as well.
    ```bash
    # Example .env content (add necessary variables if required)
    # SOME_API_KEY=your_api_key_here
    ```

### Using Docker (Recommended)

1.  **Build the Docker Image:**
    Open your terminal in the root directory of the `klavis` project and run:
    ```bash
    docker build -t youtube-mcp-server -f mcp_servers/youtube/Dockerfile .
    ```
    *   `-t youtube-mcp-server`: Assigns a tag (name) to the image.
    *   `-f mcp_servers/youtube/Dockerfile`: Specifies the path to the Dockerfile.
    *   `.`: Specifies the build context (the current directory, `klavis`). This is important because the Dockerfile copies files from this context.

2.  **Run the Docker Container:**
    ```bash
    docker run -p 5000:5000 --env-file .env youtube-mcp-server
    ```
    *   `-p 5000:5000`: Maps port 5000 on your host machine to port 5000 inside the container (where the server listens).
    *   `--env-file .env`: Provides the environment variables from your `.env` file to the container.
    *   `youtube-mcp-server`: The name of the image to run.

The server should now be running and accessible at `http://localhost:5000`.

### Using Python Virtual Environment

1.  **Navigate to Project Root:**
    Ensure your terminal is in the root directory of the `klavis` project.

2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate Virtual Environment:**
    *   **Linux/macOS:** `source venv/bin/activate`
    *   **Windows:** `venv\Scripts\activate`

4.  **Install Dependencies:**
    The server relies on local packages (`mcp`, `markitdown`) and packages listed in `requirements.txt`. Install them in editable mode first, then the requirements:
    ```bash
    # Install local packages (ensure they are set up for installation e.g., with setup.py)
    pip install -e mcp
    pip install -e markitdown

    # Install specific requirements for the youtube server
    pip install -r mcp_servers/youtube/requirements.txt
    ```

5.  **Create `.env` File:**
    Ensure you have created the `.env` file in the `klavis` root directory as mentioned in the prerequisites.

6.  **Run the Server:**
    ```bash
    python mcp_servers/youtube/server.py
    ```

The server should now be running and accessible at `http://localhost:5000`.

## Usage

Once the server is running (either via Docker or Python environment), it listens for MCP requests on port 5000.

You can interact with it using an MCP client or tool. The available tool is:

*   `convert_youtube_to_markdown`:
    *   **Description:** Retrieve the transcript/subtitles for a given YouTube video and convert it to markdown.
    *   **Input Parameter:** `url` (string) - The URL of the YouTube video. Must start with `http` or `https`.
    *   **Returns:** (string) - The transcript/subtitles in Markdown format.
