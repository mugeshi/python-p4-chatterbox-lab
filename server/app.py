from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Get all messages ordered by created_at in ascending order
        messages = Message.query.order_by(Message.created_at.asc()).all()
        message_list = [{'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at} for message in messages]
        return jsonify(message_list)
    elif request.method == 'POST':
        # Create a new message with data from the request
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message created successfully!'}), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'}), 404

    if request.method == 'PATCH':
        # Update the body of the message
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify({'message': 'Message updated successfully!'})
    elif request.method == 'DELETE':
        # Delete the message
        db.session.delete(message)
        db.session.commit()
        
if __name__ == '__main__':
    app.run(port=5555)
