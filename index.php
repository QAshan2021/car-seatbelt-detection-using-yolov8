

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YOLO Object Detection - Advanced Interface</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #eef2f7;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            border-radius: 20px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            padding: 30px;
        }
        .form-label {
            font-weight: 600;
            color: #495057;
        }
        .report-container {
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            border-radius: 15px;
            padding: 25px;
            background-color: #ffffff;
            margin-top: 30px;
        }
        .btn-primary {
            background: linear-gradient(45deg, #4c8bf5, #3068e0);
            border: none;
        }
        .btn-primary:hover {
            background: linear-gradient(45deg, #3068e0, #4c8bf5);
        }
        h2 {
            color: #2a4365;
            font-weight: 700;
        }
    </style>
</head>
<body>


<div class="container py-5">
    <div class="card">
        <h2 class="mb-4 text-center"><i class="fa-solid fa-camera-retro"></i> YOLO Object Detection</h2>
        <form action="" method="POST" enctype="multipart/form-data">
            <div class="mb-3">
                <label class="form-label">Upload Image:</label>
                <input type="file" name="image" required class="form-control">
            </div>
            <div class="mb-4">
                <label class="form-label">Confidence Threshold: <span id="confValue">0.6</span></label>
                <input type="range" class="form-range" name="confidence" min="0.1" max="1" value="0.6" step="0.05" onchange="document.getElementById('confValue').innerText=this.value;">
            </div>
            <button class="btn btn-primary w-100" type="submit" name="submit"><i class="fa-solid fa-play"></i> Run Detection</button>
        </form>
    </div>

    <?php
    if (isset($_POST['confidence']) && isset($_FILES['image'])) {
        $upload_dir = 'uploads/';
        if (!file_exists($upload_dir)) mkdir($upload_dir, 0777, true);

        $uploaded_file = $upload_dir . basename($_FILES['image']['name']);
        move_uploaded_file($_FILES['image']['tmp_name'], $uploaded_file);

        $confidence = escapeshellarg($_POST['confidence']);
        $cmd = escapeshellcmd("python yolo_detection.py " . escapeshellarg($uploaded_file) . " test_output " . $confidence);
        $output = shell_exec($cmd);

        $result = json_decode($output, true);

        if ($result) {
            $html_report = file_get_contents($result['html_report']);
            $image_url = 'test_output/' . $result['output_image_relative'];
            $html_report = str_replace($result['output_image_relative'], $image_url, $html_report);

            echo "<div class='report-container'>";
            echo $html_report;
            echo "</div>";

            echo "<div class='text-center mt-4'>";
            echo "<a href='index.php' class='btn btn-secondary'><i class='fa-solid fa-arrow-left'></i> Try New</a>";
            echo "</div>";
        } else {
            echo "<div class='alert alert-danger mt-4'>Failed to detect objects.</div>";
        }
    }
    ?>
</div>

<script>
    const range = document.querySelector('input[type="range"]');
    rangeValue = document.querySelector('#confValue');
    range.oninput = () => rangeValue.textContent = range.value;
</script>
</body>
</html>