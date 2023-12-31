# File Management
import os
import pickle

# Data Processing
import re

# Data Manipulation
import pandas as pd

# Data Preprocessing
from sklearn.preprocessing import StandardScaler, PowerTransformer, OrdinalEncoder

import openai
from openai.embeddings_utils import get_embedding

class EmbeddingGenerator:

    api_key = '3289261e6cc84fa8aef58d38e2264fa9'

    openai.api_key = api_key
    openai.api_base = "https://openai-demo-mb-001.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'
    
    deployment_name_embedding = 'openaidemomb002'

    def normalize_text(self,string, sep_token = " \n "):
        string = re.sub(r'\s+',  ' ', string).strip()
        string = re.sub(r". ,","",string)
        # remove all instances of multiple spaces
        string = string.replace("..",".")
        string = string.replace(". .",".")
        string = string.replace("\n", "")
        string = string.strip()
        
        return string
    def get_embeddedings(self,persona_df):

         # Text Normalisation
        # persona_df['customer360']= persona_df["customer360"].apply(lambda text : self.normalize_text(text))
        # Tokenization
        # tokenizer = tiktoken.get_encoding("cl100k_base")
        # persona_df['n_tokens'] = persona_df["customer360"].apply(lambda x: len(x))
        # persona_df = persona_df[persona_df.n_tokens<8192]

        # Embedding creation for vectorization  
        persona_df['customer_360_embedded'] = persona_df["customer360"].apply(lambda x: get_embedding(x, engine=self.deployment_name_embedding))  

        # Save persona_df as embedded_df  
        # embedded_df = persona_df.copy()
        print(persona_df.head(3))
        return persona_df  





if __name__=='__main__':

    path = r'C:\Users\839152\Downloads\Gen AI\RecommendationSystem\caching'
                # Change the directory
    os.chdir(path)
    persona_df = pd.read_pickle('persona.pkl')
    # openai.embed
    eg = EmbeddingGenerator()    
    ed = eg.get_embedded_dataframe(True,persona_df)
    print(type(ed[1]))
