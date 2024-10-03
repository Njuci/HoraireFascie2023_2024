FROM python:3.10-slim

# Set the working directory
WORKDIR /HoraireFascie2023_2024

# Create the sources.list file if it doesn't exist and use a different Debian mirror
RUN [ ! -f /etc/apt/sources.list ] && echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list
RUN sed -i 's|http://deb.debian.org/debian|http://ftp.de.debian.org/debian|g' /etc/apt/sources.list

# Install pkg-config, gcc, wget, and MariaDB development libraries
RUN apt-get update && \
    apt-get install -y pkg-config gcc wget libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements with increased timeout
RUN pip install --default-timeout=100 -r requirements.txt

# Copy the rest of the files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate --noinput
CMD ["gunicorn", "--bind", ":8000", "horairefascie2023_2024.wsgi"] 
