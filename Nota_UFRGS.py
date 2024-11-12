import streamlit as st
import pandas as pd

# Título do App
st.title("Cálculo da Nota - UFRGS")

# Carregar o arquivo fixo de pesos
pesos_file = 'Pesos_UFRGS.xlsx'
df_pesos = pd.read_excel(pesos_file, engine='openpyxl')
    
#Criação das colunas para entrada de acertos
st.subheader("Escolha o curso e a língua estrangeira")

# Selecionar o curso
cursos = df_pesos['CURSOS'].unique()
#curso_selecionado = st.selectbox("Escolha o curso:", cursos)
curso_selecionado = st.selectbox("Escolha o curso:", cursos, index=list(cursos).index('Medicina - Bacharelado'))

# Selecionar o língua estrangeira
lingua_estrangeira = st.selectbox("Escolha a Língua Estrangeira:", ['Inglês', 'Espanhol', 'Italiano', 'Francês', 'Alemão'])

# Obter os pesos do curso selecionado
pesos_curso = df_pesos[df_pesos['CURSOS'] == curso_selecionado].iloc[0]

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
st.subheader("Preencha os acertos para cada disciplina")

# Usar as colunas para reduzir o espaço
col1, col2 = st.columns(2)

# Primeira coluna para os primeiros 5 campos
with col1:
    acertos_portugues = st.number_input("Acertos em Português:", min_value=0, max_value=15, step=1)
    acertos_redacao = st.number_input("Nota em Redação:", min_value=0.0, max_value=15.0, step=0.05)
    acertos_literatura = st.number_input("Acertos em Literatura:", min_value=0, max_value=15, step=1)
    acertos_historia = st.number_input("Acertos em História:", min_value=0, max_value=15, step=1)
    acertos_matematica = st.number_input("Acertos em Matemática:", min_value=0, max_value=15, step=1)

# Segunda coluna para os próximos 5 campos
with col2:
    acertos_lingua = st.number_input(f"Acertos em {lingua_estrangeira}:", min_value=0, max_value=15, step=1)
    acertos_fisica = st.number_input("Acertos em Física:", min_value=0, max_value=15, step=1)
    acertos_quimica = st.number_input("Acertos em Química:", min_value=0, max_value=15, step=1)
    acertos_geografia = st.number_input("Acertos em Geografia:", min_value=0, max_value=15, step=1)
    acertos_biologia = st.number_input("Acertos em Biologia:", min_value=0, max_value=15, step=1)

# Adiciona o botão
st.button("Atualizar")

# Cálculo de escore bruto para Português e Redação
acertos_port_red = acertos_portugues + acertos_redacao
peso_port_red = pesos_curso[disciplina_peso_map['Português e Redação']]

# Lista para armazenar os dados de entrada
dados_aluno = [
    {
        'Disciplina': 'Português e Redação',
        'Peso': peso_port_red,
        'Escore Bruto (Acertos)': acertos_port_red,
        'Média': medias['Português e Redação'],
        'Desvio Padrão': desvios['Português e Redação']
    }
]

# Adicionar dados de língua estrangeira
peso_lingua = pesos_curso[disciplina_peso_map['Língua Estrangeira']]

dados_aluno.append({
    'Disciplina': lingua_estrangeira,
    'Peso': peso_lingua,
    'Escore Bruto (Acertos)': acertos_lingua,
    'Média': medias[lingua_estrangeira],
    'Desvio Padrão': desvios[lingua_estrangeira]
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
        'Escore Bruto (Acertos)': acertos,
        'Média': medias[disciplina],
        'Desvio Padrão': desvios[disciplina]
    })

# Transformar em DataFrame
df_acertos = pd.DataFrame(dados_aluno)

# Calcular Escore Padronizado
df_acertos['Escore Padronizado'] = df_acertos.apply(
    lambda x: 500 + ((x['Escore Bruto (Acertos)'] - x['Média']) / x['Desvio Padrão']) * 100,
    axis=1
)

# Calcular a Nota Ponderada
df_acertos['Nota Ponderada'] = df_acertos['Peso'] / df_acertos['Escore Padronizado']

# Calcular a média ponderada total
nota_final = df_acertos['Peso'].sum() / df_acertos['Nota Ponderada'].sum() 

print()
# Mostrar a tabela formatada
st.subheader("Tabela de Notas")
 
df_formatada = df_acertos[['Disciplina', 'Peso', 'Escore Bruto (Acertos)',  'Média', 'Desvio Padrão', 'Escore Padronizado']]
df_formatada.set_index('Disciplina', inplace=True)

# Exibir a tabela formatada
st.dataframe(
    df_formatada.style.format(
        {'Peso': '{:.0f}', 'Escore Bruto (Acertos)': '{:.2f}', 
         'Média': '{:.4f}', 'Desvio Padrão': '{:.4f}', 
         'Escore Padronizado': '{:.2f}'}
    )
)

# Exibir a nota final
st.subheader(f"Nota Final: {nota_final:.2f}")


# Notas de corte para Medicina
notas_corte = {
    "Medicina - Bacharelado": {
        "Ampla Concorrência (AC/A0)": 722.70,
        "Escola Pública (L3/L5)": 717.52,
    }
}

# Exibir notas de corte apenas para Medicina
if curso_selecionado == "Medicina - Bacharelado":
    st.subheader("Notas de Corte")
    for modalidade, nota_corte in notas_corte.get(curso_selecionado, {}).items():
        st.write(f"{modalidade}: {nota_corte:.2f}")
else:
    st.write('')
