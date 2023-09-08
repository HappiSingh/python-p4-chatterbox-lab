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
        messages = Message.query.order_by(Message.created_at).all()
        messages_serialized = [message.to_dict() for message in messages]

        response = make_response(
            messages_serialized,
            200
        )
        return response
    

    elif request.method == 'POST':
        messages = Message.query.all()
        msg = request.get_json()
        new_message = Message(
            body=msg["body"],
            username=msg["username"],
        )
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            new_message_dict,
            201
        )
        return response

@app.route('/messages/<int:id>', methods=["PATCH","DELETE"])
def messages_by_id(id):
    
    message = Message.query.get(id)
    if request.method == "PATCH":
       msg = request.get_json()
       message.body = msg["body"]
       db.session.add(message)
       db.session.commit()

       message_serialized = message.to_dict()    
       response = make_response(message_serialized,200 )
       return response
    else:
       db.session.delete(message)
       db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
