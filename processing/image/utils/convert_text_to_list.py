from dotenv import load_dotenv
import openai
import os
import json

load_dotenv()


def convert_text_to_list(sentence: str) -> dict:
    """
    Convert text to a json list.

    :param sentence: string representation of a sentence.
    :returns dict: a dictionary that represents the list needed.
    """
    bearer_token = os.getenv('CHAT_GPT_TOKEN')
    openai.api_key = bearer_token
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
                def get_to_do_lists_from_sentence(sentence):
                    return {
                        "list": [
                            {
                                "TaskId": 1
                                "Description": "to do 1 summary"
                            },
                            {
                                "TaskId": 2
                                "Description": "to do 2 summary"
                            },
                        ]
                    }
            """
             },
            {"role": "user", "content": "I want to wash my hair and dry my clothes and get dressed"},
            {"role": "system", "content": """
                    {
                        "list": [
                            {
                                "TaskId": 1
                                "Description": "Wash hair"
                            },
                            {
                                "TaskId": 2
                                "Description": "Dry clothes"
                            },
                            {
                                "TaskId": 3
                                "Description": "Get dressed"
                            },
                        ]
                    }
            """
             },
            {"role": "user", "content": f'{sentence}'},
        ]
    )

    try:
        generated_response = response['choices'][0]['message']['content']
        return json.loads(generated_response.strip())
    except Exception:
        raise TypeError("Invalid JSON response.")
