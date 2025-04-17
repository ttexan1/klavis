import os
import logging
import re
from typing import Any, Dict, Annotated, List, Optional
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import aiohttp
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-mcp-server")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable is required")

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
YOUTUBE_MCP_SERVER_PORT = int(os.getenv("YOUTUBE_MCP_SERVER_PORT", "5000"))

mcp = FastMCP(
    "Youtube",
    instructions="Retrieve the transcript or video details for a given YouTube video.",
    port=YOUTUBE_MCP_SERVER_PORT,
)

def _extract_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from various URL formats.
    Supports standard youtube.com URLs and youtu.be short URLs.
    
    Args:
        url: YouTube URL in various formats
        
    Returns:
        The video ID extracted from the URL
        
    Raises:
        ValueError: If the URL is not a valid YouTube URL or if video ID couldn't be extracted
    """
    if not url:
        raise ValueError("Empty URL provided")
        
    # Pattern 1: Standard YouTube URL (youtube.com/watch?v=VIDEO_ID)
    if "youtube.com/watch" in url:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        video_ids = query_params.get("v")
        if video_ids and len(video_ids[0]) > 0:
            return video_ids[0]
            
    # Pattern 2: Short YouTube URL (youtu.be/VIDEO_ID)
    if "youtu.be/" in url:
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path and path.startswith("/"):
            return path[1:].split("?")[0]
            
    # Pattern 3: Embedded YouTube URL (youtube.com/embed/VIDEO_ID)
    if "youtube.com/embed/" in url:
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path and path.startswith("/embed/"):
            return path[7:].split("?")[0]
            
    # Pattern 4: YouTube shorts URL (youtube.com/shorts/VIDEO_ID)
    if "youtube.com/shorts/" in url:
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path and path.startswith("/shorts/"):
            return path[8:].split("?")[0]
    
    raise ValueError(f"Could not extract video ID from URL: {url}")

async def _make_youtube_request(endpoint: str, params: Dict[str, Any], headers: Dict[str, Any] = None) -> Any:
    """
    Makes an HTTP request to the YouTube Data API.
    """
    params["key"] = YOUTUBE_API_KEY
    url = f"{YOUTUBE_API_BASE}/{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()
                if endpoint == "captions/download":
                    return await response.text()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(f"YouTube API request failed: {e.status} {e.message} for GET {url}")
            error_details = e.message
            try:
                error_body = await e.response.json()
                error_details = f"{e.message} - {error_body}"
            except Exception:
                pass
            raise RuntimeError(f"YouTube API Error ({e.status}): {error_details}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred during YouTube API request: {e}")
            raise RuntimeError(f"Unexpected error during API call to {url}") from e

async def get_video_details(
    video_id: Annotated[
        str,
        Field(
            description="The ID of the YouTube video to get details for."
        ),
    ]
) -> Dict[str, Any]:
    """Get detailed information about a specific YouTube video."""
    logger.info(f"Executing tool: get_video_details with video_id: {video_id}")
    try:
        params = {
            "part": "snippet,contentDetails,statistics",
            "id": video_id
        }
        
        result = await _make_youtube_request("videos", params)
        
        if not result.get("items"):
            return {"error": f"No video found with ID: {video_id}"}
        
        video = result["items"][0]
        snippet = video.get("snippet", {})
        content_details = video.get("contentDetails", {})
        statistics = video.get("statistics", {})
        
        return {
            "id": video.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "publishedAt": snippet.get("publishedAt"),
            "channelId": snippet.get("channelId"),
            "channelTitle": snippet.get("channelTitle"),
            "thumbnailUrl": snippet.get("thumbnails", {}).get("high", {}).get("url"),
            "tags": snippet.get("tags", []),
            "categoryId": snippet.get("categoryId"),
            "duration": content_details.get("duration"),
            "viewCount": statistics.get("viewCount"),
            "likeCount": statistics.get("likeCount"),
            "commentCount": statistics.get("commentCount"),
            "url": f"https://www.youtube.com/watch?v={video_id}"
        }
    except Exception as e:
        logger.exception(f"Error executing tool get_video_details: {e}")
        raise e

@mcp.tool()
async def get_youtube_video_transcript(
    url: Annotated[
        str,
        Field(
            description="The URL of the YouTube video to retrieve the transcript/subtitles for. (e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        ),
    ],
) -> Dict[str, Any]:
    """
    Retrieve the transcript or video details for a given YouTube video.
    """
    try:
        video_id = _extract_video_id(url)
        logger.info(f"Executing tool: get_video_transcript with video_id: {video_id}")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        return {
            "video_id": video_id,
            "transcript": transcript
        }
    except ValueError as e:
        logger.exception(f"Invalid YouTube URL: {e}")
        return {
            "error": f"Invalid YouTube URL: {str(e)}"
        }
    except Exception as e:
        error_message = str(e)
        logger.exception(f"Error fetching transcript for video URL {url}: {error_message}")
        try:        
            # Fall back to get_video_details
            video_details = await get_video_details(video_id)
            return {
                "video_id": video_id,
                "error": "Transcript unavailable. This could be due to disabled captions or region restrictions.",
                "video_details": video_details,
                "fallback_used": True
            }
        except Exception as fallback_error:
            logger.exception(f"Fallback to get_video_details also failed: {fallback_error}")
            return {
                "error": f"Failed to fetch transcript and video details: {error_message}"
            }

def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
