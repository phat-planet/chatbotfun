import logging
import os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from gtts import gTTS
# from playsound import playsound
import pygame
import speech_recognition as sr
import time

global mood


# Upon running for the first time, you need to edit chatbotfun\venv\Lib\site-packages\sqlalchemy\util\compat.py
# go to line 264, replace time.clock with time.process_time()

def text2speech(tts):
    speech = gTTS(text=tts, lang='en', slow=False)
    speech.save("talk.mp3")
    pygame.mixer.init()
    nextline = pygame.mixer.music.load('talk.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.quit()
    os.remove("talk.mp3")


# mic setup
mic_name = "USB PnP Sound Device: Audio (hw:2,0)"
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
mic_list = sr.Microphone.list_microphone_names()
for i, microphone_name in enumerate(mic_list):
    print(microphone_name)
    if microphone_name == mic_name:
        device_id = i

bad_words = ['jabroni', 'doofus', 'dumbass', 'pinhead']  # the bot will not say phrases containing these words

name = input('Please enter your name: ')  # we want the user's name

bot = ChatBot(  # defining properties and attributes
    'spork',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # this defines the database the bot will use to learn
    preprocessors=[  # these will clean up the text so the bot can understand
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    logic_adapters=[
        {
            'import_path': 'camera_adapter.CameraAdapter'
        },
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'What is my name?',
            'output_text': ('Your name is ' + name + '.'),
            'similarity_threshold': 0.7
        },
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'What is your name?',
            'output_text': 'I don\'t have one, at the moment.',
            'similarity_threshold': 0.7
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',  # if the bot can't think of a response, it will give a
            'default_response': 'Sorry, I don\'t quite understand.',  # default response
            'maximum_similarity_threshold': 0.6,
            'excluded_words': bad_words
        },

        'chatterbot.logic.MathematicalEvaluation',  # this gives the bot the ability to solve math equations
        # {
        #   'import_path': 'mood_adapter.MoodAdapter'
        # },
        {
            'import_path': 'newtime_adapter.NewTimeLogicAdapter',  # this gives the bot the ability to tell time
        }

    ],
    database_url='sqlite://database.sqlite3'
)
print('Starting bot. . . . ')

# pygame.init()
# mysfx = pygame.mixer.Sound('startup.wav')
# mysfx.play()
# pygame.time.wait(2000)
# pygame.quit()

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
            "chatterbot.corpus.english.conversations",
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.emotion"
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
        logging.basicConfig(filename="log.txt",
                            level=logging.INFO,
                            format='%(levelname)s: %(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S')
        print('logging should be enabled')  # enable logging
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

print('Chatbot is now active')

while True:
    try:
        starttimer = time.time()
        with sr.Microphone(device_index=device_id, sample_rate=sample_rate,
                           chunk_size=chunk_size) as source:
            r.adjust_for_ambient_noise(source)
            if sfx:
                pygame.init()
                mysfx = pygame.mixer.Sound('message.wav')
                mysfx.play()
                pygame.time.wait(300)
                pygame.quit()
            endtimer = time.time()
            print(endtimer - starttimer)
            print("Speak into the mic")
            audio = r.listen(source)
            request = r.recognize_google(audio)
            print(name + ': ' + request)

        # request = (input(name + ': '))

        # time.sleep(random.randint(1, 4))  # small delay, so the bot will act like it's "thinking"
        if request == "Bye" or request == 'bye' or request == 'goodbye' or request == 'Goodbye' or request == 'shut up':
            print('Chatbot: Bye. Shutting down. . . .')  # if you say these things to the bot, it will quit
            if voice:
                text2speech('Bye. Shutting down')
            break
        else:
            response = bot.get_response(request)
            print("Chatbot: ", end='')
            print(response)
            if voice:
                tts = (str(response))
                text2speech(tts)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
    except sr.UnknownValueError:
        print('Chatbot: I couldn\'t understand you. Can you repeat that?')
        if voice:
            text2speech('I couldn\'t understand you. Can you repeat that?')
        continue
