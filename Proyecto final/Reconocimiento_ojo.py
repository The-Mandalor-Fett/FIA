from pickle import TRUE
import cv2

#VIDEOCAPTURA
captura = cv2.VideoCapture(0)
captura.set(3,1280)
captura.set(4,720)

while True :
    #REALIZA LECTURA DE VIDEOCAPTURA Y SI LA CAPTURA ES EXITOSA
    ret, frame = captura.read()

    if ret == False:
        break

    #EXTRAE ANCHO Y ALTO
    alto, ancho, c = frame.shape

    #CALCULA EL CENTRO DE LA IMAGEN
    x1 = int(ancho / 3)
    x2 = int(x1 * 2)

    y1 = int(alto / 3)
    y2 = int(y1 * 2)

    cv2.putText(frame,"Porfavor coloca tu ojo en el rectángulo",(x1 - 50, y1 - 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.rectangle(frame,(x1,x2),(y1,y2),(0,255,0),2)

    #RECORTE DE NUESTRA ZON DE INTERÉS
    recorte = frame[y1:y2, x1:x2]

    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (3,3),0)

    #SE USA UN UMBRAL PARA DETECTAR LA PUPILA GRACIAS AL NEGRO DE NUESTRA PUPILA
    _ , umbral = cv2.threshold(gris , 7, 255, cv2.THRESH_BINARY_INV)

    #EXTRAEMOS LOS CONTORNOS DE LA ZONA DE LA PUPILA
    contornos , _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #ORGANIZAMOS LOS CONTORNOS
    contornos =  sorted(contornos, key = lambda x: cv2.contourArea(x), reverse = TRUE)

    #DIBUJA CONTORNOS
    for contorno in contornos:
        (x, y, ancho, alto) = cv2.boundingRect(contorno)

        #DIBUJA
        cv2.rectangle(frame,(x + x1, y + y1),(x + ancho + x1, y + alto + y1),(0,255,0),1)

        break
    
    cv2.imshow("Ojos", frame)
    cv2.imshow("Recorte", recorte)
    cv2.imshow("Umbral", umbral)

    tecla = cv2.waitKey(1)
    if tecla == 27:
        break
    captura.release()
    cv2.destroyAllWindows()


