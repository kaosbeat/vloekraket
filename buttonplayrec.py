import pyaudio
import wave
import sys
import RPi.GPIO as gpio 
from recorder import Recorder 
gpio.setmode(gpio.BCM)  
import time
import pickle
import random



class ButtonRecorder(object): 
    def __init__(self, filename): 
        self.filename = filename 
        gpio.setup(23, gpio.IN, pull_up_down=gpio.PUD_UP) 
        self.rec = Recorder(channels=2) 

    def start(self): 
        gpio.add_event_detect(23, gpio.FALLING, callback=self.falling, bouncetime=10) 

    def rising(self, channel): 
        gpio.remove_event_detect(23) 
        print 'Button up' 
        gpio.add_event_detect(23, gpio.FALLING, callback=self.falling, bouncetime=10) 
        #TODO: dim red LED
        self.recfile.stop_recording() 
        self.recfile.close() 
    
    def falling(self, channel): 
        ts = time.time()
	gpio.remove_event_detect(23) 
        print 'Button down' 
        gpio.add_event_detect(23, gpio.RISING, callback=self.rising, bouncetime=10) 
        #TODO: lit green LED        
        play = PlayFile(vloeken.keys()[random.randint(0,len(vloeken))])
        play.start()
        #TODO: dim green, lite red LED
        vloeken[self.filename + str(ts) + '.wav'] = {'inputfor':[]}
        with open('vloeken.log', 'wb') as handle:
            pickle.dump(vloeken, handle)
        self.recfile = self.rec.open(self.filename + str(ts) + '.wav', 'wb')    
        self.recfile.start_recording() 
		
class PlayFile(object):
    def __init__(self, filename):
        self.p = pyaudio.PyAudio()
	self.chunk_size = 1024    
        self.filename = filename
        self.wf = wave.open(self.filename , 'rb')
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True)    
    
    def start(self):
        self.data = self.wf.readframes(self.chunk_size)
        while self.data != '':
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk_size)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

#a = {
#  'vloek1433022058.28.wav' : {'inputfor':['vloek1433022072.44.wav']} ,
#  'vloek1433022072.44.wav' : {'inputfor':[]}
#}

#with open('vloeken.log', 'wb') as handle:
#  pickle.dump(a, handle)	    

with open('vloeken.log', 'rb') as handle:
    vloeken = pickle.loads(handle.read())

print vloeken

rec = ButtonRecorder('vloek')
rec.start() 

try: 
    raw_input() 

except KeyboardInterrupt: 
    pass 

gpio.cleanup()
