# Database
import psycopg2
import pandas as pd
from pgvector.psycopg2 import register_vector

class DatabasePostgresqlAWS:

    db_conn = psycopg2.connect(
        host = 'genai-postgres-db.cbqq6u5jkrks.us-east-2.rds.amazonaws.com',
        dbname = 'genaidb',
        user = 'postgres',
        password = 'genai-rds',
        sslmode = 'require'   
        )
    # Day 0 : Profile insertion to customer_persona_tbl 
    def persona_insertion(self,persona_df):
        cursor = self.db_conn.cursor()# Create a list of tupples from the dataframe values
        for index,row in persona_df.iterrows(): 
            cursor.execute(""" 
                        INSERT INTO CUSTOMERS.customer_persona_tbl (
                        customer_name,
                        age_in_years,
                        gender,
                        occupation,
                        location,
                        travel_purpose,
                        travel_duration,
                        budget,
                        reservation_lead_time,
                        room_type,
                        amenities_availed,
                        discount,
                        source_of_booking,
                        transportation_requests,
                        final_price,
                        background,
                        goals,
                        challenges,
                        persona_summary,
                        customer_360,
                        additional_preferences) 
                        VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s) ON CONFLICT DO NOTHING ;
                    """, ( row[0],row[1],row[2],row[3], row[4], row[5],row[6],row[7],row[8],row[9], row[10], row[11],row[12], row[13], row[14],row[15],row[16],row[17], row[18], row[19],row[20]))
        cursor.execute('COMMIT;') 
        cursor.close()
        print("Inserted Persona Profiles to Database")
        return True
    
    # Insertion of Vector Embeddings to customer_embedding_tbl
    def embedding_insertion(self,embedded_df):
        cursor = self.db_conn.cursor()
        for index,row in embedded_df.iterrows():
            # print(row[0],row[1],row[2],row[3],row[4]) 
            cursor.execute("""
                           INSERT INTO Customers.customer_embedding_tbl (
                                customer_id,
                                customer_name,
                                cluster_name,
                                customer_360_embedded
                           )  VALUES (%s, %s,null,%s) ON CONFLICT DO NOTHING; 
                           """,(row[0],row[1],row[3]))
        cursor.execute('COMMIT;')
        cursor.close()
        print('Inserted Embedding Vectors to Database')
        return True
    
    def cluster_insertion(self,clustered_df):
        cursor = self.db_conn.cursor()
        for index,row in clustered_df.iterrows(): 
            cursor.execute("""
                           INSERT INTO CUSTOMERS.customer_cluster_mapping_tbl (hash_id,customer_name, customer_360,cluster_id)  
                           VALUES (%s, %s,%s,%s) ON CONFLICT DO NOTHING;  
                           """,(row[0],row[1],row[2],row[3]))
        cursor.execute('COMMIT;')
        cursor.close()
        return True
    
    def segment_insertion(self,segments):
        cursor = self.db_conn.cursor()
        for key,value in segments.items(): 
            cursor.execute("""
                           INSERT INTO CUSTOMERS.cluster_label_tbl (cluster_num, cluster_label)  VALUES (%s, %s) ON CONFLICT DO NOTHING; 
                           """,(str(key),str(value)))
        cursor.execute('COMMIT;')
        cursor.close()
        return True
    

    
    def fetch_embeddings(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT * FROM CUSTOMERS.embedding_tbl ;
        '''
        )
        result = cursor.fetchall()
        cursor.close()
        embeddings ={}
        for tuple in result:
            embeddings[tuple[1]] = tuple[0]
        print(len(embeddings),' Embeddings fetched from db ')
        return embeddings
    def fetch_profiles(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT * FROM CUSTOMERS.customer_persona_tbl ;
        '''
        )
        
        # column_names = [desc[0] for desc in cursor.d]escription] 
        # print(column_names)
        result = cursor.fetchall()
        cursor.close()
        return pd.DataFrame(result, columns=['customer_id','customer_name',
                                 
                                'age', 
                                'gender', 
                                'occupation',
                                'location',
                                'travelpurpose', 
                                'travelduration',
                                'budget',
                                'reservationleadtime',
                                'roomtype',
                                'amenitiesavailed',
                                'discount',
                                'sourceofbooking',
                                'transportationrequests',
                                'finalprice',
                                'background',
                                'goals',
                                'challenges',
                                'personasummary',
                                'customer360',
                                'additionalpreferences'
                                ])
    
    # Fetch CUtomer details from customer_persona_tbl
    def retrieve_customer_info(self):
        cursor = self.db_conn.cursor()
        cursor.execute(
            '''
            SELECT customer_id,customer_name,customer_360
                        FROM CUSTOMERS.customer_persona_tbl ;
            ''')
        result = cursor.fetchall()
        cursor.close()
        return pd.DataFrame(result, columns=['customer_id','customer_name','customer360'])
    
    #Fetch Vector Embeddings and Clusters from customer_embedding_tbl
    def retrieve_embedded_data(self):
        cursor = self.db_conn.cursor()
        cursor.execute(
            '''
            SELECT customer_id,customer_name,cluster_name,customer_360_embedded
                        FROM CUSTOMERS.customer_embedding_tbl ;
            ''')
        result = cursor.fetchall()
        cursor.close()
        return pd.DataFrame(result, columns=['customer_id','customer_name','cluster_name','customer_360_embedded'])

    def update_clusters(self,clustered_df):
        cursor = self.db_conn.cursor()
        for index,row in clustered_df.iterrows(): 
            cursor.execute("""
                           UPDATE CUSTOMERS.customer_embedding_tbl SET cluster_name = %s
                           WHERE customer_id = %s;                             
                           """,(row[4],row[0]))
        cursor.execute('COMMIT;')
        cursor.close()
        print('Updated Customers Vector Embeddings with Clustering Labels')
        return True
    
    def find_similar_customers(self,vector):
        # <->    <=>    <#>
        cursor = self.db_conn.cursor()
        import numpy as np
        register_vector(self.db_conn)
        embedding_array = np.array(vector)
        cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        cursor.execute('''
            SELECT customer_id,customer_name,(SELECT offers from customers.customer_segment_tbl WHERE segment_id =cluster_name::int) 
                    FROM customers.customer_embedding_tbl 
                    ORDER BY customer_360_embedded <=> %s LIMIT 3;
        ''',(embedding_array,)
        )
        
        result = cursor.fetchall()
        cursor.close()
        return result
    
    # Additon of new customers : customer_segemt_mapping_tbl1
    def insert_new_customers(self,new_customer):
        cursor = self.db_conn.cursor()
        # cursor.execute('SELECT (nextval(\'customer_persona_tbl_customer_id_seq\'::regclass);')
        
        cursor.execute("""
                           INSERT INTO CUSTOMERS.customer_segemt_mapping_tbl1 
                           VALUES (nextval(\'customer_persona_tbl_customer_id_seq\'::regclass), 
                           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                           ) RETURNING CUSTOMER_ID; 
                           """,(new_customer))
        customer_id = cursor.fetchone()[0]
        cursor.execute('COMMIT;')
        # print('Adding New customers to Database')
        return customer_id
    
    # Find and insert best Segments to a customer
    def get_customer_segments(self,vector,customer_id):
        # <->    <=>    <#>
        cursor = self.db_conn.cursor()
        import numpy as np
        register_vector(self.db_conn)
        embedding_array = np.array(vector)
        cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
        cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        cursor.execute('''
            SELECT cet.cluster_name,cet.customer_360_embedded <=> %s AS similarity,cst.offers
                    FROM customers.customer_embedding_tbl cet
                    inner join CUSTOMERS.customer_segment_tbl cst
			        on cst.segment_id = CAST(cet.cluster_name as INTEGER)
                    ORDER BY customer_360_embedded <=> %s LIMIT 3;
        ''',(embedding_array,embedding_array)
        )        
        result = cursor.fetchall()
        # cluster_set = {i[0] for i in result}
        # clusters =
        # print(result)
        for i in result:
            # print(i)
            cursor.execute('''
                UPDATE CUSTOMERS.customer_segemt_mapping_tbl1
                        SET segment_id = %s,segment_score = %s
                        WHERE customer_id = %s
            ''',(i[0],i[1],customer_id)
            )        
        cursor.execute('COMMIT;')
        cursor.close()
        print('Updated Segmnets for new Customers ')
        return result[0]
    
    def fetch_offers(self,customer_360):
        cursor = self.db_conn.cursor()
        query_string = """
        SELECT cpt.customer_id,cpt.customer_name,et.cluster_name,
            similarity(cpt.customer_360,CAST('leisure' AS TEXT)),
            offers
            FROM customers.customer_embedding_tbl et
			inner join customers.customer_persona_tbl cpt
			on et.customer_id = cpt.customer_id
			inner join CUSTOMERS.customer_segment_tbl cst
			on cst.segment_id = CAST(et.cluster_name as INTEGER)
            ORDER BY similarity(cpt.customer_360,CAST('leisure' AS TEXT)) LIMIT 3;
        """
        cursor.execute(query_string, (customer_360,))
        result = cursor.fetchall()
        print(result)
        cursor.close()
        return result

    # Rerieve Customers for web
    def retrieve_segmented_customer(self,customer_id):
        cursor = self.db_conn.cursor()
        print(customer_id)
        
        query_string = """
        SELECT a.*, b.segment_name, b.segment_description, b.offers
        FROM CUSTOMERS.customer_segemt_mapping_tbl1 a,
        CUSTOMERS.customer_segment_tbl b 
        WHERE a.customer_id= %s AND a.segment_id = b.segment_id;
        """
    
        cursor.execute(query_string, (customer_id,))
        result = cursor.fetchall()
        print(result)
        cursor.close()
        return pd.DataFrame(result, columns=['customer_id',
                                'customer_name',                        
                                'age', 
                                'gender', 
                                'occupation',
                                'location',
                                'travelpurpose', 
                                'travelduration',
                                'budget',
                                'reservationleadtime',
                                'roomtype',
                                'amenitiesavailed',
                                'discount',
                                'sourceofbooking',
                                'transportationrequests',
                                'finalprice',
                                'background',
                                'goals',
                                'challenges',
                                'personasummary',
                                'customer360',
                                'additionalpreferences',
                                'customer_360_embedded',
                                'segment_id',
                                'segment_score',
                                'new_segment_id',
                                'segment_name',
                                'segment_description',
                                'offers'
                                ])


    

if __name__=='__main__':
    db = DatabasePostgresqlAWS()
    result = db.fetch_profiles()
    print(result)
    # print(db.persona_insertion())
    # print(db.fetch_offers())