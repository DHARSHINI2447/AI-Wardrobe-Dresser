import os
import cv2
import numpy as np
import json
import random
import requests
import base64
import gradio as gr

machine_number = 0
model = os.path.join(os.path.dirname(__file__), "models/eva/Eva_0.png")

MODEL_MAP = {
    "AI Model Rouyan_0": 'models/rouyan_new/Rouyan_0.png',
    "AI Model Rouyan_1": 'models/rouyan_new/Rouyan_1.png',
    "AI Model Rouyan_2": 'models/rouyan_new/Rouyan_2.png',
    "AI Model Eva_0": 'models/eva/Eva_0.png',
    "AI Model Eva_1": 'models/eva/Eva_1.png',
    "AI Model Simon_0": 'models/simon_online/Simon_0.png',
    "AI Model Simon_1": 'models/simon_online/Simon_1.png',
    "AI Model Xuanxuan_0": 'models/xiaoxuan_online/Xuanxuan_0.png',
    "AI Model Xuanxuan_1": 'models/xiaoxuan_online/Xuanxuan_1.png',
    "AI Model Xuanxuan_2": 'models/xiaoxuan_online/Xuanxuan_2.png',
    "AI Model Yaqi_0": 'models/yaqi/Yaqi_0.png',        
    "AI Model Yaqi_3": 'models/yaqi/Yaqi_3.png',
    "AI Model Yifeng_0": 'models/yifeng_online/Yifeng_0.png',
    "AI Model Yifeng_1": 'models/yifeng_online/Yifeng_1.png',
    "AI Model Yifeng_2": 'models/yifeng_online/Yifeng_2.png',
    "AI Model Yifeng_3": 'models/yifeng_online/Yifeng_3.png',
}

def add_waterprint(img):
    h, w, _ = img.shape
    img = cv2.putText(img, 'Powered by OutfitAnyone', (int(0.3 * w), h - 20), cv2.FONT_HERSHEY_PLAIN, 2, (128, 128, 128), 2, cv2.LINE_AA)
    return img

def get_public_ip():
    # Force to use localhost for local testing
    return '127.0.0.1'

def get_tryon_result(model_name, garment1, garment2, seed=1234):
    model_name = "AI Model " + model_name.split("/")[-1].split(".")[0]
    print("Model:", model_name)

    encoded_garment1 = cv2.imencode('.jpg', garment1)[1].tobytes()
    encoded_garment1 = base64.b64encode(encoded_garment1).decode('utf-8')

    if garment2 is not None:
        encoded_garment2 = cv2.imencode('.jpg', garment2)[1].tobytes()
        encoded_garment2 = base64.b64encode(encoded_garment2).decode('utf-8')
    else:
        encoded_garment2 = ''

    # Set the server port for local testing
    port = 8000  # Ensure this matches your backend server port

    # Construct the URL with localhost IP and port
    url = f'http://127.0.0.1:{port}'

    headers = {'Content-Type': 'application/json'}
    seed = random.randint(0, 1222222222)
    data = {
        "garment1": encoded_garment1,
        "garment2": encoded_garment2,
        "model_name": model_name,
        "seed": seed
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Response Code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            result = base64.b64decode(result['images'][0])
            result_np = np.frombuffer(result, np.uint8)
            result_img = cv2.imdecode(result_np, cv2.IMREAD_UNCHANGED)
            final_img = add_waterprint(result_img)
            return final_img
        else:
            print('Server error:', response.text)
            return None
    except requests.ConnectionError as e:
        print('Connection error:', e)
        return None

with gr.Blocks(css=".output-image, .input-image, .image-preview {height: 400px !important} ") as demo:
    gr.HTML(
        """
        <div style="display: flex; justify-content: center; align-items: center; text-align: center;">
        <div>
            <h1>Outfit Anyone: Ultra-high quality virtual try-on for Any Clothing and Any Person</h1>
            <h4>v0.9</h4>
            <h5 style="margin: 0;">If you like our project, please give us a star on Github to stay updated with the latest developments.</h5>
        </div>
        </div>
        """
    )
    with gr.Row():
        with gr.Column():
            init_image = gr.Image(sources='clipboard', type="filepath", label="model", value=model)
            example = gr.Examples(inputs=init_image,
                                  examples_per_page=4,
                                  examples=[
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Rouyan_0', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Rouyan_2', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Eva_0', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Simon_1', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Eva_1', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Simon_0', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Xuanxuan_0', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Xuanxuan_2', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Yaqi_0', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Yifeng_0', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Yifeng_3', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Rouyan_1', 'models/default.png')),
                                      os.path.join(os.path.dirname(__file__), MODEL_MAP.get('AI Model Yifeng_2', 'models/default.png')),
                                  ])
        with gr.Column():
            gr.HTML(
                """
                <div style="display: flex; justify-content: center; align-items: center; text-align: center;">
                <div>
                    <h3>Models are fixed and cannot be uploaded or modified; we only support users uploading their own garments.</h3>
                    <h4 style="margin: 0;">For a one-piece dress or coat, you only need to upload the image to the 'top garment' section and leave the 'lower garment' section empty.</h4>
                </div>
                </div>
                """
            )
            with gr.Row():
                garment_top = gr.Image(sources='upload', type="numpy", label="top garment")
                example_top = gr.Examples(inputs=garment_top,
                                          examples_per_page=5,
                                          examples=[
                                              os.path.join(os.path.dirname(__file__), "garments/top222.JPG"),
                                              os.path.join(os.path.dirname(__file__), "garments/top5.png"),
                                              os.path.join(os.path.dirname(__file__), "garments/top333.png"),
                                              os.path.join(os.path.dirname(__file__), "garments/dress1.png"),
                                              os.path.join(os.path.dirname(__file__), "garments/dress2.png"),
                                          ])
                garment_down = gr.Image(sources='upload', type="numpy", label="lower garment")
                example_down = gr.Examples(inputs=garment_down,
                                           examples_per_page=5,
                                           examples=[
                                               os.path.join(os.path.dirname(__file__), "garments/bottom1.png"),
                                               os.path.join(os.path.dirname(__file__), "garments/bottom2.PNG"),
                                               os.path.join(os.path.dirname(__file__), "garments/bottom3.JPG"),
                                               os.path.join(os.path.dirname(__file__), "garments/bottom4.PNG"),
                                               os.path.join(os.path.dirname(__file__), "garments/bottom5.png"),
                                           ])

                run_button = gr.Button(value="Run")
            with gr.Column():
                gallery = gr.Image()

                run_button.click(fn=get_tryon_result, 
                                 inputs=[init_image, garment_top, garment_down], 
                                 outputs=[gallery],
                                 concurrency_limit=2)
    
    # Examples
    gr.Markdown("## Examples")
    with gr.Row():
        reference_image1  = gr.Image(label="model", scale=1, value="examples/basemodel.png")
        reference_image2  = gr.Image(label="garment", scale=1, value="examples/garment1.jpg")
        reference_image3  = gr.Image(label="result", scale=1, value="examples/result1.png")
    gr.Examples(
        examples=[
            ["examples/basemodel.png", "examples/garment1.png", "examples/result1.png"],
            ["examples/basemodel.png", "examples/garment2.png", "examples/result2.png"],
            ["examples/basemodel.png", "examples/garment3.png", "examples/result3.png"],
        ],
        inputs=[reference_image1, reference_image2, reference_image3],
        label=None,
    )

if __name__ == "__main__":
    demo.queue(max_size=10)
    demo.launch()
