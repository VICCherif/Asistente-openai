import openai
import pyttsx3
import speech_recognition as sr
import tkinter as tk
import datetime
from PIL import Image, ImageTk

openai.api_key = "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"

engine = pyttsx3.init()

raiz = tk.Tk()
raiz.title("Asistente Voz")
raiz.geometry("1920x1080")

def cargar_imagen_fondo(raiz, ruta_imagen):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((1000, 500), Image.ANTIALIAS)
    foto = ImageTk.PhotoImage(imagen)
    return foto

def cargar_imagen_boton(raiz, ruta_imagen):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((100, 50), Image.ANTIALIAS)
    foto = ImageTk.PhotoImage(imagen)
    return foto

result_box = None
limpiar_boton = None
pregunta_label = None
respuesta_label = None

def pregunta():
    global result_box
    global limpiar_boton
    global pregunta_label
    global respuesta_label

    # Elimina el recuadro de respuesta y el botón de limpiar si ya existen
    if result_box is not None:
        result_box.destroy()
    if limpiar_boton is not None:
        limpiar_boton.destroy()

    # Reconocimiento de voz 
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Interfaz gráfica para ver los resultados
    if pregunta_label is None:
        pregunta_label = tk.Label(raiz, text="Escuchando.......", font='Helvetica 10 bold')
        pregunta_label.pack()
    else:
        pregunta_label.config(text="Escuchando.......")
    raiz.update()

    try:
        query = recognizer.recognize_google(audio, language='es-es')
        pregunta_label.config(text="Tu pregunta: " + query)
        raiz.update()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt= query,
            max_tokens=2048,
            temperature=1,
        )

        if respuesta_label is None:
            respuesta_label = tk.Label(raiz, text="Respuesta: ", font='Helvetica 10 bold')
            respuesta_label.pack()
        raiz.update()

        # Crear el recuadro de respuesta y el botón de limpiar
        result_box = tk.Text(raiz, wrap=tk.WORD, width=80, height=10)
        result_box.insert(tk.END, response['choices'][0]['text'])
        result_box.pack()
        raiz.update()

        def limpiar():
            result_box.delete(1.0, tk.END)

        limpiar_boton = tk.Button(raiz, text="Limpiar", command=limpiar)
        limpiar_boton.pack()
        raiz.update()
        
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 150)
        engine.setProperty('voice', voices[1].id)
        engine.say(response['choices'][0]['text'])
        engine.runAndWait()

        nombreArchivo = datetime.datetime.now()
        nombreArchivo = str(nombreArchivo.strftime('%Y-%m-%d %H-%M-%S'))

        import os
        os.mkdir(nombreArchivo)
        Rtext = response['choices'][0]['text']

        if "python" in query.lower():
            archivo = open(nombreArchivo + "/" + nombreArchivo + ".py", "w")
        else:
            archivo = open(nombreArchivo + "/" + nombreArchivo + ".txt", "w")

        archivo.write(Rtext)
        archivo.close()

        print("Archivo creado con éxito")
    except:
        pregunta_label.config(text="No pude entenderte")
        raiz.update()
        engine.say("No pude entenderte")
        engine.runAndWait()

imagen_fondo = cargar_imagen_fondo(raiz, 'F.jpg')
canvas = tk.Canvas(raiz, width=1000, height=800)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

imagen_boton = cargar_imagen_boton(raiz, 'microfono.png')
boton = tk.Button(raiz, image=imagen_boton, command=pregunta)
boton.image = imagen_boton
canvas.create_window(450, 400, anchor=tk.NW, window=boton)
canvas.create_window(450, 400, anchor=tk.NW, window=boton)

raiz.mainloop()
