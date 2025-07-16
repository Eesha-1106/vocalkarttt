import openai
from dotenv import load_dotenv
import os
import whisper
from googletrans import Translator

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
translator = Translator()
model = whisper.load_model("base")

def transcribe_voice(audio_file):
    audio_bytes = audio_file.file.read()
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp.wav")
    return result["text"]

def generate_description(input_text):
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        messages=[{"role": "system", "content": "Generate a product description."},
                  {"role": "user", "content": input_text}]
    )
    return response['choices'][0]['message']['content']

def categorize_product(input_text):
    prompt = f"What category does this product belong to? '{input_text}'"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=30
    )
    return response['choices'][0]['text'].strip()

def detect_missing_fields(text):
    required = ["name", "price", "quantity"]
    missing = [field for field in required if field not in text.lower()]
    return missing

def translate_text(text, target="en"):
    return translator.translate(text, dest=target).text

def get_market_insights():
    prompt = "Give latest market insights for rural farmers and sellers."
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def ai_chat_assistant(user_prompt):
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response['choices'][0]['message']['content']
