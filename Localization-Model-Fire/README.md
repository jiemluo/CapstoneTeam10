# Faster R-CNN Object Detection

This repository contains a **Faster R-CNN** model trained using `PyTorch` and `torchvision` for the detection of fire using custom fire data from Kaggle.
You can download the dataset from the following link: https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo



---

## Files
- Training_RCNN.ipynb - Used for training the RCNN model
- Testing_RCNN.ipynb - Used for testing images and getting test metrics on the trained model
- Live_Videofeed_Demo_RCNN.iynb - Used to run a live camera demonstration on the model on an available camera
- test_model_01.pth - The trained model file that can be used for testing and live footage


---
## How to test the RCNN model on a live camera
1. Download the 'Localization-Model-Fire/Live_Videofeed_Demo_RCNN.ipynb', and 'test_model_01.pth' file.
2. Update the second block within the IPython notebook file such that once you run it in your environment, the .pth model file location is updated according to where the file is in your system.
3. Once you run the next cell, your camera will open, and you will be able to test how the model works.
4. Press 'q' in order to quit. If that doesn't work, manually stop the cell and rerun the last two lines within it.

The model was trained mostly on large fires. Because of this, among other reasons, it will not work properly on small symmetrical fires like that from a lighter. You will either need a bigger fire, like that on a pot stove, or have a secondary screen with images of fire or a video of a fire-related incident to put into the frame of the camera. Because of the nature of the test, if you do end up testing live fire, please make sure that it is being done outdoors in a safe environment. If it is indoors, make sure it is under a functional kitchen hood, with proper safety equipment present nearby. Please be cautious and play with fire at your own risk. 
