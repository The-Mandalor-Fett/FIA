import cv2 
import numpy as np

teclado = np. zeros((1000, 1200, 3), np.uint8)
key_caps ={0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "Y", 
           6: "U", 7: "I", 8: "O", 9: "P", 10: "A", 11: "S", 12: "D",
           13: "F", 14: "G", 15: "H", 16: "J", 17: "K", 18: "L", 19: "Ñ",
           20: "Z", 21: "X", 22: "C", 23: "V", 24: "B", 25: "N", 26: "M",}

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
    

for i in range(27):
    if i == 5:
        letra_blanco = True
    else:
        letra_blanco = False
    letras(i, key_caps[i], letra_blanco)



cv2.imshow("Teclado",teclado)
cv2.waitKey(0)
cv2.destroyAllWindows()