from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import uuid
from models import db, Card

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest_books', methods=['POST'])
def suggest_books():
    data = request.json
    subject = data.get('subject')
    api_key = request.headers.get('Authorization').split(' ')[1] if 'Authorization' in request.headers else None

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    client = OpenAI(api_key=api_key)

    prompt = f"Suggest a list of books on the subject '{subject}'. Provide just the titles in a comma-separated list."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    books = response.choices[0].message.content.split(', ')
    return jsonify({"books": books})

@app.route('/suggest_principles', methods=['POST'])
def suggest_principles():
    data = request.json
    book_title = data.get('book_title')
    api_key = request.headers.get('Authorization').split(' ')[1] if 'Authorization' in request.headers else None

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    client = OpenAI(api_key=api_key)

    prompt = f"Suggest a list of principles from the book '{book_title}'. Provide just the principles in a comma-separated list."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    principles = response.choices[0].message.content.split(', ')
    return jsonify({"principles": principles})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    book_title = data.get('book_title')
    principle = data.get('principle')
    api_key = request.headers.get('Authorization').split(' ')[1] if 'Authorization' in request.headers else None

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    # Check if the card already exists in the database
    existing_card = Card.query.filter_by(book_title=book_title, principle=principle).first()
    if existing_card:
        return jsonify({"sections": existing_card.content.split("\n\n")})

    client = OpenAI(api_key=api_key)

    prompt = f"""Generate a detailed and concise knowledge card for the principle "{principle}" from the book "{book_title}". Include sections: Surprising Info, Concept, Key Insight, Innovation Catalyst, Action Plan, Real-World Playbook, Common Pitfalls, Quick Recap, and Impact Statement. Ensure each card is self-contained and clear, providing enough detail for a reader to understand and apply the principle."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    card_content = response.choices[0].message.content
    card_sections = card_content.split("\n\n")

    # Save the new card to the database
    new_card = Card(book_title=book_title, principle=principle, content=card_content)
    db.session.add(new_card)
    db.session.commit()
    
    return jsonify({"sections": card_sections})

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    api_key = request.headers.get('Authorization').split(' ')[1] if 'Authorization' in request.headers else None

    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    client = OpenAI(api_key=api_key)

    # Check if the audio already exists in the database
    existing_card = Card.query.filter_by(content=text).first()
    if existing_card and existing_card.audio_path:
        return jsonify({"url": existing_card.audio_path})

    file_id = str(uuid.uuid4())
    file_path = os.path.join('static', f'output_{file_id}.mp3')

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    # Handle the response content
    with open(file_path, 'wb') as audio_file:
        audio_file.write(response.content)

    # Update the card with the audio path
    if existing_card:
        existing_card.audio_path = file_path
        db.session.commit()
    else:
        new_card = Card(book_title="Unknown", principle="Unknown", content=text, audio_path=file_path)
        db.session.add(new_card)
        db.session.commit()

    return jsonify({"url": file_path})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
