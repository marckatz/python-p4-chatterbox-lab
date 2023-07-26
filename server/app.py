from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Messages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]
        response = make_response(
            messages, 
            200,
            {"Content-Type": "application/json"}
        )
        return response
    def post(self):
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(
            message_dict,
            201
        )
        return response

api.add_resource(Messages, '/messages')

class MessagesById(Resource):
    
    def patch(self, id):
        message = Message.query.filter(Message.id == id).first()
        for attr in request.get_json():
            setattr(message, attr, request.get_json()[attr])

        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(
            message_dict,
            200
        )
        return response

    def delete(self, id):    
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Message deleted."    
        }

        response = make_response(
            response_body,
            200
        )

        return response

api.add_resource(MessagesById, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
