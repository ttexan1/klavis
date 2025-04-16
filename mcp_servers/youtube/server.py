import os
import logging
import json
import base64
from typing import Any, Dict, List, Optional, Annotated
from dotenv import load_dotenv
import aiohttp
from mcp.server.fastmcp import FastMCP
from pydantic import Field

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-mcp-server")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable is required")

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
YOUTUBE_MCP_SERVER_PORT = int(os.getenv("YOUTUBE_MCP_SERVER_PORT", "5000"))

mcp = FastMCP(
    "youtube-server", 
    instructions="Interact with YouTube Data API to search videos, get channel information, video details, and more.",
    port=YOUTUBE_MCP_SERVER_PORT
)

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


# @mcp.tool()
# async def search_videos(
#     query: Annotated[
#         str,
#         Field(
#             description="The search query to search for videos."
#         ),
#     ],
#     max_results: Annotated[
#         int,
#         Field(
#             description="The maximum number of results to return (1-50).",
#             default=10
#         ),
#     ] = 10
# ) -> List[Dict[str, Any]]:
#     """Search for YouTube videos based on a query."""
#     logger.info(f"Executing tool: search_videos with query: {query}, max_results: {max_results}")
#     try:
#         clamped_max_results = max(1, min(max_results, 50))  # Ensure max_results is between 1 and 50
        
#         params = {
#             "part": "snippet",
#             "q": query,
#             "type": "video",
#             "maxResults": clamped_max_results
#         }
        
#         result = await _make_youtube_request("search", params)
        
#         videos = []
#         for item in result.get("items", []):
#             video_id = item.get("id", {}).get("videoId")
#             snippet = item.get("snippet", {})
#             videos.append({
#                 "id": video_id,
#                 "title": snippet.get("title"),
#                 "description": snippet.get("description"),
#                 "publishedAt": snippet.get("publishedAt"),
#                 "channelId": snippet.get("channelId"),
#                 "channelTitle": snippet.get("channelTitle"),
#                 "thumbnailUrl": snippet.get("thumbnails", {}).get("default", {}).get("url"),
#                 "url": f"https://www.youtube.com/watch?v={video_id}"
#             })
        
#         return videos
#     except Exception as e:
#         logger.exception(f"Error executing tool search_videos: {e}")
#         raise e


# @mcp.tool()
# async def get_video_details(
#     video_id: Annotated[
#         str,
#         Field(
#             description="The ID of the YouTube video to get details for."
#         ),
#     ]
# ) -> Dict[str, Any]:
#     """Get detailed information about a specific YouTube video."""
#     logger.info(f"Executing tool: get_video_details with video_id: {video_id}")
#     try:
#         params = {
#             "part": "snippet,contentDetails,statistics",
#             "id": video_id
#         }
        
#         result = await _make_youtube_request("videos", params)
        
#         if not result.get("items"):
#             return {"error": f"No video found with ID: {video_id}"}
        
#         video = result["items"][0]
#         snippet = video.get("snippet", {})
#         content_details = video.get("contentDetails", {})
#         statistics = video.get("statistics", {})
        
#         return {
#             "id": video.get("id"),
#             "title": snippet.get("title"),
#             "description": snippet.get("description"),
#             "publishedAt": snippet.get("publishedAt"),
#             "channelId": snippet.get("channelId"),
#             "channelTitle": snippet.get("channelTitle"),
#             "thumbnailUrl": snippet.get("thumbnails", {}).get("high", {}).get("url"),
#             "tags": snippet.get("tags", []),
#             "categoryId": snippet.get("categoryId"),
#             "duration": content_details.get("duration"),
#             "viewCount": statistics.get("viewCount"),
#             "likeCount": statistics.get("likeCount"),
#             "commentCount": statistics.get("commentCount"),
#             "url": f"https://www.youtube.com/watch?v={video_id}"
#         }
#     except Exception as e:
#         logger.exception(f"Error executing tool get_video_details: {e}")
#         raise e


