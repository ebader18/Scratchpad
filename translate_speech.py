# Make sure to install this specific version of googletrans==3.1.0a0

import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pygame
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--mic_or_wav", required=True, type=str, default="mic", help="mic for microphne, file name for audio file")
ap.add_argument("--source_language", required=False, type=str, default="en", help="What language do yo want to translate from?")
ap.add_argument("--dest_language", required=False, type=str, default="fr", help="what language do you want to translate to?")
args = vars(ap.parse_args())

r = sr.Recognizer()
translator = Translator()

source_language = args["source_language"]
dest_language = args["dest_language"]

def Speech2Text(language):
	if args["mic_or_wav"] == "mic":
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source, duration=0.2)
			audio = r.listen(source)
	else:
		fname = args["mic_or_wav"]
		with sr.AudioFile(fname) as source:
			audio = r.record(source, duration=30)

	try:	
		txt = r.recognize_google(audio, language=language)
		txt = txt.lower()
		return txt
		
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
	
	except sr.UnknownValueError:
		print("unknown error occurred")

def SpeakText(txt, language):
	tts = gTTS(text=txt, lang=language)
	tts.save('output.mp3')
	pygame.mixer.init()
	pygame.mixer.music.load('output.mp3')
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue
	pygame.mixer.quit()
	os.remove('output.mp3')

def TranslateText(txt, src_lang, dst_lang):
	txt_dest = translator.translate(txt, src=src_lang, dest=dst_lang)
	return txt_dest

# Speech to text
text_original = Speech2Text(source_language)
print(text_original)

# Read original speech
SpeakText(text_original, source_language)

# Translate text
text_translated = TranslateText(text_original, source_language, dest_language)
print(text_translated.text)

# Read translated speech
SpeakText(text_translated.text, dest_language)