from tkinter import font
import cv2
from cv2 import cvtColor
import numpy as np
import imutils as nimu
import dlib as db
import math 

captura = cv2.VideoCapture(0)
recuadro = np.zeros((500, 500), np.uint8)
recuadro[:] = 255

#DETECTOR DE LA CARA DE DLIB
detectorCara = db.get_frontal_face_detector()
#PREDICTOR DE 68 PUNTOS DE REFERENCIA
predictor = db.shape_predictor("shape_predictor_68_face_landmarks.dat")

#CREAMOS EL TECLADO
teclado = np. zeros((1000, 1200, 3), np.uint8)
key_caps ={0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "Y", 
           6: "U", 7: "I", 8: "O", 9: "P", 10: "A", 11: "S", 12: "D",
           13: "F", 14: "G", 15: "H", 16: "J", 17: "K", 18: "L", 19: "Ñ",
           20: "Z", 21: "X", 22: "C", 23: "V", 24: "B", 25: "N", 26: "M",}

frames = 0
index_teclas = 0
contador_parpadeos = 0
palabras = ""
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

def letras(index_letra, letra, blanco_tecla):
    if index_letra == 0:
        x = 0
        y = 0
    elif index_letra == 1:
        x = 200
        y = 0
    elif index_letra == 2:
        x = 400
        y = 0
    elif index_letra == 3:
        x = 600
        y = 0
    elif index_letra == 4:
        x = 800
        y = 0
    elif index_letra == 5:
        x = 1000
        y = 0
    elif index_letra == 6:
        x = 0
        y = 200 
    elif index_letra == 7:
        x = 200
        y = 200
    elif index_letra == 8:
        x = 400
        y = 200
    elif index_letra == 9:
        x = 600
        y = 200
    elif index_letra == 10:
        x = 800
        y = 200 
    elif index_letra == 11:
        x = 1000
        y = 200
    elif index_letra == 12:
        x = 0
        y = 400
    elif index_letra == 13:
        x = 200
        y = 400
    elif index_letra == 14:
        x = 400
        y = 400
    elif index_letra == 15:
        x = 600
        y = 400 
    elif index_letra == 16:
        x = 800
        y = 400
    elif index_letra == 17:
        x = 1000
        y = 400
    elif index_letra == 18:
        x = 0
        y = 600
    elif index_letra == 19:
        x = 200
        y = 600 
    elif index_letra == 20:
        x = 400
        y = 600
    elif index_letra == 21:
        x = 600
        y = 600
    elif index_letra == 22:
        x = 800
        y = 600
    elif index_letra == 23:
        x = 1000
        y = 600
    elif index_letra == 24:
        x = 0
        y = 800 
    elif index_letra == 25:
        x = 200
        y = 800
    elif index_letra == 26:
        x = 400
        y = 800

    #TECLAS
    alto = 200
    ancho = 200
    grueso = 3
    
    if letra_blanco is True:
        cv2.rectangle(teclado,(x + grueso , y + grueso), (x + ancho - grueso, y + alto - grueso), (255,255,255), -1)
    else:
        cv2.rectangle(teclado,(x + grueso , y + grueso), (x + ancho - grueso, y + alto - grueso), (0,255,0), grueso)

    #FORMATO DE LAS TECLAS
    escala_letra = 10
    letra_grueso = 4
    tamanio = cv2.getTextSize(letra, cv2.FONT_HERSHEY_PLAIN, escala_letra, letra_grueso)[0]
    texto_ancho , texto_alto = tamanio[0], tamanio[1]
    texto_x = int((ancho - texto_ancho)/2) + x
    text_y = int((alto + texto_alto)/2) + y
    cv2.putText(teclado, letra, (texto_x,text_y), cv2.FONT_HERSHEY_PLAIN, escala_letra, (0,255,0), letra_grueso)




