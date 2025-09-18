# Hand-Gesture-Volume-Control

A Python project that lets you control your system volume using hand gestures detected from your webcam, using OpenCV, MediaPipe, and Pycaw.

## Features

- **Real-time Hand Detection:** Uses your webcam and MediaPipe to detect hand landmarks.
- **Gesture-Based Volume Control:** Adjusts volume by measuring the distance between your thumb and index finger.
- **Volume Lock:** Hold down your middle finger to lock/unlock volume adjustments to prevent accidental changes.
- **Visual Feedback:** Displays current volume percentage, lock status, and hand landmark overlays.

## Demo

   <img width="1101" height="407" alt="image" src="https://github.com/user-attachments/assets/0022bb77-76d9-4702-889e-8f30548cd83b" />


## Requirements

- Python 3.7+
- Windows OS (uses Pycaw for audio control; see notes for other platforms)

Install dependencies:
```bash
pip install -r requirements.txt
```

## How It Works

1. **Hand Detection:** MediaPipe detects and tracks a single hand in the webcam frame.
2. **Landmark Extraction:** The tips of the thumb and index finger are used to determine the gesture.
3. **Volume Mapping:** The distance between the thumb and index finger maps to the system volume range.
4. **Lock Feature:** Lowering your middle finger "locks" the volume to avoid accidental changes.
5. **Visuals:** The app shows the current volume, lock status, and highlights gesture landmarks.

## Usage

1. Make sure your webcam is connected.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Use your hand in front of the camera:
   - **Thumb and Index Finger:** Pinch them together to lower the volume, spread apart to increase.
   - **Middle Finger Down:** Locks the volume (prevents changes).
   - **Middle Finger Up:** Unlocks volume control.
   - **Press 'q'** to quit.

## Notes

- **Windows only:** This script uses Pycaw, which relies on Windows Core Audio APIs.
- For Mac/Linux, alternative audio control libraries are needed; the rest of the code (MediaPipe, OpenCV) is cross-platform.

## Dependencies

- [OpenCV](https://opencv.org/)
- [MediaPipe](https://google.github.io/mediapipe/)
- [PyCaw](https://github.com/AndreMiras/pycaw) (Windows only)
- [NumPy](https://numpy.org/)

Install all dependencies via:
```bash
pip install -r requirements.txt
```

## License

MIT License

## Credits

- Hand tracking powered by [MediaPipe](https://google.github.io/mediapipe/).
- Audio control via [PyCaw](https://github.com/AndreMiras/pycaw).

---

Feel free to contribute or open issues!
