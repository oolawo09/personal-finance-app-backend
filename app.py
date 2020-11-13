#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

import models # doing this here to avoid import errors. models need db obj

#TODO: add individual URI
debts = [
            {
                'id': 1,
                'description': u'Friday night drinks',
                'fulfilled': False,
                'debtor_id': '2',
                'creditor_id': '3',
            },

            {
                'id': 4,
                'description': u'Brunch',
                'fulfilled': False,
                'debtor_id': '3',
                'creditor_id': '2',
            }
        ]

def make_public(debt):
    new_debt = {}
    for field in debt:
        if field == 'id':
            new_debt['url'] = url_for('get_debt', debt_id=debt['id'],
                    _external=True)
        else:
            new_debt[field] = debt[field]
    return new_debt

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@auth.verify_password
def verify_password(username_or_token):
    user = User.verify_auth_token(username_or_token)
    g.user = user 
    return True

@app.route('/x/api/v1.0/debts', methods=['GET'])
def get_debts():
    return jsonify({'debts': [make_public(debt) for debt in debts]})

@app.route('/x/api/v1.0/debts/<int:debt_id>', methods=['GET'])
def get_debt(debt_id):
    # TODO: figure out why this throws an error 404 unexpectedly
    debt = [debt for debt in debts if debt['id'] == debt_id]
    if len(debt) == 0:
        abort(404)
    return jsonify({'debt': make_public(debt[0])})

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/x/api/v1/debts/', methods=['POST'])
def create_debt():
    if not request.json or not description in request.json \
        or not debtor_id in request.json or not creditor_id in request.json \
            or not fulfilled in request.json:
                abort(400)
    debt = {
            'id': debts[-1]['id'] + 1,
            'description': request.json['description'],
            'fulfilled': request.json['fulfilled'],
            'debtor_id': request.json['debtor_id'],
            'creditor_id': request.json['creditor_id']
            }

    debts.append(debt)
    return jsonify({'debt': make_public(debt)}), 201

@app.route('/x/api/v1/debts/<int:debt_id>', methods=['PUT'])
def update_debt(debt_id):
    debt = [debt for debt in debts if debt['id'] == debt_id]
    if len(debt) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'fulfilled' in request.json and type(request.json['fulfilled']) \
            is not bool:
                abort(400)

    debt[0]['fulfilled'] = request.json.get('fulfilled', debt[0]['fulfilled'])

    return jsonify({'debt': debt[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
