# LaneVision: Lane Detection using Python, OpenCV, Numpy, and Matplotlib

LaneVision is a simple lane detection software built using Python, OpenCV, Numpy, and Matplotlib. The software takes in a video and returns the detected lane lines as an MP4 video. It's intended for use in self-driving cars as a basic building block.

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

Before running the project, you need to have the following installed:

- Python 3.x
- OpenCV
- Numpy
- Matplotlib
- MoviePy

You can install the required libraries using pip:

pip install -r requirements.txt


### Running the Project

1. Clone this repository:
2.Install dependencies
    pip3 install -r requirements.txt
3. Run project
    python main.py

Replace `input_video.mp4` with the path to your input video and `output_video.mp4` with the desired path for the output video.


How it works?
1. LaneVision uses computer vision techniques to identify and highlight lane lines in an input video. The main steps involved in the process are:

2. Grayscale conversion: Convert each frame of the input video to grayscale. This simplifies the image by retaining only the intensity information and discarding color data.

3. Gaussian blur: Apply a Gaussian blur to the grayscale image to reduce noise and smooth the image, making it easier to detect edges.

4. Canny edge detection: Use the Canny edge detection algorithm to identify edges in the smoothed grayscale image. This step highlights areas of rapid intensity change, which often correspond to lane lines.

5. Region of interest (ROI) selection: Define a region of interest (usually a trapezoidal shape) to focus on the area of the image where lane lines are most likely to be found. This helps reduce false detections from irrelevant edges.

6. Hough transform: Apply the Hough transform on the masked edges to detect lines in the image. The Hough transform identifies points in the image that lie on a straight line, effectively detecting the lane lines.

7. Separate left and right lane lines: Based on the slope of the lines detected by the Hough transform, separate the lines into left and right lane lines. This allows for independent processing and averaging of the lines on each side.

8. Average and extrapolate lines: For each side (left and right), average the detected lines' coordinates and calculate a single line that best represents the lane line. Then, extrapolate the line to cover the entire region of interest.

9. Draw lane lines: Overlay the averaged and extrapolated lane lines onto the original frame, creating a visual representation of the detected lanes.

10. Combine frames: Combine the processed frames back into a video, which is then saved as an MP4 file.


### Resources

https://numpy.org/doc/stable/user/quickstart.html

https://docs.opencv.org/4.x/d9/df8/tutorial_root.html

https://docs.opencv.org/