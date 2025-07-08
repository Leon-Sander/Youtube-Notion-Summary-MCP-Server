# YouTube Transcript MCP Server

A simple MCP server that fetches YouTube video transcripts and saves them to Notion.

## Features

- 🎥 Fetch full text transcripts from YouTube videos
- 📝 Get video titles automatically  
- 💾 Save summaries to Notion
- 🔐 Secure HTTP transport with authentication
- 🐳 Docker ready for easy deployment
- 🌐 Proxy support for cloud deployments

## Quick Start

### 1. Environment Setup

**For Local Development** - Create a `.env` file:
```env
MCP_API_KEY=your-secret-api-key-here
NOTION_API_TOKEN=your-notion-integration-token
NOTION_DATABASE_ID=your-notion-database-id

# Optional: Proxy for cloud deployments (required for Render, AWS, etc.)
PROXY_URL=http://username:password@proxy-server:port
```

**⚠️ Cloud Platform Note:** YouTube blocks most cloud provider IPs (AWS, Google Cloud, Railway, etc.). You need a proxy service for reliable operation.

### 🆓 Free Proxy Setup (Webshare)

1. **Sign up at Webshare:** https://www.webshare.io/
2. **Get 10 free proxies** (no credit card required)
3. **Find your proxy details** in their dashboard
4. **Format:** `http://username:password@proxy-endpoint:port`
5. **Add to Railway Variables:** `PROXY_URL` = your webshare proxy URL

### 2. Run with Docker

```bash
# Build the image
docker build -t youtube-transcript-mcp .

# Run the server
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env youtube-transcript-mcp
```

The server will be available at `http://localhost:8000`

### 3. Configure MCP Client

Add to your MCP client configuration (e.g., `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "youtube-notion-server": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer your-secret-api-key-here"
      }
    }
  }
}
```

## Available Tools

- `fetch_youtube_transcript(url)` - Get transcript and title from YouTube video
- `save_to_notion(link, title, summary)` - Save video info to Notion database

## Development

Install dependencies:
```bash
uv sync
```

Run locally:
```bash
uv run fetch_youtube_transcripts.py --transport http
```
