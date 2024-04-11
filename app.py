import os
import shutil
import uuid  # Import the os module
from flask import Flask, render_template, request, session, send_from_directory, g
from compressor import process_json_file, process_directory  # Import the modified Python script functions

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4());
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 Megabytes
app.config['UPLOAD_FOLDER'] = 'uploads'
# Add print statements for debugging
print(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    if 'user_folder' not in session:
        session['user_folder'] = str(uuid.uuid4())  # Create a unique folder for this session

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_folder'])
    os.makedirs(user_folder, exist_ok=True)  # Create the folder if it doesn't exist
    g.user_folder = user_folder  # Store user_folder in g

    uploaded_files = request.files.getlist("files")
    quality = request.form.get("quality")

    all_compression_info = []
    for file in uploaded_files:
        if file.filename.endswith('.json'):
            file_path = os.path.join(user_folder, file.filename)  # Save file in user's unique folder
            file.save(file_path)
            # Run main function and get info back
            compression_info = process_json_file(file_path, quality)
            if compression_info is not None:
                download_path = compression_info[-1]['new_json_file_path']  
                lottie_details = compression_info[-1]
                compression_info.pop()

                all_compression_info.append({
                    'image_details': compression_info,
                    'download_path': download_path,
                    'file_name': file.filename,
                    'session_path': session['user_folder'],
                    'lottie_details': lottie_details
                }) 
            # # Run main function and get info back
            # compression_info = process_json_file(file_path, quality)
            # # Extract variables to pass to user
            # download_path = compression_info[-1]['new_json_file_path']  
            # lottie_details = compression_info[-1]
            # # Remove lottie details and only keep images
            # compression_info.pop()

            # all_compression_info.append({
            #     'image_details': compression_info,
            #     'download_path': download_path,
            #     'file_name': file.filename,
            #     'session_path': session['user_folder'],
            #     'lottie_details': lottie_details
            # })
 
            #os.remove(file_path)  # Remove temporary file after processing
    return render_template('result.html', all_compression_info=all_compression_info)

# Serve files in uploads folder
@app.route('/uploads/<path:filename>')
def uploaded_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
