from fastapi import FastAPI
import pyttsx3
import os
from fastapi.middleware.cors import CORSMiddleware
from serial import Serial

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tts/{text}")
def read_item(text: str):
    engine = pyttsx3.init()

    fullPath = os.path.join(os.getcwd(), "test.wav")
    os.remove(fullPath)
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    print(rate)  # printing current voice rate
    engine.setProperty('rate', 125)  # setting up new voice rate

    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    print(volume)  # printing current volume level
    engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1

    voices = engine.getProperty('voices')  # getting details of current voice
    # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

    engine.save_to_file(text, fullPath)
    engine.runAndWait()
    return {"message": "Text converted to speech successfully"}


@app.get("/piano/{notes}")
def read_item(notes: str):
    parsed = [int(x) for x in notes.split(",")]
    with Serial("/dev/tty.usbmodem1103", 9600) as s:
        for i in range(8):
            for j in range(4):
                s.write(parsed[4 * i + j].to_bytes(2, "big"))
                s.write(int(250).to_bytes(2, "big"))
            _ = s.readline()
    return {"message": notes}
