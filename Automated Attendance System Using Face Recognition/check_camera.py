def camer():
    try:
        import cv2

        # Load the cascade
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # To capture video from webcam.
        
        cap = cv2.VideoCapture(0)

        while True:
            # Read the frame
            _, img = cap.read()
            # img = cv2.resize(img,(600,400))
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect the faces
            faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(30, 30))

            # Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,0), 2)
            # Display
            cv2.imshow('Webcam Check', img)

            # Stop if escape key is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    except:
        print("Something went wrong...")

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
