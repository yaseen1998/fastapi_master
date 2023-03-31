from gtts import gTTS
from pydub import AudioSegment

text = """clinic, dentist, reception, appointment, staff selection, colleague,
workshop, showroom, information desk, employer, employment, unemployed, technical
cooperation, team leaders, stress, ability, vision, confidence, employee, internship"""

def readText():
    filename = "/mnt/d/lesten/workplace.mp3"
    text2 = text.split(',')
    audio = AudioSegment.silent(duration=1000) # add a 1 second silence at the beginning
    first = False
    for item in text2:
        tts = gTTS(item)
        tts.save("temp.mp3")
        item_audio = AudioSegment.from_mp3("temp.mp3")
         # add a 1 second silence after each item
        # if first:
        audio = audio + item_audio + AudioSegment.silent(duration=3000)
        
    audio.export(filename, format="mp3")
        

            
            

            
        
if __name__ == '__main__':
    readText()