while True:
    #REALIZA LECTURA DE VIDEOCAPTURA Y QUE LA CAPTURA ES EXITOSA
    ret,frame = captura.read()
    #CREAMOS UN NUEVO RECUADRO PARA MOSTRAR DONDE MIRAMOS
    nuevo_frame = np.zeros((500,500,3),np.uint8)
    #MODIFICA EL TAMAÑO DE LA VENTANA
    frame = nimu.resize(frame,width=720)
    frameGris =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#EN ESTA SE APLICA EL DETECTOR FACIAL
    cuadrosDelimitadores = detectorCara(frameGris,1)#OBTIENE LOS CUADROS DELIMITADORES DEL ROSTRO
    
    frames += 1
    teclado[:] = (0,0,0)

    for cara in cuadrosDelimitadores:
        codr_x, cord_y = cara.left(), cara.top()
        codr_x1, cord_y1 = cara.right(), cara.bottom()
        #cv2.rectangle(frame, (codr_x, cord_y), (codr_x1, cord_y1), (0,255,0), 2)
        #print (cara)

        puntosCara = predictor(frameGris,cara)
        parpadeo_ojoIzq = obtener_Parpadeo([36,37,38,39,40,41], puntosCara)
        parpadeo_ojoDer = obtener_Parpadeo([42,43,44,45,46,47], puntosCara)
        parpadeoAmbosOjos = (parpadeo_ojoIzq + parpadeo_ojoDer)/2

        if(parpadeoAmbosOjos > 5.9):
            cv2.putText(frame,"Parpadeo",(50,150),font,4,(0,255,0),3)

            letra_activa = key_caps[index_teclas] #OBTENEMOS LA LETRA PARPADEANDO
            contador_parpadeos += 1
            frames -= 1

            if contador_parpadeos == 5:
                palabras += letra_activa
        else:
            contador_parpadeos = 0
            #print(letra_activa)
        
        #DETECIÓN DE LA MIRADA
        mirada_ojo_izq = mirada([36,37,38,39,40,41], puntosCara)
        mirada_ojo_der = mirada([42,43,44,45,46,47], puntosCara)
        miradaOjos = (mirada_ojo_izq + mirada_ojo_der)/2

        
        
        '''if miradaOjos <= 1:
            cv2.putText(frame, "Derecha", (50,100), font, 2, (0,255,0), 3)
            nuevo_frame[:] = (0,0,255)
        elif 1 < miradaOjos < 3:
            cv2.putText(frame, "Centro", (50,100), font, 2, (0,255,0), 3)
            nuevo_frame[:] = (0,255,0)
        else:
            cv2.putText(frame, "Izquierda", (50,100), font, 2, (0,255,0), 3)
            nuevo_frame[:] = (255,0,0)
        '''
        #umbralOjo = cv2.resize(umbralOjo, None, fx = 4, fy = 4)
        #ojo = cv2.resize(ojoGris, None, fx = 4, fy = 4)
        #ojo = nimu.resize(ojo, height=120, width=120)
        #cv2.imshow("Ojo",ojo)

        #cv2.imshow("Umbral ojo", umbralOjo)
        #cv2.imshow("Mascara", ojo_izquierdo)

        '''for i in range (0, 68):
            x , y = puntosCara.part(i).x, puntosCara.part(i).y
            cv2.circle(frame, (x, y),2, (0,0,255),-1)'''
    
    if frames == 15:
        index_teclas += 1
        frames = 0
        
    if index_teclas == 27:
        index_teclas = 0

    for i in range(27):
        if i == index_teclas:
            letra_blanco = True
        else:
            letra_blanco = False
        letras(i, key_caps[i], letra_blanco)

    cv2.putText(recuadro, palabras, (100,100), font, 4, (0,255,0), 4)
    cv2.imshow("Video",frame)
    #cv2.imshow("Nuevo frame", nuevo_frame)
    cv2.imshow("Teclado", teclado)
    cv2.imshow("Cuadro del texto", recuadro)
    #SI LA LECTURA DE LA CAPTURA ES CORRECTA NO CIERRA EL PROGRAMA
    if ret == False:
        break

    #CIERRA EL PROGRAMA PRESIONANDO ESC O ENTER
    tecla = cv2.waitKey(1)
    if tecla == 27 or tecla == 13:
        break


captura.release()
cv2.destroyAllWindows()

