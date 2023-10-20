from flask import Flask, request, jsonify
import os
import psycopg2
import json
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
@app.route('/chats', methods=['GET'])
@cross_origin()
def find_all_chats():  
    cwd = os.getcwd()
    print('Current working directory : ', cwd)
    # for file in os.listdir():
    os.chdir(path)
    chat_list = os.listdir()
    # print(chat_list)
    json_list = []
    for i in chat_list:
        name_date = {}
        name_date['name'] = i.split('.')[0].split('_')[0]
        name_date['date'] = i.split('.')[0].split('_')[1]
        json_list.append(name_date)
        # print(name_date)
    json_chat_list = json.dumps(json_list)
    print(json_chat_list)
    return json_chat_list
if __name__ == '__main__':
    app.run(debug=True,port=8001)
