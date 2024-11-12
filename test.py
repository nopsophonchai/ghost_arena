import cv2

video_path = './video/loopbg.avi'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Cannot open the video file: {video_path}")
else:
    print("Video file opened successfully.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow('Frame', frame)
        if cv2.waitKey(42) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
