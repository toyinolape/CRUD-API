from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main___':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URL'] = os.environ.get(DATABASE_URL)
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eng_text = db.Column(db.String(120), unique=False, nullable=False)
    lang = db.Column(db.String(120), unique=False, nullable=False)
    lang_text = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self, eng_text,lang,lang_text):
        self.eng_text = eng_text
        self.lang =  lang
        self.lang_text = lang_text

    db.create_all()

    @app.route('/items/<id>', methods=['GET'])
    def get_item(id):
        item = Item.query.get(id)
        del item.__dict__['sa_instance_state']
        return jsonify(item.__dict__)

    @app.route('/items', methods=['GET'])
    def get_items():
        items = []
        for item in db.session.query(Item).all():
            del item.__dict__['_sa_instance_state']
            items.append(item.__dict__)
            return jsonify(items)

    @app.route('/items', methods=['POST'])
    def create_item():
        body = request.get_json()
        db.session.add(Item(body['eng_text'], body['lang'], body['lang_text']))
        db.session.commit()
        return 'item is created'

    @app.route('/items/<id>', methods=['PUT'])
    def update_item(id):
        body = request.get_json()
        db.session.query(Item).filter_by(id=id).update(
            dict(eng_text=body['eng_text'],lang=body['lang'], lang_text=body['lang_text'])
        )
        db.session.commit()
        return 'item updated'
    @app.route('/items/<id>', methods=['DELETE'])
    def delete_item(id):
        db.session.query(Item).flter_by(id=id).delete()
        db.session.commit()
        return 'item deleted'


