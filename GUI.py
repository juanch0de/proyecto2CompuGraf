import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import libGraf 

# Interfaz

# La imagen al abrir se maneja con las clase Image de la librería Pillow

def abrir_imagen():
    global imagen_original, imagen_resultado
    ruta = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", ".png .jpg .jpeg .bmp .gif .tiff")]
    )
    if not ruta:
        return
    imagen_original = Image.open(ruta).convert("RGB").resize((500, 350)) #Carga la imagen y la ajusta 500x300 pixeles 
    imagen_resultado = imagen_original.copy() #Guarda una copia en imagen_original e imagen_resultado
    mostrar_imagen(imagen_original)

def abrir_imagen_secundaria():
    """Permite cargar una segunda imagen para fusión sin abrir cada vez."""
    global imagen_secundaria
    ruta = filedialog.askopenfilename(
        title="Selecciona segunda imagen para fusión",
        filetypes=[("Imágenes", ".png .jpg .jpeg .bmp .gif .tiff")]
    )
    if not ruta:
        return
    imagen_secundaria = Image.open(ruta).convert("RGB").resize((500, 350))
    messagebox.showinfo("Imagen cargada", "Segunda imagen lista para fusión.")

def mostrar_imagen(img):
    global imagen_resultado
    imagen_resultado = img
    foto = ImageTk.PhotoImage(img)  #Convierte la imagen en formato que Tkinter puede mostrar
    lbl_imagen.config(image=foto)
    lbl_imagen.image = foto  

# Funcionalidad de los botones 

def aplicar_brillo_global():  #Aumenta o disminuye el brillo general de la imagen
    global imagen_original
    if imagen_original is None: return
    val = simpledialog.askfloat("Brillo global (-1 a 1)", "Ingrese el brillo:", minvalue = -1, maxvalue= 1) 
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = libGraf.ajustarBrillo(img_np, val)
    img_np = np.clip(img_np * 255, 0, 255)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) # Convierte la imagen a un arreglo numpy, suma un valor (multiplicado por 255)

def aplicar_brillo_canal(): # Modifica el brillo de cada canal de color (Rojo, Verde y Azul)
    global imagen_original
    if imagen_original is None: return
    r = simpledialog.askfloat("Brillo R", "Valor R (-1 a 1):", minvalue=-1, maxvalue=1)
    g = simpledialog.askfloat("Brillo G", "Valor G (-1 a 1):", minvalue=-1, maxvalue=1)
    b = simpledialog.askfloat("Brillo B", "Valor B (-1 a 1):", minvalue=-1, maxvalue=1)
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = libGraf.ajustarBrilloPorCanal(img_np, r, g, b)
    img_np = np.clip(img_np * 255, 0, 255)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) # Pide tres valores (uno por canal) mediante cuadros de dialogo, luego aplica la función brillo_por_canal para modificar cada matriz RGB

def aplicar_contraste_log(): #Resalta las zonas oscuras de la imagen
    if imagen_original is None: return
    
    # 0 oscurece la imagen completamente.
    # Para valores mayores a 600, ya no es perceptible el cambio en la imagen
    factorContraste = simpledialog.askfloat("Factor", "Factor de contraste logarítimico:")

    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = libGraf.contrastarLogaritmico(img_np, factorContraste)
    img_np = np.clip(img_np * 255, 0, 255)

    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) 

def aplicar_contraste_exp(): #Aplica un contraste exponencial (gamma correction)
    if imagen_original is None: return
    
    # Valor de 0 oscurece la imagen completamente.
    # Valores mayores a 3 ya no hacen perceptible el cambio en la imagen
    factorContraste  = simpledialog.askfloat("Factor", "Factor de contraste exponencial:")

    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = libGraf.contrastarExponencial(img_np, factorContraste)
    img_np = np.clip(img_np * 255, 0, 255)

    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) 

def aplicar_recorte():  #Permite recortar una parte especifica de la imagen 
    if imagen_original is None: return

    imgRecorte = np.array(imagen_original, dtype = np.float32)
    
    x1 = simpledialog.askinteger("Recorte", "x1:")
    x2 = simpledialog.askinteger("Recorte", "x2:")
    y1 = simpledialog.askinteger("Recorte", "y1:")
    y2 = simpledialog.askinteger("Recorte", "y2:")

    imgRecorte = libGraf.recortarImagen(imgRecorte, x1, x2, y1, y2)
    imgRecorte = np.clip(imgRecorte * 255, 0, 255)
    
    mostrar_imagen(Image.fromarray(imgRecorte.astype(np.uint8)))

