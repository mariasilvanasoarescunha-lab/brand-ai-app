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
# BASE DE CONCORRÊNCIA
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
        st.warning(f"⚠️ O canal com pior performance (menor conversão) é {pior_canal}")

    elif "pior regiao" in pergunta or "pior região" in pergunta:
        st.warning(f"⚠️ A região com pior taxa de conversão é {pior_regiao}")

    elif "perdendo" in pergunta:
        st.warning(f"⚠️ Estamos perdendo performance no canal {pior_canal} e na região {pior_regiao}")

    # 🟢 INVESTIMENTO
    elif "investir" in pergunta:
        st.success(f"➡️ Recomendamos investir mais no canal {melhor_canal} e expandir na região {melhor_regiao}")

    # 🟢 MELHOR CANAL
    elif "melhor canal" in pergunta:
        st.success(f"📊 O canal com melhor conversão é {melhor_canal}")

    # 🟢 CRESCIMENTO (IMPORTANTE 🔥)
    elif "cresce" in pergunta or "crescimento" in pergunta:
        st.success(
            f"📈 A região com mais leads (crescimento) é {melhor_regiao}, "
            f"porém a conversão mais baixa está em {pior_regiao}"
        )

    # 🟢 REGIÃO (RESPOSTA INTELIGENTE)
    elif "regiao" in pergunta or "região" in pergunta:
        st.success(
            f"📊 A região com mais leads é {melhor_regiao}, "
            f"mas a pior taxa de conversão está em {pior_regiao}"
        )

    # 🟢 SEGMENTO
    elif "segmento" in pergunta:
        st.success(f"🏆 O segmento com melhor conversão é {melhor_segmento}")

    # 🔵 CONCORRÊNCIA
    elif "concorrente" in pergunta or "concorrencia" in pergunta:
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        st.success(
            f"📊 O concorrente com melhor performance é {melhor_concorrente['empresa']}, "
            f"com foco no canal {melhor_concorrente['canal_top']}"
        )

    elif "comparar" in pergunta:
        st.success(
            f"➡️ Nosso melhor canal é {melhor_canal}, enquanto concorrentes focam em {df_conc['canal_top'].values[0]}"
        )

    # ⚪ FALLBACK
    else:
        st.info("Ainda estou aprendendo essa pergunta 😊")

# ------------------------
# RECOMENDAÇÃO AUTOMÁTICA
# ------------------------
st.subheader("💡 Recomendações estratégicas")

st.write(f"➡️ Aumentar investimento em {melhor_canal}")
st.write(f"➡️ Revisar estratégia no canal {pior_canal}")
st.write(f"➡️ Expandir presença na região {melhor_regiao}")
