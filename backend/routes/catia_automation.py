from flask import Flask, Blueprint, request, render_template, flash, jsonify, session

import requests


ollama_api_url = "http://localhost:11434/api/generate"
# model_name = "qwen2.5vl:7b"
model_name = "llama3.2:1b"


  # Enable CORS globally

catia_automation = Blueprint('catia_automation', __name__, template_folder='../templates')

@catia_automation.route('/catia_automation', methods=['GET', 'POST'])
def catiaautomation():
    if request.method == "GET":
        cad_screenshots = session.get('cad_screenshot', None)
        print("cad screenshots type and data", type(cad_screenshots), cad_screenshots)
        if isinstance(cad_screenshots, str):
            import ast
            try:
                cad_screenshots = ast.literal_eval(cad_screenshots)
            except (ValueError, SyntaxError):
                cad_screenshots = []
    
        print("cad screenshots type and data 2:", type(cad_screenshots), cad_screenshots)
        return render_template('catia_automation.html', cad_screenshots = cad_screenshots)
    elif request.method == "POST":
        file = request.files.get('catpart_file')
        if not file:
            flash('Please upload a valid .CATPart file.', 'warning')
        # handle file here...
        return render_template('catia_automation.html')




@catia_automation.route("/api/ollama", methods=["POST"])
def ollama_chat():
    data = request.get_json(silent=True) or {}
    print('user data;, ', data)
    prompt = data.get("prompt", "").strip()
    print("user prompt", prompt)
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False  # ensure you get a full JSON response
    }

    try:
        resp = requests.post(ollama_api_url, json=payload)
        print('resp',resp)
        # resp.raise_for_status()
        resp_json = resp.json()
        llm_response = resp_json.get("response", "")
        print('llm response', llm_response)
        return jsonify({"response": llm_response})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500








# @catia_automation.route('/catia_automation', methods=['GET', 'POST'])
# def index():
#     if request.method == "GET":
#         return render_template('index.html')
#     elif request.method == 'POST':
#         file = request.files.get('catpart_file')
#         # if file and file.filename.endswith('.CATPart'):
#         #     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         #     file.save(file_path)
#         #     success = open_catpart_in_catia(file_path)
#         # if success:
#         #     flash('File opened in CATIA successfully!', 'success')
#         # else:
#         #     flash('Failed to open file in CATIA.', 'error')
#     else:
#         flash('Please upload a valid .CATPart file.', 'warning')
#     return render_template('index.html')
