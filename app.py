import streamlit as st
import pandas as pd

# Base de dados simulada
dados = {
    "cnpj": ["001", "002", "003", "004", "005"],
    "regiao": ["SP", "SP", "RJ", "NE", "Sul"],
    "segmento": ["Tecnologia", "Serviços", "Comércio", "Serviços", "Tecnologia"],
    "tipo": ["MEI", "PME", "MEI", "PME", "MEI"],
    "canal": ["Google Ads", "Instagram", "Google Ads", "Facebook", "Instagram"],
    "leads": [100, 200, 150, 300, 120],
    "conversao": [0.10, 0.05, 0.12, 0.04, 0.08],
    "cac": [50, 70, 45, 80, 60]
}

df = pd.DataFrame(dados)

# Título
st.title("CONTABILIZEI Brand AI")

st.write("Pergunte sobre campanhas, regiões ou performance")

# Campo de pergunta
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:

    if "canal" in pergunta.lower():
        melhor = df.groupby("canal")["conversao"].mean().idxmax()
        st.success(f"📊 Melhor canal: {melhor}")

    elif "regiao" in pergunta.lower():
        regiao = df.groupby("regiao")["leads"].sum().idxmax()
        st.success(f"🌎 Região com maior volume: {regiao}")

    elif "segmento" in pergunta.lower():
        segmento = df.groupby("segmento")["conversao"].mean().idxmax()
        st.success(f"🎯 Segmento com melhor conversão: {segmento}")

    else:
        st.warning("Ainda estou aprendendo essa pergunta 😉")

# Gráfico
st.subheader("Leads por canal")
st.bar_chart(df.groupby("canal")["leads"].sum())

# Insight
st.subheader("💡 Recomendação")
melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
st.write(f"Investir mais em {melhor_canal} pode gerar melhores resultados.")
