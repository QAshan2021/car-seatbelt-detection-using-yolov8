import os
import cv2
from ultralytics import YOLO
from datetime import datetime
import json
import sys

# Ensure unique filenames for output
def get_unique_filepath(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(directory, unique_filename := f"{base}_{counter}{ext}")):
        counter += 1
    return os.path.join(directory, base + ext if counter == 0 else f"{base}_{counter}{ext}")

# Generate stylish HTML report using Bootstrap
def generate_html(results, output_image_filename, output_image_relative_path):
    detection_count = len(results)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>YOLO Detection Results</title>
        <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
        <style>
            body {{ background-color: #f8f9fa; padding: 20px; }}
            table {{ box-shadow: 0 2px 5px rgba(0,0,0,0.15); }}
            th, td {{ text-align: center; }}
            .image-preview {{ max-width: 100%; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        </style>
    </head>
    <body>
        <div class=\"container\">
            <h2 class=\"text-center mb-4\">YOLO Detection Report</h2>
            <div class=\"text-center mb-4\">
                <img src=\"{output_image_relative_path}\" class=\"image-preview\" alt=\"Detected Image\">
            </div>
            <p><strong>File:</strong> {output_image_filename}</p>
            <p><strong>Timestamp:</strong> {timestamp}</p>
            <p><strong>Total Detections:</strong> {detection_count}</p>

            <table class=\"table table-striped table-bordered\">
                <thead class=\"table-dark\">
                    <tr>
                        <th>#</th>
                        <th>Class Label</th>
                        <th>Confidence (%)</th>
                        <th>Coordinates</th>
                    </tr>
                </thead>
                <tbody>
    """

    for idx, res in enumerate(results, start=1):
        html_content += f"""
            <tr>
                <td>{idx}</td>
                <td>{res['label'].capitalize()}</td>
                <td>{res['confidence']*100:.2f}%</td>
                <td>{res['coordinates']}</td>
            </tr>
        """

    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    return html_content

# YOLO detection function
def yolo_inference_and_save(input_image_path, output_directory, confidence_threshold=0.6):
    model = YOLO(r'C:\Users\Administrator\Desktop\models training\yolov8\yolov8_seatbelt34\weights\best.pt')
    results = model.predict(input_image_path, verbose=False)
    image = cv2.imread(input_image_path)

    detection_results = []

    for result in results:
        boxes = result.boxes.xyxy
        conf = result.boxes.conf
        class_ids = result.boxes.cls

        for i, box in enumerate(boxes):
            confidence = conf[i].item()
            if confidence >= confidence_threshold:
                class_id = int(class_ids[i])
                label = model.names[class_id]

                if label == 'seatbelt':
                    label = 'no seatbelt'
                elif label == 'person-noseatbelt':
                    label = 'seatbelt'

                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                detection_results.append({
                    'label': label,
                    'confidence': confidence,
                    'coordinates': (x1, y1, x2, y2)
                })

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_filepath = get_unique_filepath(output_directory, os.path.basename(input_image_path))
    cv2.imwrite(output_filepath, image)

    output_image_relative_path = os.path.basename(output_filepath)
    html_output_path = output_filepath.rsplit('.', 1)[0] + '.html'
    html_content = generate_html(detection_results, os.path.basename(output_filepath), output_image_relative_path)

    with open(html_output_path, 'w') as html_file:
        html_file.write(html_content)

    return json.dumps({
    "output_image": os.path.abspath(output_filepath),
    "html_report": os.path.abspath(html_output_path),
    "output_image_relative": output_image_relative_path,
    "detections": detection_results
    })


if __name__ == '__main__':
    input_image_path = sys.argv[1]
    output_directory = sys.argv[2]
    confidence_threshold = float(sys.argv[3])

    result_json = yolo_inference_and_save(input_image_path, output_directory, confidence_threshold)
    print(result_json)
