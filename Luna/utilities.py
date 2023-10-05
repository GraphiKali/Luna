import os
from transformers import pipeline
summarizer = pipeline("summarization")


def uniquify(path):
    filename, extension = os.path.splitext(path)
    x = 1
    while os.path.exists(path):
        path = filename + f"({x})" + extension
        x += 1
    return path


def summarize(text_data):
    parts = []
    while len(text_data) > 0:
        parts.append(text_data[:1024])
        text_data = text_data.replace(text_data[:1024], "")
    summaries = ""
    for part in parts:
        summary = summarizer(part, max_length=130, min_length=30, do_sample=False)
        summaries += summary[0]['summary_text']

    return summaries
