from pickle import FALSE
import cv2
import mediapipe as mp
from tkinter import *
from PIL import Image, ImageTk
import threading

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
flag = 0
flag_color = 0
root= Tk()
file1 = Image.open('irom-plan.jpg')
file2 = Image.open('busterirom-plan.jpg')
im= ImageTk.PhotoImage(file1)
image2 = ImageTk.PhotoImage(file2)
#dimensiones de la imagen
width1 = file1.width
width2 = file2.width
height1 = file1.height
height2 = file2.height

def frame():
    global flag
    global flag_color
    root.title('jeff')
    root.configure(bg='#000000')
    
    def gif():
        if flag_color == 1:
            label_señal.configure(fg='#0000ff')
        else:
            label_señal.configure(fg='#ffffff')
        if flag == 1:
            label.configure(image=im)

        elif flag == 2:
            label.configure(image=image2)
        
        root.after(100, lambda : gif())

    label = Label(image='')
    label.pack()
    label_señal = Label(text='by designed The New King',bg='#000000')
    label_señal.pack()
    gif()
    root.mainloop()

def detection_hand():
    global flag
    global flag_color
    listax = []
    with mp_hands.Hands(
        static_image_mode = False,
        max_num_hands = 2,
        min_detection_confidence = 0.5) as hands:
    
        while True:
            ret, frame = cap.read()
            if ret == False:
                break

            height, width, _ = frame.shape
            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(image_rgb)

            if result.multi_hand_landmarks is not None:
                flag_color = 1
                for hand_landmarks in result.multi_hand_landmarks:
                    #dibujamos la plantilla de las manos
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    #obtenemos la posicion(par ordenado) de la punta del dedo indice
                    x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                    y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                    #Obtenemos la posicion(par ordenado) de la punta del dedo medio
                    x2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
                    y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)
                    #Obtenemos la posicion (par ordenado) del punto de torque del dedo indice y medio respectivamente
                    mx1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * width)
                    my1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * height)
                    mx2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * width)
                    my2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * height)
                    #Obtenemos posicion del dedo anular
                    an1x = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * width)
                    an1y = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * height)
                    an2x = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x * width)
                    an2y = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * height)
                    #Posicion del dedo meñique
                    me1x = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width)
                    me1y = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)
                    me2x = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x * width)
                    me2y = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * height)

                    #movemos el mause en la posicion de las coordenadas del dedo
                    #pyautogui.moveTo(x1,y1)

                    #dibujamos linea 
                    cv2.line(frame, (x1,y1), (x2,y2), (255,0,0), 5)
                    #Dibujamos circulo en el frame
                    cv2.circle(frame, (x1,y1), 5, (0,0,255), 3)
                    cv2.circle(frame, (x2,y2), 5, (0,255,0), 3)
                    cv2.circle(frame, (mx1,my1), 5, (0,0,255), 3)
                    cv2.circle(frame, (mx2,my2), 5, (0,255,0), 3)

                    ###
                    if(y1 < my1):
                        listax.append(x1)
                        xdif = listax[0] - listax[-1]
                        if xdif > 200:
                            flag = 1
                            listax = []
                        elif xdif < -200:
                            flag = 2
                            listax = []

                    
            else:
                flag_color = 0
            #frame = cv2.flip(frame, 1)
            cv2.imshow("image", frame)
            k = cv2.waitKey(1)
            if k == ord('s'):
                break
    cap.release()
    cv2.destroyAllWindows()

thread = threading.Thread(target=detection_hand)
thread.daemon = True
thread.start()
frame()