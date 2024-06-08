from flask import Flask, render_template, request, jsonify, url_for
from openai import OpenAI
import os
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Card  # Import the db instance and Card model from models.py

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///local_database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the db instance with the app
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest_books', methods=['POST'])
def suggest_books():
    data = request.json
    subject = data.get('subject')
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    api_key = api_key.split(' ')[1]

    client = OpenAI(api_key=api_key)

    prompt = f"Suggest a list of books on the subject '{subject}'. Provide just the titles in a comma-separated list. Just the list, No quotation marks or numbers."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        books = response.choices[0].message.content.split(', ')
        return jsonify({"books": books})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/suggest_principles', methods=['POST'])
def suggest_principles():
    data = request.json
    book_title = data.get('book_title')
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    api_key = api_key.split(' ')[1]

    # Check if principles for the given book title already exist in the database
    existing_principles = db.session.query(Card.principle).filter_by(book_title=book_title).distinct().all()

    if existing_principles:
        principles = [principle[0] for principle in existing_principles]
        return jsonify({"principles": principles})

    client = OpenAI(api_key=api_key)

    prompt = f"Suggest a list of principles from the book '{book_title}'. Provide just the principles in a comma-separated list. Just the list, No quotation marks or numbers."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        principles = response.choices[0].message.content.split(', ')

        # Save principles to the database as placeholders
        for principle in principles:
            new_card = Card(book_title=book_title, principle=principle, content="", language=data.get('language', 'en'))
            db.session.add(new_card)
        db.session.commit()

        return jsonify({"principles": principles})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    book_title = data.get('book_title')
    principle = data.get('principle')
    language = data.get('language', 'en')
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    api_key = api_key.split(' ')[1]

    try:
        app.logger.info(f"Generating card for book: {book_title}, principle: {principle}, language: {language}")

        existing_card = Card.query.filter_by(book_title=book_title, principle=principle, language=language).first()
        if existing_card and existing_card.content:
            app.logger.info("Card found in database, returning existing card.")
            return jsonify({"sections": [section for section in existing_card.content.split("\n\n") if section.strip()]})

        client = OpenAI(api_key=api_key)

        if language == 'he':
            prompt = f"""צור כרטיס מידע מפורט ותמציתי עבור העקרון "{principle}" מתוך הספר "{book_title}". כלול חלקים: מידע מפתיע, מושג, תובנה מרכזית, קטליזטור חדשנות, תוכנית פעולה, ספר משחקים אמיתי, מלכודות נפוצות, סיכום מהיר, והצהרת השפעה. אל תקרא לזה בשמות הללו, השתמש בכותרות משמעותיות שמסכמות את הכרטיס. שים נקודה בסוף כותרות. וודא שכל כרטיס הוא עצמאי וברור, ומספק מספיק פרטים כדי שהקורא יוכל להבין וליישם את העקרון."""
        else:
            prompt = f"""Generate a detailed and concise knowledge card for the principle "{principle}" from the book "{book_title}". Include sections: Surprising Info, Concept, Key Insight, Innovation Catalyst, Action Plan, Real-World Playbook, Common Pitfalls, Quick Recap, and Impact Statement. add Period at the end of titles. Not call it in this names, use meaningful titles that sum the card. Ensure each card is self-contained and clear, providing enough detail for a reader to understand and apply the principle. Generate in English."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        card_content = response.choices[0].message.content.strip()
        if not card_content:
            return jsonify({"error": "Generated content is empty."}), 400

        card_sections = [section for section in card_content.split("\n\n") if section.strip()]

        if card_sections:
            if existing_card:
                existing_card.content = "\n\n".join(card_sections)
            else:
                new_card = Card(book_title=book_title, principle=principle, content="\n\n".join(card_sections), language=language)
                db.session.add(new_card)
            db.session.commit()

        return jsonify({"sections": card_sections})

    except Exception as e:
        app.logger.error(f"Error generating card: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    texts = data.get('texts', [])
    language = data.get('language', 'en')
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    api_key = api_key.split(' ')[1]

    client = OpenAI(api_key=api_key)
    audio_urls = []

    for text in texts:
        if not text.strip():
            app.logger.info("Skipping empty text.")
            continue

        try:
            existing_card = Card.query.filter_by(content=text, language=language).first()
            if existing_card and existing_card.audio_path:
                audio_urls.append(url_for('static', filename=existing_card.audio_path, _external=True))
                continue

            file_id = str(uuid.uuid4())
            file_name = f'output_{file_id}.mp3'
            file_path = os.path.join(app.static_folder, file_name)

            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=text,
            )

            if not os.path.exists(app.static_folder):
                os.makedirs(app.static_folder)

            with open(file_path, 'wb') as audio_file:
                audio_file.write(response.content)

            if existing_card:
                existing_card.audio_path = file_name
                db.session.commit()
            else:
                new_card = Card(book_title="Unknown", principle="Unknown", content=text, language=language, audio_path=file_name)
                db.session.add(new_card)
                db.session.commit()

            audio_urls.append(url_for('static', filename=file_name, _external=True))

        except Exception as e:
            app.logger.error(f"Error generating TTS for text: {text} - {str(e)}")

    return jsonify({"urls": audio_urls})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
