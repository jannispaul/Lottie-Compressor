import ujson
import base64
import os
import logging
import re
import subprocess
import tempfile

logging.basicConfig(level=logging.INFO)

def find_and_compress_images(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                match = re.search(r'data:image/png;base64,([\w+/=]+)', value)
                if match:
                    logging.info(f"Found image in {key}")
                    image_base64 = match.group(1)

                    # Convert base64 to image
                    image_bytes = base64.b64decode(image_base64)
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        tmp_file.write(image_bytes)
                        tmp_file.close()

                    # Log original file size
                    original_size = len(image_bytes)
                    logging.info(f"Original size of {key}: {original_size} bytes")

                    # Compress image with pngquant
                    pngquant_output = subprocess.check_output(['pngquant', '--quality', '50', '--force', '--output', '-', tmp_file.name])

                    # Further optimize with oxipng
                    oxipng_output = subprocess.check_output(['oxipng', '--quiet', '--strip', 'all', '--out', tmp_file.name, '-'], input=pngquant_output)

                    # Read the optimized compressed image
                    with open(tmp_file.name, 'rb') as f:
                        compressed_image_bytes = f.read()

                    # Log compressed file size before and after
                    compressed_size_before = len(image_bytes)
                    compressed_size_after_PNGQUANT = len(pngquant_output)
                    compressed_size_after = len(compressed_image_bytes)
                    logging.info(f"Compressed size of {key} before: {compressed_size_before} bytes")
                    logging.info(f"Compressed size of {key} after PNGQuant: {compressed_size_after_PNGQUANT} bytes")
                    logging.info(f"Compressed size of {key} after: {compressed_size_after} bytes")

                    # Convert compressed image to base64
                    compressed_base64 = base64.b64encode(compressed_image_bytes).decode('utf-8')

                    # Replace original string
                    data[key] = value.replace(image_base64, compressed_base64)
                    logging.info(f"Replaced {key} in JSON")
            elif isinstance(value, (dict, list)):
                find_and_compress_images(value)
    elif isinstance(data, list):
        for item in data:
            find_and_compress_images(item)

def process_json_file(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = ujson.load(file)

        find_and_compress_images(data)

        new_json_file_path = os.path.splitext(json_file_path)[0] + "-small.json"

        with open(new_json_file_path, 'w') as file:
            ujson.dump(data, file, ensure_ascii=False, separators=(',', ':'))
            logging.info(f"Created compressed JSON file: {new_json_file_path}")
    except Exception as e:
        logging.error(f"Error processing JSON file: {e}")

def process_directory(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            logging.info(f"Processing JSON file: {file_path}")
            process_json_file(file_path)

if __name__ == "__main__":
    input_path = input("Enter the path to the JSON file or directory: ")
    if os.path.isfile(input_path):
        process_json_file(input_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    else:
        logging.error("Invalid file or directory path.")
