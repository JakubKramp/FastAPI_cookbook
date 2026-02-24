FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy only dependency files first - this layer is cached until they change
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

# Then copy the rest of the code
COPY . .

ENV UV_NO_DEV=1
ENV PATH="/app/.venv/bin:$PATH"

ARG INSTALL_PLAYWRIGHT=false
RUN pip install playwright
RUN if [ "$INSTALL_PLAYWRIGHT" = "true" ]; then playwright install chromium && playwright install-deps chromium; fi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]