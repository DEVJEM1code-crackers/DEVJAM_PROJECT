#!/usr/bin/env python
# coding: utf-8

# # Install requirements

# In[ ]:


import warnings

warnings.filterwarnings("ignore")





# ## Translation

# In[4]:


import torchaudio
from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText

processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2ForTextToText.from_pretrained("facebook/seamless-m4t-v2-large")


# In[6]:


def translate_from_darija_to_english(sentence):
  text_inputs = processor(text = sentence, src_lang="ary", return_tensors="pt")
  output_tokens = model.generate(**text_inputs, tgt_lang="eng")
  translated_text_from_text = processor.decode(output_tokens[0].tolist(), skip_special_tokens=True)
  return translated_text_from_text


# In[7]:


translate_from_darija_to_english("فينك")


# In[9]:


translate_from_darija_to_english("خليني عليك")


# In[10]:


def translate_from_en_to_darija(sentence):
  text_inputs = processor(text = sentence, src_lang="eng", return_tensors="pt")
  output_tokens = model.generate(**text_inputs, tgt_lang="ary")
  translated_text_from_text = processor.decode(output_tokens[0].tolist(), skip_special_tokens=True)
  return translated_text_from_text


# In[11]:


translate_from_en_to_darija('Where are you')


# In[12]:


translate_from_en_to_darija('I want to kiss you')


# ## MAP options

# In[15]:


import os

from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

# In[16]:


instructor_embeddings = HuggingFaceInstructEmbeddings()


# In[17]:


my_apiKey = "AIzaSyA27dATTsKGFQIJ3f1xYieo0nAzziR1D0c"


# In[18]:


llm = GooglePalm(google_api_key=my_apiKey, temperature=0.1 )


# In[19]:


result = llm("give me the definition of bravery ")
result


# In[20]:


vecordb_path = "faiss_index"
myfile_path = "questions_and_answers.csv"


# In[21]:


def create_vector_db():
  #load CSV file :
  my_file = CSVLoader(file_path= myfile_path,
                      source_column= "prompt", encoding="iso-8859-1") # to avoid the encoding
  my_data = my_file.load()
  from langchain.vectorstores import FAISS

  # Create a FAISS instance for vector database from 'data'
  vectordb = FAISS.from_documents(documents=my_data,
                                  embedding=instructor_embeddings)


  vectordb.save_local(folder_path=vecordb_path)# save locally


# In[22]:


def get_qa_chain():
  vectordb = FAISS.load_local(vecordb_path,instructor_embeddings)
  # Create a retriever for querying the vector database
  retriever = vectordb.as_retriever(score_threshold=0.7)

  # Create RetrievalQA chain along with prompt template :


  prompt_template = """Given the following context and a question, generate an answer based on this context only.
  In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
  If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

  CONTEXT: {context}

  QUESTION: {question}"""


  PROMPT = PromptTemplate(
      template=prompt_template, input_variables=["context", "question"]
  )
  chain_type_kwargs = {"prompt": PROMPT}




  chain = RetrievalQA.from_chain_type(llm=llm,
                              chain_type="stuff",
                              retriever=retriever,
                              input_key="query",
                              return_source_documents=False,
                              chain_type_kwargs=chain_type_kwargs)
  return chain





# In[23]:


create_vector_db()
chain = get_qa_chain()


# In[24]:


chain("How can I get from Ain Diab Beach to the Morocco Mall?")['result']


# In[25]:


chain("How can I get from Casablanca to the Hassan II Mosque without spending much?")['result']


# # Image recognition

# In[ ]:

# -*- coding: UTF-8 -*-
import base64
import os
import pickle
import sys
#from db_tables import employees
import threading
import time
from datetime import datetime

import numpy
from flask import Flask, jsonify, render_template, request

#from it_jam import (get_qa_chain, translate_from_darija_to_english,translate_from_en_to_darija)

# insert at 1, 0 is the script path (or '' in REPL)


# Initiating the Flask app
app = Flask(__name__)



import io

import cv2
import torch
import torch.nn as nn
import torch.optim as optim
import torchaudio
import torchvision.transforms as transforms
from flask_cors import CORS
from PIL import Image
from torchvision import models

CORS(app)

