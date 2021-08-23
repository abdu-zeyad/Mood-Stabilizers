# Import all packages and libraries
from train import *
# Code for GUI and mapping with emojis

# start the webcam feed
cap = cv2.VideoCapture(0)
while True:
    # Find haarcascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        break
    bounding_box = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml"
    )
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    num_faces = bounding_box.detectMultiScale(
        gray_frame, scaleFactor=1.3, minNeighbors=5
    )

    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
        roi_gray_frame = gray_frame[y: y + h, x: x + w]
        cropped_img = np.expand_dims(
            np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0
        )
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        cv2.putText(
            frame,
            emotion_dict[maxindex],
            (x + 20, y - 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    cv2.imshow("Video", cv2.resize(
        frame, (1200, 860), interpolation=cv2.INTER_CUBIC))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
