import cv2 
import numpy as np

teclado = np. zeros((1000, 1500, 3), np.uint8)

cv2.imshow("Teclado",teclado)
cv2.waitKey(0)
cv2.destroyAllWindows()