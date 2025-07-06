
import os
import win32com.client
import pythoncom

from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from utils_scripts.file_loader import open_catpart_in_catia
from dotenv import load_dotenv


app = Flask(__name__, template_folder="../templates")
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/health")
def health():
    return jsonify({"Status": "OK"})



def open_catpart_in_catia(file_path):
    try:
        pythoncom.CoInitialize()  # Initialize COM for this thread
        catia = win32com.client.Dispatch("CATIA.Application")
        catia.Visible = True
        documents = catia.Documents
        documents.Open(file_path)
        return True
    except Exception as e:
        print(f"Error opening file in CATIA: {e}")
        return False




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == 'POST':
        file = request.files.get('catpart_file')
        if file and file.filename.endswith('.CATPart'):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            success = open_catpart_in_catia(file_path)
        if success:
            flash('File opened in CATIA successfully!', 'success')
        else:
            flash('Failed to open file in CATIA.', 'error')
    else:
        flash('Please upload a valid .CATPart file.', 'warning')
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('catpart_file')
    if file and file.filename.endswith('.CATPart'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        open_catpart_in_catia(os.path.abspath(file_path))
    return '', 204





if __name__ == "__main__":
    app.run(debug=True, port=5000)