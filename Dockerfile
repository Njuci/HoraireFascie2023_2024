FROM python:3.10-slim

# Set the working directory
WORKDIR /HoraireFascie2023_2024

# Update package sources and install necessary libraries
RUN apt-get update && \
    apt-get install -y pkg-config gcc wget libmariadb-dev-compat libmariadb-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --default-timeout=100 --retries=5 -r requirements.txt

# Copy the rest of the files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate --noinput

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "horairefascie2023_2024.wsgi:application"]
