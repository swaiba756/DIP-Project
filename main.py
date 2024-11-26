import cv2

# Define color profiles
def colorProfiles(n):
    if n == 0:
        name = "Pepsi"
        hsv_lower = (95, 100, 100)
        hsv_upper = (115, 255, 255)
        return name, hsv_lower, hsv_upper
    elif n == 1:
        name = "Coke"
        hsv_lower = (0, 100, 100)
        hsv_upper = (10, 255, 255)
        return name, hsv_lower, hsv_upper

# Read the image
frame = cv2.imread("assets/bottle.png")
if frame is None:
    print("Error: Image not found. Please check the path.")
    exit()

# Convert the image to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Dictionary to store detected rectangles
rects = {}

# Iterate through color profiles
for i in range(2):
    # Get color profile
    name, hsv_lower, hsv_upper = colorProfiles(i)

    # Create a mask for the current color
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

    # Find contours
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours:
        # Get the largest contour
        biggest = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        # Get bounding rectangle
        rect = cv2.boundingRect(biggest)
        x, y, w, h = rect

        # Draw the rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        print(f"Detected {name} at: x={x}, y={y}, w={w}, h={h}")
    else:
        print(f"No contours found for {name}!")

# Display the final image
cv2.imshow("Detected Objects", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
