import cv2
import json
import time
from twilio.rest import Client

# Load config from file
def load_config():
    with open("config.json") as f:
        return json.load(f)

# Function to call the number
def make_call():
    config = load_config()
    client = Client(config["twilio_sid"], config["twilio_auth_token"])
    call = client.calls.create(
        to=config["to_number"],
        from_=config["from_number"],
        twiml='<Response><Say>Warning! Human detected!</Say></Response>'
    )
    print("Calling:", config["to_number"])

# Start camera and detect faces
def start_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    detected = False

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0 and not detected:
            print("Human detected!")
            make_call()
            detected = True
            time.sleep(10)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
