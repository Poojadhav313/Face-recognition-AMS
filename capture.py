import face_recognition
import cv2
import numpy as np
import os

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.


cp = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

# get all images and encode them
face = {}
faceEncoding = {}
x=0

imagesFolder = os.listdir(os.getcwd()+"/images")
for i in imagesFolder:
    li = i.split('.')[0]
    print(li)
    
    
    face["face{0}.format(x)"] = face_recognition.load_image_file("images/"+i)
    faceEncoding["faceEncoding{0}.format(x)"] = face_recognition.face_encodings(face["face{0}.format(x)"])[0]
    
    known_face_encodings.append(faceEncoding["faceEncoding{0}.format(x)"])
    known_face_names.append(li)

    x = x+1


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame1 = cp.read()
    frame = cv2.flip(frame1,1)  

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top-30), (right, bottom+30), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom), (right, bottom+30), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom + 20), font, 0.6, (255, 255, 255), 1)
 
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cp.release()
cv2.destroyAllWindows()