import cv2

#0 is the deafult
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Camera Test - Press ESC to Exit", frame)

    # esc to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

