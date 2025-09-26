FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy project files
COPY . .

# Set default environment variables for Django superuser
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@admin.com
ENV DJANGO_SUPERUSER_PASSWORD=admin

# Expose port
EXPOSE 8000

RUN echo '#!/bin/bash\n\
  echo "Starting Django setup..."\n\
  echo "Making migrations..."\n\
  uv run python manage.py makemigrations\n\
  echo "Applying migrations..."\n\
  uv run python manage.py migrate\n\
  echo "Creating superuser..."\n\
  uv run python manage.py createsuperuser --noinput || echo "Superuser already exists"\n\
  echo "Starting Django development server..."\n\
  uv run python manage.py runserver 0.0.0.0:8000\n\
  ' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
