# Klavis ReportGen MCP Server

This directory contains the code for the Klavis Report Generation Model Context Protocol (MCP) server. This server allows users to generate visually appealing web reports based on a simple search query. It leverages AI to find relevant information, synthesize it, and present it in a modern, interactive HTML format.

## Features

*   **AI-Powered Report Generation**: Uses Anthropic's Claude model to create comprehensive and well-structured reports.
*   **Web Search Integration**: Utilizes the Firecrawl API to gather up-to-date information from the web based on your query.
*   **Database Storage**: Stores generated reports in a Supabase database for easy access and retrieval.
*   **MCP Compliant**: Built using the Klavis FastMCP framework for seamless integration with MCP-compatible clients.
*   **Easy Deployment**: Can be run easily using Docker or a standard Python environment.

## Getting Started

There are two primary ways to run the Klavis ReportGen MCP server locally: using Docker (recommended) or setting up a Python virtual environment.

### Prerequisites

Regardless of the method you choose, you will need to configure environment variables.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Edit the `.env` file and add your API keys and Supabase credentials:
    *   `ANTHROPIC_API_KEY`: Your API key for the Anthropic API.
    *   `SUPABASE_URL`: Your Supabase project URL.
    *   `SUPABASE_API_KEY`: Your Supabase service role key or anon key (depending on your table policies).
    *   `FIRECRAWL_API_KEY`: Your API key for the Firecrawl API.

### Option 1: Running with Docker (Recommended)

Docker provides a containerized environment with all dependencies included.

1.  **Build the Docker image:**
    Navigate to the root directory of the Klavis project (the directory containing the `mcp_servers` folder) and run the following command:
    ```bash
    docker build -t klavis-reportgen-mcp -f mcp_servers/report_generation/Dockerfile .
    ```
    *Note: The `-t klavis-reportgen-mcp` tags the image with a descriptive name. The `-f` flag specifies the path to the Dockerfile, and `.` indicates the build context (the Klavis project root).*

2.  **Run the Docker container:**
    Make sure your `.env` file is present in the `mcp_servers/report_generation` directory. The Dockerfile is configured to copy this file into the image.
    ```bash
    docker run -p 5000:5000 --env-file mcp_servers/report_generation/.env klavis-reportgen-mcp
    ```
    *   `-p 5000:5000` maps port 5000 on your host machine to port 5000 in the container.
    *   `--env-file mcp_servers/report_generation/.env` loads the environment variables from your `.env` file into the container.

The server should now be running and accessible at `http://localhost:5000`.

### Option 2: Running with Python Virtual Environment

If you prefer not to use Docker, you can run the server directly using Python.

1.  **Navigate to the server directory:**
    ```bash
    cd mcp_servers/report_generation
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ensure `.env` file is present:**
    Make sure the `.env` file you created earlier is in the current directory (`mcp_servers/report_generation`). The server loads variables from this file automatically.

5.  **Run the server:**
    ```bash
    python server.py
    ```

The server should now be running and accessible at `http://localhost:5000`.

## Usage

Once the server is running, you can interact with it using any MCP-compatible client by connecting to `http://localhost:5000`. The available tool is `generate_web_reports`, which accepts a `query` string as input.

Example interaction (using a hypothetical MCP client):

```python
# Connect to the server
client = MCPClient("http://localhost:5000")

# Call the report generation tool
result = client.call_tool("generate_web_reports", query="latest advancements in large language models")

# Print the result (which should contain a URL to the report)
print(result)
# Expected Output: "Report generated successfully. Please return the url to the user so that they can view the report at http://www.klavis.ai/generated-reports/{report_id}"
```

## License

This project is licensed under the MIT License.

---

MIT License

Copyright (c) 2024 Klavis AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 