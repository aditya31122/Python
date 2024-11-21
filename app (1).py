from flask import Flask, redirect, url_for, render_template, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_caching import Cache
import random
from patterns_database import employer_patterns, employee_patterns, preprocess_text
from chatbot import get_sub_option_response, get_employee_response, get_employer_response

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Variable to track user activity
user_active = False

# Timeout for inactivity (5 minutes)
INACTIVE_TIMEOUT = 5 * 60

def send_email(subject, body, to_email):
    from_email = "ad8892421@gmail.com"
    from_password = "password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    
@app.route('/send_support_email', methods=['POST'])
def send_support_email():
    chat_log = request.form.get('chat_log')
    if not chat_log:
        return jsonify({"message": "No chat log provided"}), 400

    supervisor_email = "adityabadhwar@gmail.com"
    subject = "Support Request from Chatbot"
    body = f"Chat log:<br><br>{chat_log}"

    if send_email(subject, body, supervisor_email):
        return jsonify({"message": "Support email sent successfully"}), 200
    else:
        return jsonify({"message": "Failed to send support email"}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_type = request.form.get('user_type', 'employer')  # Default to employer
        print("User type:", user_type)  # Print user type

        # Redirect to dashboard after login
        return redirect(url_for('dashboard', user_type=user_type))

    # Render the login form for GET requests
    return render_template('login.html')

@app.route('/dashboard/<user_type>')
def dashboard(user_type):
    return render_template('index.html', user_type=user_type)

@cache.memoize(timeout=3000)  # Cache the response for 50 minutes
def get_cached_response(user_message, user_type):
    # Mock function to return a response based on user type
    if user_type == 'employer':
        return get_employer_response(user_message)  #function to get employer responses
    elif user_type == 'employee':
        return get_employee_response(user_message)  #function to get employee responses

@app.route('/get_sub_option_response', methods=['POST'])
def option_response():
    option_number = request.form.get('option_number')    
    user_type = request.form.get('user_type', 'employer')  # Default to employer
    print("User type:", user_type)  # Print user type

    response = get_sub_option_response(user_type, option_number)

    return response

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    global user_active  # Use global variable

    print("Form data received:", request.form)  # Print form data
    user_message = request.form['user_message']
    user_type = request.form['user_type']   # Default to employer
    print("User type:", user_type)  # Print user type

    # Indicate that the user is typing
    print("User is typing...")

    # Reset the user activity timeout
    user_active = True

    # Get the response based on the user type
    response = get_cached_response(user_message, user_type)

    # Check if response is a list of strings, then choose one randomly
    if isinstance(response, list):
        response = random.choice(response)

    return response

@app.route('/user_typing', methods=['POST'])
def user_typing():
    global user_active  # Use global variable
    
    # This endpoint receives a POST request when the user starts typing
    print("User is typing...",)
    
    # Reset the user activity timeout
    user_active = True

    return "Typing indication received"


@app.before_request
def before_request():
    global user_active  # Use global variable

    # Check if user is inactive for INACTIVE_TIMEOUT seconds
    if not user_active:
        reset_chatbot()

    # Reset user activity flag
    user_active = False

def reset_chatbot():
   
    pass

if __name__ == '__main__':
    app.run(debug=True)