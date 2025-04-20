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
        filename = f"tmp_img/{uuid.uuid4()}.jpg"
        try:
            print("attempted filename is: ", filename)
            with open(filename, "wb") as f:
                f.write(img_stream.read())
        except Exception as e:
            raise RuntimeError(f"[File Save Error] Couldn't save uploaded image: {e}")

        try:
            image = cv2.imread(filename)
            dimensions = (128, 128)
            image = cv2.resize(image, dimensions)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = (image/255).astype(np.float16)
            image_data = image.reshape(1, 128, 128, 3)
            prediction = model.predict(image_data)
            class_label = "🔥 Fire" if np.argmax(prediction) == 1 else "❌ Non-Fire"
            return class_label
        except Exception as e:
            print(e)
            raise RuntimeError(f"Failed: {e}")
        
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"[Cleanup Warning] Could not delete temp file {filename}: {e}")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img_stream = io.BytesIO(contents) 
        classification = get_prediction(model, img_stream)
        return Response(classification)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))