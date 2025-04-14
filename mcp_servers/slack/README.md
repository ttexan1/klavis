# Slack MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This server implements the Model Context Protocol (MCP) to provide access to various Slack API functionalities as tools for language models or other MCP clients. It allows interacting with Slack workspaces programmatically through a standardized interface.

This server is based on the reference implementation from [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/slack).

## Features

The server exposes the following Slack API functions as MCP tools:

*   `slack_list_channels`: List public channels in the workspace.
*   `slack_post_message`: Post a new message to a channel.
*   `slack_reply_to_thread`: Reply to a specific message thread.
*   `slack_add_reaction`: Add a reaction emoji to a message.
*   `slack_get_channel_history`: Get recent messages from a channel.
*   `slack_get_thread_replies`: Get all replies in a message thread.
*   `slack_get_users`: Get a list of users in the workspace.
*   `slack_get_user_profile`: Get detailed profile information for a user.

## Prerequisites

Before you begin, ensure you have the following:

*   **Node.js and npm:** Required for local development (check versions with `node -v` and `npm -v`).
*   **Docker:** Required for running the server in a container (Recommended).
*   **Slack Bot Token:** A Slack Bot token with the necessary permissions (scopes) to perform the actions listed in the Features section (e.g., `channels:read`, `chat:write`, `reactions:write`, `groups:read`, `users:read`, `users:read.email`). You can create a Slack App and obtain a Bot User OAuth Token from the "OAuth & Permissions" page in your Slack App settings.
*   **Slack Team ID:** The ID of your Slack workspace (starts with `T`). You can often find this in URLs or by using Slack API methods.

## Setup

You can run the server using Docker (recommended) or locally.

### Docker (Recommended)

1.  **Create Environment File:**
    Create a file named `.env` in the `mcp_servers/slack` directory with the following content:
    ```env
    # Required: Your Slack Workspace/Team ID
    SLACK_TEAM_ID=TXXXXXXXXXX 
    
    # Optional: Your Slack Bot OAuth Token
    # If provided, this takes precedence over the x-auth-token header
    SLACK_AUTH_TOKEN=xoxb-your-token-here
    ```
    Replace `TXXXXXXXXXX` with your actual Slack Team ID. If `SLACK_AUTH_TOKEN` is not set, 
    the Slack Bot Token must be provided via the `x-auth-token` header with each request (see Configuration).

2.  **Build Docker Image:**
    Navigate to the root `klavis` directory (one level above `mcp_servers`) in your terminal and run the build command:
    ```bash
    docker build -t slack-mcp-server -f mcp_servers/slack/Dockerfile .
    ```
    *(Make sure the path to the Dockerfile is correct relative to your current directory.)*

3.  **Run Docker Container:**
    Run the container, mapping the server's port (5000) to a port on your host machine (e.g., 5000):
    ```bash
    # Note: The .env file created in step 1 is copied into the image during the build process specified in the Dockerfile.
    docker run -p 5000:5000 --name slack-mcp slack-mcp-server 
    ```
    The server will start and listen on port 5000 inside the container.

### Local Development

1.  **Clone Repository:** (If you haven't already)
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Navigate to Directory:**
    ```bash
    cd mcp_servers/slack
    ```

3.  **Create Environment File:**
    Create a file named `.env` in this directory as described in Step 1 of the Docker setup:
    ```env
    # Required: Your Slack Workspace/Team ID
    SLACK_TEAM_ID=TXXXXXXXXXX 
    
    # Optional: Your Slack Bot OAuth Token
    # If provided, this takes precedence over the x-auth-token header
    SLACK_AUTH_TOKEN=xoxb-your-token-here
    ```

4.  **Install Dependencies:**
    ```bash
    npm install
    ```

5.  **Build and Run:**
    This command compiles the TypeScript code and starts the server:
    ```bash
    npm start
    ```
    The server will start and listen on `http://localhost:5000`.

## Configuration

*   **`SLACK_TEAM_ID` (Environment Variable):** This is required for certain API calls (`getChannels`, `getUsers`) and must be set in the `.env` file (both for Docker build and local run).
*   **`SLACK_AUTH_TOKEN` (Environment Variable):** Optional. If set, this Bot Token will be used for all Slack API calls. This takes precedence over the token provided in request headers.
*   **Slack Bot Token (Request Header):** If `SLACK_AUTH_TOKEN` is not set, the server expects the Slack Bot Token to be provided in the `x-auth-token` HTTP header for every request made to the `/messages` endpoint. The server uses this token to authenticate with the Slack API for the requested operation.

## Usage

MCP clients can connect to this server via Server-Sent Events (SSE) and interact with it:

1.  **Establish SSE Connection:** Clients connect to the `/sse` endpoint (e.g., `http://localhost:5000/sse`).
2.  **Send Messages:** Clients send MCP requests (like `call_tool`) as JSON payloads via POST requests to the `/messages?sessionId=<session_id>` endpoint.
3.  **Authentication:** Each POST request to `/messages` **must** include the Slack Bot Token in the `x-auth-token` header.

Refer to the [MCP SDK documentation](https://github.com/modelcontextprotocol) for details on client implementation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file (you might need to add one) for details. 