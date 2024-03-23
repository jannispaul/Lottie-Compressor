import ujson
import base64
import os
import logging
import re
import subprocess
import tempfile


logging.basicConfig(level=logging.INFO)


def find_and_compress_images(json_file_path, data, quality):
    """
    Finds and compresses images in a JSON data structure.

    Args:
        data (dict or list): The JSON data structure to process.

    Returns:
        None
    """
    images = []
    image_index = 0
    stack = [data]

    while stack:
        current_data = stack.pop()

        if isinstance(current_data, dict):
            for key, value in current_data.items():
                if isinstance(value, str):
                    # Each match is an individual PNG in the lottie file
                    match = re.search(r'data:image/png;base64,([\w+/=]+)', value)

                    if match:
                        # logging.info(f"{image_index} index")
                        image_base64 = match.group(1)
                        image_bytes = base64.b64decode(image_base64)

                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            tmp_file.write(image_bytes)
                            tmp_file.close()

                        pngquant_output = subprocess.check_output(['pngquant', '--quality', quality, '--force', '--output', '-', tmp_file.name])
                        oxipng_output = subprocess.check_output(['oxipng', '--quiet', '--strip', 'all', '--out', tmp_file.name, '-'], input=pngquant_output)

                        with open(tmp_file.name, 'rb') as f:
                            compressed_image_bytes = f.read() 

                        compressed_base64 = base64.b64encode(compressed_image_bytes).decode('utf-8')

                        current_data[key] = value.replace(image_base64, compressed_base64)
                        
                        # Save the match as a PNG to the static folder
                        static_folder = os.path.dirname(json_file_path)
                        image_path = os.path.join(static_folder, f'image_{image_index}.png')
                        with open(image_path, 'wb') as f:
                            f.write(image_bytes)
                     

                        images.append({
                            'path': image_path,
                            # 'key': key,
                            # 'match': match.group(1),
                            'index': image_index,
                            'image_bytes': base64.b64decode(match.group(1)),
                            'file_link': f'image_{image_index}.png',
                            'original_size': len(image_bytes),
                            'compressed_size_after_PNGQUANT': len(pngquant_output),
                            'compressed_size_after_OXIPNG': len(compressed_image_bytes)
                        })
                        
                        images[-1]['relative_savings'] = round((1 - images[-1]["compressed_size_after_OXIPNG"] / images[-1]["original_size"]) * 100)
                        image_index += 1

                        # logging.info(f"{images[-1]['index'] + 1} Image(s)")
                        # logging.info(f"{images[-1]['file_link']}")
                        # logging.info(f"{images[-1]['original_size']}")
                        # logging.info(f"{images[-1]['compressed_size_after_PNGQUANT']}")
                        # logging.info(f"{images[-1]['compressed_size_after_OXIPNG']}")


                elif isinstance(value, (dict, list)):
                    stack.append(value)
        elif isinstance(current_data, list):
            for item in current_data:
                stack.append(item)
    return images


def process_json_file(json_file_path, quality = "75"):
    """
    Processes a JSON file by finding and compressing images.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        None
    """
    try:
        with open(json_file_path, 'r') as file:
            data = ujson.load(file)
            file_size = os.path.getsize(json_file_path)
        
        compression_info = find_and_compress_images(json_file_path, data, quality)
      

        
        # After updating the JSON data
        # Create a path to save the new file
        new_json_file_path = os.path.splitext(json_file_path)[0] + "-small.json"
        # Save the compressed json file
        with open(new_json_file_path, 'w') as file:
            ujson.dump(data, file, ensure_ascii=False, separators=(',', ':'))
            # logging.info(f"Created compressed JSON file: {new_json_file_path}")


        compressed_file_size = os.path.getsize(new_json_file_path)
        # Calculate the compressed file size
        relative_savings = round((1 - compressed_file_size / file_size) * 100)

        compression_info.append({
            'original_size': file_size,
            'compressed_size': compressed_file_size,
            'relative_savings': relative_savings,
            'new_json_file_path': new_json_file_path
        })

        logging.info("compression info", compression_info) 
        return compression_info
        
    except Exception as e:
        logging.error(f"Error processing JSON file: {e}")

def process_directory(directory_path):
    """
    Processes all JSON files in a directory by finding and compressing images.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        None
    """
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            # logging.info(f"Processing JSON file: {file_path}")
            process_json_file(file_path)

if __name__ == "__main__":
    input_path = input("Enter the path to the JSON file or directory: ")
    if os.path.isfile(input_path):
        process_json_file(input_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    else:
        logging.error("Invalid file or directory path.")