@mcp.tool()
async def get_channel_info(
    channel_id: Annotated[
        str,
        Field(
            description="The ID of the YouTube channel to get information for."
        ),
    ]
) -> Dict[str, Any]:
    """Get information about a specific YouTube channel."""
    logger.info(f"Executing tool: get_channel_info with channel_id: {channel_id}")
    try:
        params = {
            "part": "snippet,statistics,brandingSettings",
            "id": channel_id
        }
        
        result = await _make_youtube_request("channels", params)
        
        if not result.get("items"):
            return {"error": f"No channel found with ID: {channel_id}"}
        
        channel = result["items"][0]
        snippet = channel.get("snippet", {})
        statistics = channel.get("statistics", {})
        branding = channel.get("brandingSettings", {}).get("channel", {})
        
        return {
            "id": channel.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "customUrl": snippet.get("customUrl"),
            "publishedAt": snippet.get("publishedAt"),
            "thumbnailUrl": snippet.get("thumbnails", {}).get("high", {}).get("url"),
            "country": snippet.get("country"),
            "viewCount": statistics.get("viewCount"),
            "subscriberCount": statistics.get("subscriberCount"),
            "videoCount": statistics.get("videoCount"),
            "keywords": branding.get("keywords"),
            "url": f"https://www.youtube.com/channel/{channel_id}"
        }
    except Exception as e:
        logger.exception(f"Error executing tool get_channel_info: {e}")
        raise e


@mcp.tool()
async def get_video_comments(
    video_id: Annotated[
        str,
        Field(
            description="The ID of the YouTube video to get comments for."
        ),
    ],
    max_results: Annotated[
        int,
        Field(
            description="The maximum number of comments to return (1-100).",
            default=20
        ),
    ] = 20
) -> List[Dict[str, Any]]:
    """Get comments for a specific YouTube video."""
    logger.info(f"Executing tool: get_video_comments with video_id: {video_id}, max_results: {max_results}")
    try:
        clamped_max_results = max(1, min(max_results, 100))  # Ensure max_results is between 1 and 100
        
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": clamped_max_results,
            "order": "relevance"  # Can be "time" or "relevance"
        }
        
        result = await _make_youtube_request("commentThreads", params)
        
        comments = []
        for item in result.get("items", []):
            comment = item.get("snippet", {}).get("topLevelComment", {})
            snippet = comment.get("snippet", {})
            comments.append({
                "id": comment.get("id"),
                "authorDisplayName": snippet.get("authorDisplayName"),
                "authorProfileImageUrl": snippet.get("authorProfileImageUrl"),
                "authorChannelId": snippet.get("authorChannelId", {}).get("value"),
                "textDisplay": snippet.get("textDisplay"),
                "textOriginal": snippet.get("textOriginal"),
                "likeCount": snippet.get("likeCount"),
                "publishedAt": snippet.get("publishedAt"),
                "updatedAt": snippet.get("updatedAt"),
                "replyCount": item.get("snippet", {}).get("totalReplyCount", 0)
            })
        
        return comments
    except Exception as e:
        logger.exception(f"Error executing tool get_video_comments: {e}")
        raise e