def aplicar_zoom(): #Amplia o reduce el tamaño de la imagen
    if imagen_original is None: return

    imgZoom = np.array(imagen_original, dtype = np.float32)

    factor = simpledialog.askinteger("Zoom", "Factor (1.5 = 150%):", minvalue=0.1)
    area = simpledialog.askinteger("Área", "Área:", minvalue = 0)
    imgZoom = libGraf.hacerZoom(imgZoom, factor, area)
   
    imgZoom = np.clip(imgZoom * 255, 0 , 255) 

    mostrar_imagen(Image.fromarray(imgZoom.astype(np.uint8)))

def aplicar_rotacion():  
    if imagen_original is None: return

    imagenRotada = np.array(imagen_original, dtype = np.float32)

    angulo = simpledialog.askfloat("Rotación", "Ángulo en grados:", minvalue = 0, maxvalue = 180)

    imagenRotada = libGraf.rotarImagen(imagenRotada, angulo)
    imagenRotada = np.clip(imagenRotada * 255, 0, 255)

    mostrar_imagen(Image.fromarray(imagenRotada.astype(np.uint8))) 

def mostrar_histograma(): #Muestra el histograma de la imagen
    if imagen_original is None: return
    histograma(imagen_original) #Llama a la función histograma(), que calcula de intensidades de pixeles de 0 a 255

def aplicar_fusion(): #Fusiona dos imagenes diferentes
    global imagen_original, imagen_secundaria

    if imagen_original is None or imagen_secundaria is None:
        messagebox.showwarning("Fusión", "Debes cargar dos imágenes (principal y secundaria).")
        return

    img1_np = np.array(imagen_original, dtype = np.float32)
    img2_np = np.array(imagen_secundaria, dtype = np.float32)
    img_fusion = libGraf.fusionarImagenes(img1_np, img2_np)
    img_fusion = np.clip(img_fusion * 255, 0, 255)
    mostrar_imagen(Image.fromarray(img_fusion.astype(np.uint8)))

def aplicar_fusion_ecualizada(): #Lo mismo que la función anterior, pero ecualiza ambas imagenes antes de mezclarlas 
    global imagen_original, imagen_secundaria
    if imagen_original is None or imagen_secundaria is None:
        messagebox.showwarning("Fusión", "Debes cargar dos imágenes (principal y secundaria).")
        return
    alpha = simpledialog.askfloat("Fusión", "Alpha (0-1):", minvalue=0, maxvalue=1)
    img1_np = np.array(imagen_original, dtype = np.float32)
    img2_np = np.array(imagen_secundaria, dtype = np.float32)
    img_fusion = libGraf.fusionarEqualizadas(img1_np, img2_np, alpha)
    img_fusion = np.clip(img_fusion * 255, 0, 255)
    mostrar_imagen(Image.fromarray(img_fusion.astype(np.uint8)))



def aplicar_negativo():  #Invierte los colores de la imagen
    if imagen_original is None: return

    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = libGraf.invertirColor(img_np)
    img_np = np.clip(img_np * 255, 0, 255)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) # Cada pixel p se convierte en 255 - p

def aplicar_grises(): # Convierte la imagen a escala de grises 
    if imagen_original is None: return

    img_gris = np.array(imagen_original, dtype = np.float32)

    img_gris = libGraf.pasarAGrises(img_gris)

    img_gris = np.clip(img_gris * 255, 0, 255)
    
    mostrar_imagen(Image.fromarray(img_gris.astype(np.uint8)))

def aplicar_binarizacion(): 
    if imagen_original is None: return

    img_binaria = np.array(imagen_original, dtype = np.float32)

    # Valores < 0 es totalmente blanco
    # Valor de 1 es totalmente negro
    umbral = simpledialog.askfloat("Umbral", "Umbral:")

    img_binaria = libGraf.binarizar(img_binaria, umbral)
    img_binaria = np.clip(img_binaria * 255, 0, 255)
    
    mostrar_imagen(Image.fromarray(img_binaria.astype(np.uint8)))

def aplicar_rgb(): #Separa los tres canales de color (rgb)
    if imagen_original is None: return
    redChannel = np.array(imagen_original, dtype = np.float32)
    greenChannel = np.array(imagen_original, dtype = np.float32)
    blueChannel = np.array(imagen_original, dtype = np.float32)

    redChannel, greenChannel, blueChannel = libGraf.extraerCapasRGB(imagen_original)

    redChannel = np.clip(redChannel * 255, 0, 255)
    greenChannel = np.clip(greenChannel * 255, 0, 255)
    blueChannel = np.clip(blueChannel * 255, 0, 255)
    redChannel = Image.fromarray(redChannel.astype(np.uint8))
    greenChannel = Image.fromarray(greenChannel.astype(np.uint8))
    blueChannel = Image.fromarray(blueChannel.astype(np.uint8))

    redChannel.show(title="Canal Rojo")
    greenChannel.show(title="Canal Verde")
    blueChannel.show(title="Canal Azul")

