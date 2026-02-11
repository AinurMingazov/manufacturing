FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /manufacturing

COPY pyproject.toml ./
RUN pip install uv && uv sync --no-dev --no-install-project

COPY . .
RUN uv sync --no-dev --no-install-project

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
