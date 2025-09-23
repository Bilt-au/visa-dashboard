FROM node:18-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app
COPY . .

# Copy frontend build from previous stage
COPY --from=frontend /app/build ./static/

# Collect static files
RUN python manage.py collectstatic --noinput

# Set environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE $PORT

# Run migrations and start server
CMD python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT