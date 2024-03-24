FROM python:3.8

# Install dependencies
RUN apt-get update && apt-get install -y curl git

# Install Homebrew
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH
ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"

# Install pngquant and oxipng
RUN brew install pngquant oxipng

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Start the application using Gunicorn
CMD gunicorn -b 0.0.0.0:$PORT app:app