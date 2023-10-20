import pandas as pd  
from sumy.parsers.plaintext import PlaintextParser  
from sumy.nlp.tokenizers import Tokenizer  
from sumy.summarizers.lex_rank import LexRankSummarizer
import re  
import string  
import nltk  
import pandas as pd  
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize 

class Segmentation:

    
 

    def clean_text(self,text):  
        # Remove HTML tags  
        text = re.sub('<.*?>', '', text)
        # Convert to lowercase  
        text = text.lower()
        # Remove punctuation  
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove numbers  
        text = re.sub(r'\d+', '', text)  

        # Remove extra whitespaces  
        text = re.sub('\s+', ' ', text).strip()  

        return text  

    def preprocess_summary(self,summary):  
        # Clean the text  
        cleaned_summary = self.clean_text(summary)  

        # Remove stopwords  
        stop_words = set(stopwords.words('english'))  
        tokens = word_tokenize(cleaned_summary)  
        cleaned_tokens = [token for token in tokens if token not in stop_words and len(token) > 1]  
        cleaned_summary = ' '.join(cleaned_tokens)  

        return cleaned_summary
    def segment_extraction(self, clustered_df):
        def process_clusters(data):  
                clusters = sorted(data['cluster'].unique())  
                cluster_data = {}  
                for cluster in clusters:  
                    cluster_data[cluster] = data[data['cluster'] == cluster]  
                return cluster_data  

        cluster_data = process_clusters(clustered_df)  
        summary_list ={}
        for cluster_number, cluster_df in cluster_data.items():  
            customer_360 = cluster_df['customer360'].tolist()  
            combined_360 = ";".join(customer_360)  

            parser = PlaintextParser.from_string(combined_360, Tokenizer('english'))  
            summarizer = LexRankSummarizer()  
            summary = summarizer(parser.document, sentences_count=2) 
            summary_text = ' '.join(str(sentence) for sentence in summary)  
            summary_text = self.preprocess_summary(summary_text)
            print("Cluster", cluster_number)  
            print("Summary:", summary_text)  
            print() 
            summary_list[cluster_number] = summary_text
        return summary_list






# if __name__=='__main__':