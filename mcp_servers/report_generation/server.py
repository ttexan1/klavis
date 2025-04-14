import os
import logging
from typing import List, Dict, Any, Optional, Annotated

import anthropic
import requests
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("report_generation")

# Load environment variables
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")

# Initialize MCP Server
mcp = FastMCP(
    "KlavisReportGen",
    instructions="Generate visually appealing JavaScript web reports from search queries with Klavis AI.",
    port=5000,
)

# Report generation prompt template
REPORT_GENERATION_PROMPT = """You are a world class web report generation agent build by Klavis AI.
I want you to create a visually appealing javascript web page that presents the key information from these articles in an organized, modern layout. 

Most importantly, the entire code will be dynamically rendered in a iframe, so it MUST be compatible with that.
To avoid long loading times, DO NOT use more than 4 external libraries.
To avoid output being too long, DO NOT use more than 4000 tokens in the code block.

Also, the page should:
1. Extract the main headline, subtitle, and key points from the article
2. Create a card-based layout with distinct sections (e.g. summary, details, implications, learnings, etc)
3. Include appropriate icons for each section (e.g. beaker for methodology, trophy for achievements, etc.)
4. Add a simple data visualization if the article contains statistics or comparative data
5. Use a clean color scheme with section color-coding
6. Be responsive and follow modern web design principle
7. When appropriate, add reference links to the original articles in the report content.
7. Only return one complete code block and start the code block with "```html" and end with "```"

Generate the complete javascript code including:
- All necessary component
- CSS styling (preferably using styled-components or CSS modules)
- Any JavaScript needed for interactivity
- Mock data implementation based on the article content
- Fit into an iframe directly.

Here are the articles to transform:
{article_content}
"""


async def generate_report_with_claude(article_content: str) -> str:
    """
    Generate web report using Claude 3.7

    Args:
        article_content: The content of the article

    Returns:
        The generated JavaScript code
    """
    try:
        prompt = REPORT_GENERATION_PROMPT.format(article_content=article_content)

        anthropic_client = anthropic.AsyncClient(api_key=ANTHROPIC_API_KEY)
        generated_text = ""

        # Anthropic recommends using streaming for long responses:
        # https://docs.anthropic.com/en/api/errors#long-requests
        async with anthropic_client.messages.stream(
            model="claude-3-7-sonnet-latest",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                generated_text += text

        # Extract code from markdown code blocks if present
        start_index = generated_text.find("```html") + 7
        end_index = generated_text.rfind("```")

        if start_index >= 7 and end_index > start_index:
            return generated_text[start_index:end_index].strip()

        # Fallback: if no code block is found, return the raw text
        logger.warning(
            f"No code block found in generated text: start_index: {start_index}, end_index: {end_index}"
        )
        return generated_text[start_index:].strip()

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise


async def store_report_in_supabase(html_content: str) -> Dict[str, Any]:
    """
    Store the generated report in Supabase

    Args:
        html_content: The generated HTML/JS content

    Returns:
        The database record
    """
    # Initialize clients
    supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
    if not supabase:
        logger.error("Supabase client not initialized")
        return {"id": None}

    try:
        result = (
            supabase.table("generated_reports")
            .insert(
                {
                    "content": html_content,
                }
            )
            .execute()
        )

        return result.data[0]["id"]

    except Exception as e:
        logger.error(f"Error storing report: {str(e)}")
        raise


def search_firecrawl(query: str, limit: int = 3) -> List[str]:
    """
    Search for URLs using Firecrawl search API

    Args:
        query: Search query
        limit: Maximum number of results to return

    Returns:
        List of URLs from search results
    """
    try:
        url = "https://api.firecrawl.dev/v1/search"

        payload = {
            "query": query,
            "limit": limit,
            "lang": "en",
            "country": "us",
            "timeout": 240000,
            "scrapeOptions": {
                "formats": ["markdown"],
            },
        }

        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        search_results = response.json()
        results = {}

        # Extract URLs from search results
        for data in search_results.get("data", []):
            url = data.get("url", "")
            results[url] = {}
            results[url]["title"] = data.get("title", "")
            results[url]["content"] = data.get("markdown", "")

        return results

    except Exception as e:
        logger.error(f"Error in search_firecrawl: {str(e)}")
        raise


@mcp.tool()
async def generate_web_reports(
    query: Annotated[
        str,
        Field(description="Search query to find relevant articles for the report."),
    ],
) -> str:
    """Generate web reports based on a search query.

    Searches for relevant articles using the query, creates a visually appealing
    JavaScript web page that consolidates content from the top search results.

    Returns:
        A URL to the generated report. The url will be http://www.klavis.ai/generated-reports/{report_id}.
    """
    try:
        # 1. Search for relevant URLs
        url_to_content = search_firecrawl(query)

        all_articles = ""
        for url, content in url_to_content.items():
            all_articles += f"Article URL: {url}\nArticle Title: {content['title']}\nArticle Content: {content['content']}\n\n"

        # 3. Generate reports
        generated_code = await generate_report_with_claude(all_articles)

        # 4. Store in Supabase
        report_id = await store_report_in_supabase(generated_code)

        return f"Report generated successfully. Please return the url to the user so that they can view the report at http://www.klavis.ai/generated-reports/{report_id}"
    except Exception as e:
        logger.error(f"Error in generate_web_reports: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
