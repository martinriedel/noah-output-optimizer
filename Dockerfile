ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and pip
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make run script executable
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]