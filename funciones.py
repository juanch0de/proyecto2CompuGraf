import numpy as np
import matplotlib.pyplot as plt

img1 = plt.imread(r'/home/juan/Documents/proyectoInterfaz/proyecto2CompuGraf/bicho.jpeg') / 255.0

# --- Crear figura ---
plt.figure("Ajuste de brillo")

# Imagen original
plt.subplot(1, 2, 1)
plt.axis('off')
plt.title('Imagen Original')
plt.imshow(img1)

# Imagen con ajuste de brillo
plt.subplot(1, 2, 2)
brillo = 0.5
imgBrillo = img1 + brillo
plt.axis('off')
plt.title('Imagen con Brillo')
plt.imshow(imgBrillo)

# Mostrar ambas
plt.show()

#Brllo por canal
# Imagen original
plt.subplot(1, 2, 1)
plt.axis('off')
plt.title('Imagen Original')
plt.imshow(img1)

# Imagen con ajuste en el canal rojo
plt.subplot(1, 2, 2)
brillo = 0.5
imgCanal = np.copy(img1)

Canal = 0  # Canal Rojo (0=R, 1=G, 2=B)
imgCanal[:, :, Canal] = img1[:, :, Canal] + brillo

# Evitar que se pase de 1.0
imgCanal = np.clip(imgCanal, 0, 1)

plt.axis('off')
plt.title('Ajuste del Canal Rojo')
plt.imshow(imgCanal)

plt.show()


#CONTRASTES
plt.figure("Ajuste de Contraste", figsize=(10, 8))

# Imagen original
plt.subplot(3, 1, 1)
plt.axis('off')
plt.title('Imagen Original')
plt.imshow(img1)

# Ajuste de contraste para zonas oscuras (usando log)
Contraste = 0.5
plt.subplot(3, 1, 2)
ImgContraste = Contraste * np.log10(1 + img1)
plt.axis('off')
plt.title('Contraste Zonas Oscuras')
plt.imshow(ImgContraste)

# Ajuste de contraste para zonas claras (usando exp)
plt.subplot(3, 1, 3)
ImgContraste = Contraste * np.exp(img1 - 1)
plt.axis('off')
plt.title('Contraste Zonas Claras')
plt.imshow(ImgContraste)

plt.show()

#BINARIZAR
# Convertir a escala de grises (promedio de R,G,B)
Gris = (img1[:, :, 0] + img1[:, :, 1] + img1[:, :, 2]) / 3

# Definir umbral
Umbral = 0.5

# Binarización (True=blanco, False=negro)
ImgBin = (Gris > Umbral)

# Mostrar resultado
plt.figure("Imagen Binarizada")
plt.imshow(ImgBin, cmap='gray')
plt.axis('off')
plt.show()


#TRASLADO DE IMAGEN
dx, dy = 50, 30  # mover 50 píxeles en x y 30 en y

# Crear una nueva imagen del mismo tamaño llena de ceros (fondo negro)
trasladada = np.zeros_like(img1)

# Calcular límites válidos para el copiado
h, w = img1.shape[:2]
x_origen_inicio = 0
x_origen_fin = w - dx
y_origen_inicio = 0
y_origen_fin = h - dy

# Asignar los valores trasladados
trasladada[dy:h, dx:w] = img1[y_origen_inicio:y_origen_fin,
                             x_origen_inicio:x_origen_fin]

