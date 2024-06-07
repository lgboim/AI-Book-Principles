# Book principles generator

A Flask web application to generate and read knowledge cards about books and their principles using OpenAI's API. This application helps users explore book recommendations, select principles, and generate detailed knowledge cards that can be read aloud.

## Features

- Fetch book suggestions based on a given subject.
- Select principles from a chosen book.
- Generate detailed knowledge cards for the selected principles.
- Read generated knowledge cards using text-to-speech.

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key

## Getting Started

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/AI-Book-Principles.git
    cd knowledge-card-generator
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate  # On Windows
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key**:
   Replace `your-api-key` with your actual OpenAI API key.
    ```sh
    export OPENAI_API_KEY=your-api-key  # On Linux/Mac
    set OPENAI_API_KEY=your-api-key  # On Windows
    ```

### Usage

1. **Run the Flask application**:
    ```sh
    python cards.py
    ```

2. **Open your web browser and navigate to**:
    ```
    http://127.0.0.1:5000/
    ```

3. **Use the application**:
    - Enter your OpenAI API key.
    - Enter a subject to get book suggestions.
    - Select a book and then select a principle.
    - Generate and read the cards.

### Deployment

To deploy this application on Heroku, follow these steps:

1. **Login to Heroku**:
    ```sh
    heroku login
    ```

2. **Create a new Heroku app**:
    ```sh
    heroku create your-app-name
    ```

3. **Deploy the application**:
    ```sh
    git push heroku master
    ```

4. **Set your OpenAI API key on Heroku**:
    ```sh
    heroku config:set OPENAI_API_KEY=your-api-key
    ```

5. **Open your Heroku app**:
    ```sh
    heroku open
    ```

### File Structure

