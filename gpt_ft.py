from openai import OpenAI
import argparse
import numpy as np
import pandas as pd
import os
import csv


def fine_tuning(model_name, training_file):
    with open('openai_api_key.txt', 'r') as file:
        api_key = file.read().strip()

    client = OpenAI(api_key=api_key)

    client.files.create(
        file=open(training_file, "rb"),
        purpose="fine-tune"
    )

    client.fine_tuning.jobs.create(
        training_file="train",
        model="gpt-3.5-turbo"
    )

def main():