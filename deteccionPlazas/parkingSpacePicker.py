import cv2
import numpy as np
import pickle

# Variables globales
drawing = False 
ix, iy = -1, -1 
rectangles = []  

# Función para manejar eventos del mouse
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, rectangles

    if event == cv2.EVENT_LBUTTONDOWN:  # Cuando se presiona el botón izquierdo del mouse
        drawing = True
        ix, iy = x, y  # Guardar las coordenadas iniciales

    elif event == cv2.EVENT_LBUTTONUP:  # Cuando se suelta el botón izquierdo del mouse
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)  # Dibujar el rectángulo
        rectangles.append(((ix, iy), (x, y)))  # Guardar las coordenadas del rectángulo
        print(f"Rectángulo añadido: {rectangles[-1]}")

# Cargar la imagen
img = cv2.imread("plazasLibres.png")  

# Crear una ventana y asignar la función de clic
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

while True:
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF

 # Presiona 'q' para salir
    if key == ord('q'):  
        break
  # Presiona 's' para guardar los rectángulos
    elif key == ord('s'):
        with open('carparking', 'wb') as f:
            pickle.dump(rectangles, f)
        print("Rectángulos guardados en 'carParking'")

cv2.destroyAllWindows()