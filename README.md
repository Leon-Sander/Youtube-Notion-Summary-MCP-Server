# YouTube Transcript MCP

A simple MCP server that fetches the transcript and title for a given YouTube video URL.

## Features

- Fetches the full text transcript of a YouTube video.
- Retrieves the video's title.
- Exposes this functionality as an MCP tool.

## Installation

This project uses `uv` for package management.

Install the dependencies from within the `youtube_transcript_mcp` directory:
```bash
uv venv
source .venv/bin/activate
uv add -r requirements.txt
```

## Usage

You can run the MCP server directly from your terminal or integrate it with an MCP client like Cursor.

### Running from the terminal

From the project's root directory:
```bash
uv run python fetch_youtube_transcripts.py
```

This will start the MCP server with `stdio` transport.

### Adding to Cursor

To integrate this tool with Cursor, add the following configuration to your `settings.json` file under `mcpServers`:

```json
"fetch_youtube_transcription": {
    "command": "uv",
    "args": [
        "--directory",
        "/path/to/your/project/youtube_transcript_mcp/youtube_transcript_mcp",
        "run",
        "fetch_youtube_transcripts.py"
    ]
}
```

**Note:** Make sure to replace `"/path/to/your/project/youtube_transcript_mcp/youtube_transcript_mcp"` with the absolute path to the inner `youtube_transcript_mcp` directory on your machine.

Once configured, you can call the `fetch_youtube_transcript` tool with a YouTube video URL from within Cursor or other MCP clients.
