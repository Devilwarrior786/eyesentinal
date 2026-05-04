---
# 👁️ EyeSentinel – Driver Drowsiness Detection

EyeSentinel is a real-time driver drowsiness detection system built using computer vision.
It monitors eye behavior through facial landmarks and alerts the user when prolonged eye closure is detected.

---

## 🚀 Features

* 👁️ Real-time eye tracking using facial landmarks
* 🧠 Eye Aspect Ratio (EAR) based drowsiness detection
* 🚫 Ignores normal blinking (no false alerts)
* 🟡 Works with small eyes and different face shapes
* 🔊 Audio alert system (beep)
* 🎨 Face mesh visualization for better understanding
* ⚡ Lightweight – no heavy deep learning models required

---

## 🧠 How It Works

EyeSentinel uses MediaPipe Face Mesh to extract facial landmarks.

It calculates the **Eye Aspect Ratio (EAR)**:

* Eyes open → higher EAR
* Eyes closed → lower EAR

If EAR stays below a threshold for a certain number of frames →
➡️ **Drowsiness Alert is triggered**

---

## 📦 Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/EyeSentinel.git
cd EyeSentinel
```

Create virtual environment:

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Run the Project

```bash
python main.py
```

Press **`q`** to exit.

---

## 🎯 Usage

* Look at the camera → **Status: AWAKE**
* Blink normally → No alert
* Close eyes for ~1 second → 🚨 **DROWSINESS ALERT**

---

## 🔧 Configuration

You can tweak sensitivity inside `main.py`:

```python
FULLY_CLOSED_EAR = 0.18
DROWSY_FRAMES = 18
```

* Lower EAR → stricter detection
* Higher frames → slower alert

---

## 🎬 Demo

Add your demo video or GIF here 👇
*(recommended for better engagement)*

---

## 📌 Future Improvements

* Yawning detection
* Head pose estimation
* Mobile / Raspberry Pi deployment
* UI dashboard with fatigue score

---

## ⚠️ Disclaimer

This project is a prototype and should not be used as a standalone safety system in real-world driving conditions.

---

## 🙌 Acknowledgements

* MediaPipe
* OpenCV

---

## ⭐ Show Your Support

If you found this useful, consider giving it a ⭐ on GitHub!

---

## 🏁

Built as a step towards safer roads 🚗

---
