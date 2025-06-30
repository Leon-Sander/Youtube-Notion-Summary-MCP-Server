from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("youtube-transcriber-server")

@mcp.tool()
def fetch_youtube_transcript(url: str) -> dict:
    """Fetch transcripts of a youtube video."""
    try:
        video_id = url.split("v=")[-1]
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        full_text = " ".join(snippet.text for snippet in fetched_transcript)
        video_title = get_video_title(url)
        return {"transcript" : full_text, "title" : video_title}
    except Exception as e:
        logger.error(f"Error fetching transcript for url {url}, {str(e)}")
        return {"error" : f"Error fetching transcript for url {url}, {str(e)}"}
    
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
    mcp.run(transport="stdio")