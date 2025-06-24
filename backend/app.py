from flask import Flask, jsonify, render_template


app = Flask(__name__, template_folder="../templates")


@app.route("/health")
def health():
    return jsonify({"Status": "OK"})



@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)