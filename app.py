import streamlit as st
import pandas as pd

# ------------------------
# BASE DE DADOS INTERNA
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
# DADOS AVANÇADOS (NOVO 🔥)
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
# INSIGHTS
# ------------------------
melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
pior_canal = df.groupby("canal")["conversao"].mean().idxmin()

regiao_leads = df.groupby("regiao")["leads"].sum()
regiao_conversao = df.groupby("regiao")["conversao"].mean()

melhor_regiao = regiao_leads.idxmax()
pior_regiao = regiao_conversao.idxmin()

melhor_segmento = df.groupby("segmento")["conversao"].mean().idxmax()

# ------------------------
# UI
# ------------------------
st.title("📊 CONTABILIZEI Brand AI")
st.write("Insights de marketing, clientes e concorrência em linguagem simples")

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
    pergunta = pergunta.lower()

    # 🔴 PROBLEMAS
    if "pior canal" in pergunta:
        st.warning(f"⚠️ O canal com pior performance é {pior_canal}")

    elif "pior regiao" in pergunta or "pior região" in pergunta:
        st.warning(f"⚠️ A região com pior conversão é {pior_regiao}")

    elif "perdendo" in pergunta or "perdas" in pergunta:
        st.warning(f"⚠️ Estamos perdendo performance no canal {pior_canal} e na região {pior_regiao}")

    # 💰 MAIORES CLIENTES
    elif "maiores clientes" in pergunta or "maior cliente" in pergunta:
        top = df.sort_values(by="receita", ascending=False).head(3)
        st.success(f"💰 Maiores clientes estão nos segmentos: {', '.join(top['segmento'])}")

    # 📉 CHURN
    elif "churn" in pergunta or "cancelamento" in pergunta:
        churn_rate = df["churn"].mean()
        st.warning(f"📉 Taxa de churn estimada: {churn_rate:.2%}")

    # 📈 CRESCIMENTO
    elif "cresce" in pergunta or "crescimento" in pergunta:
        st.success(
            f"📈 A região com mais leads é {melhor_regiao}, "
            f"porém apresenta baixa conversão em {pior_regiao}"
        )

    elif "onde crescemos" in pergunta:
        st.success(f"📈 Crescimento concentrado na região {melhor_regiao}")

    # 😡 SATISFAÇÃO
    elif "satisfacao" in pergunta or "insatisfeito" in pergunta:
        problema = df_sat.sort_values(by="quantidade", ascending=False).iloc[0]
        st.warning(f"😡 Principal insatisfação: {problema['problema']}")

    elif "queixa" in pergunta or "reclamacao" in pergunta:
        problema = df_sat.sort_values(by="quantidade", ascending=False).iloc[0]
        st.warning(f"📢 Maior queixa dos clientes: {problema['problema']}")

    # 🟢 INVESTIMENTO
    elif "investir" in pergunta:
        st.success(f"➡️ Investir mais em {melhor_canal} e expandir em {melhor_regiao}")

    # 🟢 MELHOR CANAL
    elif "melhor canal" in pergunta:
        st.success(f"📊 Melhor canal: {melhor_canal}")

    # 🟢 REGIÃO
    elif "regiao" in pergunta or "região" in pergunta:
        st.success(
            f"📊 Mais leads em {melhor_regiao}, "
            f"mas pior conversão em {pior_regiao}"
        )

    # 🟢 SEGMENTO
    elif "segmento" in pergunta:
        st.success(f"🏆 Melhor segmento: {melhor_segmento}")

    # 🔵 CONCORRÊNCIA
    elif "concorrente" in pergunta or "concorrencia" in pergunta:
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        st.success(
            f"📊 Melhor concorrente: {melhor_concorrente['empresa']} "
            f"(canal: {melhor_concorrente['canal_top']})"
        )

    elif "comparar" in pergunta:
        st.success(
            f"➡️ Nosso canal: {melhor_canal} vs concorrência: {df_conc['canal_top'].values[0]}"
        )

    # ⚪ FALLBACK
    else:
        st.info("Ainda estou aprendendo essa pergunta 😊")

# ------------------------
# RECOMENDAÇÕES
# ------------------------
st.subheader("💡 Recomendações estratégicas")

st.write(f"➡️ Investir em {melhor_canal}")
st.write(f"➡️ Melhorar {pior_canal}")
st.write(f"➡️ Expandir em {melhor_regiao}")
