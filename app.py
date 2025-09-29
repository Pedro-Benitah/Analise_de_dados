
import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Spotify Churn Dashboard", layout="wide")

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    return df

st.title("Spotify Churn Dashboard")

default_path = "spotify_churn_dataset.csv"
if os.path.exists(default_path):
    df = load_data(default_path)
else:
    st.error("Arquivo 'spotify_churn_dataset.csv' não encontrado. Coloque o CSV na mesma pasta ou adicione um uploader.")
    st.stop()

if os.path.exists(default_path):
    df = load_data(default_path)

with st.expander("Ver colunas e amostra do dataset", expanded=False):
    st.write(df.head())
    st.write(df.dtypes)

st.sidebar.header("Filtros")

map_churn = {0: "Não cancelado", 1: "Cancelado"}
churn_labels = [map_churn[val] for val in sorted(df["is_churned"].dropna().unique())]

country_opts = st.sidebar.multiselect("País", options=sorted(df["country"].dropna().unique()), default=[])
plan_opts = st.sidebar.multiselect("Plano", options=sorted(df["subscription_type"].dropna().unique()), default=[])
device_opts = st.sidebar.multiselect("Dispositivo", options=sorted(df["device_type"].dropna().unique()), default=[])
gender_opts = st.sidebar.multiselect("Gênero", options=sorted(df["gender"].dropna().unique()), default=[])
churned_opts = st.sidebar.multiselect("Status de Cancelamento", options=churn_labels, default=[])

df_f = df.copy()
if country_opts:
    df_f = df_f[df_f["country"].isin(country_opts)]
if plan_opts:
    df_f = df_f[df_f["subscription_type"].isin(plan_opts)]
if device_opts:
    df_f = df_f[df_f["device_type"].isin(device_opts)]
if gender_opts:
    df_f = df_f[df_f["gender"].isin(gender_opts)]
if churned_opts:
    selected_vals = [k for k, v in map_churn.items() if v in churned_opts]
    df_f = df_f[df_f["is_churned"].isin(selected_vals)]

total_users = len(df_f)
churn_rate = df_f["is_churned"].mean() if "is_churned" in df_f.columns and total_users > 0 else 0.0
avg_listen = df_f["listening_time"].mean() if "listening_time" in df_f.columns and total_users > 0 else 0.0
avg_skip = df_f["skip_rate"].mean() if "skip_rate" in df_f.columns and total_users > 0 else 0.0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Usuários filtrados", f"{total_users:,}")
k2.metric("Taxa de cancelamento", f"{churn_rate:,.1%}")
k3.metric("Tempo médio de escuta", f"{avg_listen:,.1f}")
k4.metric("Skip rate médio", f"{avg_skip:,.1%}")

st.divider()

left, right = st.columns([1,1])

if "subscription_type" in df_f.columns and "is_churned" in df_f.columns:
    churn_by_plan = (
        df_f.groupby("subscription_type")["is_churned"]
        .mean()
        .reset_index()
        .sort_values("is_churned", ascending=False)
    )
    fig1 = px.bar(churn_by_plan, x="subscription_type", y="is_churned", title="Taxa de Cancelamento por Plano (média)")
    fig1.update_yaxes(tickformat=".0%")
    left.plotly_chart(fig1, use_container_width=True)

if "device_type" in df_f.columns and "is_churned" in df_f.columns:
    churn_by_dev = (
        df_f.groupby("device_type")["is_churned"]
        .mean()
        .reset_index()
        .sort_values("is_churned", ascending=False)
    )
    fig2 = px.bar(churn_by_dev, x="device_type", y="is_churned", title="Taxa de Cancelamento por Dispositivo (média)")
    fig2.update_yaxes(tickformat=".0%")
    right.plotly_chart(fig2, use_container_width=True)

if "ads_listened_per_week" in df_f.columns and "is_churned" in df_f.columns:
    st.subheader("Anúncios por Semana por Status de Cancelamento")

    fig_ads_box = px.box(
        df_f, x="is_churned", y="ads_listened_per_week", points="suspectedoutliers",
        title="Distribuição de Anúncios por Semana por Status de Cancelamento",
        labels={
            "is_churned": "Status (0 = fidelizado, 1 = cancelado)",
            "ads_listened_per_week": "Anúncios por semana"
        }
    )
    fig_ads_box.update_xaxes(
        tickmode="array", tickvals=[0,1], ticktext=["Fidelizado (0)", "Cancelado (1)"]
    )
    st.plotly_chart(fig_ads_box, use_container_width=True)

    st.write(
        df_f.groupby("is_churned")["ads_listened_per_week"].agg(
            contagem="count", media="mean", mediana="median", q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75), desvio="std"
        )
    )

if "age" in df_f.columns and "is_churned" in df_f.columns:
    st.subheader("Idade por Status de Cancelamento")

    fig_age_box = px.box(
        df_f, x="is_churned", y="age", points="suspectedoutliers",
        title="Distribuição de Idade por Status de Cancelamento",
        labels={
            "is_churned": "Status (0 = fidelizado, 1 = cancelado)",
            "age": "Idade"
        }
    )
    fig_age_box.update_xaxes(
        tickmode="array", tickvals=[0,1], ticktext=["Fidelizado (0)", "Cancelado (1)"]
    )
    st.plotly_chart(fig_age_box, use_container_width=True)

    st.write(
        df_f.groupby("is_churned")["age"].agg(
            contagem="count", media="mean", mediana="median", q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75), desvio="std"
        )
    )