def aplicar_cmyk(): #Convierte la imagen de RGB a CMYK (modelo usado en impresión)
    if imagen_original is None: return
    cyanChannel = np.array(imagen_original, dtype = np.float32)
    magentaChannel = np.array(imagen_original, dtype = np.float32)
    yellowChannel = np.array(imagen_original, dtype = np.float32)
    
    cyanChannel, magentaChannel, yellowChannel = libGraf.extraerCapasCMYK(imagen_original)

    cyanChannel = np.clip(cyanChannel * 255, 0, 255)
    magentaChannel = np.clip(magentaChannel * 255, 0, 255)
    yellowChannel = np.clip(yellowChannel * 255, 0, 255)

    cyanChannel = Image.fromarray(cyanChannel.astype(np.uint8))
    magentaChannel = Image.fromarray(magentaChannel.astype(np.uint8))
    yellowChannel = Image.fromarray(yellowChannel.astype(np.uint8))

    cyanChannel.show(title = "Canal Cyan")
    magentaChannel.show(title = "Canal Magenta")
    yellowChannel.show(title = "Canal Amarillo")


def guardar_imagen():
    """Guarda la imagen procesada actual en el formato elegido."""
    global imagen_resultado
    if imagen_resultado is None:
        messagebox.showwarning("Guardar", "No hay imagen procesada para guardar.")
        return
    ruta = filedialog.asksaveasfilename(
        title="Guardar imagen",
        defaultextension=".png",
        filetypes=[("PNG", ".png"), ("JPEG", ".jpg"), ("BMP", "*.bmp")]
    )
    if ruta:
        imagen_resultado.save(ruta)
        messagebox.showinfo("Guardar", f"Imagen guardada en:\n{ruta}")

# Diseño de la interfaz 

root = tk.Tk()
root.title(" Editor de Imágenes Avanzado")
root.geometry("980x700")
root.configure(bg="#f0f0f0")

# FRAME SUPERIOR (abrir imagen + brillo global)
frame_superior = tk.Frame(root, bg="#dfe6e9", pady=10)
frame_superior.pack(fill="x")

btn_abrir = tk.Button(frame_superior, text="📂 Abrir Imagen", bg="#0984e3", fg="white", font=("Segoe UI", 10, "bold"), command=abrir_imagen)
btn_abrir.pack(side="left", padx=10)

btn_abrir2 = tk.Button(frame_superior, text="➕ Cargar 2da Imagen", bg="#6c5ce7", fg="white", font=("Segoe UI", 10, "bold"), command=abrir_imagen_secundaria)
btn_abrir2.pack(side="left", padx=10)

btn_guardar = tk.Button(frame_superior, text="💾 Guardar Resultado", bg="#00b894", fg="white", font=("Segoe UI", 10, "bold"), command=guardar_imagen)
btn_guardar.pack(side="left", padx=10)

tk.Label(frame_superior, text="Brillo Global:", bg="#dfe6e9", font=("Segoe UI", 10)).pack(side="left", padx=5)
entry_brillo = tk.Entry(frame_superior, width=6)
entry_brillo.insert(0, "0.5")
entry_brillo.pack(side="left")
tk.Button(frame_superior, text="Aplicar", bg="#00cec9", fg="white", command=aplicar_brillo_global).pack(side="left", padx=5)

#Frame de los botones 
frame_botones = tk.LabelFrame(root, text="Operaciones de Imagen", bg="#f0f0f0", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
frame_botones.pack(fill="x", padx=15, pady=10)

botones = [
    ("Brillo global", aplicar_brillo_global),
    ("Brillo por canal", aplicar_brillo_canal),
    ("Contraste log", aplicar_contraste_log),
    ("Contraste exp", aplicar_contraste_exp),
    ("Recorte", aplicar_recorte),
    ("Zoom", aplicar_zoom),
    ("Rotación", aplicar_rotacion),
    ("Histograma", mostrar_histograma),
    ("Fusión", aplicar_fusion),
    ("Fusión Ecualizada", aplicar_fusion_ecualizada),
    ("Negativo", aplicar_negativo),
    ("Escala Grises", aplicar_grises),
    ("Binarización", aplicar_binarizacion),
    ("Capas RGB", aplicar_rgb),
    ("Capas CMYK", aplicar_cmyk)
]

for i, (texto, comando) in enumerate(botones):
    tk.Button(
        frame_botones,
        text=texto,
        command=comando,
        width=18,
        bg="#74b9ff",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        relief="raised",
        bd=2
    ).grid(row=i//4, column=i%4, padx=10, pady=6)

#Frame de imagen
frame_imagen = tk.Frame(root, bg="#f0f0f0")
frame_imagen.pack(fill="both", expand=True)

lbl_imagen = tk.Label(frame_imagen, bg="white", relief="sunken", width=600, height=400)
lbl_imagen.pack(pady=20)

root.mainloop()
