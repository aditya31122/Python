import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from patterns_database import employer_patterns, employee_patterns, preprocess_text

# Preprocessing patterns and responses separately for employer and employee
preprocessed_employer_patterns = [preprocess_text(pattern) for pattern, _ in employer_patterns]
employer_responses = [response for _, response in employer_patterns]

preprocessed_employee_patterns = [preprocess_text(pattern) for pattern, _ in employee_patterns]
employee_responses = [response for _, response in employee_patterns]

# Vectorizing preprocessed text for employer and employee
employer_vectorizer = TfidfVectorizer()
employee_vectorizer = TfidfVectorizer()

employer_vectorized_patterns = employer_vectorizer.fit_transform(preprocessed_employer_patterns)
employee_vectorized_patterns = employee_vectorizer.fit_transform(preprocessed_employee_patterns)

# Function to find the most similar pattern index for employer and employee
def get_most_similar_index(vectorizer, vectorized_patterns, message):
    preprocessed_message = preprocess_text(message)
    if not preprocessed_message:
        return None
    vectorized_message = vectorizer.transform([preprocessed_message])
    similarities = cosine_similarity(vectorized_message, vectorized_patterns)
    most_similar_index = similarities.argmax()
    return most_similar_index

def get_response(vectorizer, vectorized_patterns, responses, message):
    preprocessed_message = preprocess_text(message)
    if not preprocessed_message:
        return "Sorry, I didn't understand that."
    

    vectorized_message = vectorizer.transform([preprocessed_message])
    similarities = cosine_similarity(vectorized_message, vectorized_patterns)
    most_similar_index = similarities.argmax()

    for i, response in enumerate(responses):
        if i == most_similar_index:
            return random.choice(response) # Return the first element of the response tuple

    return "Sorry, I don't have a response for that."

def get_employer_response(message):
    return get_response(employer_vectorizer,  employer_vectorized_patterns, employer_responses, message)

def get_employee_response(message):
    return get_response(employee_vectorizer, employee_vectorized_patterns, employee_responses, message)

def get_sub_option_response(user_type, option_number):
    """Return the appropriate response for the given user type and option number."""
    option_number = str(option_number)  # Ensure option_number is a string
    if user_type == "employee":  
        for pattern, response in employee_patterns:
            if pattern.lower() == f"option {option_number}":
                return response
    elif user_type == "employer":
        for pattern, response in employer_patterns:
            if pattern.lower() == f"option {option_number}":
                return response
    return "Sorry, I don't have a response for that option."


def get_employer_pattern_response(pattern_number):
    if pattern_number < len(employer_responses):
        return employer_responses[pattern_number]
    else:
        return "Pattern not found."

def get_employee_pattern_response(pattern_number):
    if pattern_number < len(employee_responses):
        return employee_responses[pattern_number]
    else:
        return "Pattern not found."

if __name__ == "__main__":
    print("Bot: Hi there! I'm Aida. How can I assist you today?")
    
    #user type is obtained from login
    user_type = ""
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit' or user_input.lower() == 'bye':
            print("Bot: Bye, take care!")
            break
        
        if user_type == 'employer':
            response = get_employer_response(user_input)
            print("Bot:", response)
            
        elif user_input.lower() == 'option':
            print("Bot: Please specify the option number you want to select.")
            print("Available options:")
            options = {'1': 'EMI', '2': 'How is AI', '3': 'Can I apply for loan'}
            for i in range(1, 4):
                print(f"{i}. {options[str(i)]}")

        elif user_input.lower().startswith('option') and len(user_input.split()) > 1:
            option_number = user_input.split()[1]
            response = get_sub_option_response(option_number)
            print("Bot:", response)
            
        elif user_type == 'employee':
            response = get_employee_response(user_input)
            print("Bot:", response)