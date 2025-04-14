# Pandoc MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-00a393.svg)](https://fastapi.tiangolo.com/)
[![Pandoc](https://img.shields.io/badge/Pandoc-latest-blue.svg)](https://pandoc.org/)

## 📖 Overview

Pandoc MCP Server is a Model Context Protocol (MCP) implementation that converts Markdown text into various document formats using Pandoc. It provides a standardized interface for document conversion, uploading to Google Cloud Storage (GCS), and returning publicly accessible signed URLs.

## 🚀 Features

This server provides the following capabilities through MCP tools:

| Tool | Description |
|------|-------------|
| `convert_markdown_to_file` | Converts markdown text to various formats (PDF, DOCX, DOC, HTML, HTML5) and returns a GCS signed URL |

## 🔧 Prerequisites

You'll need one of the following:

- **Docker:** Docker installed and running (recommended)
- **Python:** Python 3.12+ with pip

Additionally, you'll need:

- **Google Cloud Storage (GCS) Bucket:** A GCS bucket where the server can upload converted files
- **Google Cloud Credentials:** Application Default Credentials (ADC) configured in your environment

You can configure ADC by running:
```bash
gcloud auth application-default login
```

For local Python setup, you'll also need:
- **Pandoc:** The Pandoc document converter
- **LaTeX:** A LaTeX distribution (like TeX Live or MiKTeX) for PDF conversion

## ⚙️ Setup & Configuration

### Environment Configuration

1. **Create your environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your GCS bucket name:
   ```
   GCS_BUCKET_NAME=your-gcs-bucket-name
   ```

## 🏃‍♂️ Running the Server

### Option 1: Docker (Recommended)

The Docker build must be run from the project root directory (`klavis/`):

```bash
# Navigate to the root directory of the project
cd /path/to/klavis

# Build the Docker image
docker build -t pandoc-mcp-server -f mcp_servers/pandoc/Dockerfile .

# Run the container (with Google Cloud credentials mounted)
docker run -p 5000:5000 --rm -v ~/.config/gcloud:/root/.config/gcloud pandoc-mcp-server
```

To use your local .env file instead of building it into the image:

```bash
docker run -p 5000:5000 --rm --env-file mcp_servers/pandoc/.env -v ~/.config/gcloud:/root/.config/gcloud pandoc-mcp-server
```

### Option 2: Python Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

Once running, the server will be accessible at `http://localhost:5000`.

## 🔌 API Usage

The server implements the Model Context Protocol (MCP) standard. Here's an example of how to call a tool:

```python
import httpx

async def call_pandoc_tool():
    url = "http://localhost:5000/execute"
    payload = {
        "tool_name": "convert_markdown_to_file",
        "tool_args": {
            "markdown_text": "# Hello World\n\nThis is a test document.",
            "output_format": "pdf"
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        result = response.json()
        return result
```

## 📋 Common Operations

### Converting Markdown to PDF

```python
payload = {
    "tool_name": "convert_markdown_to_file",
    "tool_args": {
        "markdown_text": "# Hello World\n\nThis is a test document.",
        "output_format": "pdf"
    }
}
```

### Converting Markdown to DOCX

```python
payload = {
    "tool_name": "convert_markdown_to_file",
    "tool_args": {
        "markdown_text": "# Hello World\n\nThis is a test document.",
        "output_format": "docx"
    }
}
```

## 🛠️ Troubleshooting

### Docker Build Issues

- **File Not Found Errors**: If you see errors like `failed to compute cache key: failed to calculate checksum of ref: not found`, this means Docker can't find the files referenced in the Dockerfile. Make sure you're building from the root project directory (`klavis/`), not from the server directory.

### Common Runtime Issues

- **GCS Bucket Not Found**: Verify your GCS bucket exists and you have the correct permissions
- **Google Cloud Authentication**: Ensure your ADC is properly configured
- **PDF Generation Issues**: Avoid using emojis or complex characters in markdown text when converting to PDF, as they might cause issues with LaTeX
- **Missing LaTeX**: For local setup, ensure a LaTeX distribution is installed if you need PDF conversion

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
