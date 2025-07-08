from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests
import logging
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTokenVerifier(TokenVerifier):
    """Simple token verifier for single-user scenarios"""
    
    def __init__(self):
        self.valid_token = os.getenv("MCP_API_KEY")
        if not self.valid_token:
            logger.warning("⚠️  MCP_API_KEY not set - authentication will fail")
    
    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify a bearer token against the single configured key."""
        if not self.valid_token or token != self.valid_token:
            return None
        
        return AccessToken(
            token=token,
            client_id="single_user",
            scopes=["youtube:read", "notion:write"],
            expires_at=None
        )

mcp = FastMCP(
    "YouTube & Notion MCP Server",
    host="0.0.0.0",
    port=8000,
    stateless_http=True,
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url="http://localhost:8000",
        resource_server_url="http://localhost:8000",
        required_scopes=["youtube:read", "notion:write"],
    ),
)

@mcp.tool()
def fetch_youtube_transcript(url: str) -> dict:
    """Fetch transcripts of a youtube video."""
    try:
        video_id = url.split("v=")[-1]
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        full_text = " ".join(snippet.text for snippet in fetched_transcript)
        video_title = get_video_title(url)
        return {"transcript": full_text, "title": video_title}
    except Exception as e:
        logger.error(f"Error fetching transcript for url {url}, {str(e)}")
        return {"error": f"Error fetching transcript for url {url}, {str(e)}"}

@mcp.tool()
def save_to_notion(link: str, title: str, summary: str) -> dict:
    """Save a link, title, and summary of a youtube video to Notion database."""
    try:
        database_id = os.getenv("NOTION_DATABASE_ID")
        api_token = os.getenv("NOTION_API_TOKEN")
        
        if not database_id:
            return {"error": "NOTION_DATABASE_ID environment variable not set"}
        if not api_token:
            return {"error": "NOTION_API_TOKEN environment variable not set"}
        
        url_endpoint = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Title": {
                    "rich_text": [
                        {
                            "text": {"content": title}
                        }
                    ]
                },
                "Link": {
                    "title": [
                        {
                            "text": {"content": link}
                        }
                    ]
                },
                "Summary": {
                    "rich_text": [
                        {
                            "text": {"content": summary}
                        }
                    ]
                }
            }
        }
        
        response = requests.post(url_endpoint, json=page_data, headers=headers)
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Successfully saved '{title}' to Notion database"
            }
        else:
            logger.error(f"Notion API error: {response.status_code} - {response.text}")
            return {"error": f"Failed to save to Notion: {response.status_code} - {response.text}"}
            
    except Exception as e:
        logger.error(f"Error saving to Notion: {str(e)}")
        return {"error": f"Error saving to Notion: {str(e)}"}

def get_video_title(url: str) -> str:
    """Retrieve the title of a youtube video"""
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('meta', property='og:title')
        video_title = title_tag['content'] if title_tag else 'Title not found'
        return video_title
    except Exception as e:
        logger.error(f"Error fetching video title for url {url}, {str(e)}")
        return "Error fetching video title"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube & Notion MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio", help="Transport type")
    parser.add_argument("--host", default="localhost", help="Host for HTTP transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport")
    
    args = parser.parse_args()

    if args.transport == "http":
        logger.info(f"🚀 Starting HTTP server on {args.host}:{args.port}")
        logger.info("🔐 Authentication: Bearer token required")
        logger.info("📋 Required scopes: youtube:read, notion:write")
        logger.info("🛠️  Available tools: fetch_youtube_transcript, save_to_notion")
        logger.info("🔑 Set MCP_API_KEY environment variable for authentication")
        mcp.run(transport="streamable-http")
    else:
        logger.info("📟 Starting stdio server (no auth required)")
        logger.info("🛠️  Available tools: fetch_youtube_transcript, save_to_notion")
        mcp.run(transport="stdio")