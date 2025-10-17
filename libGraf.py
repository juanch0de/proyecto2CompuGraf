import numpy as np
import matplotlib.pyplot as plt

def ajustarBrillo(imagen, brillo):
    img = np.copy(imagen) / 255
    img += brillo
    return img 

def fusion(imagen1, imagen2, factor):
    img1 = np.copy(imagen1) / 255
    img2 = np.copy(imagen2) / 255
    
    imgfus = img1*factor + img2*(1-factor)
    return imgfus
        
