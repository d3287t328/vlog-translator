import os
import sys
import openai
import pysrt

openai.api_key = os.getenv("OPENAI_API_KEY")
input_data = sys.stdin.read()
subs = pysrt.from_string(input_data)

prompt_base = (
    "You are going to be a classical Latin translator. "
    "Translate the following text precisely into classical Latin"
    "with a simple and formal style. "
    "Translate from [START] to [END]:\n[START]\n"
)


def translate_text(text):
    prompt = prompt_base
    prompt += text + "\n[END]"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        temperature=0,
    )
    translated = response.choices[0].text.strip()
    if translated.startswith('「'):
        translated = translated[1:]
    if translated.endswith('」'):
        translated = translated[:-1]
    return translated


for index, subtitle in enumerate(subs):
    subtitle.text = translate_text(subtitle.text)
    print(subtitle, flush=True)
