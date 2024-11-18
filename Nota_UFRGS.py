import streamlit as st
import pandas as pd
import os

# Título do App
st.title("Cálculo da Nota - UFRGS")

# Carregar o arquivo de Pesos e Notas de Corte
pesos_file = 'Pesos_NotasCortes_UFRGS.csv'
df_pesos = pd.read_csv(pesos_file, sep=';', encoding='latin-1')
   
#Criação das colunas para entrada de acertos
st.subheader("Escolha o curso e a língua estrangeira")

# Selecionar o curso
cursos = df_pesos['CURSO'].unique()
#curso_selecionado = st.selectbox("Escolha o curso:", cursos)
curso_selecionado = st.selectbox("Escolha o curso:", cursos, index=list(cursos).index('Medicina - Bacharelado'))

# Selecionar o língua estrangeira
lingua_estrangeira = st.selectbox("Escolha a Língua Estrangeira:", ['Inglês', 'Espanhol', 'Italiano', 'Francês', 'Alemão'])

# Obter os pesos do curso selecionado
pesos_curso = df_pesos[df_pesos['CURSO'] == curso_selecionado].iloc[0]

# Disciplinas e mapeamento de pesos
disciplinas = [
    'Português e Redação', 'Literatura', 'História', 
    'Geografia', 'Matemática', 'Língua Estrangeira', 
    'Física', 'Química', 'Biologia'
]

# Mapeamento de colunas do arquivo de pesos para disciplinas
disciplina_peso_map = {
    'Português e Redação': 'LINGUA PORTUGUESA E REDACAO',
    'Literatura': 'LITERATURA EM LINGUA PORTUGUESA',
    'História': 'HIS',
    'Geografia': 'GEO',
    'Matemática': 'MAT',
    'Língua Estrangeira': 'LINGUA ESTRANGERIA MODERNA',
    'Física': 'FIS',
    'Química': 'QUI',
    'Biologia': 'BIO'
}

# Médias e desvios padrão
medias = {
    'Português e Redação': 18.8296,
    'Literatura': 8.5644,
    'História': 7.6036,
    'Matemática': 5.3935,
    
    'Inglês': 5.8173,
    'Espanhol': 5.5619,
    'Italiano': 8.1600,  
    'Francês': 6.6000,
    'Alemão': 8.4762,
    
    'Física': 4.4384,
    'Química': 5.4012,    
    'Geografia': 7.1512,
    'Biologia': 5.8274
}

desvios = {
    'Português e Redação': 4.033,
    'Literatura': 3.0594,
    'História': 2.6330,    
    'Matemática': 2.5637,
    
    'Inglês': 2.7626,
    'Espanhol': 2.0791,    
    'Italiano': 3.1709,  
    'Francês': 4.3405,
    'Alemão': 3.7240,
    
    'Física': 2.4054,
    'Química': 2.3546,    
    'Geografia': 2.6252,
    'Biologia': 2.463
}

# Criação das colunas para entrada de acertos
#st.subheader("Preencha os acertos para cada disciplina")

# Usar as colunas para reduzir o espaço
col1, col2 = st.columns(2)

# Primeira coluna para os primeiros 5 campos
with col1:
    st.subheader("1° Dia") 
    #st.markdown("<h2>1° Dia </h2>", unsafe_allow_html=True, font-size: 14px)
    acertos_portugues = st.slider("Acertos em Português:", min_value=0, max_value=15, step=1)
    acertos_literatura = st.slider("Acertos em Literatura:", min_value=0, max_value=15, step=1)
    acertos_historia = st.slider("Acertos em História:", min_value=0, max_value=15, step=1)
    acertos_geografia = st.slider("Acertos em Geografia:", min_value=0, max_value=15, step=1)
    acertos_matematica = st.slider("Acertos em Matemática:", min_value=0, max_value=15, step=1)

