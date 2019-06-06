#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:41:26 2019

@author: gabrielpundrich
"""

import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])



install("vaderSentiment")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:48:10 2019

@author: gabrielpundrich
"""




from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


sentiment_analyzer_scores("The day is almost good.")
sentiment_analyzer_scores("The day is almost not not good.")



from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
vs = analyzer.polarity_scores("VADER Sentiment looks interesting, I have high hopes!")
print(vs)



