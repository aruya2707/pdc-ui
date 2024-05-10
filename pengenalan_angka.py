import cv2
import numpy as np
import json

from app import numbers_to_recognize

def resize_image(image_path, target_size=(100, 100)):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
    return resized_image

def extract_contour_freeman_chain_code(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]
    chain_code = []
    for i in range(len(contour) - 1):
        x_start, y_start = contour[i][0]
        x_end, y_end = contour[i + 1][0]
        direction = (x_end - x_start, y_end - y_start)
        chain_code.append(direction)
    return chain_code

def thinning_freeman_chain_code(image):
    # Thinning process
    thinned_image = cv2.ximgproc.thinning(image)
    chain_code = extract_contour_freeman_chain_code(thinned_image)
    return chain_code

def convert_chain_code_to_json_serializable(chain_code):
    serializable_chain_code = [(int(x), int(y)) for x, y in chain_code]
    return serializable_chain_code

def save_knowledge_based(knowledge_based, file_path):
    with open(file_path, 'w') as file:
        json.dump(knowledge_based, file)

def recognize_digit(input_digit, method='contour'):
    # Load knowledge-based (contour or thinning)
    if method == 'contour':
        knowledge_based_path = "knowledge_based_contour.json"
    elif method == 'thinning':
        knowledge_based_path = "knowledge_based_thinning.json"
    else:
        print("Invalid method!")
        return None

    with open(knowledge_based_path, 'r') as file:
        knowledge_based = json.load(file)

    # Perform digit recognition
    if len(input_digit) == 1:  # Jika input adalah angka tunggal
        if input_digit in knowledge_based:
            recognized_digit = knowledge_based[input_digit]
            print(f"Digit {input_digit} recognized as: {recognized_digit} (Method: {method})")
        else:
            print(f"Unable to recognize digit {input_digit} (Method: {method})")
    elif len(input_digit) == 2:  # Jika input adalah angka ganda
        if input_digit in knowledge_based:
            recognized_digit = knowledge_based[input_digit]
            print(f"Number {input_digit} recognized as: {recognized_digit} (Method: {method})")
        else:
            # Pisahkan input menjadi digit tunggal dan lakukan pengenalan digit untuk setiap digit tunggal
            for digit in input_digit:
                if digit in knowledge_based:
                    recognized_digit = knowledge_based[digit]
                    print(f"Digit {digit} recognized as: {recognized_digit} (Method: {method})")
                else:
                    print(f"Unable to recognize digit {digit} (Method: {method})")
    else:
        print("Invalid input format!")



def kenali_angka(numbers_to_recognize):
    # Load images and resize them
    digits = {}
    for i in range(10):
        image_path = f"static/img/digits/digit_{i}.png"
        resized_image = resize_image(image_path)
        digits[str(i)] = resized_image

    # Extract contour and thinning for each digit
    knowledge_based_contour = {}
    knowledge_based_thinning = {}
    for digit, image in digits.items():
        contour_chain_code = extract_contour_freeman_chain_code(image)
        thinning_chain_code = thinning_freeman_chain_code(image)
        serializable_contour_chain_code = convert_chain_code_to_json_serializable(contour_chain_code)
        serializable_thinning_chain_code = convert_chain_code_to_json_serializable(thinning_chain_code)
        knowledge_based_contour[digit] = serializable_contour_chain_code
        knowledge_based_thinning[digit] = serializable_thinning_chain_code

    # Save knowledge-based to files
    save_knowledge_based(knowledge_based_contour, "knowledge_based_contour.json")
    save_knowledge_based(knowledge_based_thinning, "knowledge_based_thinning.json")

    recognized_images = []
    for number in numbers_to_recognize:
        if len(number) > 1:
            for digit in number:
                recognized_image_path = recognize_digit(digit)
                if recognized_image_path:
                    recognized_images.append(recognized_image_path)
                recognized_image_path_thinning = recognize_digit(digit, method='thinning')  # Call thinning method here
                if recognized_image_path_thinning:
                    recognized_images.append(recognized_image_path_thinning)
        else:
            recognized_image_path = recognize_digit(number)
            if recognized_image_path:
                recognized_images.append(recognized_image_path)
            recognized_image_path_thinning = recognize_digit(number, method='thinning')  # Call thinning method here
            if recognized_image_path_thinning:
                recognized_images.append(recognized_image_path_thinning)
    return recognized_images


# Example usage:
# numbers_to_recognize = ["1", "089", "6901", "2023", "34", "38"]
# kenali_angka(numbers_to_recognize)