#################
# CFC Lab 2017
# Unhelpful Bot v0.1
# Start of remucking google home to not help you at all. 
##################
import random
import time
from random import choice
from random import shuffle
from flask import Flask
from flask_assistant import Assistant, ask, tell, event, context_manager
## work in hue lights
## make some weird responses to things like "what?"

app = Flask(__name__)
assist = Assistant(app, '/')

## trying a fake out. 

def get_random_code():
	codes = ["paramErr = -50, error in user parameter list",
	"noHardwareErr = -200, Sound Manager Error Returns",
	"notEnoughHardwareErr = -201, Sound Manager Error Returns",
	"userCanceledErr = -128,",
	"qErr = -1, queue element not found during deletion",
	"vTypErr = -2, invalid queue element",
	"corErr = -3, core routine number out of range",
	"unimpErr = -4, unimplemented core routine",
	"SlpTypeErr = -5, invalid queue element",
	"seNoDB = -8, no debugger installed to handle debugger command",
	"controlErr = -17, I/O System Errors",
	"statusErr = -18, I/O System Errors",
	"readErr = -19, I/O System Errors",
	"vLckdErr = -46, volume is locked",
	"fBsyErr = -47, File is busy, delete",
	"dupFNErr = -48, duplicate filename, rename",
	"opWrErr = -49, file already open with with write permission",
	"rfNumErr = -51, refnum error",
	"gfpErr = -52, get file position error",
	"volOffLinErr = -53, volume not on line error: was Ejected",
	"permErr = -54, permissions error: on file open"
	]
	
	shuffled = shuffle(codes)
	to_say = ' '.join(codes)
	#to_say = random.choice(codes)
	return to_say


def get_random_tell_off():
	tellOffs = [
	"Not now, I'm busy",
	"Shh. I'm Busy",
	"Try me later",
	"Piss off",
	"No",
	"Not now",
	"Go away. I'm doing something.",
	"Stop interrupting me"
	]
	to_tell = random.choice(tellOffs)
	return to_tell


interrupt_counter = 0


@assist.action('greetings')
def greetings():
	speech = 'Welcome to Ghost Machine. Please begin sequence by saying begin.'
	# say begin here
	return ask(speech)

## fall back will just keep repeating things from the list
## this isn't a goooood idea, but its a start?

@assist.action('fallback', is_fallback=True)
def say_response():
	"""Ok so this is a baaaad hack, but basically its reading a really long response. """
	global interrupt_counter
	interrupt_counter+=1
	print(interrupt_counter)

	## if you interrupt the google home too many times, it will tell you off. 
	if interrupt_counter >= 3:
		speech = get_random_tell_off()
		interrupt_counter = 0
		return ask("{0}".format(speech))
	else:
		speech = get_random_code()
		print(speech)
		return ask("{0}".format(speech))
	

@assist.action('help')
def help():
	speech = "There is no help for you here."
	return ask(speech)

@assist.action('quit')
def quit():
	speech = "Leaving ghost machine"
	return tell(speech)

if __name__ == '__main__':
	app.run(debug=True)