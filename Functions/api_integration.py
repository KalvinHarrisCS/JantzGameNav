# Functions/api_integration.py

import requests

class ElevenLabsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.voice_id = '8aKC1tJmw2H0VAETY4sJ'  # Default voice ID; change if desired

    def text_to_speech(self, text):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            'Accept': 'audio/mpeg',
            'Content-Type': 'application/json',
            'xi-api-key': self.api_key,
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        try:
            print("Sending text to ElevenLabs API for TTS conversion...")
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                audio_file = 'output.mp3'
                with open(audio_file, 'wb') as f:
                    f.write(response.content)
                print(f"Audio content saved to '{audio_file}'.")
                return audio_file
            else:
                print(f"API request failed with status code {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred while calling the ElevenLabs API: {e}")
            return None

    
 
