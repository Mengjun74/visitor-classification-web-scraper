def generate_multiple_choice_questions_with_gpt(category, content, client):
    prompt = (
        f"I want you to generate 2 questions related to the category '{category}', and the content '{content}' "
        f"each with 3 multiple-choice options. The questions should be clear and concise. "
        f"that would help us understand user preferences or needs. "
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
    output = response.choices[0].message.content.strip()
    return parse_questions(output)

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
    output = response.choices[0].message.content.strip()
    return parse_related_questions(output)

def parse_questions(input_string):
    # Split the input string into individual questions based on the double newline character
    questions = input_string.strip().split('\n\n')
    
    # Initialize an empty list to store the result
    result = []

    for question in questions:
        # Split the question into lines
        lines = question.split('\n')
        
        # The first line is the question, the rest are options
        question_text = lines[0]
        options = [line[3:].strip() for line in lines[1:]]  # Skip the option labels (e.g., "a) ")
        
        # Append the question and its options to the result list
        result.append({
            "question": question_text,
            "options": options
        })

    return result

def parse_related_questions(input_string):
    # Split the input string into individual questions based on the double newline character
    questions = input_string.strip().split('\n\n')
    
    # Create a list to store the questions as dictionaries
    result = []
    
    # Loop through the questions and add them to the result list
    for question in questions:
        result.append({"question": question.strip()})  # Create a dictionary for each question
        
    return result