def agente_contabilizei(pergunta, df, df_sat, df_conc):
    pergunta = pergunta.lower()

    # ------------------------
    # INTENÇÕES (PALAVRAS-CHAVE)
    # ------------------------
    palavras_melhor = ["melhor", "top", "mais eficiente", "performance"]
    palavras_pior = ["pior", "ruim", "baixo"]
    palavras_canal = ["canal", "marketing"]
    palavras_regiao = ["regiao", "região", "local"]
    palavras_segmento = ["segmento", "setor"]
    palavras_conversao = ["conversao", "conversão"]
    palavras_churn = ["churn", "cancelamento", "cancelamentos"]
    palavras_crescimento = ["crescimento", "cresce", "crescendo"]
    palavras_investimento = ["investir", "investimento", "onde investir"]
    palavras_satisfacao = ["satisfacao", "insatisfacao", "reclamacao", "problema"]
    palavras_concorrencia = ["concorrente", "concorrencia"]

    # ------------------------
    # MÉTRICAS
    # ------------------------
    melhor_canal = df.groupby("canal")["conversao"].mean().idxmax()
    pior_canal = df.groupby("canal")["conversao"].mean().idxmin()

    melhor_regiao = df.groupby("regiao")["leads"].sum().idxmax()
    pior_regiao = df.groupby("regiao")["conversao"].mean().idxmin()

    melhor_segmento = df.groupby("segmento")["conversao"].mean().idxmax()
    churn_rate = df["churn"].mean()

    # ------------------------
    # FUNÇÕES AUXILIARES
    # ------------------------
    def tem(lista):
        return any(p in pergunta for p in lista)

    # ------------------------
    # INTELIGÊNCIA DO AGENTE
    # ------------------------

    # 🔴 PROBLEMAS
    if tem(palavras_pior) and tem(palavras_canal):
        return f"⚠️ O canal com pior performance é {pior_canal}. Recomendo revisar campanhas nesse canal."

    if "perdendo" in pergunta or "perda" in pergunta:
        return f"⚠️ Estamos perdendo performance no canal {pior_canal} e na região {pior_regiao}."

    # 💰 CLIENTES
    if "maiores clientes" in pergunta or "maior cliente" in pergunta:
        top = df.sort_values(by="receita", ascending=False).head(3)
        return f"💰 Os maiores clientes estão nos segmentos: {', '.join(top['segmento'])}"

    # 📉 CHURN
    if tem(palavras_churn):
        return f"📉 A taxa de churn atual é {churn_rate:.2%}"

    # 📈 CRESCIMENTO
    if tem(palavras_crescimento):
        return f"📈 A região com maior crescimento é {melhor_regiao}, porém com baixa conversão em {pior_regiao}"

    # 😡 SATISFAÇÃO
    if tem(palavras_satisfacao):
        problema = df_sat.sort_values(by="quantidade", ascending=False).iloc[0]
        return f"😡 Principal problema relatado pelos clientes: {problema['problema']}"

    # 🟢 INVESTIMENTO
    if tem(palavras_investimento):
        return f"➡️ Recomendo investir mais em {melhor_canal} e expandir na região {melhor_regiao}"

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
        return f"📊 O melhor concorrente é {melhor_concorrente['empresa']} (canal: {melhor_concorrente['canal_top']})"

    if "comparar" in pergunta:
        melhor_concorrente = df_conc.loc[df_conc["conversao_media"].idxmax()]
        return f"➡️ Nosso melhor canal é {melhor_canal}, enquanto o concorrente utiliza {melhor_concorrente['canal_top']}"

    # ⚪ FALLBACK INTELIGENTE
    return """🤖 Não entendi totalmente sua pergunta.

Tente algo como:
• Qual o melhor canal?
• Onde investir?
• Qual região cresce mais?
• Qual o churn?
"""
