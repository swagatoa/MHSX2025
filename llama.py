from openai import OpenAI
from time import time
import os
import base64

with open("gemini_api_key.txt", "r") as txt:
    client = OpenAI(api_key=txt.read(), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")





def askLlama(system, user, model="gemini-2.5-flash"):
    start = time()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0,
        max_tokens=512
    )

    answer = response.choices[0].message.content
    print(f"Time taken: {time() - start:.2f} seconds")
    return answer


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def askLlamaImg(system, image_path, model="gemini-2.5-flash"):
    start = time()

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }}
                ]
            }
        ],
        temperature=0,
        max_tokens=512
    )

    answer = response.choices[0].message.content
    print(f"Time taken: {time() - start:.2f} seconds")
    return answer

if __name__ == "__main__":
    answer = askLlama(
        system="You are a helpful assistant.",
        user="What's the capital of India?"
    )
    print(answer)