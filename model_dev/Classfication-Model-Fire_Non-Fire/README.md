## 🔥 Fire Detection with Binary Classification

This project performs binary classification to identify whether an image contains fire or not. The model was trained using a dataset created by our team during the **NASA Space Apps Challenge 2018**.

### Dataset

The dataset used for training and testing the model can be found on Kaggle: [Fire Dataset on Kaggle](https://www.kaggle.com/datasets/phylake1337/fire-dataset/data)

The dataset contains two folders:
1. **fire_images** - 755 outdoor-fire images, some of which contain heavy smoke.
2. **non_fire_images** - 244 nature images, including forest, trees, grass, rivers, people, foggy forests, lakes, animals, roads, and waterfalls.

---

### Prerequisites

- Google Colab 
- Python 3.x
- NumPy
- OpenCV
- TensorFlow
- scikit-learn
- Matplotlib
- Seaborn

**Environment Notes**

Some utilities used in this project are specific to **Google Colab** and are not required (or available) in other environments. The table below outlines which libraries has been included in `requirements.txt` and which should be skipped:

| Import                          | Include in `requirements.txt`? | Notes                                 |
|---------------------------------|-------------------------------|----------------------------------------|
| `from google.colab import drive` | ❌ No                          | Only available in Google Colab         |
| `from google.colab import files` | ❌ No                          | Only available in Google Colab         |
| `os`, `zipfile`                 | ❌ No                          | Built-in Python standard libraries     |
| `numpy`, `cv2`, `tensorflow`, `sklearn`, `matplotlib`, `seaborn` | ✅ Yes | Must be listed in `requirements.txt` for installation |


If you are running this notebook **outside of Google Colab**, you may need to **modify** Colab-specific code blocks (e.g., `drive.mount()` or `files.upload()`) and ensure all required packages are installed using `pip install -r requirements.txt`.

---

### Getting Started

#### Step 1: Download the Dataset
Download the dataset from the Kaggle link above.

#### Step 2: Clone the Repository
```bash
git clone https://github.com/yourusername/fire-detection.git
cd fire-detection
```

#### Step 3: Upload the Dataset
For running on Google Colab, upload the Kaggle dataset as the input in the 3rd cell of the notebook. If using other platforms, adjust the image upload method accordingly.

#### Step 4: Run the Notebook
Follow the cell order and execute each cell in sequence.
After running the model save cell, you will find the saved model in a folder named fire_detection_model.h5.

#### Step 5: Test the Model
Upload your test images and use the following code to test:
```python
def predict_fire(img_path, model):
    img = cv2.imread(img_path)

    # Check if image is loaded
    if img is None:
        print(f"❌ Error: Unable to load image at '{img_path}'. Check the file path!")
        return None

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))  # Resize
    img = img / 255.0  # Normalize
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    prediction = model.predict(img)
    class_label = "🔥 Fire" if np.argmax(prediction) == 1 else "❌ Non-Fire"

    return class_label

# Example usage
test_image_path = "test_image.jpg"  # Modify this with your image path
print(f"Prediction: {predict_fire(test_image_path, model)}")
```
