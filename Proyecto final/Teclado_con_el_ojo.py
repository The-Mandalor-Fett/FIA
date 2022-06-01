import cv2
import numpy as np
import imutils as nimu
import dlib as db

captura = cv2.VideoCapture(0)
#DETECTOR DE LA CARA DE DLIB
detectorCara = db.get_frontal_face_detector()
#PREDICTOR DE 68 PUNTOS DE REFERENCIA
predictor = db.shape_predictor("shape_predictor_68_face_landmarks.dat")
while True:
    #REALIZA LECTURA DE VIDEOCAPTURA Y QUE LA CAPTURA ES EXITOSA
    ret,frame = captura.read()

    #MODIFICA EL TAMAÑO DE LA VENTANA
    frame = nimu.resize(frame,width=720)
    frameGris =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#EN ESTA SE APLICA EL DETECTOR FACIAL
    cuadrosDelimitadores = detectorCara(frameGris,1)#OBTIENE LOS CUADROS DELIMITADORES DEL ROSTRO
    for cara in cuadrosDelimitadores:
        codr_x, cord_y = cara.left(), cara.top()
        codr_x1, cord_y1 = cara.right(), cara.bottom()
        cv2.rectangle(frame, (codr_x, cord_y), (codr_x1, cord_y1), (0,255,0), 2)
        #print (cara)
        puntosCara = predictor(frameGris,cara)
        for i in range (0, 68):
            x , y = puntosCara.part(i).x, puntosCara.part(i).y
            cv2.circle(frame, (x, y),2, (0,0,255),-1)
    cv2.imshow("Video",frame)

    #SI LA LECTURA DE LA CAPTURA ES CORRECTA NO CIERRA EL PROGRAMA
    if ret == False:
        break

    #CIERRA EL PROGRAMA PRESIONANDO ESC O ENTER
    tecla = cv2.waitKey(1)
    if tecla == 27 or tecla == 13:
        break
captura.release()
cv2.destroyAllWindows()

