FROM python:3.11

WORKDIR /app

# System dependencies for mysqlclient and building Python packages
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages (main PyPI mirror)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

# Copy all project files
COPY . .

EXPOSE 8000

# Default command for Django web
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

