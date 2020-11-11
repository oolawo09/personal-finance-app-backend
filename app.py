#!flask/bin/python
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

debts = [
            {
                'id': '1',
                'description': u'Friday night drinks',
                'fulfilled': False,
                'debtor_id': '2',
                'creditor_id': '3',
            },

            {
                'id': '4',
                'description': u'Brunch',
                'fulfilled': False,
                'debtor_id': '3',
                'creditor_id': '2',
            }
        ]

@app.route('/x/api/v1.0/debts', methods=['GET'])
def get_debts():
    return jsonify({'debts': debts})

@app.route('/x/api/v1.0/debts/<int:debt_id>', methods=['GET'])
def get_debt(debt_id):
    # TODO: figure out why this throws an error 404 unexpectedly
    debt = [debt for debt in debts if debt['id'] == debt_id]
    if len(debt) == 0:
        abort(404)
    return jsonify({'debt': debt})

@app.route('/')
def index():
    return "Hello, World!"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
