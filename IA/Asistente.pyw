import openai
import pyttsx3
import speech_recognition as sr
import tkinter as tk
import datetime
from PIL import Image, ImageTk

openai.api_key = "Ingresa la key de tu cuenta Openai"

engine = pyttsx3.init()

raiz = tk.Tk()
raiz.title("Asistente Voz")
raiz.geometry("1000x600")

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

def pregunta():
    # Reconocimiento de voz
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)

    try:
        query = recognizer.recognize_google(audio, language='es-es')
        respuesta.config(state=tk.NORMAL)
        respuesta.delete(1.0, tk.END)
        respuesta.insert(tk.END, "Tu pregunta: " + query + "\n")
        raiz.update()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=2048,
            temperature=1,
        )

        respuesta.insert(tk.END, "Respuesta: " + response['choices'][0]['text'])
        respuesta.config(state=tk.DISABLED)
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

        archivo = open(nombreArchivo + "/" + nombreArchivo + ".txt", "w")
        archivo.write(response['choices'][0]['text'])
        archivo.close()

        print("Archivo Creado con éxito")
    except:
        respuesta.config(state=tk.NORMAL)
        respuesta.delete(1.0, tk.END)
        respuesta.insert(tk.END, "No pude entenderte")
        respuesta.config(state=tk.DISABLED)
        raiz.update()
        engine.say("No pude entenderte")
        engine.runAndWait()

imagen_fondo = cargar_imagen_fondo(raiz, 'F.jpg')
canvas = tk.Canvas(raiz, width=1000, height=600)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

imagen_boton = cargar_imagen_boton(raiz, 'microfono.png')
boton = tk.Button(raiz, image=imagen_boton, command=pregunta)
boton.image = imagen_boton
canvas.create_window(450, 400, anchor=tk.NW, window=boton)

respuesta = tk.Text(raiz, wrap=tk.WORD, height=10, width=80, state=tk.DISABLED)
canvas.create_window(100, 500, anchor=tk.NW, window=respuesta)

raiz.mainloop()
