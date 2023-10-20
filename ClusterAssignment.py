# Data Manipulation
import pandas as pd
import numpy as np

# Data Processing
import json
import csv
import re
import operator

# File Management
import os
import pickle

# Data Visualization
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Data Preprocessing
from sklearn.preprocessing import StandardScaler, PowerTransformer, OrdinalEncoder
import tiktoken

# Clustering
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, silhouette_samples, accuracy_score, classification_report

# Dimensionality Reduction
from sklearn.decomposition import PCA
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning

from openai.embeddings_utils import cosine_similarity

import operator

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class ClusterAssignment:

    def find_cluster(self,vec,embedded_dict,persona_df):
        similarity_dict = {}
        for key, value in embedded_dict.items():
            similarity_dict[key] = cosine_similarity(value,vec)
        print(persona_df['hash_id'].isin(max(similarity_dict.items(), key=operator.itemgetter(1))[0]))
        return persona_df.loc[persona_df['hash_id'].isin(max(similarity_dict.items(), key=operator.itemgetter(1))[0]),'cluster']
    
    def cluster_assigment(self,enable_caching,new_embeddings, new_persona):
        if enable_caching:
            try:
                path = r'C:\Users\839152\Downloads\Gen AI\RecommendationSystem\caching'
                # Change the directory
                os.chdir(path)
                # read pickle file
                persona_df = pd.read_pickle('clustering.pkl')
                print('Importing Clustering data')

                with open('embeddings.pkl', 'rb') as fp:
                    embedded_dict = pickle.load(fp)
                    print('Importing Embeddings data')
            except:
                print('Clustering data not cached')
            for key, value in new_embeddings.items():
                new_embeddings[key] = self.find_cluster(value,embedded_dict,persona_df)
            
            new_persona['cluster'] = list(new_embeddings.values())
        return new_persona
    
    def get_clustered_dataframe(self,enable_caching,embedded_df): 
        # Extract and normalize the embedded vectors         
        embedded_df['customer_360_embedded'] = embedded_df['customer_360_embedded'].astype(str)  
        embedded_vectors = np.array([eval(embedded) for embedded in embedded_df['customer_360_embedded']])
        # print(embedded_vectors)
        scaler = StandardScaler()  
        normalized_vectors = scaler.fit_transform(embedded_vectors)  

        # Apply PCA for dimensionality reduction  
        pca = PCA(n_components=2)    
        reduced_features = pca.fit_transform(normalized_vectors)  

        # Perform k-means clustering   
        inertia = []    
        silhouette_scores = []    
        for k in range(2, 11):    
            kmeans = KMeans(n_clusters=k, random_state=0)    
            cluster_labels = kmeans.fit_predict(reduced_features)    
            inertia.append(kmeans.inertia_)    
            silhouette_avg = silhouette_score(reduced_features, cluster_labels)    
            silhouette_scores.append(silhouette_avg)    
            print(f"For n_clusters = {k}, the average silhouette_score is: {silhouette_avg}")  

        # Elbow Method graph    
        import matplotlib.pyplot as plt    
        plt.plot(range(2, 11), inertia, marker='o')    
        plt.xlabel('Number of Clusters')    
        plt.ylabel('Inertia')    
        plt.title('Elbow Method')    
        plt.show()  
        plt.savefig('Elbow Method.png')    

        # Silhouette Score graph    
        plt.plot(range(2, 11), silhouette_scores, marker='o')    
        plt.xlabel('Number of Clusters')    
        plt.ylabel('Average Silhouette Score')    
        plt.title('Silhouette Score')    
        plt.show()  
        plt.savefig('Silhouette Score.png')    

        # Perform K-means clustering on the reduced features with optimal number of clusters    
        optimal_num_clusters = silhouette_scores.index(max(silhouette_scores)) + 2    
        kmeans = KMeans(n_clusters=optimal_num_clusters, random_state=0)    
        cluster_labels = kmeans.fit_predict(reduced_features)    

        # Assign cluster labels to the DataFrame    
        embedded_df['cluster'] = cluster_labels  
        embedded_df.to_csv('cluster_embedded.csv')  
        embedded_df.to_excel('cluster_embedded.xlsx')          
        # print(embedded_df)  

        # Print clusters with associated customer names    
        for cluster_num in range(optimal_num_clusters):    
            cluster_data = embedded_df[embedded_df['cluster'] == cluster_num]    
            print(f"Cluster {cluster_num}:")    
            for customer_name in cluster_data['customer_name']:    
                print(customer_name)    
            print("\n")      


        # Visualize the clusters (optional)  
        plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=cluster_labels, cmap='viridis')  
        plt.title('PCA Reduced Features with K-means Clustering')  
        plt.xlabel('Dimension 1')  
        plt.ylabel('Dimension 2')  
        # plt.show()  
        plt.savefig('PCA Reduced Features with K-means Clustering.png')  

        return embedded_df


    # @ignore_warnings(category=ConvergenceWarning)
    def get_clustered_dataframe1(self,enable_caching,embedded_df, embedding_dict):
        # Extract and normalize the embedded vectors 
        # embedded_vectors = np.stack(embedded_df['customer_360_embedded'].apply(eval).values)
        print( embedding_dict.keys())
        embeddeding_list = list(embedding_dict.values())
        print(len(embeddeding_list[0]))
        embedded_vectors = np.array([eval(str(embedded)) for embedded in embeddeding_list])
        scaler = StandardScaler()
        normalized_vectors = scaler.fit_transform(embedded_vectors)

        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=2)  
        reduced_features = pca.fit_transform(normalized_vectors)
        # Perform k-means clustering
        inertia = []  
        silhouette_scores = []  
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=0)
            cluster_labels = kmeans.fit_predict(reduced_features)
            inertia.append(kmeans.inertia_)
            silhouette_avg = silhouette_score(reduced_features, cluster_labels)
            silhouette_scores.append(silhouette_avg)  

            print(f"For n_clusters = {k}, the average silhouette_score is: {silhouette_avg}")

 

        # Elbow Method graph
        import matplotlib.pyplot as plt  
        plt.plot(range(2, 11), inertia, marker='o')  
        plt.xlabel('Number of Clusters')  
        plt.ylabel('Inertia')  
        plt.title('Elbow Method')  
        # plt.show()
        plt.savefig('Elbow Method.png')  
    
        # Silhouette Score graph  
        plt.plot(range(2, 11), silhouette_scores, marker='o')  
        plt.xlabel('Number of Clusters')  
        plt.ylabel('Average Silhouette Score')  
        plt.title('Silhouette Score')  
        # plt.show()
        plt.savefig('Silhouette Score.png')  
       
        # Perform K-means clustering on the reduced features with optimal number of clusters  
        optimal_num_clusters = silhouette_scores.index(max(silhouette_scores)) + 2  
        kmeans = KMeans(n_clusters=optimal_num_clusters, random_state=0)  

        cluster_labels = kmeans.fit_predict(reduced_features)
        print(len(cluster_labels))

        # Assign cluster labels to the DataFrame  
        clustered_df = embedded_df
        clustered_df['cluster'] = cluster_labels[:len(clustered_df)]
        clustered_df.to_csv('cluster_embedded.csv')
        clustered_df.to_excel('cluster_embedded.xlsx') 

        # Print clusters with associated customer names  

        for cluster_num in range(optimal_num_clusters):
            cluster_data = clustered_df[clustered_df['cluster'] == cluster_num]
            print(f"Cluster {cluster_num}:")
            for customer_name in cluster_data['customer_name']:
                print(customer_name)
            print("\n")  

        if(enable_caching):
            try:
                path = r'C:\Users\839152\Downloads\Gen AI\RecommendationSystem\caching'
                # Change the directory
                os.chdir(path)
                # read pickle file
                clustered_df.to_pickle('clustering.pkl')
                print('Cached Clustering data')
            except:
                print('Clustering data not cached')
            
                

        return clustered_df

if __name__=='__main__':

    ca =ClusterAssignment()
    path = r'C:\Users\839152\Downloads\Gen AI\RecommendationSystem\caching'
    # Change the directory
    os.chdir(path)
    persona_df = pd.read_pickle('persona.pkl')
    with open('embeddings.pkl', 'rb') as fp:
        embedded_dict = pickle.load(fp)
        # print(embedded_dict)
    clustered_df = ca.get_clustered_dataframe(True,persona_df,embedded_dict)

    print(clustered_df.info())