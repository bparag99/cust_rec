

'''
#####################################################################################################################
    # Step 1: Extract Customer Profile
        # Extracted customer profiles from OpenAI Model interactions. 
    # Step 2: Embedding creation and vectorization
        #Applied embeddings to the customer profile vectors to represent them in a meaningful way.
        #Transformed customer profiles into numerical vectors.
    # Step 3: Clustering
        # Performed clustering on the embedded customer profiles to group similar profiles together.
    # Step 4: Segmentation
        # Identify common features within clusters, such as booking details and budget.
    # Step 5: Database Insertion
        # Export the Customer profiles, vector embedding into Database
    # Step 6: Recommendation ( Work in Progress)
        # Recommend hotels or services based on shared features among customers within each cluster.
#####################################################################################################################
'''
import os
import pickle
import time
import pandas as pd

# Local Classes
from PersonaExtraction import PersonaExtraction
from EmbeddingGenerator import EmbeddingGenerator
from ClusterAssignment import ClusterAssignment
from Segmentation import Segmentation
from DatabasePostgresqlAWS import DatabasePostgresqlAWS
from OfferRecommendation import OfferRecommendation

class Recommendation:
    def create_recommendation(self,file_name):
        response_time = []
        chat_path = r'C:\Users\839152\Downloads\Gen AI\RecommendationSystem\test'
        # if __name__=='__main__':

    # Step 1 : Extract Customer Profile
        start_time = time.time()

        print('# Recommending New Customers ', time.asctime(time.gmtime()))
        persona_extraction = PersonaExtraction()    
        
        print('Extracting Customer profile information and attributes through Azure OpenAI')
        persona_df = persona_extraction.profile_extraction(chat_path,file_name)
        # persona_df = persona_extraction.profile_extraction(file_name)

        response_time.append(time.time()-start_time)

    # Step 2: Embedding creation and vectorization
        start_time = time.time()
        print('# Step 2: Embedding creation and vectorization : ', time.asctime(time.gmtime()))
        embedding_generator =  EmbeddingGenerator()

        print('Creating embeddings for each Customer Profile')
        # persona_df.head()
        embedded_df =embedding_generator.get_embeddedings(persona_df)
        print('Embeddings generated for each Customer Profile')

        response_time.append(time.time()-start_time)
        databaseAWS = DatabasePostgresqlAWS()    
        new_customer = embedded_df.copy()
        print(f'Adding {len(new_customer)} New customers to Database')
        # print(new_customer.columns)
        # new_customer.head(2)    
        # databaseAWS.insert_new_customers(new_customer)
        for row in new_customer.itertuples(name=None,index=False):
            
            print(f'Inserting New customers to Database')
            customer_id = databaseAWS.insert_new_customers(row)

            print('Fetching and Assigning the best segment for the new customers')
            vec = row[21]
            best_matches = databaseAWS.get_customer_segments(vec,customer_id)
            print('Assigned cluster',best_matches[0], ' to ' , row[0], 'with similarity score of ',best_matches[1] , 
                  '\n Offer :',best_matches[2] )

        response_time.append(time.time()-start_time)
        print('\n Total time taken for Day 0 Loading : ', sum(response_time), response_time, '\n')
        if file_name is not None:
            return customer_id


if __name__=='__main__':
    recommendation = Recommendation()
    # recommendation.create_recommendation(None)
    recommendation.create_recommendation('CaseyThomas_20-10-23.ctx.chatG')
