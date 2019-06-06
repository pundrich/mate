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
    return True


install("html2text")


install("python-edgar")






#install("vaderSentiment")

#install("plotly")

#install("cufflinks")
install("tensorflow")

install("stop_words")
install("gensim")




pip install fastai==0.7.0