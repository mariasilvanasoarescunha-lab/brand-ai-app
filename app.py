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
    pergunta = pergunta.lower()

    if "melhor canal" in pergunta or "canal" in pergunta:
        st.success(f"O melhor canal é {melhor_canal}")

    elif "regiao" in pergunta or "região" in pergunta:
        st.success(f"A região com maior crescimento é {melhor_regiao}")

    elif "segmento" in pergunta:
        st.success(f"O melhor segmento é {melhor_segmento}")

    elif "investir" in pergunta:
        st.success(f"Recomendamos investir mais no canal {melhor_canal} e focar na região {melhor_regiao}")

    elif "pior" in pergunta:
        pior_canal = df.groupby("canal")["conversao"].mean().idxmin()
        st.warning(f"O canal com pior performance é {pior_canal}")

    else:
        st.info("Ainda estou aprendendo essa pergunta 😊")

# Gráfico
st.subheader("Leads por canal")
st.bar_chart(df.groupby("canal")["leads"].sum())

# Insight
st.subheader("💡 Recomendação")
melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
st.write(f"Investir mais em {melhor_canal} pode gerar melhores resultados.")
