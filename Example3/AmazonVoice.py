#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import contextlib
import os
from datetime import datetime


# CLIENT OBJETCS
# iam = boto3.client('iam') # account management
session = boto3.Session(profile_name='default')
polly = session.client('polly')


class Speaker(object):

    allVoices = ['Ricardo', 'Vitória']
    # default = mp3 (for audiostream); json (for speechmarks)
    allOutputFormats = ['mp3', 'json', 'ogg_vorbis', 'pcm']
    allSampleRatesMP3_OGG = ['8000', '16000', '22050']  # default = '22050'
    allSampleRatesPCM = ['8000', '16000']  # default = '16000'

    def __init__(self, voice=allVoices[0], outputFormat=allOutputFormats[0]):
        self.voice = voice if voice in self.allVoices else self.allVoices[0]
        self.outputFormat = outputFormat if outputFormat in self.allOutputFormats else self.allOutputFormats[0]

    def generateSpeech(self, text, path=os.getcwd(),
                       outputFilename=datetime.now().strftime("%Y%m%d%H%M%S.mp3")):

        # SYNTHESIZING SPEECH
        try:
            speechStream = polly.synthesize_speech(
                VoiceId=self.voice,
                OutputFormat=self.outputFormat,
                Text=text,
            )
        except (BotoCoreError, ClientError) as error:
            print(error)

        # WRITING FILE
        # checking chosen extension
        if not outputFilename[-3:] in self.allOutputFormats:
            print('>>> WARNING: the string outputFilename does not contain an valid extension! \n \
                    File will be saved as it was specified.')
        if 'AudioStream' in speechStream:
            with contextlib.closing(speechStream['AudioStream']) as stream:
                outputFilePath = os.path.join(path, outputFilename)
                try:
                    with open(outputFilePath, 'wb') as file:
                        file.write(stream.read())
                        file.close()
                except IOError as error:
                    print(error)
        else:
            print("StreamingBody: 'AudioStream' is null.")


# description = polly.describe_voices(LanguageCode = 'pt-BR')
# for voice in description['Voices']:
#     print(voice)


voz = Speaker()
print(voz.voice + ' ' + voz.outputFormat)
voz.generateSpeech('deu certo')


print('terminou sem problemas')
