FROM linuxbrew/brew:3.8

# Install pngquant and oxipng
RUN brew install pngquant oxipng

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Start the application using Gunicorn
CMD gunicorn -b 0.0.0.0:$PORT app:app