# Visualizar resultados
plt.figure("Traslación sin np.roll", figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Imagen Original")
plt.imshow(img1)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Imagen Trasladada")
plt.imshow(trasladada)
plt.axis('off')

plt.show()


# --- Coordenadas del recorte ---
xIni, xFin = 50, 200
yIni, yFin = 50, 200

# --- Recorte (ojo: filas=y, columnas=x) ---
ImgRecorte = img1[yIni:yFin, xIni:xFin]
print("Tamaño imagen recortada : ", ImgRecorte.shape)

# --- Mostrar resultados ---
plt.figure("Escalado de una imagen")

plt.subplot(2, 1, 1)
plt.title("Imagen Original")
plt.imshow(img1)
plt.axis('off')

plt.subplot(2, 1, 2)
plt.title("Imagen Recortada")
plt.imshow(ImgRecorte)
plt.axis('off')

plt.show()

#ROTAR IMAGEN
def rotarImg(a, ang):
    """
    Rota una imagen en sentido antihorario por un ángulo dado.

    Parámetros:
    a (numpy.ndarray): Imagen de entrada representada como un arreglo 2D.
    ang (float): Ángulo de rotación en grados. Debe estar en el rango (0, 180] grados.

    Devuelve:
    numpy.ndarray: Imagen rotada con el mismo tipo de datos que la imagen de entrada.

    Excepciones:
    ValueError: Si el ángulo está fuera del rango esperado (0 < ang <= 180).
    """
    # Convertir a radianes
    ang = np.radians(ang)
    m, n = a.shape
    cos_ang = np.cos(ang)
    sin_ang = np.sin(ang)

    # Caso 1: ángulo entre 0 y 90 grados
    if ang > 0 and ang <= np.pi / 2:
        c = int(round(m * sin_ang + n * cos_ang)) + 1
        d = int(round(m * cos_ang + n * sin_ang)) + 1
        b = np.zeros((c, d), dtype=a.dtype)

        for i in range(c):
            for j in range(d):
                iii = i - int(n * sin_ang) - 1
                ii = int(round(j * sin_ang + iii * cos_ang))
                jj = int(round(j * cos_ang - iii * sin_ang))
                if 0 <= ii < m and 0 <= jj < n:
                    b[i, j] = a[ii, jj]

    # Caso 2: ángulo entre 90 y 180 grados
    elif ang > np.pi / 2 and ang <= np.pi:
        c = int(round(m * sin_ang - n * cos_ang)) + 1
        d = int(round(m * cos_ang + n * sin_ang)) + 1
        e = -n * cos_ang
        b = np.zeros((c, d), dtype=a.dtype)

        for i in range(c):
            iii = c - i - 1
            for j in range(d):
                jjj = d - j - 1
                ii = int(round(jjj * sin_ang + iii * cos_ang))
                jj = int(round(jjj * cos_ang - iii * sin_ang))
                if 0 <= ii < m and 0 <= jj < n:
                    b[i, j] = a[ii, jj]
    else:
        raise ValueError("Ángulo fuera del rango esperado (0 < ang <= 180°)")

    return b


# =============================
# Ejemplo de uso
# =============================

# Cargar imagen
img = plt.imread(r'/home/juan/Documents/proyectoInterfaz/proyecto2CompuGraf/bicho.jpeg') / 255.0

# Convertir a escala de grises si es RGB
if img.ndim == 3:
    img = np.dot(img[..., :3], [0.299, 0.587, 0.114])

# Rotar 45 grados
rotada = rotarImg(img, 45)

# Mostrar
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.title("Original")

plt.subplot(1,2,2)
plt.imshow(rotada, cmap='gray')
plt.axis('off')
plt.title("Rotada 45°")

plt.show()



#REDUCIR RESOLUCION
# --- Factor de reducción ---
zoom_factor = 5

# Tomar 1 de cada 'zoom_factor' píxeles en filas y columnas
zoomed = img1[::zoom_factor, ::zoom_factor]

print("Tamaño imagen original: ", img1.shape)
print("Tamaño con la reducción de resolución: ", zoomed.shape)

# --- Visualización ---
plt.figure("Reducción de resolución", figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Imagen Original")
plt.imshow(img1)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Imagen Reducción de resolución")
plt.imshow(zoomed)
plt.axis('off')

plt.show()

#ZOOM
# --- Coordenadas para recortar el centro (ejemplo: 100x100 píxeles) ---
h, w = img1.shape[:2]
zoom_area = 100
start_row = h // 2 - zoom_area // 2
end_row = h // 2 + zoom_area // 2
start_col = w // 2 - zoom_area // 2
end_col = w // 2 + zoom_area // 2

# Recortar región central
recorte = img1[start_row:end_row, start_col:end_col]

# --- Aumentar tamaño del recorte (ampliación) ---
zoom_factor = 5
zoomed = np.kron(recorte, np.ones((zoom_factor, zoom_factor, 1)))

# --- Mostrar resultados ---
plt.figure("Zoom hacia adentro", figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Imagen Original")
plt.imshow(img1)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Zoom sobre región central")
plt.imshow(zoomed)
plt.axis('off')

plt.show()

#Histograma

import numpy as np
import matplotlib.pyplot as plt

# --- Cargar imagen ---
img = plt.imread(r'/home/juan/Documents/proyectoInterfaz/proyecto2CompuGraf/bicho.jpeg') / 255.0

# Asegurar que los valores estén entre 0-255
if img.max() <= 1.0:  # algunas librerías cargan imágenes en [0,1]
    img = (img * 255).astype(np.uint8)

# --- Separar canales ---
R = img[..., 0]
G = img[..., 1]
B = img[..., 2]

# --- Crear figura para mostrar los histogramas por canal ---
plt.figure(figsize=(10, 6))

# Histograma canal Rojo
plt.subplot(3, 1, 1)
plt.hist(R.ravel(), bins=256, color='red', alpha=0.7)
plt.title('Histograma del canal Rojo')
plt.xlabel('Intensidad')
plt.ylabel('Frecuencia')

# Histograma canal Verde
plt.subplot(3, 1, 2)
plt.hist(G.ravel(), bins=256, color='green', alpha=0.7)
plt.title('Histograma del canal Verde')
plt.xlabel('Intensidad')
plt.ylabel('Frecuencia')

# Histograma canal Azul
plt.subplot(3, 1, 3)
plt.hist(B.ravel(), bins=256, color='blue', alpha=0.7)
plt.title('Histograma del canal Azul')
plt.xlabel('Intensidad')
plt.ylabel('Frecuencia')

plt.tight_layout()
plt.show()
