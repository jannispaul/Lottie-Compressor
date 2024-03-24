FROM python:3.8

# Install pngquant and oxipng
RUN apt-get update && apt-get install -y pngquant oxipng

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose the port that your app runs on
# EXPOSE $PORT

# Start the application using Gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
CMD gunicorn -b 0.0.0.0:$PORT app:app