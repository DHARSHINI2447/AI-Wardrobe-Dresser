from flask import Flask, request, Response, redirect
import requests

app = Flask(__name__)

TARGET_URL = "https://huggingface.co/spaces/HumanAIGC/OutfitAnyone"

@app.route('/')
def home():
    return redirect(TARGET_URL, code=302)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    # Forward the request to the target URL
    url = f"{TARGET_URL}/{path}"
    if request.method == 'GET':
        response = requests.get(url, params=request.args)
    elif request.method == 'POST':
        response = requests.post(url, json=request.json, data=request.form)
    elif request.method == 'PUT':
        response = requests.put(url, json=request.json, data=request.form)
    elif request.method == 'DELETE':
        response = requests.delete(url)
    else:
        response = Response("Method not allowed", status=405)

    # Create a response object
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

if __name__ == "__main__":

    app.run(debug=True)
