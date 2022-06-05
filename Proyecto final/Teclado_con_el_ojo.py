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

font = cv2.FONT_HERSHEY_PLAIN

def obtener_Parpadeo(puntosOjo, puntosDeCara):
    punto_izquerda = (puntosDeCara.part(puntosOjo[0]).x, puntosDeCara.part(puntosOjo[0]).y)
    punto_derecha = (puntosDeCara.part(puntosOjo[3]).x, puntosDeCara.part(puntosOjo[3]).y)

    lineaCentral_arriba = enmedio(puntosDeCara.part(puntosOjo[1]), puntosDeCara.part(puntosOjo[2]))
    lineaCentral_abajo = enmedio(puntosDeCara.part(puntosOjo[5]), puntosCara.part(puntosOjo[4]))

    lineaHorTamanio = math.hypot((punto_izquerda[0] - punto_derecha[0]),(punto_izquerda[1] - punto_derecha[1]))
    lineaVerticalTamanio = math.hypot((lineaCentral_arriba[0] - lineaCentral_abajo[0]), (lineaCentral_arriba[1] - lineaCentral_abajo[1]))

    cv2.line(frame, punto_izquerda, punto_derecha, (0,255,0),2)
    cv2.line(frame, lineaCentral_arriba, lineaCentral_abajo, (0,255,0),2)

    parpadeo = lineaHorTamanio/lineaVerticalTamanio
    #print(lineaHorTamanio/lineaVerticalTamanio)
    #print(lineaVerticalTamanio)
    return parpadeo

def mirada(puntosOjo, puntosDeCara):
    #DETECTAMOS LA MIRADA
        zona_ojo_izquierdo = np.array([(puntosDeCara.part(puntosOjo[0]).x, puntosDeCara.part(puntosOjo[0]).y),
                                        (puntosDeCara.part(puntosOjo[1]).x, puntosDeCara.part(puntosOjo[1]).y),
                                        (puntosDeCara.part(puntosOjo[2]).x, puntosDeCara.part(puntosOjo[2]).y),
                                        (puntosDeCara.part(puntosOjo[3]).x, puntosDeCara.part(puntosOjo[3]).y),
                                        (puntosDeCara.part(puntosOjo[4]).x, puntosDeCara.part(puntosOjo[4]).y),
                                        (puntosDeCara.part(puntosOjo[5]).x, puntosDeCara.part(puntosOjo[5]).y)],np.int32)
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
        alto, ancho = umbralOjo.shape

        # DIVIDIMOS NUESTRO OJO EN DOS PARTES PARA TRABAJAR LA DETECCIÓN DE LADOS
        lado_izquierdo_umbral =  umbralOjo[0: alto, 0: int(ancho/2)]
        lado_derecho_umbral = umbralOjo[0: alto, int(ancho/2): ancho]

        #CONTAMOS LA PARTE BLANCA DEL OJO
        lado_izquierdo_blanco = cv2.countNonZero(lado_izquierdo_umbral)
        lado_derecho_blanco = cv2.countNonZero(lado_derecho_umbral)

        #ojoIzq = cv2.resize(lado_izquierdo_umbral, None, fx = 4, fy = 4)
        #ojoDer = cv2.resize(lado_derecho_umbral, None, fx = 4, fy = 4)
        #cv2.imshow("Ojo parte izquierdo", ojoIzq)
        #cv2.imshow("Ojo parte derecha", ojoDer)

        #with np.errstate(divide='ignore'):
        if lado_izquierdo_blanco == 0:
            proporcion_mirada = 1
        elif lado_derecho_blanco == 0:
            proporcion_mirada = 5
        else:
            proporcion_mirada = lado_izquierdo_blanco/lado_derecho_blanco
        return proporcion_mirada

def enmedio(p1, p2):
    return(int((p1.x + p2.x)/2), int((p1.y + p2.y)/2))


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
        parpadeo_ojoIzq = obtener_Parpadeo([36,37,38,39,40,41], puntosCara)
        parpadeo_ojoDer = obtener_Parpadeo([42,43,44,45,46,47], puntosCara)
        parpadeoAmbosOjos = (parpadeo_ojoIzq + parpadeo_ojoDer)/2

        if(parpadeoAmbosOjos > 6):
            cv2.putText(frame,"Parpadeo",(50,150),font,7,(0,255,0),3)
        
        
        #DETECIÓN DE LA MIRADA
        mirada_ojo_izq = mirada([36,37,38,39,40,41], puntosCara)
        mirada_ojo_der = mirada([42,43,44,45,46,47], puntosCara)
        miradaOjos = (mirada_ojo_izq + mirada_ojo_der)/2

        #MUESTRA LA DIRECCIÓN
        nuevo_frame = np.zeros((500,500,3),np.uint8)

        if miradaOjos <= 1:
            cv2.putText(frame, "Derecha", (50,100), font, 2, (0,255,0), 3)
            nuevo_frame[:] = (0,0,255)
        elif 1 < miradaOjos < 3:
            cv2.putText(frame, "Centro", (50,100), font, 2, (0,255,0), 3)
            nuevo_frame[:] = (0,255,0)
        else:
            cv2.putText(frame, "Izquierda", (50,100), font, 2, (0,255,0), 3)
            nuevo_frame[:] = (255,0,0)

        cv2.imshow("Nuevo frame", nuevo_frame)
        
        

        
        #umbralOjo = cv2.resize(umbralOjo, None, fx = 4, fy = 4)
        #ojo = cv2.resize(ojoGris, None, fx = 4, fy = 4)
        #ojo = nimu.resize(ojo, height=120, width=120)
        #cv2.imshow("Ojo",ojo)

        #cv2.imshow("Umbral ojo", umbralOjo)
        #cv2.imshow("Mascara", ojo_izquierdo)

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

