# This is a Mental Health Chatbot.

## Technology Stack

The Mental Health Chatbot project leverages the following technologies:

- **Python**: The primary programming language used for building the chatbot application.
- **Flask**: A lightweight web framework for hosting the chatbot and handling HTTP requests.
- **HuggingFace Transformers**: Used for natural language processing and deploying pre-trained models.
- **Twilio API**: Enables SMS-based interaction with the chatbot.
- **dotenv**: For managing environment variables securely.
- **Pytest**: A testing framework to ensure the reliability of the application.
- **HTML/CSS/JavaScript**: For creating the front-end interface of the chatbot (if applicable).

This combination of technologies ensures a robust, scalable, and user-friendly chatbot experience.

## Instructions to Run the Project

1. **Clone the Repository**:  
    Clone the repository to your local machine using the following command:
    ```bash
    git clone <repository-url>
    ```

2. **Navigate to the Project Directory**:  
    Change to the project directory:
    ```bash
    cd mentalhealth
    ```

3. **Install Dependencies**:  
    Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:  
    Create a `.env` file in the project directory and add the following variables:
    ```env
    HUGGINGFACE_MODEL_UPLOAD_KEY=<your-huggingface-api-key>
    TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
    TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
    ```

5. **Upload Model to HuggingFace**:  
    Use the provided script or instructions in the project to upload the model file to HuggingFace. Ensure the API key is correctly set in the `.env` file.

6. **Run the Application**:  
    Start the chatbot application:
    ```bash
    python app.py
    ```

7. **Access the Chatbot**:  
    Open your browser and navigate to the URL where the chatbot is hosted (e.g., `http://127.0.0.1:5000`).

8. **Interact with the Chatbot**:  
    Begin interacting with the chatbot to explore its features.

9. **Optional - Testing**:  
    Run tests to verify the application works as expected:
    ```bash
    pytest
    ```

Follow these steps to successfully run the Mental Health Chatbot project.

