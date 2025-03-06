import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
import joblib
from core.process_text import process_text
from config import DATA_DIR

# Carregar o modelo treinado
model = joblib.load(os.path.join(DATA_DIR, "svc_model.pkl"))


# Configuração do layout do Streamlit
st.set_page_config(page_title="Classificação de Texto", layout="centered")

# Título do app
st.title("Classificação de Texto para Contribuições feitas ao PDM da Prefeitura de São Paulo 🏛️")

# Caixa de entrada para texto
user_input = st.text_area("Digite o texto da solicitação:", "")
categories = model.classes_

# Botão para prever a categoria
if st.button("Classificar"):
    if user_input.strip():
        # Pré-processar o texto
        processed_text = process_text(user_input)
        

        # Fazer previsão e obter probabilidades
        probabilities = model.decision_function([processed_text])  # Para SVC com 'probability=True', usar predict_proba
        probabilities = np.exp(probabilities) / np.sum(np.exp(probabilities))  # Softmax para converter em probabilidades
        
        # Criar dicionário com categorias e probabilidades
        prob_dict = dict(zip(categories, probabilities[0]))
        
        # Exibir categoria mais provável
        predicted_category = max(prob_dict, key=prob_dict.get)
        st.success(f"Categoria prevista: **{predicted_category}**")

        # Criar gráfico de barras
        fig, ax = plt.subplots()
        ax.barh(list(prob_dict.keys()), list(prob_dict.values()), color="skyblue")
        ax.set_xlabel("Probabilidade")
        ax.set_title("Distribuição das Categorias")
        plt.gca().invert_yaxis()  # Inverter para mostrar a categoria com maior probabilidade no topo

        # Exibir gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.warning("Por favor, insira um texto válido.")

# Exibir categorias disponíveis
st.subheader("Categorias possíveis:")
st.write(", ".join(categories))


