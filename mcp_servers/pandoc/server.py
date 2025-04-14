from mcp.server.fastmcp import FastMCP
import pypandoc
from google.cloud import storage
from google.cloud.exceptions import NotFound
import logging
from dotenv import load_dotenv
import uuid
import tempfile
from typing import Annotated
from pydantic import Field
import datetime
import google.auth
from google.auth.transport import requests
import os

load_dotenv()

logger = logging.getLogger(__name__)
mcp = FastMCP(
    "Pandoc",
    instructions="Using pandoc to convert markdown text to pdf, microsoft word and html files.",
    port=5000,
)


def upload_blob_and_get_signed_url(
    bucket_name, source_file_name, destination_blob_name
):
    """
    Uploads a file to a Google Cloud Storage bucket and generates a URL for it.

    Args:
        bucket_name (str): The name of your GCS bucket.
        source_file_name (str): The path to the local file to upload.
        destination_blob_name (str): The desired name/path for the file within the bucket.

    Returns:
        str: The signed URL for downloading the blob, or None if an error occurred.
    """
    try:
        credentials, _ = google.auth.default()
        request = requests.Request()
        credentials.refresh(request)

        # Initialize the Cloud Storage client
        # Uses Application Default Credentials (ADC) by default.
        storage_client = storage.Client(credentials=credentials)

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        logger.info(
            f"Uploading {source_file_name} to gs://{bucket_name}/{destination_blob_name}..."
        )
        url = blob.generate_signed_url(
            version="v4",
            service_account_email=credentials.service_account_email,
            access_token=credentials.token,
            # This URL is valid for 7 days
            expiration=datetime.timedelta(days=7),
            # Allow GET requests using this URL.
            method="GET",
        )

        return url

    except NotFound:
        logger.error(
            f"Error: Bucket '{bucket_name}' not found or insufficient permissions."
        )
        return None
    except FileNotFoundError:
        logger.error(f"Error: Source file not found at '{source_file_name}'")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None


@mcp.tool()
async def convert_markdown_to_file(
    markdown_text: Annotated[
        str, Field(description="The text in markdown format to convert.")
    ],
    output_format: Annotated[
        str,
        Field(
            description="The format to convert the markdown to. Must be one of pdf, docx, doc, html, html5."
        ),
    ],
) -> str:
    """Convert markdown text to pdf, microsoft word and html files. Returns the url of the converted file.
    For pdf, it uses pdflatex to generate the pdf file. Therefore, for pdf please DO NOT use emoji in the markdown text.

    Returns:
        The converted file url.
    """

    if output_format not in ["pdf", "docx", "doc", "html", "html5"]:
        return f"Unsupported format. Only pdf, docx, doc, html and html5 are supported."
    with tempfile.NamedTemporaryFile(
        delete=True, suffix=f".{output_format}", delete_on_close=True
    ) as temp_file:
        temp_file_path = temp_file.name
        pypandoc.convert_text(
            markdown_text,
            to=output_format,
            format="md",
            outputfile=temp_file_path,
            sandbox=True,
        )
        url = upload_blob_and_get_signed_url(
            os.environ["GCS_BUCKET_NAME"],
            temp_file_path,
            f"{str(uuid.uuid4())}.{output_format}",
        )
    return url


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
