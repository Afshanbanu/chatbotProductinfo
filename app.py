from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)

class UnansweredQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_query = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = handle_user_input(user_input)
    return jsonify({'response': response})

def handle_user_input(user_input):
    if 'product' in user_input.lower():
        return "Sure, here's the information about our products."
    else:
        save_unanswered_query(user_input)
        return "I'm not sure about that. Let me get back to you later."

def save_unanswered_query(user_query):
    unanswered = UnansweredQuery(user_query=user_query)
    db.session.add(unanswered)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
