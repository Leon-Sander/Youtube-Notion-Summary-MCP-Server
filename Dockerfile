FROM python:3.12-slim

WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY fetch_youtube_transcripts.py .

EXPOSE 8000
CMD ["uv", "run", "fetch_youtube_transcripts.py", "--transport", "http"]