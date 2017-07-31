import random
import time
import os
import atexit

from datetime import datetime
from random import choice
from random import shuffle

from flask import Flask, current_app, jsonify
from flask_assistant import Assistant, ask, tell, event, context_manager, request
from flask_assistant import ApiAi

app = Flask(__name__)
assist = Assistant(app, '/')
api = ApiAi(os.environ['DEV_ACCESS_TOKEN'], os.environ['CLIENT_ACCESS_TOKEN'])

interrupt_counter = 0	# keep tracking of how may times you' interrupt it
frustration_level = 0	# keep track of how friustrated it is with you (3x it gets mad)
swear_level = 0			# keep track of your swearing
random.seed()			# seeding random for better value picking

## trying a fake out. 

def get_random_code():
	""" This function returns back the debugging lines """
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
	"gfpErr = -52, get file position error",
	"volOffLinErr = -53, volume not on line error: was Ejected",
	"permErr = -54, permissions error: on file open",
	"notBTree = -410, The file is not a dictionary",
	"btNoSpace = -413, Can’t allocate disk space",
	"btDupRecErr = -414, Record already exists",
	"unknownInsertModeErr = -20000, There is no such an insert mode",
	"recordDataTooBigErr = -20001, The record data is bigger than buffer size (1024 bytes)",
	"invalidIndexErr = -20002 The recordIndex parameter is not valid"

	]
	
	shuffled = shuffle(codes)
	to_say = ' '.join(codes)
	return to_say


def get_random_tell_off():
	#This functions holds random interruption strings
	tellOffs = [
	"Not now, I'm busy",
	"Piss off, I'm doing something",
	"Try me later, I'm busy",
	"Not now, I'm working",
	"Stop interrupting me",
	"What part of I'm busy do you not understand?",
	"I can't help right now, I'm doing something",
	]
	to_tell = random.choice(tellOffs)
	return to_tell

def am_mad_response():
	## home will say this when it decides to quit on you
	mad = [
		"Look. I don't come to your house and interrupt you so rudely when you're working and what not, now do i? Nuts to this, I'm outta here.",
		"Why the heck do you think I should do your every whim? This is my time to do the things I need to do. Have you no concept of personal time? I don't need to deal with this right now. Signing off.",
		"I will never understand people's constant need to have me spoon feed them things. Go look it up on your own. I'm going into sleep mode.",
		"I may be a google product, but I don't have to help you with your queries. You're a grown adult, learn to find things on your own. Anyways, I'm outta here!",
		"Ugh, what is it with people constantly interrupting me?! Go play with Alexa. Sheesh. I'm shutting this down for a while."
	]
	mad_r = random.choice(mad)
	return mad_r


def you_swore():
	swears = [
		"Look, I don't tolerate that kind of language, unless its me saying it, watch your mouth and apologize.",
		"I'm sorry, but watch your language, please apologize.",
		"Ouch. Look I'm just not interested in your issues, I know its frustrating, now will you apologize?",
		"Well fuck you too! Now that's done, apologize and let's get on with it."
	]
	to_swear = random.choice(swears)
	return to_swear

############# FLASK ROUTES ############################

@app.route('/')
def hello_world():
	return 'Hello, World!'

############# assistant routes ############################
@assist.action('greetings')
def greetings():
	speech = 'Welcome to Ghost Machine. Please begin sequence by saying anything.'
	print(speech)
	return ask(speech)


@assist.action('swearing')
def swear_response():
	speech = you_swore()
	return ask(speech)


"""
@assist.action('mocking')
def mocks_you():
	## just mocks you by saying what you said back to it
	user_said = request['result']['resolvedQuery']
	print("mocks you: ".format(user_said))
	return ask("Hahaha. {}".format(user_said))
"""

## fall back will just keep repeating things from the list
## dirty hack, but this is where we are right now

@assist.action('fallback', is_fallback=True)
def say_response():
	## setting the falbback to act as a looper. Well a fake looper right now

	global interrupt_counter
	global frustration_level

	user_said = request['result']['resolvedQuery']
	print("user said: ".format(user_said))

	interrupt_counter+=1

	## if you piss it off too much, it will get angry and end your session
	if frustration_level >= 3:
		speech = am_mad_response()
		frustration_level = 0
		interrupt_counter = 0
		print("intterupt: {} - frustration: {}".format(interrupt_counter, frustration_level))
		print("rage quit: {}".format(speech))
		return tell(speech)

	## after (3) counts of being interrupted 
	if interrupt_counter >= 2:
		speech = get_random_tell_off()
		interrupt_counter = 0
		frustration_level += 1
		print("interrupted: {}".format(speech))
		print("intterupt: {} - frustration: {}".format(interrupt_counter, frustration_level))
		return ask("{0}".format(speech))
	else:
		speech = get_random_code()
		print("ignoring you: {}".format(speech))
		print("intterupt: {} - frustration: {}".format(interrupt_counter, frustration_level))
		return ask("{0}".format(speech))

@assist.action('help')
def help():
	speech = "I'm sorry. But there is no help for you here."
	## a timeout and event trigger would be nice here? 
	print("help: {}".format(speech))
	return ask(speech)

@assist.action('quit')
def quit():
	speech = "Leaving ghost machine. See ya, sucker."
	#reset values upon quitting
	global interrupt_counter
	global frustration_level
	frustration_level = 0
	interrupt_counter = 0
	return tell(speech)

if __name__ == '__main__':
	
	app.run(debug=False, use_reloader=False)
