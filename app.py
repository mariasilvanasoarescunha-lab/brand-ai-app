import streamlit as st
import pandas as pd

# ------------------------
# BASE DE DADOS
# ------------------------
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

# ------------------------
# DADOS AVANÇADOS
# ------------------------
df["receita"] = [1000, 2000, 1500, 3000, 1200]
df["tempo_ativo"] = [12, 6, 10, 3, 8]
df["churn"] = [0, 1, 0, 1, 0]

satisfacao = {
    "problema": ["Preço", "Atendimento", "Sistema lento"],
    "quantidade": [10, 15, 8]
}

df_sat = pd.DataFrame(satisfacao)

# ------------------------
# CONCORRÊNCIA
# ------------------------
concorrencia = {
    "empresa": ["Concorrente A", "Concorrente B"],
    "canal_top": ["Instagram", "Google Ads"],
    "conversao_media": [0.09, 0.11],
    "cac_medio": [65, 55]
}

df_conc = pd.DataFrame(concorrencia)

# ------------------------
# AI AGENT (CÉREBRO)
# ------------------------
def agente_contabilizei(pergunta, df, df_sat, df_conc):
    pergunta = pergunta.lower()

    melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
    pior_canal = df.groupby("canal")["conversao"].mean().idxmin()

    melhor_regiao = df.groupby("regiao")["leads"].sum().idxmax()
    pior_regiao = df.groupby("regiao")["conversao"].mean().idxmin()

    melhor_segmento = df.groupby("segmento")["conversao"].mean().idxmax()

    # 🔴 PROBLEMAS
    if "pior canal" in pergunta:
        return f"⚠️ O canal com pior performance é {pior_canal}. Recomenda-se revisar campanhas."

    elif "perdendo" in pergunta or "perdas" in pergunta:
        return f"⚠️ Estamos perdendo performance no canal {pior_canal} e na região {pior_regiao}."

    # 💰 CLIENTES
    elif "maiores clientes" in pergunta:
        top = df.sort_values(by="receita", ascending=False).head(3)
        return f"💰 Os maiores clientes estão nos segmentos: {', '.join(top['segmento'])}"

    # 📉 CHURN
    elif "churn" in pergunta or "cancelamento" in pergunta:
        churn_rate = df["churn"].mean()
        return f"📉 A taxa de churn é {churn_rate:.2%}"

    # 📈 CRESCIMENTO
    elif "crescimento" in pergunta or "cresce" in pergunta:
        return f"📈 A região com mais crescimento é {melhor_regiao}, porém com baixa conversão em {pior_regiao}"

    # 😡 SATISFAÇÃO
    elif "satisfacao" in pergunta or "insatisfacao" in pergunta or "reclamacao" in pergunta:
        problema = df_sat.sort_values(by="quantidade", ascending=False).iloc[0]
        return f"😡 Principal problema relatado: {problema['problema']}"

    # 🟢 INVESTIMENTO
    elif "investir" in pergunta:
        return f"➡️ Recomenda-se investir em {melhor_canal} e expandir na região {melhor_regiao}"

    # 🟢 MELHOR CANAL
    elif ("melhor canal" in pergunta) or ("canal" in pergunta and "convers" in pergunta):
        return f"📊 O melhor canal é {melhor_canal}"

    # 🟢 REGIÃO
    elif "regiao" in pergunta or "região" in pergunta:
        return f"📊 Mais leads em {melhor_regiao}, mas pior conversão em {pior_regiao}"

    # 🟢 SEGMENTO
    elif "segmento" in pergunta:
        return f"🏆 O segmento com melhor performance é {melhor_segmento}"

    # 🔵 CONCORRÊNCIA
    elif "concorrente" in pergunta:
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        return f"📊 Melhor concorrente: {melhor_concorrente['empresa']} (canal: {melhor_concorrente['canal_top']})"

    elif "comparar" in pergunta:
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        return f"➡️ Nosso melhor canal: {melhor_canal} vs concorrência: {melhor_concorrente['canal_top']}"

    # ⚪ FALLBACK
    else:
        return "Ainda estou aprendendo essa pergunta 😊"

# ------------------------
# UI
# ------------------------
st.title("📊 CONTABILIZEI Brand AI")
st.write("🤖 Você está conversando com um AI Agent especialista em dados de marketing.")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Leads", df["leads"].sum())
col2.metric("Conversão média", f"{df['conversao'].mean():.2%}")
col3.metric("CAC médio", f"R${df['cac'].mean():.2f}")

# Gráfico
st.subheader("📈 Leads por canal")
st.bar_chart(df.groupby("canal")["leads"].sum())

# ------------------------
# PERGUNTAS
# ------------------------
st.subheader("🤖 Pergunte aos dados")
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    resposta = agente_contabilizei(pergunta, df, df_sat, df_conc)
    st.write(resposta)

# ------------------------
# RECOMENDAÇÕES
# ------------------------
st.subheader("💡 Recomendações estratégicas")

melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
pior_canal = df.groupby("canal")["conversao"].mean().idxmin()
melhor_regiao = df.groupby("regiao")["leads"].sum().idxmax()

st.write(f"➡️ Investir em {melhor_canal}")
st.write(f"➡️ Melhorar {pior_canal}")
st.write(f"➡️ Expandir em {melhor_regiao}")
