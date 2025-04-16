**Capstone Team 10 - The Insomniacs**

**Team Members**(falnabol-khanabd-jiemluo): 
- **Jie Luo** - jiemluo@umich.edu
- **Abdullah Khan** - khanabd@umich.edu
- **Fadi Alnabolsi** - falnabol@umich.edu

## 🔥 Fire Image Detection and Classification

Fire detection is an essential task for safety and disaster prevention. Traditional systems like heat sensors and alarms often struggle in open or large-scale environments. To enhance early detection, this project leverages **deep learning models** to analyze images and detect fire-related incidents.

We built two types of models:
- **Fire Classification Model** – Determines if an image contains fire.
- **Fire Localization Model** – Detects and highlights fire zones within an image.

Alongside the models, we've also developed a simple **React-based web app** to make predictions accessible to non-technical users.

---

### 📂 Project Structure

- The GitHub repository is organized for easy navigation and development:
- The repository contains three main components, each in its own folder with a dedicated `README.md` explaining how to run the code.

`Classification-Model-Fire:Non-Fire/`
  - `Fire_Detection_Jie_Luo.ipynb` – Main notebook for building and testing the fire classification model.
  - `fire_detection_model.h5` – Trained model file.
  - `requirements.txt` – Python package dependencies.
  - `test_image.jpg`, `test_image_2.jpg` – Sample images for testing the model.
  - `README.md` – Instructions for running the notebook.

`Localization-Model-Fire/`
  - Notebook and scripts for the fire localization model.
  - `README.md` – Instructions for training and testing localization.

`WebApp/`
  - Source code for the web interface (frontend and backend).
  - `README.md` – Setup and deployment guide.

---

### 🛠️ Installation (for Developers)

Clone the repository:

```bash
git clone https://github.com/your-username/fire-image-detection.git
cd fire-image-detection
```

Navigate to the desired component folder and follow its specific instructions.

---

### 🤝 Contribution
We welcome contributions! To get started:

- Fork this repo
- Create your branch:

  ```bash
  git checkout -b <feature-name>
  ```

- Commit your changes:
  ```bash
  git commit -am 'Add new feature'
  ```

- Push to the branch:
  ```bash
  git push origin <feature-name>
  ```

- Submit a pull request

---

### 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.
