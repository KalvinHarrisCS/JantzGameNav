# Functions/api_integration.py

import requests
import openai

class ElevenLabsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"

    def text_to_speech(self, text, voice_model_id="default"):
        if not self.api_key:
            print("No ElevenLabs API key provided.")
            return None

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

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

            audio_file = "output.mp3"
            with open(audio_file, "wb") as f:
                f.write(response.content)

            return audio_file

        except requests.exceptions.RequestException as e:
            print(f"Error while making request to ElevenLabs API: {e}")
            return None

class OpenAIAPI:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

    def get_explanation(self, text):
        if not self.openai_api_key:
            print("No OpenAI API key provided.")
            return None

        prompt = f"Explain the following text in simple terms:\n\n{text}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            explanation = response['choices'][0]['message']['content']
            return explanation.strip()
        except Exception as e:
            print(f"Error while communicating with OpenAI API: {e}")
            return None

    def summarize_text(self, text):
        if not self.openai_api_key:
            print("No OpenAI API key provided.")
            return None

        prompt = f"Summarize the following text in as few and simple words as possible:\n\n{text}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response['choices'][0]['message']['content']
            return summary.strip()
        except Exception as e:
            print(f"Error while communicating with OpenAI API: {e}")
            return None

    def answer_question(self, context, question):
        if not self.openai_api_key:
            print("No OpenAI API key provided.")
            return None

        prompt = f"Based on the following text:\n\n{context}\n\nAnswer the question:\n\n{question}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response['choices'][0]['message']['content']
            return answer.strip()
        except Exception as e:
            print(f"Error while communicating with OpenAI API: {e}")
            return None
