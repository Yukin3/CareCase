import cv2

def stream_cam():
    cap = cv2.VideoCapture(0)  # Or use 1 for USB cam if needed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("CareCase View", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

stream_cam()