class_descriptions = {
    'Hassan 2 Mosque': """A masterpiece of Arab-Muslim architecture, the Hassan 2 Mosque is one of the most beautiful religious buildings in the world.
                 Hassan 2 Mosque is actually unique in its architecture and size. With its minaret that rises to 200 m in height and has a 30km laser directed towards Mecca, it is considered to be the highest religious building in the world.
                 The idea of building a large mosque in Casablanca reflects the Royal will to provide the Casablanca metropolis with a great spiritual and civilizational monument of Morocco, giving it a harmonious urban development and allowing it to increase its radiance and influence based on faith, piety and tolerance.
                 Building the Hassan 2 Mosque His late Majesty Hassan II, may God rest his soul, laid the foundation stone of this mosque on 5 Dou Al Kiida 1406 of the Hegira, corresponding to July 11, 1986. The construction works started under the effective and daily supervision of His Majesty Hassan II, who had made sure that this great building reflects the artistic specificities of authentic Moroccan architecture, while highlighting its openness to technological innovations.
                 Through this architectural masterpiece, His Majesty Hassan II wanted to highlight the importance and value of the Hassan 2 mosque among Moroccans throughout history, just as He wanted to show that this place of worship has played an important role in the promotion of authentic architectural art and the preservation of the civilizational heritage, especially since the Casablanca Hassan 2 mosque reflects the great talents of the Moroccan Artisan.
                 The building of the Hassan 2 mosque on the Atlantic Ocean inspired by the Qur'anic verse "the throne of God was upon the water" was a pioneering idea intended to invite believers who go to this mosque to remember the greatness of God who created the sea and the sky.
                 The design of this work was the result of collaboration between the office of the French architect Michelle PINSEAU and the various Moroccan artisanal bodies that have created and revive by the hand of maâlem (master) beauty and the splendid seal of Moroccan architecture.
                 Expression of the symbiosis between a king and his people, the realization of this prestigious monument was financed thanks to the participation of all the Moroccan people who voluntarily answered the Royal call, each according to his means and his generosity .
                 This building was thus inaugurated on the occasion of the celebration by the Muslim world of aid al mawlid 12 Rabi I 1414 AH corresponding to August 30, 1993.""",
    'Hassan Tower': """The Hassan Tower
The Hassan Tower is considered the symbol of Rabat, it is one of the most famous sites in the kingdom.
 The Hassan Tower remains the only vestige of what was supposed to be, at the instigation of the Almohad sultan Yacoub Al Mansour (12th century), the largest mosque in the Muslim world.
 This oversized project would not survive, after his death, in the year 1199, nor later, after the Lisbon earthquake in 1755. Only its 44-meter-high minaret, with an architecture very close to the Koutoubia of Marrakech and the Giralda of Seville, remains and gives its name to the monument: the Hassan Tower.""",
    'Mansour Gate': """Bab Mansour was actually the last important construction project ordered by Sultan Moulay Ismail. He conceived it not as a defensive stronghold, but as an elaborate homage to himself and to the strong Muslim orthodoxy of his dynasty. The architect behind the great masterpiece was a Christian convert to Islam named Mansour Laalej (whose name translates to “victorious renegade”) who sought to ascend in the sultan's court. His name also contributed to the name of the gate (mansour means “victorious” in Arabic).

Legend has it that when the gate was completed Moulay Ismail inspected it and asked Mansour Laalej if he could do better. El Mansour felt compelled to answer “yes”, but this only angered sultan to the point that he had him executed. As colorful as this local tale may be, historical records show it probably did not occur as the gate was only completed in 1732, after the sultan's death and under the reign of his son, Moulay Abdallah.

A Splendid Homage
Local legends aside, Bab Mansour is well known all around the world for its incredible architecture. Since its original purpose was to pay homage to the sultan, great emphasis was put on the decorative details of the gate. Bab Mansour is thus intensely adorned by green and white zeillij tiles and engraved Koranic panels, all of which have unfortunately faded significantly with age. Visitors can still admire the alternating concave and convex ceramic design that decorates the greater part of the gate and creates a wonderful illusion of an intricately embroidered cloth. The wooden gateway (which stands 16m tall and 8m wide) is also not in use anymore but visitors can use a smaller side door to enter the medina.

In keeping with Moulay Ismail's efforts to erase all traces of the Saadian dynasty that preceded his, some parts of Bab Mansour were created with materials gathered from other Moroccan monuments and palaces. For example, the two marble columns that support the two bastions on both sides of the gate were taken from the nearby Roman ruins of Volubilis and the two taller Corinthian columns were retrieved from El Badi Palace in Marrakesh.""",
}


def load_model():
    model = models.resnet18(pretrained=False)
    num_classes = 3  # Number of classes in your dataset
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load('custom_resnet18.pth', map_location=torch.device('cpu')))
    model.eval()
    return model

def load_labels():
    return ['Mansour Gate', 'Hassan 2 Mosque', 'Hassan Tower']


def load_image(image_file):
    pil_image = Image.open(image_file)
    return pil_image


# Function to preprocess the image
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = transform(image).unsqueeze(0)
    return image


# Function to make predictions
def predict(model, categories, image):
    with torch.no_grad():
        output = model(image)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    predicted_index = torch.argmax(probabilities).item()
    predicted_label = categories[predicted_index]
    predicted_description = class_descriptions.get(predicted_label, 'Description not available')

    return predicted_label, predicted_description

@app.route('/predict', methods=['POST'])
def predict_image():

    # Charger l'image à partir de la requête
    image_data = request.form['image']
    image = base64.b64decode(image_data)
    image_file = Image.open(io.BytesIO(image))

    image_tensor = preprocess_image(image_file)

    # Charger le modèle
    model = load_model()

    # Faire une prédiction
    predicted_label, predicted_description = predict(model, load_labels(), image_tensor)
    print("Place",predicted_label)
    # Renvoyer le résultat
    result = {
        'predicted_description': predicted_description,
        'predicted_label':predicted_label
    }
    return predicted_description

import warnings

warnings.filterwarnings("ignore")



@app.route('/translate_darija_to_english1', methods=['POST'])
def translate_darija_to_english1():
    sentence = request.json['sentence']
    translated_text_from_text = translate_from_darija_to_english(sentence)
    return  translated_text_from_text

@app.route('/translate_english_to_darija1', methods=['POST'])
def translate_from_en_to_darija1():
    sentence = request.json['sentence']
    translated_text_from_text = translate_from_en_to_darija(sentence)
    return translated_text_from_text



import os

import dill
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

# Charger l'objet 'chain' sauvegardé
#with open('map_model.pkl', 'rb') as f:
#    chain = dill.load(f)

# Utiliser 'chain' dans votre application Flask
@app.route('/map_options', methods=['POST'])
def votre_fonction():
    # Utilisez 'chain' pour répondre à la requête
    question = request.json['sentence']
    answer = chain(question)['result']
    return  answer


if __name__ == '__main__':
    app.run(host='100.91.176.36',port= 3000, debug=False)



    




# In[27]:



# %%