@mcp.tool()
async def get_channel_videos(
    channel_id: Annotated[
        str,
        Field(
            description="The ID of the YouTube channel to get videos for."
        ),
    ],
    max_results: Annotated[
        int,
        Field(
            description="The maximum number of videos to return (1-50).",
            default=10
        ),
    ] = 10
) -> List[Dict[str, Any]]:
    """Get videos from a specific YouTube channel."""
    logger.info(f"Executing tool: get_channel_videos with channel_id: {channel_id}, max_results: {max_results}")
    try:
        clamped_max_results = max(1, min(max_results, 50))  # Ensure max_results is between 1 and 50
        
        # First get the uploads playlist ID from the channel
        params = {
            "part": "contentDetails",
            "id": channel_id
        }
        
        channel_result = await _make_youtube_request("channels", params)
        
        if not channel_result.get("items"):
            return [{"error": f"No channel found with ID: {channel_id}"}]
        
        uploads_playlist_id = channel_result["items"][0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        
        if not uploads_playlist_id:
            return [{"error": f"No uploads playlist found for channel ID: {channel_id}"}]
        
        # Now get the videos from the uploads playlist
        params = {
            "part": "snippet",
            "playlistId": uploads_playlist_id,
            "maxResults": clamped_max_results
        }
        
        result = await _make_youtube_request("playlistItems", params)
        
        videos = []
        for item in result.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            videos.append({
                "id": video_id,
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "publishedAt": snippet.get("publishedAt"),
                "thumbnailUrl": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                "position": snippet.get("position"),
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
        
        return videos
    except Exception as e:
        logger.exception(f"Error executing tool get_channel_videos: {e}")
        raise e


# @mcp.tool()
# async def get_video_captions(
#     video_id: Annotated[
#         str,
#         Field(
#             description="The ID of the YouTube video to get captions for."
#         ),
#     ],
#     language: Annotated[
#         Optional[str],
#         Field(
#             description="The language code for the captions (e.g., 'en', 'es', 'fr'). If not specified, returns all available caption tracks.",
#             default=None
#         ),
#     ] = None
# ) -> List[Dict[str, Any]]:
#     """Get available caption tracks for a specific YouTube video."""
#     logger.info(f"Executing tool: get_video_captions with video_id: {video_id}, language: {language}")
#     try:
#         print("---- video_id", video_id)
#         # First get video details to ensure it exists
#         params = {
#             "part": "snippet",
#             "id": video_id
#         }
        
#         video_result = await _make_youtube_request("videos", params)
        
#         print("---- video_result", video_result)
        
#         if not video_result.get("items"):
#             return [{"error": f"No video found with ID: {video_id}"}]
        
#         # Get caption tracks
#         params = {
#             "part": "snippet",
#             "videoId": video_id
#         }
        
#         result = await _make_youtube_request("captions", params)
        
#         print("---- result", result)
        
#         captions = []
#         for item in result.get("items", []):
#             snippet = item.get("snippet", {})
#             caption_language = snippet.get("language", "")
            
#             # Filter by language if specified
#             if language and language.lower() != caption_language.lower():
#                 continue
                
#             captions.append({
#                 "id": item.get("id"),
#                 "language": caption_language,
#                 "name": snippet.get("name"),
#                 "trackKind": snippet.get("trackKind"),
#                 "isAutoSynced": snippet.get("isAutoSynced"),
#                 "isCC": snippet.get("isCC"),
#                 "isDraft": snippet.get("isDraft"),
#                 "isEasyReader": snippet.get("isEasyReader"),
#                 "status": snippet.get("status")
#             })
        
#         return captions if captions else [{"message": f"No caption tracks found for video ID: {video_id}" + (f" in language: {language}" if language else "")}]
#     except Exception as e:
#         logger.exception(f"Error executing tool get_video_captions: {e}")
#         raise e


@mcp.tool()
async def download_caption_content(
    caption_id: Annotated[
        str,
        Field(
            description="The ID of the caption track to download."
        ),
    ],
    format: Annotated[
        str,
        Field(
            description="The format to download the caption in. Options: 'srt', 'vtt', 'ttml'.",
            default="srt"
        ),
    ] = "srt"
) -> Dict[str, Any]:
    """Download the actual caption/subtitle content for a specific caption track."""
    logger.info(f"Executing tool: download_caption_content with caption_id: {caption_id}, format: {format}")
    try:
        # Validate format
        if format.lower() not in ["srt", "vtt", "ttml"]:
            return {"error": f"Invalid format: {format}. Supported formats are: srt, vtt, ttml"}
        
        params = {
            "id": caption_id,
            "tfmt": format.lower()
        }
        
        # The captions.download endpoint requires OAuth 2.0 authentication
        # For simplicity, we're using the API key, but this might not work for all videos
        # Proper implementation would require OAuth 2.0 flow
        
        try:
            content = await _make_youtube_request("captions/download", params)
            
            print("---- content", content)
            return {
                "caption_id": caption_id,
                "format": format,
                "content": content
            }
        except Exception as e:
            # If API key authentication fails, explain the limitation
            return {
                "error": "Could not download caption content. YouTube API requires OAuth 2.0 authentication for caption downloads.",
                "message": "To download captions, you need to implement OAuth 2.0 authentication. The current implementation using API key is not sufficient.",
                "details": str(e)
            }
    except Exception as e:
        logger.exception(f"Error executing tool download_caption_content: {e}")
        raise e


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
