import cv2
import face_recognition



cap = cv2.VideoCapture(0)   #default webcam : 0

if not cap.isOpened():
    print("Error capturing video")
    exit()

while True:
    boolval, frame1 = cap.read()

    if not boolval:
        print("No frame captured")
        break

    frame = cv2.flip(frame1, 1)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) #wait for key pressed and stores ascii. if not any key pressed returns -1
    print(key)

    if key == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()

print("Video capturing closed")

