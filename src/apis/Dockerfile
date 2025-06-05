FROM python:3.10 AS backend

# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set the working directory
WORKDIR /src

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create venv and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \

# Copy the rest of the code
COPY app.py app.py

# Expose port
EXPOSE 8000

# Run using the venv's uvicorn
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
