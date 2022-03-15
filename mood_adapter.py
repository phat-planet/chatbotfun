from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class MoodAdapter(LogicAdapter):
    """
    The MoodAdapter is meant to help the chatbot form a response regarding the user's mood.

    :kwargs:
        * *mood* (``list``) --
          Mood expressions meant to detect the user's mood.
          Defaults to a list of English sentences.


    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from nltk import NaiveBayesClassifier

        # self.response_statement = Statement(text='This logic adapter is working.')
        # it needs to be a statement type variable

        self.nomood = kwargs.get('nomood', [  # here, we have examples of mood expressions
            'he is going to go get a burger',
            'she is driving him to Whataburger',
            'would you like fried with that',
            'thank you drive through',
            'what is up',
            'how are you doing',
            'are you alright',
            'come with me',
            'hello there',
            'good evening',
            'what are you doing',
            'please chat with me',
            'I don\'t feel so good',
            'I don\'t know',
            'I\'m not sure'
            'no'
            'I see'

        ])
        self.angry = kwargs.get('angry', [
            'I am so mad',
            'I\'m mad',
            'I am feeling mad',
            'I\'m feeling mad',
            'I feel mad',
            'I am pissed off',
            'I\'m pissed off',
            'I am feeling pissed',
            'I\'m feeling pissed',
            'I feel pissed off',
            'I am furious',
            'I\'m furious',
            'I am feeling furious',
            'I\'m feeling furious',
            'I feel furious',
            'I am angry',
            'I\'m angry',
            'I am feeling angry',
            'I\'m feeling angry',
            'I feel angry'
        ])
        self.disgusted = kwargs.get('disgusted', [
            'I am so disgusted',
            'I\'m disgusted',
            'I am feeling disgusted',
            'I\'m feeling disgusted',
            'I feel disgusted',
            'I am grossed out',
            'I\'m grossed out',
            'I am grossed out',
            'I\'m feeling grossed out',
            'I feel grossed out'

        ])
        self.fearful = kwargs.get('fearful', [
            'I am so fearful',
            'I\'m fearful',
            'I am feeling fearful',
            'I\'m feeling fearful',
            'I feel scared',
            'I am scared',
            'I\'m scared',
            'I am feeling scared',
            'I\'m feeling scared',
            'I am spooked',
            'I\'m spooked',
            'I am feeling spooked',
            'I\'m feeling spooked',
            'I feel spooked',
            'I am shaken up',
            'I\'m shaken up',
            'I am feeling shaken up',
            'I\'m feeling shaken up',
            'I feel shaken up'
        ])
        self.happy = kwargs.get('happy', [
            'I am so happy',
            'I\'m happy',
            'I am feeling happy',
            'I\'m feeling happy',
            'I feel happy',
            'I am glad',
            'I\'m pissed glad',
            'I am feeling glad',
            'I\'m feeling glad',
            'I feel glad',
            'I am good',
            'I\'m feeling good',
            'I am feeling good',
            'I\'m feeling good',
            'I feel good',
            'I am great',
            'I\'m great',
            'I am feeling great',
            'I\'m feeling great',
            'I feel great',
        ])
        self.neutral = kwargs.get('neutral', [
            'I am ok',
            'I\'m ok',
            'I am feeling ok',
            'I\'m feeling ok',
            'I feel ok',
            'I don\'t feel anything',
            'I am feeling neutral',
            'I\'m neutral',
            'I am feeling neutral',
            'I\'m feeling neutral',
            'I feel neutral',
            'I am alright',
            'I\'m alright',
            'I am feeling alright',
            'I\'m feeling alright',
            'I feel alright',
        ])
        self.sad = kwargs.get('sad', [
            'I am sad',
            'I\'m sad',
            'I am feeling sad',
            'I\'m feeling sad',
            'I feel sad',
            'I am down',
            'I\'m down',
            'I am feeling down',
            'I\'m feeling down',
            'I feel down',
            'I am gloomy',
            'I\'m gloomy',
            'I am feeling gloomy',
            'I\'m feeling gloomy',
            'I feel gloomy',
        ])
        self.surprised = kwargs.get('surprised', [
            'I am surprised',
            'I\'m surprised',
            'I am feeling surprised',
            'I\'m feeling surprised',
            'I feel surprised',
            'I am shocked',
            'I\'m shocked',
            'I am feeling shocked',
            'I\'m feeling shocked',
            'I feel shocked',
        ])

        labeled_data = (  # each emotion gets its own category
                [
                    (name, 0) for name in self.nomood
                ] + [
                    (name, 1) for name in self.angry
                ] + [
                    (name, 2) for name in self.disgusted
                ] + [
                    (name, 3) for name in self.fearful
                ] + [
                    (name, 4) for name in self.happy
                ] + [
                    (name, 5) for name in self.neutral
                ] + [
                    (name, 6) for name in self.sad
                ] + [
                    (name, 7) for name in self.surprised
                ]
        )

        train_set = [
            (self.mood_detection_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)  # and we use naive bayes classification to determine
        # how the user is feeling

    def mood_detection_features(self, text):  # this is for the bot to figure out how you feel
        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.nomood + self.angry + self.disgusted + self.fearful + self.happy + self.neutral +
                             self.sad + self.surprised).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in (self.nomood + self.angry + self.disgusted + self.fearful + self.happy + self.neutral +
                         self.sad + self.surprised):
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )

        for word in text.split():
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def process(self, statement, additional_response_selection_parameters=None):

        mood_features = self.mood_detection_features(statement.text.lower())
        mood_selection = self.classifier.classify(mood_features)

        if mood_selection == 1:
            response = Statement(text='So you\'re feeling angry? Did I get that right?')
            response.confidence = 1
            return response
        elif mood_selection == 2:
            response = Statement(text='So you\'re feeling disgusted? Did I get that right?')
            response.confidence = 1
            return response
        elif mood_selection == 3:
            response = Statement(text='So you\'re feeling fearful? Did I get that right?')
            response.confidence = 1
            return response
        elif mood_selection == 4:
            response = Statement(text='So you\'re feeling happy? Did I get that right?')
            response.confidence = 1
            return response
        elif mood_selection == 5:
            response = Statement(text='So you aren\'t feeling much of anything? Did I get that right?')
            response.confidence = 1
            return response
        elif mood_selection == 6:
            response = Statement(text='So you\'re feeling sad? Did I get that right?')
            response.confidence = 1
            return response
        elif mood_selection == 7:
            response = Statement(text='So you\'re feeling surprised? Did I get that right?')
            response.confidence = 1
            return response
        else:
            response = Statement(text='I see.')
            response.confidence = 0
            return response

    # response = Statement(text='The current time is ' + now.strftime('%I:%M %p'))

    # response.confidence = confidence
    # return response
