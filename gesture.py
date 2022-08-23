from cvzone.HandTrackingModule import HandDetector
import cv2
import math

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, maxHands=2)

direction = "left"
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        hand = hands[0]
        if hand["type"] == "Right":
            thumbBase = hand["lmList"][1]
            thumbTip = hand["lmList"][4]
            angle = math.atan2(thumbTip[1] - thumbBase[1], thumbTip[0] - thumbBase[0]) * 180 / math.pi

            newDirection = None
            # bottom left quadrant
            if angle > 20 and angle < 60:
                newDirection = "down"
            elif angle < -10 and angle > -40:
                newDirection = "left"
            elif angle < -40 and angle > -80:
                newDirection = "up"
            elif angle < -100 and angle > -150:
                newDirection = "right"
            
            if newDirection != None and newDirection != direction:
                direction = newDirection
                print(f"Direction changed to: {direction}")

    # Display
    cv2.imshow("Preview", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()