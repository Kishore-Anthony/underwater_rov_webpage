# URIS - Underwater Robot for Inspection and Salvage

This project implements an object detection application using YOLOv4 and provides a web interface using Flask.

## Setup

1. Install the required Python packages:

2. YOLOv4 Weights

This below drive link provides the pre-trained YOLOv4 weights file for human detection under water using the YOLOv4 algorithm. The weights file (`yolov4.weights`) can be used with the Darknet framework.
 
Download Weights

Please add the Google Drive link containing the `yolov4.weights` file in the following section:

- [YOLOv4 Weights (yolov4.weights)][(https://drive.google.com/file/d/1mn7dIS3yDpKxrh0QQcYV2L4O4eD2e38z/view?usp=drive_link)]
   

3. Run the application:

4. Access the web interface at http://localhost:5000/.

## Files

- `main.py`: Python script for object detection
- `index.html`: HTML template for the web interface
- `style.css`: CSS styles (Bootstrap and custom styles)
- Other files (YOLOv4 weights, configuration, and class names)

## Notes

- Adjust the `desired_width` and `desired_height` in `main.py` as needed.
- Replace the video feed placeholder in `index.html` with the actual video feed element.
- Implement the timer functionality if desired.

Feel free to customize and enhance this project according to your requirements!
