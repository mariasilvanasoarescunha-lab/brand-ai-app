import streamlit as st
import pandas as pd
import unicodedata

# ------------------------
# FUNÇÃO PARA REMOVER ACENTO (🔥 MELHORIA)
# ------------------------
def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

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
# AI AGENT (INTELIGENTE)
# ------------------------
def agente_contabilizei(pergunta, df, df_sat, df_conc):
    pergunta = normalizar_texto(pergunta)

    # Palavras-chave
    palavras_melhor = ["melhor", "top", "performance"]
    palavras_pior = ["pior", "ruim"]
    palavras_canal = ["canal", "marketing"]
    palavras_regiao = ["regiao", "local"]
    palavras_segmento = ["segmento", "setor"]
    palavras_conversao = ["conversao"]
    palavras_churn = ["churn", "cancelamento"]
    palavras_crescimento = ["crescimento", "cresce"]
    palavras_investimento = ["investir", "investimento"]
    palavras_satisfacao = ["satisfacao", "insatisfacao", "problema"]
    palavras_concorrencia = ["concorrente"]

    def tem(lista):
        return any(p in pergunta for p in lista)

    # Métricas
    melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
    pior_canal = df.groupby("canal")["conversao"].mean().idxmin()

    melhor_regiao = df.groupby("regiao")["leads"].sum().idxmax()
    pior_regiao = df.groupby("regiao")["conversao"].mean().idxmin()

    melhor_segmento = df.groupby("segmento")["conversao"].mean().idxmax()
    churn_rate = df["churn"].mean()

    # 🔴 PROBLEMAS
    if tem(palavras_pior) and tem(palavras_canal):
        return f"⚠️ O canal com pior performance é {pior_canal}. Recomendo revisar campanhas."

    if "perdendo" in pergunta:
        return f"⚠️ Estamos perdendo performance no canal {pior_canal} e na região {pior_regiao}."

    # 💰 CLIENTES
    if "maiores clientes" in pergunta:
        top = df.sort_values(by="receita", ascending=False).head(3)
        return f"💰 Os maiores clientes estão nos segmentos: {', '.join(top['segmento'])}"

    # 📉 CHURN
    if tem(palavras_churn):
        return f"📉 A taxa de churn é {churn_rate:.2%}"

    # 📈 CRESCIMENTO
    if tem(palavras_crescimento):
        return f"📈 A região com maior crescimento é {melhor_regiao}, porém com baixa conversão em {pior_regiao}"

    # 😡 SATISFAÇÃO (🔥 CORRIGIDO)
    if tem(palavras_satisfacao) or "reclam" in pergunta:
        problema = df_sat.sort_values(by="quantidade", ascending=False).iloc[0]
        return f"😡 A maior reclamação dos clientes é '{problema['problema']}', com {problema['quantidade']} ocorrências."

    # 🟢 INVESTIMENTO
    if tem(palavras_investimento):
        return f"➡️ Recomendo investir em {melhor_canal} e expandir na região {melhor_regiao}"

    # 🟢 MELHOR CANAL
    if tem(palavras_canal) and (tem(palavras_melhor) or tem(palavras_conversao)):
        return f"📊 O canal com melhor performance é {melhor_canal}"

    # 🟢 REGIÃO
    if tem(palavras_regiao):
        return f"📊 A região com mais leads é {melhor_regiao}, mas a pior conversão ocorre em {pior_regiao}"

    # 🟢 SEGMENTO
    if tem(palavras_segmento):
        return f"🏆 O segmento com melhor performance é {melhor_segmento}"

    # 🔵 CONCORRÊNCIA
    if tem(palavras_concorrencia):
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        return f"📊 Melhor concorrente: {melhor_concorrente['empresa']} (canal: {melhor_concorrente['canal_top']})"

    if "comparar" in pergunta:
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        return f"➡️ Nosso melhor canal: {melhor_canal} vs concorrência: {melhor_concorrente['canal_top']}"

    return """🤖 Não entendi totalmente sua pergunta.

Tente:
• Qual o melhor canal?
• Onde investir?
• Qual região cresce mais?
• Qual o churn?
• Qual a maior reclamação?
"""

# ------------------------
# UI
# ------------------------
st.title("📊 CONTABILIZEI Brand AI")
st.write("🤖 AI Agent especialista em dados de marketing")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Leads", df["leads"].sum())
col2.metric("Conversão média", f"{df['conversao'].mean():.2%}")
col3.metric("CAC médio", f"R${df['cac'].mean():.2f}")

# Gráfico
st.subheader("📈 Leads por canal")
st.bar_chart(df.groupby("canal")["leads"].sum())

# Perguntas
st.subheader("🤖 Pergunte aos dados")
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    resposta = agente_contabilizei(pergunta, df, df_sat, df_conc)
    st.write(resposta)

# Recomendações
st.subheader("💡 Recomendações estratégicas")

melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
pior_canal = df.groupby("canal")["conversao"].mean().idxmin()
melhor_regiao = df.groupby("regiao")["leads"].sum().idxmax()

st.write(f"➡️ Investir em {melhor_canal}")
st.write(f"➡️ Melhorar {pior_canal}")
st.write(f"➡️ Expandir em {melhor_regiao}")
