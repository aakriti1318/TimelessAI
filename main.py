import logging
from gensim.summarization.summarizer import summarize
import requests
import json
import re


def main(text, word_count):
    logging.info('Python HTTP trigger function processed a request.')
    if text and word_count:
        punctuatedText = punctuate_online(text)
        summary = summarize(punctuatedText, ratio=0.5,
                            split=True, word_count=int(word_count))
        summary = [re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", " ", s).strip()
                   for s in summary]
        summary = ". ".join(summary)
        results = {
            "status": 200,
            "summary": summary
        }
        return summary
    else:
        return ''


def punctuate_online(text):
    # defining the api-endpoint
    API_ENDPOINT = "http://bark.phon.ioc.ee/punctuator"
    # data to be sent to api
    data = dict(text=text)
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    punctuatedText = r.text
    return punctuatedText
