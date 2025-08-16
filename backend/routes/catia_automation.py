from flask import Flask, Blueprint, request, render_template, flash, jsonify, session

import requests
from ollama import chat, ChatResponse
import pythoncom
from ..automation_scripts.bounding_box import generate_bounding_box
import json

ollama_api_url = "http://localhost:11434/api/generate"
model_name = "qwen2.5vl:7b"
# model_name = "llama3.2:1b"


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
    print('User data:', data)

    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Instruction to analyze intent
    intent_instruction = (
        "Analyze the following user input and return a JSON object with the following format: "
        "{'user_bbox_intent': true or false, 'offset': offset value mentioned in prompt or 0(zero)}"
        "'user bbox intent' is true if the user is asking to generate a bounding box. "
        "'offset' is the number mentioned in the query, or 0 if none is provided. "
        "Respond ONLY with the JSON object."
    )

    full_prompt = f"{intent_instruction}\nUser Query: {prompt}"
    print("Full prompt for intent analysis:", full_prompt)

    intent_payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        intent_resp = requests.post(ollama_api_url, json=intent_payload)
        intent_json = intent_resp.json()
        print("Intent Response:", intent_json)
        analysis = intent_json.get("response", "{}")
        print("analysis", analysis)
        llm_response = jsonify({"response": analysis})
        print("LLM Response:", llm_response)

        # Convert response string to dictionary
        intent_data = json.loads(analysis)
        print("intent_data type", type(intent_data), intent_data)

        bbox_intent = intent_data.get("user_bbox_intent", False)
        print("bbox_intent", bbox_intent)
        offset = int(intent_data.get("offset", 0))
        print("offset", offset)

        if bbox_intent:
            # User wants to generate bounding box
            print('generating bounding box with offset:', offset)
            result = generate_bounding_box(offset)
            print('backed by calling bounding box function, result:', result)
            if result is True:
                return jsonify({"response": "Bounding Box generated successfully"})
            else:
                return jsonify({"response": result})

        else:
            # User is asking a general CAD-related question
            system_instruction = (
                "You are an expert in the automotive domain."
                "Assist users in CAD engineering, modeling, and design-related topics. "
                "Respond with precise and shot answers. Use automotive language tone while answering and highlights the key points. "
                "If a question is unrelated to automotive design or engineering, reply: "
                "'I'm sorry, I can only assist with automotive domain queries.'"
            )

            full_prompt = f"{system_instruction}\n{prompt}"
            response_payload = {
                "model": model_name,
                "prompt": full_prompt,
                "stream": False
            }

            response = requests.post(ollama_api_url, json=response_payload)
            response_json = response.json()
            print("Response JSON:", response_json)
            llm_response = response_json.get("response", "")
            print("LLM Response:", llm_response)
            return jsonify({"response": llm_response})

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500






# Working correctly
# @catia_automation.route("/api/ollama", methods=["POST"])
# def ollama_chat():
#     data = request.get_json(silent=True) or {}
#     print('user data;, ', data)
#     prompt = data.get("prompt", "").strip()
#     print("user prompt", prompt)

#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400
    
#     system_instruction = (
#         "You are an expert of automotive domain. "
#         "Your task is to assist user in CAD engineering, cad model and designand etc. related topics"
#         "Respond with precise and short answers. Use technical language appropriate for automotive professionals and highlights the key points."
#         "If a question is not related to automotive design or engineering, respond with a message - I'm sorry, I can only assist with automotive domain queries."
#     )

#     full_prompt = system_instruction + prompt


#     payload = {
#         "model": model_name,
#         "prompt": full_prompt,
#         "stream": False  # ensure you get a full JSON response
#     }

#     try:
#         resp = requests.post(ollama_api_url, json=payload)
#         print('resp',resp)
#         # resp.raise_for_status()
#         resp_json = resp.json()
#         llm_response = resp_json.get("response", "")
#         print('llm response', llm_response)
#         return jsonify({"response": llm_response})
#     except requests.RequestException as e:
#         return jsonify({"error": str(e)}), 500




