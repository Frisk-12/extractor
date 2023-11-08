#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 17:06:26 2023

@author: andreadesogus
"""


import streamlit as st
import pandas as pd
import os
import json
import openai

df = pd.read_csv("df.csv")

def responseBuilder(system,text):
    key = st.secrets["key"]
    openAIEnvironmentKey = key
    
    os.environ["OPENAI_API_BASE"] = "https://openai-francecentral-lab.openai.azure.com"
    os.environ["OPENAI_API_VERSION"] = "2023-08-01-preview"
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_KEY"] = openAIEnvironmentKey
    
    openai.api_type = "azure"
    openai.api_base = "https://openai-francecentral-lab.openai.azure.com"
    openai.api_version = "2023-08-01-preview"
    openai.api_key = openAIEnvironmentKey
    
    response = openai.ChatCompletion.create(
        engine = "gpt-35-turbo-16k", #"gpt-4-32k"
        temperature = 0,
        messages = [{"role":"system","content":system},
            {"role": "user", "content": text}
        ],
        max_tokens=12000
    )
    
    return response#str(response.choices[0]["message"]["content"])



def main():
    st.title("Framework Estrazione Dati")
    st.write("Benvenuto in questa semplice applicazione!")
    
    system = """
    Completa in formato json le seguenti info, prendendole e interpretando dal testo fornito dall'utente.

    Cognome (str)
    Nome (str)
    Titolo (str)
    Specializzazioni (list) #Ad esempio: civile, penale, tributario, societario etc.
    Hashtag (list)
    Informazioni (str)
    Interessi (list)
    Azienda attuale (str)
    Formazione - Triennale (boolean 1/0)
    Formazione - Specialistica (boolean 1/0)
    Formazione - Master (boolean 1/0)
    Formazione - Altro (boolean 1/0) 
    Paese (str)
    Città (str)
    Follower (int)
    Collegamenti (str)
    Servizi offerti (list)
    Competenze Principali (list)
    Esperienza (lista di dizionari)*posizione, azienda e durata
    Formazione (lista di dizionari)*istituto, studi e durata
    Volontariato (list)
    Licenze e certificazioni (list)
    Pubblicazioni (list)
    Riconoscimenti e Premi (list)
    Inglese - livello (str)
    Francese - Livello (str)
    Tedesco - Livello (str)
    Spagnolo - Livello (str)
    Cinese - Livello (str)
    Organizzazioni (list)
    Cause (list)
    Pagine seguite(list)
    Competenze (list)
    Appassionato digital transformation (boolean 1/0)
    Appassionato tecnologia (boolean 1/0)
    Appassionato IA (boolean 1/0)
    Appassionato innovazione (boolean 1/0)
    Effetua attività su linkedin (boolean 1/0)
    Ultime attività (list)
    Altri profili consultati (list)
    """

    
    user = "Jurix1"
    psw = st.secrets["psw"]
    
    def authenticate(user,psw,user_t,psw_t):
        if (user_t == user)&(psw_t==psw):
            
            return True
    form = None
    control = None
    user_t = st.sidebar.text_input("Inserisci il tuo username")
    psw_t  = st.sidebar.text_input("Inserisci la tua password",type='password')
    access = st.sidebar.button("Accedi")
    if (user_t) and (psw_t):
        if access:
            auth = authenticate(user,psw,user_t,psw_t)
            if auth:
                st.sidebar.success("Accesso Riuscito")
    if authenticate(user,psw,user_t,psw_t):
        text = st.text_area("Inserisci il testo da formattare:")
        form = st.button("Formatta!")
        if form:
            resp = responseBuilder(system, text)
            # Carica il JSON
            json_data = json.loads(str(resp.choices[0]["message"]["content"]))

            # Formatta il JSON in modo leggibile
            formatted_json = json.dumps(json_data, indent = 4,ensure_ascii=False)

            # Visualizza il JSON formattato
            st.code(formatted_json, language='json')

            #if st.button("Download JSON"):
            cognome = json_data['Cognome']
            nome    = json_data['Nome']

            df = pd.DataFrame([json_data],index=[0])

            # Visualizza il DataFrame di Pandas utilizzando Streamlit
            st.write(df)

            
            
            #with open(cognome_nome+".json", "w") as file:
            st.download_button(label = 'Download JSON',
                               file_name = "mount/src//extractor/"+cognome+"_"+nome+".json",
                               mime="application/json",
                               data=formatted_json)
                #json.dump(data, file)
                        

if __name__ == "__main__":
    main()
