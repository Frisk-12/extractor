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
from streamlit_gsheets import GSheetsConnection
import gspread


# Create a connection object.
# conn = st.connection("gcs", type=GSheetsConnection)
# df = conn.read(spreadsheet = st.secrets['spreadsheet'])


def responseBuilder(system,text):
    key = st.secrets["key"]
    openAIEnvironmentKey = key

    openai_api_base = st.secrets["openai_api_base"]
    os.environ["OPENAI_API_BASE"] = openai_api_base
    os.environ["OPENAI_API_VERSION"] = "2023-08-01-preview"
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_KEY"] = openAIEnvironmentKey
    
    openai.api_type = "azure"
    openai.api_base = openai_api_base
    openai.api_version = "2023-08-01-preview"
    openai.api_key = openAIEnvironmentKey
    
    response = openai.ChatCompletion.create(
        engine = "gpt-35-turbo-16k", #"gpt-4-32k"
        temperature = 0,
        messages = [{"role":"system","content":system},
            {"role": "user", "content": text}
        ],
        max_tokens=6000
    )
    
    return response#str(response.choices[0]["message"]["content"])



def main():
    st.title("Framework Estrazione Dati")
    st.write("Benvenuto in questa semplice applicazione!")
    
    system = """
    Completa in formato json le seguenti info, prendendole e interpretando dal testo fornito dall'utente. In caso di nessuna informazione, lascia o una lista vuota oppure una stringa vuota ("").
    Cognome (str)
    Nome (str)
    Titolo (str)
    Professore universitario (boolean 1/0)
    Età (str) *Se non indicata, stimare età in un range, eg 35-45, 30-40, 45-55 etc
    Professionista Legale (boolean 1/0)
    Specializzazioni (list) #Ad esempio: civile, penale, tributario, societario etc.
    Hashtag (list)
    Informazioni (str)
    Interessi (list)
    Azienda attuale (str)
    Laurea Magistrale (boolean 1/0)
    Master (boolean 1/0)
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
    Digital transformation (boolean 1/0) #1 se presenti argomenti inerenti
    Tecnologia (boolean 1/0) #1 se presenti argomenti inerenti
    Intelligenza artificiale (boolean 1/0) #1 se presenti argomenti inerenti
    Innovazione (boolean 1/0) #1 se presenti argomenti inerenti
    Effetua attività su linkedin (boolean 1/0) #1 se presenti argomenti inerenti
    Ultime attività (list)
    Altri profili consultati (list)
    Sintesi Profilo (str) #Fai una sintesi di massimo 50 parole
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
        form = st.toggle("Formatta!")
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

            add_db = st.checkbox("Aggiungi al DB")
            if add_db:
                gc = gspread.service_account_from_dict(st.secrets.connections.gcs)
                sh = gc.open("DB_PotClients")
                worksheet = sh.get_worksheet(0)

                df = pd.DataFrame(worksheet.get_all_values())
                df.columns = df.iloc[0]
                df = df[1:]

                df.loc[len(df)+1] = list(json_data.values())#[json_data]
                df = df.applymap(lambda x: str(x) if isinstance(x, list) else x)

                worksheet.update([df.columns.values.tolist()] + df.values.tolist())

                # df = pd.DataFrame(worksheet.get_all_values())
                # df = df.applymap(lambda x: literal_eval(x) if isinstance(x, str) and x.startswith("[") else x)

                # if st.checkbox("Gestisci il DF"):
                #     num = st.number_input("Quale riga vuoi eliminare?",min_value=0,max_value=len(df))
                #     if st.button("Elimina"):
                #         df = df.drop(num)

            
            
            #with open(cognome_nome+".json", "w") as file:
            st.download_button(label = 'Download JSON',
                               file_name = cognome+"_"+nome+".json",
                               mime="application/json",
                               data=formatted_json)
                #json.dump(data, file)
                        

if __name__ == "__main__":
    main()
