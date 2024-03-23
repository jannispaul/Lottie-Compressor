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
    # uploaded_files = request.files.getlist("files")
    # quality = request.form.get("quality")
    # print(quality)  # Print quality to console

    # compression_info = []
    # for file in uploaded_files:
    #     if file.filename.endswith('.json'):
    #         # file_path = f"/tmp/{file.filename}" 
    #         file_path = os.path.join('static', file.filename)  # Save file in static folder # Save file temporarily
    #         file.save(file_path)
    #         compression_info_list = process_json_file(file_path, quality)
    #         download_path = compression_info_list[0]  
    #         compression_info = compression_info_list[1] 
    #         os.remove(file_path)  # Remove temporary file after processing
    # print(compression_info_list[1])  # Add this line to check compression_info content
    # return render_template('result.html', compression_info=compression_info, download_path = download_path, file_name = file.filename)
    if 'user_folder' not in session:
        session['user_folder'] = str(uuid.uuid4())  # Create a unique folder for this session

    # user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_folder'])
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_folder'])
    os.makedirs(user_folder, exist_ok=True)  # Create the folder if it doesn't exist
    g.user_folder = user_folder  # Store user_folder in g

    uploaded_files = request.files.getlist("files")
    quality = request.form.get("quality")
    print(quality)  # Print quality to console

    compression_info = []
    for file in uploaded_files:
        if file.filename.endswith('.json'):
            file_path = os.path.join(user_folder, file.filename)  # Save file in user's unique folder
            file.save(file_path)
            
            # Run main function and get info back
            compression_info = process_json_file(file_path, quality)
            # Extract variables to pass to user
            download_path = compression_info[-1]['new_json_file_path']  
            lottie_details = compression_info[-1]
            print(compression_info)
            compression_info.pop()
 
            # compression_info = compression_info[] 
            #os.remove(file_path)  # Remove temporary file after processing
    # print(compression_info_list[1])  # Add this line to check compression_info content
    return render_template('result.html', image_details=compression_info, download_path = download_path, file_name = file.filename, session_path = session['user_folder'], lottie_details=lottie_details)


# Serve files in uploads folder
@app.route('/uploads/<path:filename>')
def uploaded_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/result', methods=['POST'])
# def result():
#     uploaded_files = request.files.getlist("files")
#     compression_info = []

#     for file in uploaded_files:
#         if file.filename.endswith('.json'):
#             file_path = f"/tmp/{file.filename}"  # Save file temporarily
#             file.save(file_path)
#             compression_info.extend(process_json_file(file_path))
#             os.remove(file_path)  # Remove temporary file after processing

#     print(compression_info)  # Add this line to check compression_info content
#     return render_template('result.html', compression_info=compression_info)


# if __name__ == '__main__':
#     app.run(debug=True)