# Segunda coluna para os próximos 5 campos
with col2:
    st.subheader("2° Dia")         
    acertos_redacao = st.slider("Nota em Redação:", min_value=0.0, max_value=15.0, step=0.05)
    acertos_lingua = st.slider(f"Acertos em {lingua_estrangeira}:", min_value=0, max_value=15, step=1)
    acertos_fisica = st.slider("Acertos em Física:", min_value=0, max_value=15, step=1)
    acertos_quimica = st.slider("Acertos em Química:", min_value=0, max_value=15, step=1)
    acertos_biologia = st.slider("Acertos em Biologia:", min_value=0, max_value=15, step=1)


# Cálculo de escore bruto para Português e Redação
acertos_port_red = acertos_portugues + acertos_redacao
peso_port_red = pesos_curso[disciplina_peso_map['Português e Redação']]

# Lista para armazenar os dados de entrada
dados_aluno = [
    {
        'Disciplina': 'Port. e Red.',
        'Peso': peso_port_red,
        'Acertos': acertos_port_red,
        'Média': medias['Português e Redação'],
        'Des. Padrão': desvios['Português e Redação']
    }
]

# Adicionar dados de língua estrangeira
peso_lingua = pesos_curso[disciplina_peso_map['Língua Estrangeira']]

dados_aluno.append({
    'Disciplina': lingua_estrangeira,
    'Peso': peso_lingua,
    'Acertos': acertos_lingua,
    'Média': medias[lingua_estrangeira],
    'Des. Padrão': desvios[lingua_estrangeira]
})

# Adicionar dados de outras disciplinas
disciplinas_acertos = {
    'Literatura':   acertos_literatura,
    'História':     acertos_historia,
    'Matemática':   acertos_matematica,
    'Física':       acertos_fisica,
    'Química':      acertos_quimica,
    'Geografia':    acertos_geografia,
    'Biologia':     acertos_biologia
}

for disciplina, acertos in disciplinas_acertos.items():
    peso = pesos_curso[disciplina_peso_map[disciplina]]
    dados_aluno.append({
        'Disciplina': disciplina,
        'Peso': peso,
        'Acertos': acertos,
        'Média': medias[disciplina],
        'Des. Padrão': desvios[disciplina]
    })

# Transformar em DataFrame
df_acertos = pd.DataFrame(dados_aluno)

# Calcular Escore Padronizado
df_acertos['Notas'] = df_acertos.apply(
    lambda x: 500 + ((x['Acertos'] - x['Média']) / x['Des. Padrão']) * 100,
    axis=1
)

# Calcular a Nota Ponderada
df_acertos['Nota Ponderada'] = df_acertos['Peso'] / df_acertos['Notas']

# Calcular a média ponderada total
nota_final = df_acertos['Peso'].sum() / df_acertos['Nota Ponderada'].sum() 

print()
# Mostrar a tabela formatada
st.subheader("Tabela de Notas")
 
df_formatada = df_acertos[['Disciplina', 'Peso', 'Acertos', 'Notas', 'Média', 'Des. Padrão']]
df_formatada.set_index('Disciplina', inplace=True)

# Exibir a tabela formatada
st.dataframe(
    df_formatada.style.format(
        {'Peso': '{:.0f}', 'Acertos': '{:.2f}', 
         'Média': '{:.4f}', 'Des. Padrão': '{:.4f}', 
         'Notas': '{:.2f}'}
    )
)


# Exibir a nota final
st.subheader(f"Nota Final: {nota_final:.2f}")

#Filtrar os dados pelo curso selecionado
df_pesos_filtrado = df_pesos[df_pesos['CURSO'] == curso_selecionado]

# Verificar se o curso foi encontrado
if not df_pesos_filtrado.empty:
    # Selecionar as colunas desejadas
    colunas_desejadas = ['CURSO', 'Densidade 2023',	'Ampla Concorrência',	'Escola Pública']    
    df_resultado = df_pesos_filtrado[colunas_desejadas]
    df_resultado.set_index('CURSO', inplace=True)  
    
    # Transpor o DataFrame
    df_transposto = df_resultado.T
    
    # Exibir a tabela no Streamlit
    st.subheader("Notas de Corte")
    st.dataframe(df_transposto)
else:
    st.write('')

st.caption("*Cálculo baseado nos dados da UFRGS 2023")
st.caption("**Não foi considerado as notas de corte após as chamadas")
st.caption("v.2024 Prof. Portal")

            
       