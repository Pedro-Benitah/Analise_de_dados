# Exploração de dados de churn

Dashboard acadêmico para explorar cancelamento de usuários por plano, dispositivo e hábitos de escuta, usando **Pandas, Streamlit e Plotly**. O repositório também contém um notebook de análise exploratória.

**Escopo:** leitura de um CSV local, filtros interativos, estatísticas descritivas e gráficos. Não há pipeline ETL agendado, banco de dados, API de dados ou modelo preditivo implementado.

## O que explorar

- Filtrar por país, plano, dispositivo, gênero e status de cancelamento.
- Comparar a proporção de cancelamento por plano e dispositivo.
- Inspecionar distribuições de idade, tempo de escuta, anúncios e taxa de pulos.
- Explorar a relação entre tempo de escuta e músicas por dia.

## Executar o dashboard

Use um ambiente virtual com Python compatível com as dependências. Execute os comandos na raiz do repositório:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço local informado pelo Streamlit, normalmente `http://localhost:8501`. O arquivo `spotify_churn_dataset.csv` precisa estar no diretório de execução; a aplicação não tem upload de arquivos.

Para abrir o notebook, instale também suas dependências:

```bash
python -m pip install jupyter matplotlib numpy seaborn
python -m jupyter notebook Norm.ipynb
```

As dependências atuais não estão fixadas por versão. Os comandos descrevem a instalação, mas não garantem um ambiente idêntico entre execuções.

## Estrutura

| Arquivo | Finalidade |
| --- | --- |
| [`app.py`](app.py) | Dashboard e filtros; carrega o CSV com Pandas. |
| [`Norm.ipynb`](Norm.ipynb) | Inspeção de categorias, valores ausentes, distribuições e estatísticas. |
| `spotify_churn_dataset.csv` | Arquivo de entrada utilizado no estudo. |
| [`requirements.txt`](requirements.txt) | Dependências do dashboard, incluindo Statsmodels para a linha de tendência. |

## Como interpretar as métricas

- **Usuários filtrados:** quantidade de linhas após os filtros. A leitura como número de usuários únicos depende de validar a unicidade de `user_id`.
- **Taxa de cancelamento:** média de `is_churned`, assumindo `0` para não cancelado e `1` para cancelado.
- **Tempo médio de escuta:** média de `listening_time`. A unidade precisa ser confirmada na fonte original.
- **Skip rate médio:** média de `skip_rate`, exibida como percentual; pressupõe valores na escala de 0 a 1.

Os gráficos mostram associações descritivas. Não demonstram causas de cancelamento nem desempenho de um modelo de previsão. Com um filtro sem linhas, os indicadores atuais podem exibir zero; isso deve ser interpretado como ausência de observações.

## Proveniência e limites dos dados

As notas em `app.py` citam o Kaggle e o nome *Spotify Analysis Dataset 2025*. O repositório não registra a URL exata, o autor, a licença ou um dicionário de dados da fonte. Por isso, a origem, a autorização de redistribuição e a natureza real ou sintética do CSV continuam pendentes de confirmação. Este estudo não representa dados oficiais do Spotify.

Antes de redistribuir o CSV, publicar uma demonstração hospedada ou usar os resultados em uma decisão real, confirme a fonte e a licença. Não acrescente dados pessoais ou corporativos ao repositório.

## Validação e próximos passos

Esta documentação foi conferida por leitura de `app.py`, `Norm.ipynb` e `requirements.txt`. Não foi realizada uma nova execução do dashboard ou do notebook nesta revisão. O repositório não inclui testes automatizados nem validações de esquema em execução.

Evoluções propostas, ainda não implementadas:

1. Registrar fonte, licença, unidades e significado das colunas.
2. Validar esquema, nulos, duplicidades e domínio de `is_churned` antes de exibir métricas.
3. Fixar versões e documentar um ambiente reproduzível.
4. Criar uma ingestão versionada e um modelo SQL com consultas de agregação, como próxima etapa de engenharia de dados.
