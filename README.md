# Car Seatbelt Detection Using YOLOv8

This project is a **Car Seatbelt Detection System** using **YOLOv8** for object detection, deployed on a **XAMPP** server with a **PHP-based user interface**.

## Features
- Detects seatbelt usage in images
- Provides a web-based interface using PHP
- Generates an HTML report with detection results
- Uses YOLOv8 for object detection
- Outputs labeled images with bounding boxes

## Installation
### Prerequisites
Ensure you have the following installed:
- Python (>=3.7)
- XAMPP Server (Apache & PHP enabled)
- Required Python libraries (listed in `requirements.txt`)

### Install Dependencies
Run the following command to install required packages:
```bash
pip install -r requirements.txt
```

## Usage
### 1. Start XAMPP Server
Make sure your Apache server is running in XAMPP.

### 2. Place Files in htdocs
Copy the project files into your `htdocs` directory of XAMPP (e.g., `C:\xampp\htdocs\yolo`).

### 3. Access the Web Interface
Open your browser and go to:
```
http://localhost/yolo/index.php
```
This will load the PHP-based user interface where you can upload images for detection.

### 4. Run YOLO Detection Script (Backend)
The detection script is triggered through the PHP interface. Alternatively, you can manually run it:
```bash
python yolo_detection.py <input_image_path> <output_directory> <confidence_threshold>
```
Example:
```bash
python yolo_detection.py input.jpg output 0.6
```
This will:
- Process the image
- Save the detected output image
- Generate an HTML report with detection details

### 5. View Detection Results
Once the script runs, results will be displayed on the web interface. You can also view them directly in the browser at:
```
http://localhost/yolo/output/detected_image.html
```

## File Structure
```
|-- demo/                          # Screenshots of the project
|-- index.php                      # PHP-based user interface for web access
|-- yolo_detection.py               # YOLOv8 Detection Script
|-- best.pt                         # Trained YOLOv8 model weights
|-- requirements.txt                # Dependencies
```

## Example Output
The detection results include:
- **Processed Image**: The image with bounding boxes drawn on detected objects.
- **HTML Report**: A generated webpage displaying detection details such as class labels, confidence scores, and bounding box coordinates.

### Example Screenshots
![Detection Example 1](https://github.com/QAshan2021/car-seatbelt-detection-using-yolov8/blob/main/demo/screencapture-localhost-yolo-2025-03-19-15_46_44.png)

![Detection Example 2](https://github.com/QAshan2021/car-seatbelt-detection-using-yolov8/blob/main/demo/screencapture-localhost-yolo-2025-03-19-15_47_56.png)
The detection results include:
- **Processed Image**: The image with bounding boxes drawn on detected objects.
- **HTML Report**: A generated webpage displaying detection details such as class labels, confidence scores, and bounding box coordinates.

## Troubleshooting
- If the web interface is not working, ensure that your Apache server is running and PHP is enabled.
- If images are not loading, check the `htdocs` folder permissions.
- If the script fails, verify that `best.pt` is correctly placed and accessible.

## License
This project is open-source under the **MIT License**.

## Contact
For any issues or suggestions, please open an issue on GitHub.

