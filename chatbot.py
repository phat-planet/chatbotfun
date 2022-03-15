import time

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from playsound import playsound
from gtts import gTTS
import os
import logging
import random


def text2speech(tts):
    speech = gTTS(text=tts, lang='en', slow=False)
    speech.save("talk.mp3")
    playsound("talk.mp3")
    os.remove("talk.mp3")


# we have to define when the bot will give the time
time_positive = ['what is the time right now', 'time', 'clock', 'what is the current time', 'what is the time now',
                 'what’s the time', 'what time is it',
                 'what time is it now', 'do you know what time it is', 'could you tell me the time, please',
                 'what is the time', 'will you tell me the time',
                 'tell me the time', 'time please', 'show me the time', 'what is time', 'whats on the clock',
                 'show me the clock',
                 'what is the time', 'what is on the clock', 'tell me time', 'time', 'clock', ]

time_negative = ['what are you doing', 'what’s up', 'when is time', 'who is time' 'could you', 'do you', 'what’s',
                 'will you', 'tell me', 'show me', 'current', 'do', 'now',
                 'will', 'show', 'tell', 'me', 'could', 'what', 'whats', 'i have time', 'who', 'who is', 'hardtime',
                 'when', 'what is', 'how',
                 'how is', 'when is', 'who is time', 'how is time', 'how is time', 'when is time', 'it is ok',
                 'you do not need to do that']

bad_words = ['jabroni', 'doofus', 'dumbass', 'pinhead']  # the bot will not say phrases containing these words

name = input('Please enter your name: ')  # we want the user's name

bot = ChatBot(  # defining properties and attributes
    'spork',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # this defines the database the bot will use to learn
    preprocessors=[  # these will clean up the text so the bot can understand
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    logic_adapters=[

        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'What is my name?',
            'output_text': ('Your name is ' + name + '.')
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'What is your name?',
            'output_text': 'My name is Spork, at the moment.'
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',  # if the bot can't think of a response, it will give a
            'default_response': 'Sorry, I don\'t quite understand.',  # default response
            'maximum_similarity_threshold': 0.75,
            'excluded_words': bad_words
        },

        'chatterbot.logic.MathematicalEvaluation',  # this gives the bot the ability to solve math equations
        {
            'import_path': 'mood_adapter.MoodAdapter'
        },
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter',  # this gives the bot the ability to tell time
            'positive': time_positive,
            'negative': time_negative
        }

    ],
    database_url='sqlite://database.sqlite3'
)
print('Starting bot. . . . ')

while True:
    choice = input("Would you like to train the bot? Enter Y/N: ")  # train bot option
    if choice == 'Y' or choice == 'y' or choice == 'yes':
        ##################################
        #           BOT TRAINING         #
        ##################################
        print('Training bot. . . . . .')
        trainer = ListTrainer(bot)
        # list trainer
        trainer.train([
            "Hello",
            "Hi there!",
            "How are you doing?",
            "I'm doing great.",
            "That is good to hear",
            "Thank you.",
            "You're welcome."
        ])
        trainer.train([  # this is for testing excluded words, the bot isn't supposed to insult you!
            "Insult me",
            "You're a dumbass."
        ])
        trainer.train([
            "Ask me about my mood",
            "How are you feeling?",
            "I am feeling",
            "So you're feeling? Did I get that right",
            "Yes",
            "Great!"
        ])
        trainer.train([
            "Ask how I'm feeling",
            "How are you feeling?"
        ])
        trainer.train([
            "How are you feeling?",
            "I am feeling",
            "So you're feeling? Did I get that right",
            "No",
            "Oh. That's ok, I'm still learning."
        ])

        trainer = ChatterBotCorpusTrainer(bot)
        trainer.train(
            "chatterbot.corpus.custom"
        )
        ##################################
        #         END OF TRAINING        #
        ##################################
        break
    if choice == 'N' or choice == 'n' or choice == 'no':
        break

while True:
    choice = input('Enable logging? Enter Y/N: ')  # logging option
    if choice == 'Y' or choice == 'y' or choice == 'yes':
        logging.basicConfig(level=logging.INFO)  # enable logging
        break
    if choice == 'N' or choice == 'n' or choice == 'no':
        break

while True:
    choice = input('Enable sound? Enter Y/N: ')  # sfx option
    if choice == 'Y' or choice == 'y' or choice == 'yes':
        sfx = True
        break
    if choice == 'N' or choice == 'n' or choice == 'no':
        sfx = False
        break

while True:
    choice = input('Enable text to speech? Enter Y/N: ')  # tts option
    if choice == 'Y' or choice == 'y' or choice == 'yes':
        voice = True
        break
    if choice == 'N' or choice == 'n' or choice == 'no':
        voice = False
        break

if sfx:
    playsound('startup.wav')
print('Spork is now active')

while True:
    try:

        request = (input(name + ': '))

        # time.sleep(random.randint(1, 4))  # small delay, so the bot will act like it's "thinking"
        if request == "Bye" or request == 'bye' or request == 'goodbye' or request == 'Goodbye' or request == 'shut up':
            print('Spork: Bye. Shutting down. . . .')  # if you say these things to the bot, it will quit
            if voice:
                text2speech('Bye. Shutting down')
            if sfx:
                playsound('shutdown.wav')
            break
        else:
            response = bot.get_response(request)
            print("spork: ", end='')
            print(response)
            if sfx:
                playsound('message.wav')
            if voice:
                tts = (str(response))
                text2speech(tts)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
