# Stage 1: Install oxipng and pngquant using Homebrew
FROM linuxbrew/brew as builder

USER linuxbrew
RUN brew install pngquant oxipng

# Stage 2: Setup Python environment
FROM python:3.8

# Copy binaries from builder stage
COPY --from=builder /home/linuxbrew/.linuxbrew/bin/pngquant /usr/local/bin/
COPY --from=builder /home/linuxbrew/.linuxbrew/bin/oxipng /usr/local/bin/

# Check if pngquant and oxipng are correctly copied and are executable
RUN ls -l /usr/local/bin/pngquant
RUN ls -l /usr/local/bin/oxipng

RUN find / -name pngquant
RUN chmod +x /usr/local/bin/pngquant

# Print PATH
RUN echo $PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Start the application using Gunicorn
CMD gunicorn -b 0.0.0.0:$PORT app:app