from tkinter import font
import cv2
from cv2 import cvtColor
import numpy as np
import imutils as nimu
import dlib as db
import math

captura = cv2.VideoCapture(0)
#DETECTOR DE LA CARA DE DLIB
detectorCara = db.get_frontal_face_detector()
#PREDICTOR DE 68 PUNTOS DE REFERENCIA
predictor = db.shape_predictor("shape_predictor_68_face_landmarks.dat")

def enmedio(p1, p2):
    return(int((p1.x + p2.x)/2), int((p1.y + p2.y)/2))
font = cv2.FONT_HERSHEY_PLAIN
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
        #cv2.rectangle(frame, (codr_x, cord_y), (codr_x1, cord_y1), (0,255,0), 2)
        #print (cara)
        puntosCara = predictor(frameGris,cara)
        punto_izquerdaI = (puntosCara.part(36).x, puntosCara.part(36).y)
        punto_derechaI = (puntosCara.part(39).x, puntosCara.part(39).y)

        punto_izquerdaD = (puntosCara.part(42).x, puntosCara.part(42).y)
        punto_derechaD = (puntosCara.part(45).x, puntosCara.part(45).y)

        lineaCentral_arribaIzquierda = enmedio(puntosCara.part(37), puntosCara.part(38))
        lineaCentral_abajoIzquierda = enmedio(puntosCara.part(41), puntosCara.part(40))

        lineaCentral_arribaDerecha = enmedio(puntosCara.part(43), puntosCara.part(44))
        lineaCentral_abajoDerecha = enmedio(puntosCara.part(46), puntosCara.part(47))
        

        '''lineaIzquierda = cv2.line(frame, punto_izquerdaI, punto_derechaI, (0,255,0),2)
        lineaDerecha = cv2.line(frame, punto_izquerdaD, punto_derechaD, (0,255,0),2)
        lineaVerticalIZQ = cv2.line(frame, lineaCentral_arribaIzquierda, lineaCentral_abajoIzquierda, (0,255,0),2)
        lineaVerticalDER = cv2.line(frame, lineaCentral_arribaDerecha, lineaCentral_abajoDerecha, (0,255,0),2)'''
        
        lineaHorIzqTamanio = math.hypot((punto_izquerdaI[0] - punto_derechaI[0]),(punto_izquerdaI[1] - punto_derechaI[1]))
        lineaVerticalIzqTamanio = math.hypot((lineaCentral_arribaIzquierda[0] - lineaCentral_abajoIzquierda[0]), (lineaCentral_arribaIzquierda[1] - lineaCentral_abajoIzquierda[1]))

        parpadeo = lineaHorIzqTamanio/lineaVerticalIzqTamanio

        if(parpadeo > 6):
            cv2.putText(frame,"Parpadeo",(50,150),font,7,(0,255,0),3)
        #print(lineaHorIzqTamanio/lineaVerticalIzqTamanio)
        #print(lineaVerticalIzqTamanio)
        
        #DETECTAMOS LA MIRADA
        zona_ojo_izquierdo = np.array([(puntosCara.part(36).x, puntosCara.part(36).y),
                                        (puntosCara.part(37).x, puntosCara.part(37).y),
                                        (puntosCara.part(38).x, puntosCara.part(38).y),
                                        (puntosCara.part(39).x, puntosCara.part(39).y),
                                        (puntosCara.part(40).x, puntosCara.part(40).y),
                                        (puntosCara.part(41).x, puntosCara.part(41).y)])
        #print(zona_ojo_izquierdo)
        #cv2.polylines(frame,[zona_ojo_izquierdo],True,(255,0,0),2)
        
        
        alto, ancho, _ = frame.shape
        mascara = np.zeros((alto, ancho), np.uint8)
        cv2.polylines(mascara,[zona_ojo_izquierdo],True,255,2)    
        cv2.fillPoly(mascara,[zona_ojo_izquierdo],255)
        ojo_izquierdo = cv2.bitwise_or(frameGris, frameGris, mask = mascara)
        #CALCULAMOS LOS VALORES MINIMOS DE LA MIRADA EN x
        minimo_x = np.min(zona_ojo_izquierdo[:,0])
        maximo_x = np.max(zona_ojo_izquierdo[:,0])
        minimo_y = np.min(zona_ojo_izquierdo[:,1])
        maximo_y = np.max(zona_ojo_izquierdo[:,1])

        #OBTENEMOS EL OJO IZQUIERDO
        ojoGris = ojo_izquierdo[minimo_y: maximo_y, minimo_x: maximo_x]
        _, umbralOjo = cv2.threshold(ojoGris,70,255,cv2.THRESH_BINARY)
        umbralOjo = cv2.resize(umbralOjo, None, fx = 4, fy = 4)
        ojo = cv2.resize(ojoGris, None, fx = 4, fy = 4)
        #ojo = nimu.resize(ojo, height=120, width=120)
        cv2.imshow("Ojo",ojo)
        cv2.imshow("Umbral ojo", umbralOjo)
        cv2.imshow("Mascara", ojo_izquierdo)

        '''for i in range (0, 68):
            x , y = puntosCara.part(i).x, puntosCara.part(i).y
            cv2.circle(frame, (x, y),2, (0,0,255),-1)'''
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

