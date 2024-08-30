import os
import anthropic


client = anthropic.Client(api_key='your api key')

def get_ai_explanation(question, correct_answer, user_answer):

    prompt = (
        "\n\nHuman: Explain very basicly and simply why this answer to the question is correct, refering to me as you. the text reply you sent me should just be made up of the explanation. straight to the point "
        "Use very simple language:\n\n"
        f"Question: {question}\n"
        f"Correct answer: {correct_answer}\n"
        f"User's answer: {user_answer}\n\n"
        "Assistant:"
    )


    response = client.completions.create(
        prompt=prompt,
        model="claude-2.0",
        max_tokens_to_sample=150,
        temperature=0.7,
    )
    
    return response.completion.strip()
