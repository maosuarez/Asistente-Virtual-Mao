import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia 
# escuchar nuestro microfono y devolver el audio con texto
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar micro
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language = "es-co")

            # prueba de que pudo ingresar:
            print("dijiste: " + pedido)

            #devolver pedido
            return pedido
        # en caso de fracasar
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups no entendi")

            #devolver error
            return "sigo esperando"
        
        # error de no resolver el pedido
        except sr.RequestError:
            
            # prueba de que no comprendio el audio
            print("ups no hay servicio")

            #devolver error
            return "sigo esperando"
        
        # error inesperado
        except:
                        
            # prueba de que no comprendio el audio
            print("ups algo ha salido mal")

            #devolver error
            return "sigo esperando"
# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice",id3)
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()     
# opciones de voz
id1 ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
id2 ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
id3 ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
def pedir_dia():
    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario
    calendario ={0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
     
    # Decir dia de calendario
    hablar(f"hoy es{calendario[dia_semana]}{dia.day}")
def pedir_hora():
    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    if hora.hour > 12:
        hour = hora.hour - 12
    else:
        hour = hora.hour
    if hora.hour != 1:
        if hora.minute != 1:
            hora = f'En este momento son las {hour} con {hora.minute} minutos'
        else:
            hora = f'En este momento son las {hour} con {hora.minute} minuto'
    else:
        if hora.minute != 1:
            hora = f"En este momento es la {hour} con {hora.minute} minutos"
        else:
            hora = f"En este momento es la {hour} con {hora.minute} minuto"
    print(hora)
    #decir la hora
    hablar(hora)
def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas Noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen Día"
    else:
        momento = "Buenas tardes"
    
    # decir el saludo
    hablar(f"{momento}, soy el asistente virtual de Mao, por favor dime si necesitas algo")
def pedir_cosas():
    #activar el saludo
    saludo_inicial()
    # variable de corte
    comenzar = True
    while comenzar:
        #activar el micro y guardar el pedido en un str
        pedido = transformar_audio_en_texto().lower()
        for x in pedido:
            if x == "á":
                pedido = pedido.replace("á","a")
            if x == "é":
                pedido = pedido.replace("é","e")
            if x == "í":
                pedido = pedido.replace("í","i")
            if x == "ó":
                pedido = pedido.replace("ó","o")
            if x =="ú":
                pedido = pedido.replace("ú","u")
        if "abrir youtube" in pedido or "abre youtube" in pedido:
            hablar("con gusto, estoy abriendo youtube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abrir navegador" in pedido:
            hablar("Claro, Estoy en eso")
            webbrowser.open("https://www.google.com")
            continue
        elif "que dia es hoy" in pedido:
            pedir_dia()
            continue
        elif "que hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido or "busca en wikipedia sobre" in pedido:
            hablar("Buscando eso en wikipedia")
            wikipedia.set_lang("es")
            try:
                pedido = pedido.replace("busca en wikipedia","")
            except:
                pedido = pedido.replace("busca en wikipedia sobre","")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar(f"Segun Wikipedia:")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("ya mismo estoy en eso")
            pedido = pedido.replace("busca en internet","")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("ok, reproduciendo")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido or "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strp()
            cartera = {"apple":"APPL",
                       "amazon":"AMZN",
                       "google": "GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontré, el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("Lo siento, no la he encontrado")
                continue
        elif "gracias asistente" in pedido or "adios" in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break
        elif "quiero un programa" in pedido or "quiero un codigo"in pedido:
            try:
                pedido = pedido.replace("quiero un programa","")
            except:
                pedido = pedido.replace("quiero un codigo","")
            Programar_Pseint(pedido)
pedir_cosas()




