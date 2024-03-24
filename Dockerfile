FROM python:3.8

# Install pngquant
RUN apt-get update && apt-get install -y pngquant

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Set a default port if PORT environment variable is not set
ENV PORT 8000

# Start the application
CMD exec gunicorn -b 0.0.0.0:$PORT app:app