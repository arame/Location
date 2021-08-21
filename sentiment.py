from math import nan
import nltk
from nltk import text
from data_cleaner import DataCleaner
# VADER (Valence Aware Dictionary and sEntiment Reasoner) 
# is a lexicon and rule-based sentiment analysis tool that is specifically 
# attuned to sentiments expressed in social media.
# See http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentiment:
    def __init__(self) -> None:
        self.POSITIVE = 1
        self.NEUTRAL = 9
        self.NEGATIVE = 0
        self.THRESHOLD = 0.05

    def get(self, csv_file):
        text_list = csv_file["Full Text"].tolist()
        self.pos = []
        self.neu = []
        self.neg = []
        self.com = []
        self.sent = []
        self.clean_text = []
        self.is_lockdown = []
        self.is_facemask = []
        self.count = 0
        self.prev_text = "N/A"
        for _text in text_list:
            _text = _text.lower()
            self.clean_text.append(DataCleaner.remove_noise(_text))
            self.is_lockdown.append("lockdown" in _text)
            self.is_facemask.append(self.facemask_in_text(_text))
            self.calc(_text)
            self.pos.append(self.positive)
            self.neu.append(self.neutral)
            self.neg.append(self.negative)
            self.com.append(self.compound)      
            self.sent.append(self._sentiment)

    def facemask_in_text(self, _text):
        if "facemask" in _text or "face-mask" in _text:
            return True

        return False


    def calc(self, text):
        self.count += 1
        self.text = text
        analyzer = SentimentIntensityAnalyzer()
        try:
            # The VADER library returns 4 values such as
            # pos: The probability of the sentiment to be positive
            # neu: The probability of the sentiment to be neutral
            # neg: The probability of the sentiment to be negative
            # compound: The normalized compound score which calculates the sum of all lexicon ratings and takes values from -1 to 1
            # See documentation https://github.com/cjhutto/vaderSentiment
            scores = analyzer.polarity_scores(self.text)
            self.positive = scores["pos"]
            self.negative = scores["neg"]
            self.neutral = scores["neu"]
            self.compound = scores["compound"]
            self._sentiment = self.get_sentiment()
            self.prev_text = text
        except:
            _t = str(text).encode('utf8')
            print(f"!! Data Error - row: {self.count}, text: {self.text}, previous text: {self.prev_text}")
            self.positive = 9
            self.negative = 9
            self.neutral = 9
            self.compound = 9
            self._sentiment = 9

    def get_sentiment(self):
        # The compound value is set between -1 and 1
        # See https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/

        # if the compound value is between -0.05 and 0.05 (ie self.THRESHOLD), the sentiment is probably neutral
        if abs(self.compound) < self.THRESHOLD:
            return self.NEUTRAL    

        # if the compound is otherwise positive, the sentiment is probably positive
        if self.compound > 0:
            return self.POSITIVE

        # if the compound is otherwise negative, the sentiment is probably negative
        return self.NEGATIVE

    def print_results(self):
        print(f"\ntext: {self.text}")
        print(f"result positive sentiment = {self.positive}")
        print(f"result negative sentiment = {self.negative}")
        print(f"result neutral sentiment = {self.neutral}")

        # Compound is the general overall sentiment of the input. Values between -1 (negative) and 1 (positive).
        print(f"result compound sentiment = {self.compound}")
        print(f"result sentiment = {self._sentiment}")
