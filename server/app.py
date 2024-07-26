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
        messages_by_ascending = [messages.to_dict() for messages in Message.query.order_by(Message.created_at.asc()).all()]

        return make_response( messages_by_ascending, 200 )
    
    elif request.method == 'POST':
        message_data = request.get_json()
        username = message_data.get("username")
        body = message_data.get("body")

        new_message = Message(
            body= body,
            username= username,
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(jsonify(new_message.to_dict()), 201)


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    if request.method == 'PATCH':
        message_data = request.get_json()
        if "username" in message_data:
            message.username = message_data["username"]
        if "body" in message_data:
            message.body = message_data["body"]

        db.session.add(message)
        db.session.commit()

        return make_response(jsonify(message.to_dict()), 200)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit

        return make_response({"delete_successful": True, "message": "Message deleted"}, 200)

if __name__ == '__main__':
    app.run(port=5555)
