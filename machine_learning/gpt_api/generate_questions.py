def generate_multiple_choice_questions_with_gpt(category, content, client):
    prompt = (
        f"I want you to generate 2 questions related to the category '{category}', and the content '{content}' "
        f"each with 3 multiple-choice options. The questions should be clear and concise. "
        f"Only include the questions themselves. "
        f"Please provide the output in a structured format:\n\n"
        f"1. Question 1?\n"
        f"a) Option 1\n"
        f"b) Option 2\n"
        f"e) Option 3\n\n"
        f"2. Question 2?\n"
        f"a) Option 1\n"
        f"b) Option 2\n"
        f"e) Option 3\n\n"
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-4o-mini",
        max_tokens=200, 
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def generate_related_questions(category, client, content):
    prompt = (
        f"Generate 2 open-ended questions related to the category '{category}' and content '{content}' "
        f"that would help us understand user preferences or needs. "
        f"Each question should be clear and engaging without providing multiple-choice options. "
        f"Please only return the questions. "
        f"Please return each question as a separate line.\n\n"
    )
    response = client.chat.completions.create(
        messages=[
            {'role':'user', 'content': prompt},
        ],
        model="gpt-4o-mini",
        max_tokens=200, 
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
