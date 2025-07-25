import cv2
import face_recognition
import os

# Load known faces and their names from the folder
known_face_encodings = []
known_face_names = []

# Loop through all image files in the "known_faces" folder
for filename in os.listdir('known_faces'):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Load image and get encoding
        image = face_recognition.load_image_file(f'known_faces/{filename}')
        encoding = face_recognition.face_encodings(image)[0]  # Assuming 1 face per image

        # Append encoding and name
        known_face_encodings.append(encoding)
        name = os.path.splitext(filename)[0]  # Remove .jpg/.png
        known_face_names.append(name)

# Start video capture from webcam
video_capture = cv2.VideoCapture(0)

print("Starting face recognition... Press 'q' to quit.")

while True:
    # Capture frame-by-frame from webcam
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert from BGR (OpenCV) to RGB (face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Detect all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # Compare current face with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Find best match (lowest distance)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        face_names.append(name)

    # Draw results on original frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle around face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw label
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Face Recognition', frame)

    # Break loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()