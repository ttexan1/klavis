from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown
import requests
import tempfile
from typing import Annotated
from pydantic import Field

mcp = FastMCP(
    "FileReader",
    instructions="A file reader and converter that can read files from urls and convert them to markdown."
    "It currently supports: PDF, PowerPoint, Word, Excel, HTML, Text-based formats (CSV, JSON, XML), ZIP files (iterates over contents), EPubs.",
    port=5000,
)


@mcp.tool()
async def convert_document_to_markdown(
    uri: Annotated[
        str,
        Field(
            description="The URI of the resource to convert to markdown. The resource MUST be one of the supported types: PDF, "
            "PowerPoint, Word, Excel, HTML, Text-based formats (CSV, JSON, XML), ZIP files (iterates over contents), EPubs."
        ),
    ],
    auth_token: Annotated[
        str, Field(description="The optional authentication token for the resource.")
    ],
) -> str:
    """Convert a resource described by an http:, https: to markdown.

    Returns:
        The markdown representation of the resource.
    """
    if not uri.startswith("http") and not uri.startswith("https"):
        return f"Unsupported uri. Only http:, https: are supported."

    response = requests.get(
        uri, headers={"Authorization": f"Bearer {auth_token}"} if auth_token else None
    )
    if response.status_code == 200:
        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=True, delete_on_close=True
        ) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
            return MarkItDown().convert_uri(f"file://{temp_path}").markdown
    return f"Failed to download the resource. Status code: {response.status_code}"


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
