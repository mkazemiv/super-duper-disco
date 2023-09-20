import os
import requests
from urllib import request
from pathlib import Path
api_key = os.getenv("API_KEY")
UPLOAD_FOLDER = 'static/results/'

def merge(audioFilename, imgFilename):
    #setting up audio
    url = "https://api.d-id.com/audios"
    audioFilepath = os.path.join(UPLOAD_FOLDER, audioFilename)
    print("audioFilepath", audioFilepath)
    files = { "audio": (audioFilename, open(audioFilepath, "rb"), "audio/mpeg") }
    headers = {
        "accept": "application/json",
        "authorization": "Basic " + api_key
    }
    response = requests.post(url, files=files, headers=headers)
    print(response.json())
    #get the audio url from the response object
    audio_url = response.json()["url"]
    print("audio_url", audio_url)

    url = "https://api.d-id.com/talks"
    imgFilepath = os.path.join(UPLOAD_FOLDER, imgFilename)
    source_url = f"https://3046.chickenkiller.com/{imgFilepath}"
    print("source_url", source_url)
    source_url = "https://3046.chickenkiller.com/static/results/man5.jpg"
    payload = {
        "script": {
            "type": "audio",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false",
            "reduce_noise": "false",
            "audio_url": audio_url
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": source_url,
        "webhook": "https://discord.com/api/webhooks/1136563031548108900/Jly73sIZdzD9KymViywrP6Eg9eBbuVRZAcLGfFh4Sb2sVCgwJQkHzjkuem04K9u7vka7"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic " + api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

    talk_id = response.json()["id"]
    url = "https://api.d-id.com/talks/" + talk_id
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic " + api_key
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    result_url = response.json()["result_url"]
    return result_url
