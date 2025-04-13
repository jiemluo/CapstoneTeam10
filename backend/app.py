import os
os.environ['TORCH_HOME'] = os.path.dirname(os.path.abspath(__file__))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import torch
import cv2
import io
import torchvision
from torchvision.io import read_image
from torchvision.transforms.functional import to_pil_image
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision import transforms
from PIL import Image
import numpy as np
import uuid

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

model_path = "RCNN_model_02.pth"

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
model.load_state_dict(torch.load("fasterrcnn_resnet50_fpn.pth", map_location="cpu"))

device = torch.device("cpu")
num_classes = 3
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model.to(device)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

def visualize_prediction(model, img_stream, device=torch.device('cpu')):
    try:
        # Set model to eval mode
        model.eval()
        filename = f"tmp_img/{uuid.uuid4()}.jpg"
        # Save uploaded file to a temporary file
        try:
            filename = f"tmp_img/{uuid.uuid4()}.jpg"
            print("attempted filename is: ", filename)
            with open(filename, "wb") as f:
                f.write(img_stream.read())
        except Exception as e:
            raise RuntimeError(f"[File Save Error] Couldn't save uploaded image: {e}")


        # Load image tensor using torchvision
        try:
            img_tensor = read_image(filename).float() / 255.0
            img_tensor = img_tensor.unsqueeze(0).to(device)
        except Exception as e:
            raise RuntimeError(f"[Tensor Conversion Error] Failed to convert image: {e}")

        # Run inference
        try:
            with torch.no_grad():
                preds = model(img_tensor)[0]
        except Exception as e:
            raise RuntimeError(f"[Model Inference Error] Prediction failed: {e}")
        
        # Load original image with OpenCV for drawing
        try:
            img = cv2.imread(filename)
            if img is None:
                raise ValueError("cv2.imread returned None")
        except Exception as e:
            raise RuntimeError(f"[Image Load Error] Could not read image for visualization: {e}")

        # Draw bounding boxes
        try:
            for i, box in enumerate(preds['boxes']):
                score = preds['scores'][i].item()
                if score > 0.5:
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                    cv2.putText(img, f"{score:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 155), 1)
        except Exception as e:
            raise RuntimeError(f"[Drawing Error] Failed to annotate image: {e}")
        
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)

            result_bytes = io.BytesIO()
            img_pil.save(result_bytes, format='JPEG')
            result_bytes.seek(0)
            return result_bytes
        except Exception as e:
            raise RuntimeError(f"[Encoding Error] Could not convert image to bytes: {e}")
        
    finally:
        #Always delete the temp file
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
        result_img = visualize_prediction(model, img_stream)
        return StreamingResponse(result_img, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))