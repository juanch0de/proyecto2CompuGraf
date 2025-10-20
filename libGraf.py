import numpy as np
import matplotlib.pyplot as plt

def ajustarBrillo(imagen, brillo):
    img = np.copy(imagen) / 255
    img += brillo
    return img 

def ajustarBrilloPorCanal(imagen, R, G, B):
    img = np.copy(imagen) / 255
    img[:,:,0] += R
    img[:,:,1] += G
    img[:,:,2] += B
    return img

def extraerCapasRGB(imagen):
    redChannel =  np.copy(imagen) / 255
    greenChannel = np.copy(imagen) / 255
    blueChannel = np.copy(imagen) / 255
    redChannel[:,:,1]= redChannel[:,:,2] = 0
    greenChannel[:,:,0] = greenChannel[:,:, 2] = 0
    blueChannel[:,:,0] = blueChannel[:,:,1] = 0

    return redChannel, greenChannel, blueChannel

def extraerCapasCMYK(imagen):
    cyanChannel = np.copy(imagen) / 255
    magentaChannel = np.copy(imagen) / 255
    yellowChannel = np.copy(imagen) / 255
    cyanChannel[:,:,0] = 0
    magentaChannel[:,:,1] = 0
    yellowChannel[:,:,2] = 0

    return cyanChannel, magentaChannel, yellowChannel

def fusionarEqualizadas(imagen1, imagen2, factor):
    img1 = np.copy(imagen1) / 255
    img2 = np.copy(imagen2) / 255
    
    imgfus = img1*factor + img2*(1-factor)
    return imgfus

def fusionarImagenes(imagen1, imagen2):
    img1 = np.copy(imagen1) / 255
    img2 = np.copy(imagen2) / 255

    imgfus = img1 + img2

    return imgfus
        
def invertirColor(imagen):
    img = np.copy(imagen) / 255
    img = 1 - img

    return img

def pasarAGrises(imagen):
    img = np.copy(imagen) / 255

    img = 0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]

    return img

def contrastarLogaritmico(imagen, factor):
    img = np.copy(imagen) / 255

    img = factor * np.log10(1 + img)

    return img

def contrastarExponencial(imagen, factor):
    img = np.copy(imagen) / 255

    img = factor * np.exp(img - 1)

    return img

def binarizar(imagen, umbral):
    img = np.copy(imagen) / 255
    img = (img[:,:,0] + img[:,:,1] + img[:,:,2])/3

    gris = img > umbral

    return gris

def recortarImagen(imagen, xi, xf, yi, yf):
    img = np.copy(imagen) / 255

    img = img[xi:xf, yi:yf]

    return img

def rotarImagen(imagen, angulo):
    img = np.copy(imagen)
    
    img = pasarAGrises(img)
    
    angle = np.radians(angulo)
    
    m, n = img.shape
    
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    
    if angle > 0 and angle <= np.pi / 2:
        c = int(round(m * sin_angle + n * cos_angle)) + 1
        d = int(round(m * cos_angle + n * sin_angle)) + 1
        
        b = np.zeros((c, d), dtype=img.dtype)
        
        for i in range(c):
            for j in range(d):
                iii = i - int(n * sin_angle)
                ii = int(round(j * sin_angle + iii * cos_angle))
                jj = int(round(j * cos_angle - iii * sin_angle))
                if 0 <= ii < m and 0 <= jj < n:
                    b[i, j] = img[ii, jj]
        
    elif angle > np.pi / 2 and angle <= np.pi:
        print(f"Angle: {np.degrees(angle)}°")
        c = int(round(abs(m * sin_angle - n * cos_angle))) + 1
        d = int(round(abs(m * cos_angle - n * sin_angle))) + 1
        print(f"Canvas size: {c}x{d}, Original: {m}x{n}")
    
        b = np.zeros((c, d), dtype=img.dtype)
        pixels_copied = 0
    
        for i in range(c):
            for j in range(d):
                jjj = j - int(round(abs(m * cos_angle))) 
                iii = i - int(round(m * sin_angle)) 

                ii = int(round(jjj * sin_angle + iii * cos_angle))
                jj = int(round(jjj * cos_angle - iii * sin_angle))
            
                if 0 <= ii < m and 0 <= jj < n:
                    b[i, j] = img[ii, jj]
                    pixels_copied += 1
    
        print(f"Pixels copied: {pixels_copied} / {c*d}")
    
    else:
        raise ValueError("Ángulo fuera del rango esperado (0 < angulo <= 180)")
    
    return b

def hacerZoom(imagen, area, factor):
    img = np.copy(imagen) / 255

    height, width = img.shape[:2]
    zoom_area = area 

    yi = height // 2 - zoom_area // 2
    yf = height // 2 + zoom_area // 2
    xi = width // 2 - zoom_area // 2
    xf = width // 2 + zoom_area // 2

    img = img[yi:yf, xi:xf]

    zoom_factor = factor
    
    img = np.kron(img, np.ones((zoom_factor,zoom_factor, 1)))

    return img
