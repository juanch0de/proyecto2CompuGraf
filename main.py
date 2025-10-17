import tkinter as tk #Libreria para la interfaz grafica 
from tkinter import filedialog, simpledialog, messagebox 
from PIL import Image, ImageTk, ImageOps #Libreria para manejar las imagenes
import numpy as np #Libreria para operar con los pixeles de las imagenes 
import matplotlib.pyplot as plt

#Variables Globales 
imagen_original = None  # Guarda la imagen subida por el usuario 
imagen_resultado = None  # Guarda la imagen que resulta despues de aplicar una transformación
imagen_secundaria = None  # Permite el manejo de una segunda imagen usada en la fusión 

#Funciones 

#Brillo global 
def brillo(img, valor):
    img_cop = np.copy(img)
    img_cop = img_cop + valor * 255
    img_cop = np.clip(img_cop, 0, 255)
    return img_cop
    
#Brillo por canal
def brillo_por_canal(img, r, g, b):
    img[:, :, 0] = np.clip(img[:, :, 0] + r * 255, 0, 255)
    img[:, :, 1] = np.clip(img[:, :, 1] + g * 255, 0, 255)
    img[:, :, 2] = np.clip(img[:, :, 2] + b * 255, 0, 255)
    return img

#Contraste logaritmico 
def contraste_logaritmico(img):
    c = 255 / np.log(1 + np.max(img))
    img = c * np.log(1 + img)
    return np.clip(img, 0, 255)

#Contraste Exponencial 
def contraste_exponencial(img, gamma=1.5):
    img = 255 * (img / 255) ** gamma
    return np.clip(img, 0, 255)

#Recorte
def recorte(img_pil, x1, y1, x2, y2):
    return img_pil.crop((x1, y1, x2, y2))

#Zoom
def zoom(img_pil, factor):
    w, h = img_pil.size
    return img_pil.resize((int(w * factor), int(h * factor)))

#Rotación 
def rotacion(img_pil, angulo):
    return img_pil.rotate(angulo, expand=True)

#Histograma 
def histograma(img_pil):
    plt.figure("Histograma")
    plt.hist(np.array(img_pil).ravel(), bins=256, color='gray')
    plt.title("Histograma de intensidades")
    plt.show()

#Fusión de imágenes 
def fusionar(img1_pil, img2_pil, alpha):
    img2_pil = img2_pil.resize(img1_pil.size)
    return Image.blend(img1_pil, img2_pil, alpha)

#Fusión ecualizada
def fusionar_ecualizadas(img1_pil, img2_pil, alpha):
    img1_eq = ImageOps.equalize(img1_pil.convert("L"))
    img2_eq = ImageOps.equalize(img2_pil.convert("L"))
    return Image.blend(img1_eq, img2_eq, alpha)

#Capas RGB
def extraer_rgb(img_pil):
    return img_pil.split()

#Capas y CMYK
def extraer_cmyk(img_pil):
    return img_pil.convert("CMYK").split()

#Negativo
def foto_negativa(img):
    return 255 - img

#Escala de grises 
def escala_grises(img_pil):
    return img_pil.convert("L")

#Binarización 
def binarizacion(img_pil, umbral):
    img_gray = np.array(img_pil.convert("L"))
    img_bin = (img_gray > umbral) * 255
    return Image.fromarray(img_bin.astype(np.uint8))


# Interfaz

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
    val = float(entry_brillo.get())
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = brillo(img_np, val)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) # Convierte la imagen a un arreglo numpy, suma un valor (multiplicado por 255)

def aplicar_brillo_canal(): # Modifica el brillo de cada canal de color (Rojo, Verde y Azul)
    global imagen_original
    if imagen_original is None: return
    r = simpledialog.askfloat("Brillo R", "Valor R (-1 a 1):", minvalue=-1, maxvalue=1)
    g = simpledialog.askfloat("Brillo G", "Valor G (-1 a 1):", minvalue=-1, maxvalue=1)
    b = simpledialog.askfloat("Brillo B", "Valor B (-1 a 1):", minvalue=-1, maxvalue=1)
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = brillo_por_canal(img_np, r, g, b)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) # Pide tres valores (uno por canal) mediante cuadros de dialogo, luego aplica la función brillo_por_canal para modificar cada matriz RGB

def aplicar_contraste_log(): #Resalta las zonas oscuras de la imagen
    if imagen_original is None: return
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = contraste_logaritmico(img_np)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) #Usa una transformación logaritmica sobre los valores de los pixeles (np.log(1 + valor)) para expandir los tonos oscuros

def aplicar_contraste_exp(): #Aplica un contraste exponencial (gamma correction)
    if imagen_original is None: return
    gamma = simpledialog.askfloat("Gamma", "Valor gamma (0.1-5.0):", minvalue=0.1, maxvalue=5.0)
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = contraste_exponencial(img_np, gamma)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8)))  # Si gamma < 1 -> aclara la imagen / Si gamma > 1 -> oscurece la imagen

