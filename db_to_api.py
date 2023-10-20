from flask import Flask, request, redirect
import os
import psycopg2
import json
from flask_cors import CORS, cross_origin
from DatabasePostgresqlAWS import DatabasePostgresqlAWS
from recommendation import Recommendation

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
    os.chdir(cwd+'/test')
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
    os.chdir(cwd)
    return json_chat_list
    
@app.route('/customer', methods=['GET'])
@cross_origin()
def view_customer_chat():
    name = request.args.get('name')
    cwd = os.getcwd()
    print('Current working directory : ', cwd)
    # for file in os.listdir():
    os.chdir(cwd+'/test')      
    for file in os.listdir():
        print(file)
        print(name)
        if file.startswith(str(name)):
            print(1)
            chat_data = {}
            # print(file)
            chat_content = open(file, 'r').read()
            print(chat_content)
            
            chat_data['name'] = file.split('.')[0].split('_')[0]
            chat_data['date'] = file.split('.')[0].split('_')[1]
            chat_data['content'] = chat_content
            chat_data['filename'] = file
            print(json.dumps(chat_data))
            os.chdir(cwd)
            return json.dumps(chat_data) 
    else:
        print(json.dumps('Error : No chats found'))
        return json.dumps('Error : No chats found')

@app.route('/process', methods=['POST'])
@cross_origin()
def generate360():
    file_name = request.form.get('filename')
    recommend = Recommendation()
    customer_id = recommend.create_recommendation(file_name)
    return redirect(f'https://customerservice-j5wx.onrender.com/name?customer_id={customer_id}')



if __name__ == '__main__':
    app.run(debug=True,port=8001)
