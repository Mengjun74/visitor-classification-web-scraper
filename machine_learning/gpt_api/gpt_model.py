initial = """
        "Given the following website content, classify it into a category. "
        "Provide only the category name without any reasoning or explanation. "
        "Content: '{}'"
"""

def llm_response(initial_prompt = initial, content = None, client = None):
    response = client.chat.completions.create(
    messages=[
        {"role":"system", "content": initial_prompt},
        {"role": "user", "content": f"Classify the following content: {content}"},
    ],
    model="gpt-4o-mini",
    max_tokens=50, 
    temperature=0.5
    )
    return response.choices[0].message.content.strip()