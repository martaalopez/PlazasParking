import cv2
import numpy as np
import pickle


with open('carparking', 'rb') as f:
    posList = pickle.load(f)

#Verificar si las plazas están libres o ocupadas en la imagen procesada
def check(img, imgPro):
    
    spaceCount = 0
    imgHeight, imgWidth = imgPro.shape[:2]  # Obtener las dimensiones de la imagen procesada
    
    for pos in posList:
       
        if isinstance(pos, tuple) and len(pos) == 2:
            start, end = pos  # Extraer las coordenadas de inicio y fin
            if isinstance(start, tuple) and isinstance(end, tuple) and len(start) == 2 and len(end) == 2:
                x1, y1 = start 
                x2, y2 = end    

                # Asegurarse de que las coordenadas estén dentro de los límites de la imagen
                if x1 < 0 or y1 < 0 or x2 > imgWidth or y2 > imgHeight:
                    print(f"Advertencia: La posición {pos} está fuera de los límites de la imagen.")
                    continue  

                # Cortar la región del rectángulo de la plaza
                crop = imgPro[y1:y2, x1:x2]
                count = cv2.countNonZero(crop)  # Contar píxeles no negros

                if count < 900:  # Umbral para considerar un espacio libre
                    spaceCount += 1
                    color = (0, 255, 0)  # Verde para espacio libre
                    thick = 5
                else:
                    color = (0, 0, 255)  # Rojo para espacio ocupado
                    thick = 2

                # Dibujar el rectángulo en la imagen original sobre la posición detectada
                #cv2.rectangle(img, (x1, y1), (x2, y2), color, thick)
            else:
                print(f"Advertencia: Posición mal formada: {pos}")
        else:
            print(f"Advertencia: Posición mal formada: {pos}")

    # Mostrar la información de espacios libres sobre la imagen original
    cv2.rectangle(img, (45, 30), (250, 75), (180, 0, 180), -1)
    cv2.putText(img, f'Free: {spaceCount}/{len(posList)}', (50, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

# Cargar la imagen original
img = cv2.imread("parking.png")  # Cambia el nombre por el archivo de tu imagen

# Procesar la imagen
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
blur = cv2.GaussianBlur(gray, (3, 3), 1)  # Aplicar desenfoque Gaussiano
Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)  # Umbral adaptativo
blur = cv2.medianBlur(Thre, 5)  # Aplicar un desenfoque mediano
kernel = np.ones((3, 3), np.uint8)  # Definir un kernel para dilatación
dilate = cv2.dilate(blur, kernel, iterations=1)  # Dilatar la imagen para mejorar la detección

# Verificar los espacios de estacionamiento
check(img, dilate)

# Mostrar la imagen con los resultados
cv2.imshow("Image", img)
cv2.waitKey(0)  # Esperar a que se presione una tecla para cerrar la ventana
cv2.destroyAllWindows()  # Cerrar las ventanas de OpenCV
