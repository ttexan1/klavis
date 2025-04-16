# YouTube MCP Server

This server provides a Managed Communication Protocol (MCP) interface to the YouTube Data API v3. It enables AI agents to search for videos, retrieve video details, channel information, comments, and more using the YouTube API.

## Features

- Search for YouTube videos based on query terms
- Get detailed information about specific videos
- Retrieve channel information and statistics
- Get video comments 
- Fetch a channel's uploaded videos
- Convert YouTube video transcripts to markdown format

## Setup

### Requirements

1. Python 3.8 or higher
2. Pip for package installation
3. YouTube Data API v3 API key

### Getting a YouTube API Key

To use this server, you'll need to obtain a YouTube Data API v3 API key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to APIs & Services > Dashboard
4. Click "+ ENABLE APIS AND SERVICES" at the top
5. Search for "YouTube Data API v3" and enable it
6. Navigate to APIs & Services > Credentials
7. Click "Create Credentials" and select "API key"
8. Copy the generated API key

### Installation

1. Clone the repository
2. Navigate to the server directory:
   ```bash
   cd mcp_servers/youtube
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your YouTube API key:
   ```
   YOUTUBE_API_KEY=YOUR_API_KEY_HERE
   YOUTUBE_MCP_SERVER_PORT=5000  # Optional, defaults to 5000
   ```

## Running the Server

Start the server with:

```bash
python server.py
```

The server will run on the port specified in your `.env` file (default: 5000).

## Available Tools

### search_videos

Search for YouTube videos based on a query.

**Parameters:**
- `query` (string, required): The search query to search for videos
- `max_results` (integer, optional, default=10): The maximum number of results to return (1-50)

**Returns:**
A list of videos with basic information including ID, title, description, and URL.

### get_video_details

Get detailed information about a specific YouTube video.

**Parameters:**
- `video_id` (string, required): The ID of the YouTube video to get details for

**Returns:**
Detailed information about the video including title, description, statistics, and more.

### get_channel_info

Get information about a specific YouTube channel.

**Parameters:**
- `channel_id` (string, required): The ID of the YouTube channel to get information for

**Returns:**
Channel information including title, description, statistics, and more.

### get_video_comments

Get comments for a specific YouTube video.

**Parameters:**
- `video_id` (string, required): The ID of the YouTube video to get comments for
- `max_results` (integer, optional, default=20): The maximum number of comments to return (1-100)

**Returns:**
A list of comments with author information, content, and statistics.

### get_channel_videos

Get videos from a specific YouTube channel.

**Parameters:**
- `channel_id` (string, required): The ID of the YouTube channel to get videos for
- `max_results` (integer, optional, default=10): The maximum number of videos to return (1-50)

**Returns:**
A list of videos from the channel with basic information.

### get_video_captions

Get available caption tracks for a specific YouTube video.

**Parameters:**
- `video_id` (string, required): The ID of the YouTube video to get captions for
- `language` (string, optional): The language code for the captions (e.g., 'en', 'es', 'fr'). If not specified, returns all available caption tracks

**Returns:**
A list of caption tracks available for the video, including language, name, and other metadata.

### convert_youtube_to_markdown

Retrieve the transcript/subtitles for a given YouTube video and convert it to markdown.

**Parameters:**
- `url` (string, required): The URL of the YouTube video to retrieve the transcript/subtitles for

**Returns:**
The transcript/subtitles of the YouTube video in markdown format.

## API Limits and Quotas

The YouTube Data API has daily quota limits. Each API request consumes a different amount of quota units. For more information, see the [YouTube Data API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost).

## Error Handling

The server includes robust error handling for API request failures, parameter validation, and more. Errors are logged and meaningful error messages are returned to the client.

## License

This project is licensed under the terms specified in the repository.
