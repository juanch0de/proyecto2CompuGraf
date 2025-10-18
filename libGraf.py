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

def fusionar(imagen1, imagen2, factor):
    img1 = np.copy(imagen1) / 255
    img2 = np.copy(imagen2) / 255
    
    imgfus = img1*factor + img2*(1-factor)
    return imgfus
        
