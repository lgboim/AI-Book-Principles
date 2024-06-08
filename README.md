# AI Book Principles

AI Book Principles is a web application designed to generate detailed knowledge cards based on principles from books. The application uses OpenAI's API to generate content and convert it into audio format for easy consumption. This project aims to provide a comprehensive learning experience by summarizing key book principles and offering voice narration.

## Features

- Generate detailed knowledge cards from book principles.
- Convert generated content into audio format.
- Responsive and modern UI design.
- Supports both English and Hebrew languages.
- Adjustable audio playback speed.
- Easy-to-navigate interface with a settings menu.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or later
- Node.js and npm (for frontend dependencies)
- An OpenAI API key

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ai-book-principles.git
    cd ai-book-principles
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install frontend dependencies:**
    ```bash
    npm install
    ```

5. **Set up the database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Set up environment variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=sqlite:///local_database.db
    ```

7. **Run the application:**
    ```bash
    flask run
    ```

### Usage

1. **Access the application:**
    Open your web browser and navigate to `http://localhost:5000`.

2. **Enter your OpenAI API key:**
    Provide your OpenAI API key to enable the application to generate content.

3. **Generate knowledge cards:**
    - Enter a subject to get book suggestions.
    - Choose a book and select a principle to generate a knowledge card.
    - Listen to the generated content using the built-in audio player.

### Project Structure

```
ai-book-principles/
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
├── migrations/
├── models.py
├── app.py
├── requirements.txt
└── README.md
```

### Contributing

To contribute to this project, follow these steps:

1. **Fork the repository:**
    Click the "Fork" button at the top right corner of the repository page.

2. **Clone your fork:**
    ```bash
    git clone https://github.com/your-username/ai-book-principles.git
    cd ai-book-principles
    ```

3. **Create a branch:**
    ```bash
    git checkout -b feature-branch
    ```

4. **Make your changes and commit them:**
    ```bash
    git commit -m "Add some feature"
    ```

5. **Push to your fork:**
    ```bash
    git push origin feature-branch
    ```

6. **Create a pull request:**
    Open your fork on GitHub and click the "New pull request" button.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgements

- [OpenAI](https://www.openai.com/) for providing the API to generate content and convert it into audio.
- [FontAwesome](https://fontawesome.com/) for the icons used in the project.

### Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.
