import pandas as pd
import plotly.express as px
import streamlit as st

# INTERFACE DO STREAMLIT
st.title('DADOS COVID - BRASIL')
st.write('Nesta aplicação, você pode escolher o estado e o tipo de informação para gerar um gráfico. Utilize o menu lateral para alterar as opções.')

# LENDO O DATASET
df = pd.read_csv('cases-brazil-states.csv')

# Conversão da coluna 'data' para o formato datetime
df['date'] = pd.to_datetime(df['date'])

# Tradução das colunas
dados_traduzidos = {
    'epi_week': 'semana_epi',
    'date': 'data',
    'country': 'país',
    'state': 'estado',
    'city': 'cidade',
    'newDeaths': 'novasMortes',
    'deaths': 'mortes',
    'newCases': 'novosCasos',
    'totalCases': 'casosTotais',
    'deathsMS': 'mortesMS',
    'totalCasesMS': 'casosTotaisMS',
    'deaths_per_100k_inhabitants': 'mortes_por_100k_habitantes',
    'totalCases_per_100k_inhabitants': 'casosTotais_por_100k_habitantes',
    'deaths_by_totalCases': 'mortes_por_casosTotais',
    'recovered': 'recuperados',
    'suspects': 'suspeitos',
    'tests': 'testes',
    'tests_per_100k_inhabitants': 'testes_por_100k_habitantes',
    'vaccinated': 'vacinados',
    'vaccinated_per_100_inhabitants': 'vacinados_por_100_habitantes',
    'vaccinated_second': 'vacinados_segundaDose',
    'vaccinated_second_per_100_inhabitants': 'vacinados_segundaDose_por_100_habitantes',
    'vaccinated_single': 'vacinados_doseUnica',
    'vaccinated_single_per_100_inhabitants': 'vacinados_doseUnica_por_100_habitantes',
    'vaccinated_third': 'vacinados_terceiraDose',
    'vaccinated_third_per_100_inhabitants': 'vacinados_terceiraDose_por_100_habitantes'
}

# MELHORANDO O NOME DAS COLUNAS DA TABELA
df.rename(columns=dados_traduzidos, inplace=True)

# SELEÇÃO DO ESTADO
estados = list(df['estado'].unique())
state1 = st.selectbox('Qual estado?', estados)

# Comparação: permite escolher outro estado para comparação
state2 = st.selectbox('Gostaria de comparar com algum estado?', estados)

# SELEÇÃO DO TIPO DE INFORMAÇÃO
colunas_opcoes = {
    'Casos Totais': 'casosTotais',
    'Casos por 100 mil habitantes': 'casosTotais_por_100k_habitantes',
    'Novos casos': 'novosCasos',
    'Novos óbitos': 'novasMortes',
    'Óbitos por 100 mil habitantes': 'mortes_por_100k_habitantes',
    'Recuperados': 'recuperados',
    'Suspeitos': 'suspeitos',
    'Testes': 'testes',
    'Tests por 100 mil habitantes': 'testes_por_100k_habitantes',
    'Vacinados': 'vacinados',
    'Vacinados - Segunda Dose': 'vacinados_segundaDose',
    'Vacinados Dose Única': 'vacinados_doseUnica',
    'Vacinados Terceira Dose': 'vacinados_terceiraDose'
}

column_option = st.selectbox('Qual tipo de informação?', list(colunas_opcoes.keys()))
column = colunas_opcoes[column_option]

# SELEÇÃO DAS LINHAS QUE PERTENCEM AO ESTADO
df_estado_1 = df[df['estado'] == state1]
df_estado_2 = df[df['estado'] == state2]

# Verificação se os estados são iguais
if state1 == state2:
    st.warning("Os estados selecionados são os mesmos. Os dados serão exibidos como uma única série.")
    df_combinado = df_estado_1  # Se os estados são iguais, usa apenas um DataFrame
else:
    df_combinado = pd.concat([df_estado_1, df_estado_2])  # Combina os DataFrames se os estados forem diferentes

# GERAÇÃO DO GRÁFICO
fig = px.line(df_combinado, x="data", y=column, color='estado', color_discrete_sequence=['blue', 'red'],
              title=f'Comparação de {column_option} entre {state1} e {state2}')
fig.update_layout(
    plot_bgcolor='black',   # Cor do fundo do gráfico
    paper_bgcolor='black',  # Cor do fundo fora do gráfico
    font_color='white',     # Cor do texto
    xaxis_title='Data', 
    yaxis_title=column_option.upper(), 
    title={'x': 0.5}
)
# EXIBIÇÃO DO GRÁFICO
st.plotly_chart(fig, use_container_width=True)

st.caption('Os dados foram obtidos a partir do site: https://github.com/wcota/covid19br')
