import cv2

import tkinter as tk



def select_order(original_image, boxes):
    def get_screen_resolution():
        root = tk.Tk()
        # Get the screen width and height using tkinter
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()  # Destroy the tkinter window
        return screen_width, screen_height


    screen_width, screen_height = get_screen_resolution()

    # Calculate the scaling factor to make image height 80% of screen height
    scale_factor = ((screen_height * 0.6) / original_image.shape[0])
    print(scale_factor)
    scale_rate=scale_factor
    # Resize the original image to half its size
    resized_image = cv2.resize(original_image, None, fx=scale_rate, fy=scale_rate)
    
    # Resize the box coordinates accordingly
    resized_boxes = [(int(x1 * scale_rate), int(y1 * scale_rate), int(x2 * scale_rate), int(y2 * scale_rate)) for (x1, y1, x2, y2) in boxes]

    clicked_points = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # clicked_points.append((x, y))
            for i, box in enumerate(resized_boxes):
                (x1, y1, x2, y2) = box
                if x1 <= x <= x2 and y1 <= y <= y2:
                    # print("Clicked inside box:", i+1)
                    if i+1 not in clicked_points:
                        clicked_points.append(i+1)
                        break

    cv2.namedWindow("original_image")
    cv2.setMouseCallback("original_image", click_event)

    for box in resized_boxes:
        (x1, y1, x2, y2) = box
        cv2.rectangle(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle

    cv2.imshow("original_image", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Points clicked on the image:", clicked_points)
    return clicked_points




if __name__ == "__main__":
    original_image = cv2.imread("assets/examples/ja_a_certain_scientific_accelerator_converted.png")  # Load your image
    boxes = [
    (100, 100, 200, 200),  # Example box 1: (x1, y1, x2, y2)
    (300, 150, 400, 250),  # Example box 2
    (200, 300, 350, 400),  # Example box 3
    # Add more boxes as needed
]
    select_order(original_image,boxes)