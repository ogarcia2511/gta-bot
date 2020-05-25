import cv2
import numpy as np

def remove_noise(image, kernel_size=3):
    """
    Gets rid of noise and tiny details from the image, such as, distant objects.
    :param image: Image through which noise needs to be removed
    :param kernel_size: Size of the kernel used for the Gaussian blur algorithm
    :return: Image with reduced noise. Sharper features.
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def convert_color(image):
    """
    Conver from color to grayscale which will highlight higher brightness values
    :param image: Color image to be converted to gray scale
    :return: Grayscaled image.
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def detect_edges(image, lower_threshold=85, higher_threshold=255):
    """
    Detects for edges by looking for quick changes in color between pixels.
    :param image: Image in which edges need to be detected.
    :param lower_threshold: If pixel value is lower thant his then it is rejected as an edge.
    :param higher_threshold: If pixel value if higher than this then it is accepted as an edge
    :return: Black and white image in which edges are detected.
    """
    return cv2.Canny(image, lower_threshold, higher_threshold)


def region_of_interest(image, vertices):
    """
    Highlight only the road and ignore all the other details of the image.
    :param image: Image on which we need to mark the region of interest.
    :param vertices: Points on the image that cover the region of interest.
    :return: Image that  only highlights the area withing the mentioned vertices.
    """
    mask = np.zeros_like(image)

    # Defining a 3-channel or 1-channel color fill for the mask
    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # Return the image only where the masked pizels are non-zero.
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# This would be some advance/later stuff that we would enjoy working on. 
# Can be ignored for the scope of this project.
def black_out_car(image):
    """
    Blacks out the player's car if it is a 3D view.
    :param image: Image from which the car needs to be removed.
    :return: Image without the car. 
    """
    new_img = convert_color(image)
    vertices = np.array([[(650, 730), (750, 500), (1030, 495), (1056, 760)]])
    mask = np.zeros_like(new_img)

    cv2.fillPoly(mask, vertices, color=255)

    masked_image = cv2.bitwise_or(new_img, mask)
    cv2.fillPoly(masked_image, vertices, color=0)

    return masked_image

def average_lines(image, lines):
    """
    To determine the mean line of all the possible lines.
    :param image: Image from which the lines need to be determined.
    :param lines: Set of lines for which the mean line needs to be found.
    :return: Set of left and right lanes.
    """
    right_lines, left_lines = [], []
    for x_1, y_1, x_2, y_2 in lines[:, 0]:
        parameters = np.polyfit((x_1, x_2), (y_1, y_2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope > 0:
            right_lines.append([slope, intercept])
        else:
            left_lines.append([slope, intercept])

    def merge_lines(image, lines):
        if len(lines) > 0:
            slope, intercept = np.average(lines, axis=0)
            y_1 = image.shape[0]
            y_2 = int(y_1 / 2)
            x_1 = int((y_1 - intercept) / slope)
            x_2 = int((y_2 - intercept) / slope)
            return np.array([x_1, y_1, x_2, y_2])

    left = merge_lines(image, left_lines)
    right = merge_lines(image, right_lines)

    return left, right

def hough_lines(image, rho=1, theta=np.pi/180, threshold=100, min_line_len=100, max_len_gap=50):
    """
    Find lines in the RoI processed image using the probabilistic Hough transform algorithm.
    :param image: Source image in which lines need to be found.
    :param rho: The resolution of the parameter r in pixels.
    :param theta: The resolution of parameter theta in radians.
    :param threshold: The minimum number of intersections to detect a line.
    :param min_line_len: The minimum number of points that can form a line.
    :param max_len_gap: The maximum gap between two points to be considered in the same line.
    :return: Set of vertices indicating the start and end of a line.
    """
    lines_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]), min_line_len, max_len_gap)
    if lines is not None:
        lines = average_lines(image, lines)
        for line in lines:
            if line is not None:
                x_1, y_1, x_2, y_2 = line
                try:
                    cv2.line(lines_image, (x_1, y_1), (x_2, y_2), (0, 0, 255), 30)
                except OverflowError as ofe:
                    pass # KILL ME LATER FOR THIS. IF YOU FIND A GOOD WORK AROUND LMK. 

    return lines_image

def draw_lines(img_src_1, img_src_2, alpha=0.9, beta=1.0, gamma=0.0):
    """
    Draws the line on the image using the points obtained from Hough transform.
    :param img_src_1: Set of lines that needs to be drawn on the original image.
    :param img_src_2: Image on which the lines need to be drawn.
    :return: Image with the lines drawn.
    """
    return cv2.addWeighted(img_src_2, alpha, img_src_1, beta, gamma)

def image_processing_pipeline(image):
    """
    Pipeline to process the screen input from the game to find the lanes.
    :param image: Screenshot of the game, driving a vehicle.
    :return: Processed image with the highlighted lanes.
    """
    processed_img = convert_color(image)
    processed_img = remove_noise(image, 5)
    processed_img = detect_edges(processed_img, 93, 233)

    pt1, pt2, pt3, pt4, pt5, pt6 = (10, 600), (10, 550), (250, 500), (750, 500), (1000, 550), (1000, 600)

    vertices = np.array([[pt1, pt2, pt3, pt4, pt5, pt6]], dtype=np.int32)

    processed_img = remove_noise(processed_img, 5)
    processed_img = region_of_interest(processed_img, vertices)

    lines_image = hough_lines(processed_img)
    processed_img = draw_lines(lines_image, image)

    return processed_img
