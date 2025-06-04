FROM python:3.10



# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create venv and install dependencies
RUN uv sync --no-cache-dir

# Copy the rest of the code
COPY . .
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run using the venv's uvicorn
CMD [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