if "listening_time" in df_f.columns and "is_churned" in df_f.columns:
    st.subheader("Tempo de Escuta por Status de Cancelamento")

    fig_time_box = px.box(
        df_f, x="is_churned", y="listening_time", points="suspectedoutliers",
        title="Distribuição do Tempo de Escuta por Status de Cancelamento",
        labels={
            "is_churned": "Status (0 = fidelizado, 1 = cancelado)",
            "listening_time": "Tempo de escuta"
        }
    )
    fig_time_box.update_xaxes(
        tickmode="array", tickvals=[0, 1], ticktext=["Fidelizado (0)", "Cancelado (1)"]
    )
    st.plotly_chart(fig_time_box, use_container_width=True)

    # Resumo estatístico por status
    st.write(
        df_f.groupby("is_churned")["listening_time"].agg(
            contagem="count",
            media="mean",
            mediana="median",
            q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75),
            desvio="std"
        )
    )

if "skip_rate" in df_f.columns and "is_churned" in df_f.columns:
    # Violin plot
    fig3 = px.violin(df_f, x="is_churned", y="skip_rate", box=True,
                     points="outliers",
                     title="Taxa da Skip Rate por Cancelamento")
    fig3.update_xaxes(
        tickmode="array",
        tickvals=[0, 1],
        ticktext=["Fidelizado (0)", "Cancelado (1)"]
    )
    fig3.update_yaxes(
        tickformat=".0%")
    st.plotly_chart(fig3, use_container_width=True)
    st.subheader("Resumo estatístico da Taxa de Pulos")
    st.write(
        df_f.groupby("is_churned")["skip_rate"].agg(
            q1=lambda s: s.quantile(0.25),
            mediana="median",
            q3=lambda s: s.quantile(0.75),
            media="mean",
            desvio="std"
        )
    )

if all(c in df_f.columns for c in ["listening_time", "songs_played_per_day", "is_churned"]):
    fig4 = px.scatter(
        df_f, x="listening_time", y="songs_played_per_day",
        color="is_churned", opacity=0.6,
        title="Tempo de Escuta x Músicas por Dia (cor = cancelamento)",
        trendline="ols" if len(df_f) <= 10000 else None
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

with st.expander("Notas & Metodologia"):
    st.markdown("""
    # Etapas do Projeto
    
    ## 1. Seleção de dados
    **a.** Escolher um conjunto de dados relevantes do Kaggle, que seja adequado para a criação de um dashboard interessante, informativo e interativo.  
    - **Resp:** O dataset escolhido foi *Spotify Analysis Dataset 2025*.  
    
    **b.** Justificar a escolha com base na aplicabilidade ao objetivo do projeto.  
    - **Resp:** A escolha se deve ao fato de o dataset conter informações sobre usuários, hábitos de escuta e cancelamento, possibilitando análises de churn que são diretamente aplicáveis a cenários reais de negócios em serviços de streaming.
     
    ---
    
    ## 2. Análise exploratória de dados
    **a.** Utilizar a biblioteca **Pandas** para carregar os dados e realizar análises exploratórias.  
    - **Resp:** As análises foram feitas no arquivo ipynb.
     
    **b.** Incluir estatísticas descritivas, visualizações básicas e identificação de tendências preliminares na análise.  
    - **Resp:** Está incluso no arquivo .ipynb.
    
    ---
    
    ## 3. Tratamento de dados
    **a.** Identificar quaisquer problemas de qualidade ou limpeza nos dados. 
    - **Resp:** Foi verificado no arquivo .ipynb.
     
    **b.** Aplicar os tratamentos necessários, como preenchimento de valores ausentes, correção de erros ou remoção de outliers.  
    - **Resp:** Como não foi necessário, nenhum tratamento foi aplicado.
    
    **c.** Caso a equipe decida não aplicar tratamentos e/ou apenas remover os dados problemáticos, apresentar os motivos e justificar essa decisão.  
    - **Resp:** Não foi identificada nenhuma irregularidade no DataFrame, como dados errados ou outliers, logo, optei por não fazer nenhuma correção.
    
    ---
    
    ## 4. Planejamento do dashboard
    **a.** Planejar as visualizações que serão incluídas no dashboard.  
    - **Resp:** Foram visualizações das colunas da tabela em comparação a taxa de pessoas que cancelavam suas contas.
    
    **b.** Considerar o público-alvo e escolher visualizações que transmitam efetivamente as informações relevantes.  
    - **Resp:** Meu público alvo seria o próprio aplicativo, diretores de marketing, para entenderem o que afasta as pessoas, se elas possuem fator em comum, achar um padrão em sua saída.
    
    ---
    
    ## 5. Criação do dashboard
    **a.** Utilizar uma ou mais ferramentas para criar o dashboard interativo  
    (exemplos: **Dash, Plotly, Streamlit, Django, Flask, Power BI, entre outras**).  
    - **Resp:** Utilizei Streamlit.
    
    **b.** Implementar filtros e outras funcionalidades que permitam a exploração dinâmica dos dados.  
    - **Resp:** Foram implementados usando Streamlit.

    """)
