FROM python:3.8

# Install pngquant, build-essential, curl and Rust for compiling oxipng from source
RUN apt-get update && apt-get install -y pngquant build-essential curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Download and compile oxipng
RUN curl -L https://github.com/optipng/oxipng/releases/download/v9.0.0/oxipng-9.0.0.tar.gz | tar xz \
    && cd oxipng-9.0.0 \
    && cargo build --release \
    && cp target/release/oxipng /usr/local/bin/

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Start the application using Gunicorn
CMD gunicorn -b 0.0.0.0:$PORT app:app