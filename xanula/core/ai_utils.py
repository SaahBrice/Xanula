import os
import anthropic

#client = anthropic.Client('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')
client = anthropic.Client(api_key='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')

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