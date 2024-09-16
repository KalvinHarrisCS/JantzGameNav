# Functions/api_integration.py

import requests

class ElevenLabsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"

    def text_to_speech(self, text, voice_model_id="default"):
        """Sends the text to ElevenLabs TTS API with a specific voice model."""
        if not self.api_key:
            print("No API key provided for ElevenLabs.")
            return None
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Use the voice model ID passed in or a default one
        url = f"{self.base_url}/text-to-speech/{voice_model_id}"

        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            # Save the response audio to a file
            audio_file = "output.mp3"
            with open(audio_file, "wb") as f:
                f.write(response.content)
            
            return audio_file

        except requests.exceptions.RequestException as e:
            print(f"Error while making request to ElevenLabs API: {e}")
            return None
