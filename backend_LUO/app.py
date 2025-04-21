import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import cv2
import io
import uuid
import cv2
import numpy as np
from tensorflow.keras.models import load_model

print(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_path = "fire_detection_model.h5"
model = load_model(model_path)


def get_prediction(model, img_stream):
    try:
        # Convert stream to a NumPy array
        file_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)

        # Decode image using OpenCV
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Image decoding failed.")

        # Resize, normalize, and expand dims
        image = cv2.resize(image, (128, 128))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        # Make prediction
        prediction = model.predict(image)
        prediction = prediction[0]

        if prediction[1] >= 0.96:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        raise RuntimeError(f"Failed: {e}")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img_stream = io.BytesIO(contents)
        classification = get_prediction(model, img_stream)
        return {"prediction": classification}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))