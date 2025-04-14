from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown
from typing import Annotated
from pydantic import Field

mcp = FastMCP(
    "Youtube",
    instructions="Retrieve the transcript/subtitles for a given YouTube video and convert it to markdown.",
    port=5000,
)


@mcp.tool()
async def convert_youtube_to_markdown(
    url: Annotated[
        str,
        Field(
            description="The URL of the YouTube video to retrieve the transcript/subtitles for."
        ),
    ],
) -> str:
    """Retrieve the transcript/subtitles for a given YouTube video and convert it to markdown.

    Returns:
        The transcript/subtitles of the YouTube video in markdown format.
    """
    if url.startswith("http") or url.startswith("https"):
        return MarkItDown().convert_uri(url).markdown
    else:
        return f"Unsupported url. Only http:, https: are supported."


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