def aplicar_recorte():  #Permite recortar una parte especifica de la imagen 
    if imagen_original is None: return
    x1 = simpledialog.askinteger("Recorte", "x1:")
    y1 = simpledialog.askinteger("Recorte", "y1:")
    x2 = simpledialog.askinteger("Recorte", "x2:")
    y2 = simpledialog.askinteger("Recorte", "y2:")
    mostrar_imagen(recorte(imagen_original, x1, y1, x2, y2)) #Solicita coordenadas (x1, y1) y (x2, y2) del area deseada

def aplicar_zoom(): #Amplia o reduce el tamaño de la imagen
    if imagen_original is None: return
    factor = simpledialog.askfloat("Zoom", "Factor (1.5 = 150%):", minvalue=0.1)
    mostrar_imagen(zoom(imagen_original, factor)) #Usa un factor de escala y redimensiona la imagen con un resize

def aplicar_rotacion():  #Gira la imagenun número de grados indicado por el usuario
    if imagen_original is None: return
    angulo = simpledialog.askfloat("Rotación", "Ángulo en grados:")
    mostrar_imagen(rotacion(imagen_original, angulo)) #Usa image.rotate (angulo) para rotar la imagen sin alterar sus dimensiones originales

def mostrar_histograma(): #Muestra el histograma de la imagen
    if imagen_original is None: return
    histograma(imagen_original) #Llama a la función histograma(), que calcula de intensidades de pixeles de 0 a 255

def aplicar_fusion(): #Fusiona dos imagenes diferentes mediante un factor de mezcla alpha
    global imagen_original, imagen_secundaria
    if imagen_original is None or imagen_secundaria is None:
        messagebox.showwarning("Fusión", "Debes cargar dos imágenes (principal y secundaria).")
        return
    alpha = simpledialog.askfloat("Fusión", "Alpha (0-1):", minvalue=0, maxvalue=1)
    mostrar_imagen(fusionar(imagen_original, imagen_secundaria, alpha))

def aplicar_fusion_ecualizada(): #Lo mismo que la función anterior, pero ecualiza ambas imagenes antes de mezclarlas 
    global imagen_original, imagen_secundaria
    if imagen_original is None or imagen_secundaria is None:
        messagebox.showwarning("Fusión Ecualizada", "Debes cargar dos imágenes primero.")
        return
    alpha = simpledialog.askfloat("Fusión Ecualizada", "Alpha (0-1):", minvalue=0, maxvalue=1)
    mostrar_imagen(fusionar_ecualizadas(imagen_original, imagen_secundaria, alpha)) #Aplica ecualización del histograma para que ambas tengan rangos tonales similares y la fusión sea más uniforme

def aplicar_negativo():  #Invierte los colores de la imagen
    if imagen_original is None: return
    img_np = np.array(imagen_original, dtype=np.float32)
    img_np = foto_negativa(img_np)
    mostrar_imagen(Image.fromarray(img_np.astype(np.uint8))) # Cada pixel p se convierte en 255 - p

def aplicar_grises(): # Convierte la imagen a escala de grises 
    if imagen_original is None: return
    mostrar_imagen(escala_grises(imagen_original)) # Calcula una media ponderada de los canales RGB (ejemplo: 0.3R + 0.59G + 0.11B).

def aplicar_binarizacion(): #Convierte la imagen a blanco y negro puro, según un umbral definido por el usuario
    if imagen_original is None: return
    umbral = simpledialog.askinteger("Binarización", "Umbral (0-255):", minvalue=0, maxvalue=255)
    mostrar_imagen(binarizacion(imagen_original, umbral)) # Si el valor del píxel > umbral → blanco (255) / Si no → negro (0).

def aplicar_rgb():
    if imagen_original is None:
        return
    r, g, b = extraer_rgb(imagen_original)
    rojo = Image.merge("RGB", (r, Image.new("L", r.size), Image.new("L", r.size)))
    verde = Image.merge("RGB", (Image.new("L", g.size), g, Image.new("L", g.size)))
    azul = Image.merge("RGB", (Image.new("L", b.size), Image.new("L", b.size), b))
    rojo.show(title="Canal Rojo (R)")
    verde.show(title="Canal Verde (G)")
    azul.show(title="Canal Azul (B)")


def aplicar_cmyk(): #Convierte la imagen de RGB a CMYK (modelo usado en impresión)
    if imagen_original is None: return
    c, m, y, k = extraer_cmyk(imagen_original)
    c.show(title="Cian"); m.show(title="Magenta"); y.show(title="Amarillo"); k.show(title="Negro") # Calcula los canales Cian, Magenta, Amarillo y Negro, y los muestra por separado.

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
