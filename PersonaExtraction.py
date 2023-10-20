# OpenAI
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

# File Management
import os
import hashlib
import numpy as np

# Data Manipulation
import pandas as pd

class PersonaExtraction:

    api_key = '3289261e6cc84fa8aef58d38e2264fa9'

    openai.api_key = api_key
    openai.api_base = "https://openai-demo-mb-001.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    deployment_name = 'openaidemomb003'

    # Persona creation from Chat data using OpenAI Model[Named Entity Recognition System]
    def openai_chat_completion_response(self,chat_data):

        SYSTEM_PROMPT = """You are an assistant designed to create a customer persona based on a chat conversation between a customer and one of your hotel agents. Your task is to use this conversation to create a general customer persona that represents the typical customer who books hotels through your company.
        Your persona should include the following details:
        Name: The name of the customer should not be taken from chat, it should be genric as "Customer" for all customers.
        Age: The age range of the customer, such as between 25 to 55.
        Gender: The gender of the customer such as Male or Female, which can be a generic one or else None.
        Occupation: The occupation of the customer, which can be a range of common occupations such as business professional, retiree, student, etc.
        Location: The location of the customer, which can be a range of locations such as North America, Europe, Asia, etc.
        Travel Purpose: The purpose of the customer's travel, which can be a range of purposes such as leisure, business, family vacation, etc.
        Travel Duration: The duration of the customer's travel, which can be a range of durations such as 2-14 days.
        Budget: The budget range of the customer, such as low, moderate, high.
        Reservation Lead Time: The amount of time between booking and arrival.
        Room Type: The type of room booked by the customer, such as One Bedroom, Deluxe, etc.
        Amenities Availed: The amenities that the customer has availed during their stay, such as Breakfast Buffet, Spa Massage, Gym, etc.
        Discount: The final discount percentage applied to the customer's booking such as 10%, 20% etc.
        Source of Booking: The website, app, or other platform through which the customer made their reservation.
        Transportation Requests: Any requests for transportation services such as airport shuttles or car rentals.
        Final Price: The total price paid by the customer for their booking, including any taxes and fees.
        Background: Any relevant information about the customer's background that can be inferred from the chat conversation.
        Goals: The customer's goals and motivations for the trip, as expressed in the chat conversation.
        Challenges: Any challenges or concerns the customer has about booking a hotel, as expressed in the chat conversation.
        Persona Summary: A brief summary of the customer persona, including their key characteristics, goals, and challenges. It should be detailed enough to help the company better understand and serve customers who book hotels through the company.
        Customer 360: Feature that defines a customer's travel preferences, goals, challenges, and background, based on their interactions with a travel assistant or agent. It includes details such as the customer's name, age, gender, occupation, location, travel purpose, duration, budget, booking information, background, goals, challenges, and additional preferences.
        Additional Preferences: Any additional preferences that the customer has requested such as restaurants, nearby places, and local sightseeing.
        If no text is presented in any categories keep it [None] only.
        """

        USER_PROMPT_1 = """Examples:
        Chat Transcript 1: 
        Agent: Hello Aisha, how may I assist you today? 
        Customer: Hi Sophie, I am looking for a hotel to stay in during my upcoming trip to Budapest. 
        Agent: That's great to hear! Our hotel, the Grand Budapest Hotel, is a wonderful option for your stay. 
        Customer: Can you tell me more about the hotel? 
        Agent: Of course, our hotel is a refurbished castle with a lot of history and character. We have a variety of themed lodgings to choose from and we're located near many historic landmarks and museums. 
        Customer: That sounds perfect! What are the room rates like? 
        Agent: Our average daily room rate is $150, but I can offer you a special discount of 15% off, bringing the rate down to $127.50 per day. 
        Customer: Hmm, that's still a bit high for my budget. 
        Agent: I completely understand. May I ask if there are any additional features or amenities you are looking for in a hotel? 
        Customer: Actually, I am interested in educational tours or activities related to the history and culture of Budapest. 
        Agent: We have a variety of tours and activities available that focus on the history and culture of Budapest. Additionally, we offer a complimentary breakfast buffet every morning and have a spa on-site for relaxation. 
        Customer: That all sounds wonderful. I think I will take you up on your offer of 15% off the room rate. 
        Agent: Great! I have added the discount to your reservation and your new average daily room rate will be $127.50. Is there anything else I can assist you with today? 
        Customer: No, that's all for now. Thank you for your help! 
        Agent: You're welcome, Aisha. We look forward to hosting you at the Grand Budapest Hotel!
        """
        
        ASSISTANT_PROMPT_1 = """
        Your output response should contain the below details from the chat input.
        {
        "Name": ["Customer"],
        "Age": ["Between 25 to 30"],
        "Gender": ["Female"],
        "Occupation": [None],
        "Location": [None],
        "Travel Purpose": ["Leisure"],
        "Travel Duration": [None],
        "Budget": ["Low to moderate"],
        "Reservation Lead Time": ["5 Days"],
        "Room Type": [None],
        "Amenities Availed": ["Complimentary breakfast buffet, spa on-site"],
        "Discount": ["15% off"],
        "Source of Booking": [None],
        "Transportation Requests": [None],
        "Final Price": [None],
        "Background":
        ["The customer who is looking for a hotel to stay in during her upcoming trip to Budapest. She is interested in a hotel with history and character, and also wants to find educational tours or activities related to the history and culture of Budapest. The customer is price-conscious and wants to stay within her budget."],
        "Goals":
        ["Book a hotel with a rich history and character. Find educational tours or activities related to the history and culture of Budapest. Stay within her budget"],
        "Challenges":
        ["Finding a hotel with a rich history and character within her budget. Finding educational tours or activities that fit her interests and schedule"],
        "Persona Summary":
        ["The customer is a budget-conscious leisure traveler who values a hotel with history and character, as well as educational tours or activities related to the city's culture and history. She is open to recommendations from the hotel's concierge service and was pleased to receive a discount on her room rate."],
        "Customer 360": ["The customer is a female customer between the ages of 25 to 30 who is interested in booking a hotel for leisure purposes during her upcoming trip to Budapest. She is price-conscious and has a low to moderate budget. The customer is specifically looking for a hotel with history and character, and wants to find educational tours or activities related to the history and culture of Budapest. Her goals are to book a hotel with a rich history and character, find educational tours or activities related to the history and culture of Budapest, and stay within her budget. Aisha's main challenges are finding a hotel with a rich history and character within her budget, and finding educational tours or activities that fit her interests and schedule. Overall, Aisha is a budget-conscious leisure traveler who values a hotel with history and character, as well as educational tours or activities related to the city's culture and history."],
        "Additional Preferences": [None]
        If no text is presented in any categories keep it [None]
        }
        """

        # Define the user prompt for the specific chat data
        USER_PROMPT_2 = f"Create a customer persona based on a {chat_data} between a customer and one of your hotel agents. Please don't provide any other text input. The output format should be same like the one mentioned in ASSISTANT_PROMPT_1. If no text is presented in any of the categories keep it [None] only."
        
        GUIDELINES_PROMPT = """
        Persona Definition:
        1. Name: The name of the customer can be a generic name such as "Customer".
        2. Age: The age range of the customer, such as between 25 to 55.
        3. Gender: The gender of the customer, which can be a generic one or else None.
        4. Occupation: The occupation of the customer, which can be a range of common occupations such as business professional, retiree, student, etc.
        5. Location: The location of the customer, which can be a range of locations such as North America, Europe, Asia, etc.
        6. Travel Purpose: The purpose of the customer's travel, which can be a range of purposes such as leisure, business, family vacation, etc.
        7. Travel Duration: The duration of the customer's travel, which can be a range of durations such as 2-14 days.
        8. Budget: The budget range of the customer, such as low, moderate, high.
        9. Reservation Lead Time: The amount of time between booking and arrival.
        10. Room Type: The type of room booked by the customer, such as One Bedroom, Deluxe, etc.
        11. Amenities Availed: The amenities that the customer has availed during their stay, such as Breakfast Buffet, Spa Massage, Gym, etc.
        12. Discount: The final discount percentage applied to the customer's booking such as 10%, 20% etc.
        13. Source of Booking: The website, app, or other platform through which the customer made their reservation.
        14. Transportation Requests: Any requests for transportation services such as airport shuttles or car rentals.
        15. Final Price: The total price paid by the customer for their booking, including any taxes and fees.
        16. Background: Any relevant information about the customer's background that can be inferred from the chat conversation.
        17. Goals: The customer's goals and motivations for the trip, as expressed in the chat conversation.
        18. Challenges: Any challenges or concerns the customer has about booking a hotel, as expressed in the chat conversation.
        19. Persona Summary: A brief summary of the customer persona, including their key characteristics, goals, and challenges. It should be detailed enough to help the company better understand and serve customers who book hotels through the company.
        20. Customer 360: Feature that defines a customer's travel preferences, goals, challenges, and background, based on their interactions with a travel assistant or agent. It includes details such as the customer's name, age, gender, occupation, location, travel purpose, duration, budget, booking information, background, goals, challenges, and additional preferences.
        21. Additional Preferences: Any additional preferences that the customer has requested such as restaurants, nearby places, and local sightseeing.
        
        Output Format:
        {{"Name": [], "Age": [], "Gender": [], "Occupation": [], "Location": [], "Travel purpose": [], "Travel duration": [], "Budget": [], "Reservation Lead Time": [], "Room Type": [], "Amenities Availed": [], "Discount": [], "Source of Booking": [], "Transportation Requests": [], "Final Price": [], "Background": [], "Goals": [], "Challenges": [], "Persona Summary": [], "Customer 360": [], "Additional Preferences": []}}
        """
        
        response = openai.ChatCompletion.create(
            engine=self.deployment_name,
            model=self.deployment_name,
            max_tokens=1024,
            messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": USER_PROMPT_1},
                        {"role": "assistant", "content": ASSISTANT_PROMPT_1},
                        {"role": "user", "content": USER_PROMPT_2},
                        {"role": "user", "content": GUIDELINES_PROMPT}
                    ]
                )
        return response['choices'][0]['message']['content'].strip(" \n")
    def valid_response(self,profile_dict):  
        notnone={}
        for i,j in profile_dict.items():
            if j.find('None') == -1:
                notnone[i.strip()]=j.strip()
            else:
                notnone[i.strip()]='None'
        return notnone

    def str_to_dict(self,string):    
        string=string.replace('\n','').lower().strip()
        string =string.replace('not specified','None').replace('none mentioned','None').replace('unknown','None').replace('not requested','None').replace('none','None')
        slist=string.split('],')
        dict={}
        for i in slist:
            split=i.split('\": ')
            # print(split)
            if len(split)==1:
                split.append('[none]') 
            if split[0].replace('\"','').strip() != '':
                dict[split[0].replace('\"','').replace(' ','').strip()] = split[1].replace('\"','').replace('[','').strip()
        # print(dict.items())
        return dict

    # Read the chat data from a text file
    def read_text_file(self,file_path):
        with open(file_path, 'r') as f:
            return f.read()
    def df_parser(self,persona_df):
        # print(persona_df.columns)
        persona_df = persona_df.replace('None',np.NaN)
        persona_df = persona_df[
                            ['customer_name', 
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
                                ]]
        # none_df = persona_df[persona_df['customer360'] == 'None']
        # print("persona with none customer 360 : ",none_df )
        return persona_df#.dropna(subset=["customer360"], how="any")
    def file_processing(self,customer_name,file):
        chat_data = self.read_text_file(file)      
        print('Adding Customer Profile : ', customer_name)
        cust_data ={}
        cust_data['customer_name'] = customer_name
        #Extract features from each chat using OpenAI [Named Entity Recognition System]
        ners = self.openai_chat_completion_response(chat_data)
        ners = ners.replace('{','').replace('}','').strip()
                    # Convert the response to a dictionary
        profile_dict=self.str_to_dict(ners)
                # Filter out valid responses
        valid_data = self.valid_response(profile_dict)
        cust_data.update(valid_data)
            #Append valid response from each chat to a list
        # final_list.append()
        return cust_data
    
    def retrieve_customer_entity(self,chat_path,file_name):
        final_list =[]        
        # Change the directory
        # os.chdir(chat_path)      
        if file_name is None:
            for file in os.listdir():                
                # Check whether file is in text format or not
                if file.endswith("hatG"):
                    customer_name = str(file.split('.')[0].split('_')[0])
                    final_list.append(self.file_processing(customer_name,file))
        else:
            chat_data = open(file_name, 'r')  
            customer_name = str(file_name.split('.')[0].split('_')[0])
            final_list.append(self.file_processing(customer_name,file_name))      
        # print(final_list)
        persona_df =pd.DataFrame(final_list)
        # print(persona_df.columns)
        return persona_df
    
    # generating profile persona using OpenAI Model [Azure]   
    def profile_extraction(self,chat_path,file_name):

        print('Retrieveing Customer Attributes as well as customer 360 information')
        persona_df = self.retrieve_customer_entity(chat_path,file_name)
        print('Retrieveing Customer Attributes as well as customer 360 information completed. Saving it into cache') 
        persona_df = self.df_parser(persona_df)
        # print('Saved into cache file successfully')
        # print('Extracting required columns from the Customer profile dump')
        return persona_df
        # generating profile persona using OpenAI Model [Azure]   
    def extract_profile(self,file_name):

        print('Retrieveing Customer Attributes as well as customer 360 information')
        persona_df = self.retrieve_customer_entity(chat_path)
        print('Retrieveing Customer Attributes as well as customer 360 information completed. Saving it into cache') 
        persona_df = self.df_parser(persona_df)
        # print('Saved into cache file successfully')
        # print('Extracting required columns from the Customer profile dump')
        return persona_df
    

if __name__=='__main__':

    pe = PersonaExtraction()
    persona_db = pd.read_pickle('persona.pkl')
    persona_df = pe.profile_extraction(True,persona_db)
    print(persona_df)

