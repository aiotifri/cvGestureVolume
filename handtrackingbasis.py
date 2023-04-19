import cv2
import mediapipe as mp


cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
mpDraw=mp.solutions.drawing_utils # Module pour dessinéer
hands=mpHands.Hands(
static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5
)



while cap.isOpened():
    ret,frame=cap.read()
    # On récupére les images de la camera frame par frame
    #Convertir BGR en RGB
    imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # On applique le modele sur l'image
    results=hands.process(imgRGB)

    # On aura un tableau de valeur
    #print(results)
    #print(results.multi_hand_landmarks) on a une liste d'objet landmarks

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):

                # On récupere les informations sur l'image
                h,w,c=frame.shape
                # Nous alons récupéré
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)

            mpDraw.draw_landmarks(frame,handlms,mpHands.HAND_CONNECTIONS)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == 13:  # 13 is the Enter Key
        break

# Release camera and close windows
cap.release()

cv2.destroyAllWindows()