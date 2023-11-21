#This version of the code is broken down into smaller, more manageable functions, each with a single responsibility. 
#The comments provide a brief description of what each function does. This makes the code easier to understand and maintain.

import cv2
import numpy as np
from moviepy.editor import VideoFileClip

class LaneDetector:
    def __init__(self, input_video, output_video):
        """ Initialize LaneDetector with input and output video filenames. """
        self.input_video = input_video
        self.output_video = output_video

    def _convert_to_gray(self, frame):
        """ Convert a frame to grayscale. """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def _apply_blur(self, frame):
        """ Apply Gaussian blur to a frame. """
        return cv2.GaussianBlur(frame, (5, 5), 0)

    def _detect_edges(self, frame):
        """ Detect edges in a frame using Canny edge detection. """
        return cv2.Canny(frame, 50, 150)

    def _region_of_interest(self, frame, edges):
        """ Create a masked edges frame using a region of interest. """
        height, width = frame.shape[:2]
        roi_vertices = np.array([[(0, height), (width // 2, height // 2), (width, height)]], dtype=np.int32)
        mask = np.zeros_like(edges)
        cv2.fillPoly(mask, roi_vertices, 255)
        return cv2.bitwise_and(edges, mask)

    def _hough_transform(self, masked_edges):
        """ Detect lines in a frame using Hough transform. """
        return cv2.HoughLinesP(masked_edges, 2, np.pi / 180, 100, minLineLength=40, maxLineGap=20)

    def _separate_lines(self, lines):
        """ Separate lines into left and right lanes based on their slope. """
        left_lane_lines, right_lane_lines = [], []

        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    slope = (y2 - y1) / (x2 - x1)
                    if slope < -0.5:  # negative slope, left lane
                        left_lane_lines.append((x1, y1, x2, y2))
                    elif slope > 0.5:  # positive slope, right lane
                        right_lane_lines.append((x1, y1, x2, y2))

        return left_lane_lines, right_lane_lines

    def _average_lines(self, lines, img_height):
        """ Average the position of lines and extrapolate to create a single line. """
        if len(lines) == 0:
            return []

        x1_avg = sum(line[0] for line in lines) // len(lines)
        y1_avg = sum(line[1] for line in lines) // len(lines)
        x2_avg = sum(line[2] for line in lines) // len(lines)
        y2_avg = sum(line[3] for line in lines) // len(lines)

        slope = (y2_avg - y1_avg) / (x2_avg - x1_avg)
        intercept = y1_avg - slope * x1_avg

        y1_new = img_height
        x1_new = int((y1_new - intercept) / slope)
        y2_new = img_height // 2
        x2_new = int((y2_new - intercept) / slope)

        return [(x1_new, y1_new, x2_new, y2_new)]

    def _draw_lines(self, frame, left_lane, right_lane):
        """ Draw the left and right lane lines on a blank frame. """
        line_image = np.zeros_like(frame)

        for lane in [left_lane, right_lane]:
            if len(lane) > 0:
                x1, y1, x2, y2 = lane[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        return cv2.addWeighted(frame, 0.8, line_image, 1, 0)

    def process_frame(self, frame):
        """ Process a frame to detect lane lines and draw them. """
        gray_frame = self._convert_to_gray(frame)
        blurred_frame = self._apply_blur(gray_frame)
        edges = self._detect_edges(blurred_frame)
        masked_edges = self._region_of_interest(frame, edges)
        lines = self._hough_transform(masked_edges)
        left_lane_lines, right_lane_lines = self._separate_lines(lines)
        left_lane = self._average_lines(left_lane_lines, frame.shape[0])
        right_lane = self._average_lines(right_lane_lines, frame.shape[0])
        return self._draw_lines(frame, left_lane, right_lane)

    def process_video(self):
        """ Process the input video to detect and draw lane lines. """
        try:
            clip = VideoFileClip(self.input_video)
            processed_clip = clip.fl_image(self.process_frame)
            processed_clip.write_videofile(self.output_video, audio=False)
            print(f"Processed video is saved as {self.output_video}")
        except Exception as e:
            print(f"Failed to process the video due to: {str(e)}")

          
if __name__ == '__main__':
    input_video = '/input_video.mp4'
    output_video = '/output_video.mp4'
    lane_detector = LaneDetector(input_video, output_video)
    lane_detector.process_video()