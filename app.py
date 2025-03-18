# import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from huggingface_hub import InferenceClient
from twilio.rest import Client


# App Configuration
app = Flask(__name__, template_folder="./templates")
app.config["SECRET_KEY"] = "mysecretkey"  # Secure session data
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # SQLite Database URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking

# Initialize Extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect to login if unauthenticated


# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.Numeric(10), nullable=False)


# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Initialize Hugging Face Client (Replace with actual model you want to use)
HF_TOKEN = "YOUR_TOKEN_HERE"
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)


# Utility function to generate initial chatbot message
def generate_initial_message():
    return (
        "Welcome to Mental Health Support. I'm here to listen and provide compassionate support. "
        "Feel free to share your thoughts or concerns, and I'll do my best to help you."
    )


# Function to handle the query using the model (Hugging Face)
def get_model_response(query):
    prompt = f"You are a compassionate mental health assistant. Respond empathetically to the user's query:\n\nUser query: {query}"
    messages = [{"role": "user", "content": prompt}]
    response_content = client.chat_completion(
        messages=messages, max_tokens=2000, stream=False
    )
    response = response_content.choices[0].message.content.strip()
    return response


def check_for_suicide_thoughts(text):
    suicide_keywords = [
        "suicide",
        "death",
        "kill",
        "die",
        "cutting",
        "self-injury",
        "self-harm",
        "burning",
        "overdose",
        "poison",
        "harm",
        "suicidal",
        "end it all",
        "no reason to live",
        "want to die",
        "take my life",
        "feel like dying",
        "pills",
        "guns",
        "rope",
        "hanging",
        "jump",
        "bridge",
        "knife",
        "sleeping pills",
        "goodbye",
    ]

    # check if text contains any of the suicode keywords
    for keyword in suicide_keywords:
        if keyword in text.lower():
            return True
    return False


def send_text_message(user_query, user_phone):
    # Twilio credentials (replace with your actual credentials)
    ACCOUNT_SID = "ACCOUNT-SID"
    AUTH_TOKEN = "AUTH-TOKEN"
    TWILIO_PHONE = "TWILLIO_PHONE"
    x = f"+91{user_phone}"
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Prepare the message content
    message = (
        f"!!!!! THIS IS AN EMERGENCY !!!!!\n"
        f"Hello, the user {current_user.username} sent the following message to Dhyana AI:\n"
        f'"{user_query}"\n'
        f"This message seems to indicate suicidal thoughts. Please contact the user immediately."
    )
    print(x)
    try:
        # Send the SMS
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=x,  # Ensure the phone number is in E.164 format
        )
        print("[INFO] SMS sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send SMS: {e}")


# Route for Home Page
@app.route("/")
@login_required
def home():
    return redirect(url_for("chatbot"))


# About
@app.route("/about")
@login_required
def about():
    return render_template("about.html")


# feedback
@app.route("/feedback")
@login_required
def feedback():
    return render_template("feedback.html")


# faq
@app.route("/faq")
@login_required
def faq():
    return render_template("faq.html")


# crisis
@app.route("/crisis")
@login_required
def crisis():
    return render_template("crisis.html")


# educationalsupport
@app.route("/educationalsupport")
@login_required
def educationalsupport():
    return render_template("educationalsupport.html")


# features
@app.route("/features")
@login_required
def features():
    return render_template("features.html")


# Route for Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("chatbot"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


# Route for Sign Up Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        phone = request.form["phone"]

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("signup"))

        # Hash the password before saving
        hashed_password = generate_password_hash(password, method="scrypt")

        # Create and save the new user
        new_user = User(username=username, password=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        flash("Sign up successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# Route for Logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    # Clear session data before logging out
    session.pop("chat_history", None)  # Remove chat history from session
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# Route for Chatbot Page
@app.route("/chatbot", methods=["GET", "POST"])
@login_required
def chatbot():
    if "chat_history" not in session:
        session["chat_history"] = [
            {"role": "bot", "content": generate_initial_message()}
        ]

    # Handle "Clear Chat History" button
    if request.method == "POST" and "clear_history" in request.form:
        session["chat_history"] = [
            {"role": "bot", "content": generate_initial_message()}
        ]
        session.modified = True
        return render_template("chatbot.html", chat_history=session["chat_history"])

    # Handle user message
    if request.method == "POST" and "user_message" in request.form:
        user_message = request.form["user_message"]

        session["chat_history"].append({"role": "user", "content": user_message})
        session.modified = True

        # Check for suicidal thoughts

        if check_for_suicide_thoughts(user_message):
            phone = int(current_user.phone)
            print(phone)
            send_text_message(user_message, phone)
            return render_template(
                "chatbot.html", chat_history=session["chat_history"], chat_disabled=True
            )

        try:
            bot_response = get_model_response(
                user_message
            )  # Get response from the model
        except Exception as e:
            print(f"[ERROR] Error querying the model: {e}")
            bot_response = "I'm here to support you. Could you rephrase your question?"

        session["chat_history"].append(
            {
                "role": "bot",
                "content": bot_response or "I'm here to listen. Tell me more.",
            }
        )
        session.modified = True

    return render_template(
        "chatbot.html", chat_history=session["chat_history"], chat_disabled=False
    )


# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5001, debug=False)
