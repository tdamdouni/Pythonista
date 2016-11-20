# coding: utf-8

# https://gist.github.com/jsbain/8381f7a28dbfade5ce1e1a69329ac4e5

from objc_util import *
AVSpeechUtterance=ObjCClass('AVSpeechUtterance')
AVSpeechSynthesizer=ObjCClass('AVSpeechSynthesizer')
AVSpeechSynthesisVoice=ObjCClass('AVSpeechSynthesisVoice')

# it seems in ios8.3 name and quality are not present... 
voices=AVSpeechSynthesisVoice.speechVoices()
print(voices)
#on ios9, there should be a name and quality field.. but not on ios8. so i cant test, but you could try sesrching through voicces to see if quality() is different
	
voice=AVSpeechSynthesisVoice.voiceWithLanguage_('de-DE')
#if you find what you need in voices, use that instead. 
#I am not sure of the exact code, but something like the following
# though maybe v.identifier() or v.name()
# for v in voices:
#     if 'Enhanced' in str( v.description()):
#			voice=v	
#			break
synthesizer=AVSpeechSynthesizer.new()

utterance=AVSpeechUtterance.speechUtteranceWithString_("Es tut mir leid, Taha. Ich kann das nicht ausführen!")

#the value that sounds good apparantly depends on ios version
utterance.rate=0.1
utterance.voice=voice
utterance.useCompactVoice=False 
synthesizer.speakUtterance_(utterance)

#you will want to read about AVSpeechSynthesizer if you want to queue, pause, etc.
