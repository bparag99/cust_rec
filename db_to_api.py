from flask import Flask, request, jsonify

import psycopg2
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/name', methods=['GET'])
@cross_origin()
def getData():
    print('2')
    input_var = request.args.get('input_var')
    print('3')
    conn = psycopg2.connect(

    host='llm-vector-database.postgres.database.azure.com',

    dbname='postgres',

    user='llm_vector_database@llm-vector-database',

    password='Letmein@0987',

    sslmode='require'

    )
    print('4')
    cursor = conn.cursor()

    print(input_var)

    cursor.execute('SELECT * FROM customers WHERE customer_name LIKE %s;', ('%'+input_var+'%',))

    result = cursor.fetchall()

    conn.close()

    # Converting the query result to JSON
    print(len(result))
    response = [{
        'customer_id': row[0], 
        'Customer_Name': row[1], 
        'age': row[2],
        'gender': row[3], 
        'occupation': row[4], 
        'location': row[5],
        'travel_purpose': row[6], 
        'travel_duration': row[7], 
        'budget': row[8],
        'reservation_lead_time': row[9], 
        'room_type': row[10], 
        'amenities_availed': row[11],
        'discount': row[12], 
        'source_of_booking': row[13], 
        'transportation_requests': row[14],
        'final_price': row[15], 
        'background': row[16], 
        'goals': row[17],
        'challenges': row[18], 
        'persona_summary': row[19], 
        'customer_360': row[20],
        'additional_preferences': row[21]
        } for row in result] # Adjust column names as needed

    return jsonify(response)


if __name__ == '__main__':
    print('1')
    app.run(debug=True)
