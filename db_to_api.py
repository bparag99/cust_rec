from flask import Flask, request, jsonify

import psycopg2
from flask_cors import CORS, cross_origin
from DatabasePostgresqlAWS import DatabasePostgresqlAWS
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/name', methods=['GET'])
@cross_origin()
def fetch_customers():
    customer_id = request.args.get('customer_id')
    databaseAWS = DatabasePostgresqlAWS()
    customer_df = databaseAWS.retrieve_segmented_customer(customer_id)
    print(customer_df)
    json = customer_df.to_json(orient='table', index=False)
    # Print json object
    print(json)

    return json

if __name__ == '__main__':
    app.run(debug=True,port=8001)
