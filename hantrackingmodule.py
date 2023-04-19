import cv2
import mediapipe as mp


class handDetector:
    # On y mets les parametre de hands
    def __init__(self,mode=False,maxHands=2,detectionConf=0.5,trackConf=0.5,complexity=1):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionConf=detectionConf
        self.trackConf=trackConf
        self.complexity=complexity

        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils  # Module pour dessinéer
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=self.complexity,
            min_detection_confidence=self.detectionConf,
            min_tracking_confidence=self.trackConf
        )


    def findHands(self,frame,draw=True):

        # On récupére les images de la camera frame par frame
        # Convertir BGR en RGB
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # On applique le modele sur l'image
        self.results = self.hands.process(imgRGB)

        # On aura un tableau de valeur
        # print(results)
        # print(results.multi_hand_landmarks) on a une liste d'objet landmarks

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handlms, self.mpHands.HAND_CONNECTIONS)
        return frame


    def findPosition(self,frame,handNo=0,draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # On récupere les informations sur l'image
                h, w, c = frame.shape
                # Nous alons récupéré
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)

        return lmList

def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()



        detector=handDetector()
        detector.findHands(frame,draw=True)
        lm=detector.findPosition(frame)



        if len(lm)!=0:
            print(lm[4])

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 13:  # 13 is the Enter Key
            break

    # Release camera and close windows
    cap.release()

    cv2.destroyAllWindows()

if __name__=="__main__":
    main()