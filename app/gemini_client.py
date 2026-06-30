import google.generativeai as genai

from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(system_prompt, user_prompt):

    response = model.generate_content(
        [
            system_prompt,
            user_prompt
        ]
    )

    return response.text