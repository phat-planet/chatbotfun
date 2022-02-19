import time

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from playsound import playsound
import logging
import random

logging.basicConfig(level=logging.INFO)

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
                 'how is', 'when is', 'who is time', 'how is time', 'how is time', 'when is time']

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
            'import_path': 'chatterbot.logic.BestMatch',  # if the bot can't think of a response, it will give a
            'default_response': 'Sorry, I don\'t quite understand.',  # default response
            'maximum_similarity_threshold': 0.75
        },
        'chatterbot.logic.MathematicalEvaluation',  # this gives the bot the ability to solve math equations
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter',  # this gives the bot the ability to tell time
            'positive': time_positive,
            'negative': time_negative
        }

    ],
    database_url='sqlite:///database.sqlite3'
)

print('Training bot. . . . . .')
playsound('startup.wav')
trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "chatterbot.corpus.english"
)

name = input('Please enter your name: ')  # we want the user's name
print('Spork is now active')

while True:
    try:

        request = (input(name + ': '))
        # if you say these things to the bot, it will quit
        time.sleep(random.randint(1, 4))
        if request == "Bye" or request == 'bye' or request == 'shut up':
            print('Spork: Bye')
            playsound('shutdown.wav')
            break
        else:
            response = bot.get_response(request)
            print("spork: ", end='')
            print(response)
            playsound('message.wav')

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
