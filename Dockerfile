FROM python:3.10 AS backend

# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set the working directory
WORKDIR /apis

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create venv and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \

# Copy the rest of the code
COPY src/apis/app.py src/apis/app.py

# Expose port
EXPOSE 8000

# Run using the venv's uvicorn
CMD ["nohup", "uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10 AS frontend

# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set the working directory
WORKDIR /front

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create venv and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync 

# Copy the rest of the code
COPY src/webapp/app.py src/webapp/app.py

# Expose port
EXPOSE 8501

# Run using the venv's uvicorn
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=127.0.0.1"]
