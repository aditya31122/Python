import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Patterns for employer
employer_patterns = [
    (r'option 1.1', ['As an employer,Your remaining EMI is ₹15000.']),
    (r'option 1.2', ['As an employer,AI is advancing rapidly and has many applications in various fields.']),
    (r'option 1.3', ['As an employer,You can apply']),

    (r'option 2.1', ['As an employer,2.1']),
    (r'option 2.2', ['As an employer,2.2']),
    (r'option 2.3', ['As an employer,2.3']),
    (r'option 2.4', ['As an employer,2.4']),


    (r'option 3.1', ['As an employer,3.1']),
    (r'option 3.2', ['As an employer,3.2.']),
    (r'option 3.3', ['As an employer,3.3']),
    (r'option 3.4', ['As an employer,3.4']),
    

    (r'remaining emi|emi', ['As an employer, you can check the remaining EMI by contacting our finance department.']),
    (r'month left', ['As an employer, you can check the remaining months by contacting our finance department.']),
    (r'emi per month', ['As an employer, you can check the EMI per month by contacting our finance department.']),

    (r'ai', ['you can learn about AI advancements from our research and development team.']),
    (r'ai working', ['you can learn about AI working principles from our AI experts.']),
    (r'what is it', [' you can explore more about AI by attending our workshops.']),
    
    
    (r'apply', ['you can apply for business loans through our finance department.']),
    (r'how can i apply', ['you can learn how to apply for business loans by contacting our finance department.']),
    (r'where', ['you can find loan application forms at our finance department.']),
    
    (r'hi|hello|hey', ['Hello!', 'Hey there!', 'Hi!']),
    (r'what is ai', ['AI, also known as artificial intelligence, is the simulation of human intelligence processes by machines, especially computer systems.']),
    (r'goodbye|bye|quit', ['Bye, take care!', 'Goodbye, have a great day!']),
    (r'whats the weather', ['It is sunny outside']),
    (r'how are you|how r u |how are u|how r you', ['I am fine, thanks for asking']),
    (r'what is finance wellbeing\??', ['Financial well-being means how much your financial situation and money choices provide you with security and freedom of choice']),
    (r'what is finance', ['Finance is the study and discipline of money, currency, and capital assets. It is related to and distinct from Economics, which is the study of production, distribution, and consumption of goods and services.'])
]

# Patterns for employee
employee_patterns = [
    (r'option 1.1', ['Your remaining EMI is ₹15000.']),
    (r'option 1.2', ['AI is advancing rapidly and has many applications in various fields.']),
    (r'option 1.3', ['You can apply']),

    (r'option 2.1', ['2.1']),
    (r'option 2.2', ['2.2']),
    (r'option 2.3', ['2.3']),
    (r'option 2.4', ['2.4']),    

    (r'option 3.1', ['3.1']),
    (r'option 3.2', ['3.2.']),
    (r'option 3.3', ['3.3']),
    (r'option 3.4', ['3.4']),

    (r'remaining emi|emi', ['Your remaining EMI is ₹8000.']),
    (r'month left', ['You have 3 months left to complete your EMI payments.']),
    (r'emi per month', ['Your remaining EMI per month is ₹5000.']),
    
    (r'ai', ['AI is advancing rapidly and has many applications in various fields.']),
    (r'ai working', ['NLP']),
    (r'what is it', ['Artificial human brain']),
    
    (r'how to apply', ['You can learn how to apply for loans from our customer service representatives.']),
    (r'where', ['You can find loan application forms online or at our branch offices.']),
    (r'hi|hello|hey', ['Hello!', 'Hey there!', 'Hi!']),
    (r'what is ai', ['AI, also known as artificial intelligence, is the simulation of human intelligence processes by machines, especially computer systems.']),
    (r'goodbye|bye|quit', ['Bye, take care!', 'Goodbye, have a great day!']),
    (r'whats the weather', ['It is sunny outside']),
    (r'how are you', ['I am fine, thanks for asking']),
    (r'what is finance wellbeing\??', ['Financial well-being means how much your financial situation and money choices provide you with security and freedom of choice']),
    (r'what is finance', ['Finance is the study and discipline of money, currency, and capital assets. It is related to and distinct from Economics, which is the study of production, distribution, and consumption of goods and services.'])
]



stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

CACHE_MAX_SIZE = 1000
CACHE_TIMEOUT_SECONDS = 3600  #1 hour

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Lowercase the text
    text = lemmatizer.lemmatize(text)  # Lemmatize the text
    return text 
