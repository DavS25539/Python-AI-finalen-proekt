import os
import re
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _extract_rating(text):
    """
    Safely extract first number from a string like:
    '7', '7/10', 'Rating: 7 out of 10'
    """
    matches = re.findall(r"\d+", text)
    if matches:
        return int(matches[0])
    return 0


def _generate_with_retry(prompt, model="gemini-3-flash-preview", retries=3, delay=1.5):
    last_error = None

    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=prompt
            )
        except Exception as e:
            last_error = e
            time.sleep(delay)

    raise last_error


def generate_ai(argument, side):
    opposite = "against" if side == "for" else "for"

    prompt = f"""
You are a debate assistant.

User side: {side}
User argument: {argument}

Please provide:
1. A counter-argument from the {opposite} side.
2. A numeric rating from 1 to 10 (NUMBER ONLY).
3. One short feedback sentence.

Format your response EXACTLY like this:
COUNTER: ...
RATING: ...
FEEDBACK: ...
"""

    try:
        response = _generate_with_retry(prompt)

        text = response.text.strip()

        counter = text.split("COUNTER:")[1].split("RATING:")[0].strip()
        rating_val = text.split("RATING:")[1].split("FEEDBACK:")[0].strip()
        feedback = text.split("FEEDBACK:")[1].strip()

        rating = _extract_rating(rating_val)

        return counter, feedback, rating

    except Exception:
        return (
            "The AI is currently busy.",
            "Servers are overloaded. Please try again in a moment.",
            0
        )


def generate_counter_ai(original_argument, user_counter):
    prompt = f"""
You are a debate judge.

Original argument:
{original_argument}

User counter argument:
{user_counter}

Provide:
1. Short response to the counter argument.
2. Rating from 1 to 10 (NUMBER ONLY).
3. One feedback sentence.

Format EXACTLY:
REPLY: ...
RATING: ...
FEEDBACK: ...
"""

    try:
        response = _generate_with_retry(prompt)

        text = response.text.strip()

        reply = text.split("REPLY:")[1].split("RATING:")[0].strip()
        rating_val = text.split("RATING:")[1].split("FEEDBACK:")[0].strip()
        feedback = text.split("FEEDBACK:")[1].strip()

        rating = _extract_rating(rating_val)

        return reply, feedback, rating

    except Exception:
        return (
            "The AI is currently busy.",
            "Servers are overloaded. Please try again in a moment.",
            0
        )

# wdd