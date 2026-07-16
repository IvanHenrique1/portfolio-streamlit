import streamlit as st
import pandas as pd
import os
import random

# --- FUNÇÃO PARA CARREGAR CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Configuração da página
st.set_page_config(page_title="Meu Portfólio de Dados", page_icon="📊", layout="wide")

# --- CARREGAR ARQUIVOS CSS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
css_file_path = os.path.join(script_dir, "style.css")
load_css(css_file_path) # Carrega as animações e estilos
st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.15.1/devicon.min.css">', unsafe_allow_html=True) # Carrega ícones

# Cabeçalho
st.write("") # Espaço para o CSS carregar e evitar pular o título

st.title("Olá! Eu sou o Ivan Henrique 👋")
st.subheader("Analista de Performance e Dados | Python • SQL • Power BI")

st.write("""
Sou movido a transformar complexidade em simplicidade: dados viram insights, tarefas 
repetitivas viram assistentes automatizados, sistemas frágeis viram soluções confiáveis. 
Uso Python, PostgreSQL e automação de interface (Selenium, PyAutoGUI) para construir pipelines 
e ferramentas que devolvem tempo às equipes. 
         
Minha trajetória em tecnologia começou há mais de 5 anos, atuando inicialmente com suporte ao usuário e 
infraestrutura. Essa experiência me proporcionou uma visão ampla dos processos de TI, além de desenvolver 
uma forte capacidade de resolução de problemas, análise e melhoria contínua.

Hoje atuo na área de dados, desenvolvendo soluções para diferentes áreas do negócio, como Comercial, 
Logística e Gerenciamento de Risco. Meu foco é transformar necessidades operacionais em soluções escaláveis 
por meio de análise de dados, automação e inteligência de negócios.

Explore alguns dos meus projetos abaixo e veja como essas soluções foram aplicadas na prática!
""")

st.divider() # Linha de separação

# Seção de Tecnologias
st.header("Tecnologias e Ferramentas")
st.write("Estas são algumas das ferramentas e tecnologias que utilizo no meu dia a dia.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Linguagens e Bancos")
    st.markdown("""
        <p><i class="devicon-python-plain" style="font-size: 1.2em;"></i> Python</p>
        <p><i class="devicon-postgresql-plain" style="font-size: 1.2em;"></i> SQL (PostgreSQL)</p>
    """, unsafe_allow_html=True)
with col2:
    st.subheader("Análise e Visualização")
    st.markdown("""
        <p><i class="devicon-pandas-original" style="font-size: 1.2em;"></i> Pandas</p>
        <p><i class="devicon-rstudio-plain" style="font-size: 1.2em; color: #FF4B4B;"></i> Streamlit</p>
        <div style="display: flex; align-items: center; gap: 8px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#F2C811" viewBox="0 0 24 24"><path d="M12.501.001H0v24h12.501a11.5 11.5 0 0 0 0-23.998zM10 18.5H2.5v-5H10v5zm0-7.5H2.5v-5H10v5z"/></svg>
            <span>Power BI</span>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.subheader("Automação e Outros")
    st.markdown("""
        <p><i class="devicon-selenium-original" style="font-size: 1.2em;"></i> Selenium</p>
        <p><i class="devicon-pytest-plain" style="font-size: 1.2em;"></i> PyAutoGUI</p>
        <p><i class="devicon-github-original" style="font-size: 1.2em;"></i> Git & GitHub</p>
    """, unsafe_allow_html=True)

st.divider()

# Seção de Projetos
st.header("Meus Projetos")

# --- Projeto 1 ---
with st.container(border=True):
    st.subheader("Consolidação de Dados de Faturamento Multiempresa")
    st.write("**Tecnologias usadas:** Python, DAX, PowerBI, PostgreSQL")
    st.write("""
        **Problema:** Os dados de faturamento estavam distribuídos em 32 bancos independentes, um para cada operação. Essa arquitetura dificultava análises consolidadas, exigia consultas separadas e aumento do tempo para geração de indicadores.
        
        **Solução:** Desenvolvi um processo de consolidação utilizando consultas SQL (UNION ALL), unificando os dados das diferentes operações em uma única visão analítica. Após a padronização das informações, os dados eram disponibilizados em um dashboard com mais de 1 milhão de linhas exibidas em indicadores, filtros dinâmicos e análises de faturamento por produto, depósito, cliente e período.
    """)

    try:
        # 2. Função para buscar e tratar os dados
        @st.cache_data(ttl=3600) # Cache de 1 hora
        def fetch_data():
            # Pega a conexão DENTRO da função para garantir que ela esteja sempre ativa
            conn = st.connection("neon_db", type="sql")

            # Puxa um número aleatório de linhas entre 200 e 500
            random_limit = random.randint(200, 500)
            df = conn.query(f"SELECT * FROM vendas LIMIT {random_limit};", ttl=600)
            
            # --- MANOBRA NOS DADOS ---
            # Renomeia valores inadequados antes de qualquer análise
            if 'NomeDeposito' in df.columns:
                df['NomeDeposito'] = df['NomeDeposito'].replace('Pinto', 'Fernandes')

            # Identifica os 5 depósitos com maior volume e filtra o dataframe
            if not df.empty and 'NomeDeposito' in df.columns:
                top_5_depositos_por_volume = df.groupby('NomeDeposito')['Volume'].sum().nlargest(5).index
                df = df[df['NomeDeposito'].isin(top_5_depositos_por_volume)]
            
            return df

        df_vendas = fetch_data() # Carrega os dados brutos

        # --- LAYOUT DO DASHBOARD ---
        st.write("---")
        st.write("#### 📈 **Dashboard de Análise**")
        st.write(f"📄 Analisando **{len(df_vendas)}** registros • 🔒 Dados Reais Anonimizados • 🟢 PostgreSQL Cloud")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Vendas", f"R$ {df_vendas['ValorTotalNF'].sum():,.2f}" if not df_vendas.empty else "R$ 0,00")
        col2.metric("Nº de Notas Fiscais", f"{df_vendas['NumeroNF'].nunique():,}" if not df_vendas.empty else "0")
        col3.metric("Ticket Médio", f"R$ {df_vendas['ValorTotalNF'].mean():,.2f}" if not df_vendas.empty else "R$ 0,00")

        st.write("##### Faturamento por Produto")
        if not df_vendas.empty:
            # Agrupa os dados por produto e soma o valor total da nota fiscal
            faturamento_por_produto = df_vendas.groupby('Produto')['ValorTotalNF'].sum().sort_values(ascending=False)
            st.bar_chart(faturamento_por_produto)
            st.caption("☁️ Consulta em tempo real a uma base PostgreSQL de homologação hospedada em nuvem, contendo dados reais anonimizados.")

            st.write("##### Volume por Depósito")
            # Agrupa os dados por depósito e soma o volume
            volume_por_deposito = df_vendas.groupby('NomeDeposito')['Volume'].sum().sort_values(ascending=False)
            st.bar_chart(volume_por_deposito)

            st.caption("☁️ Consulta em tempo real a uma base PostgreSQL de homologação hospedada em nuvem, contendo dados reais anonimizados.")
        else:
            st.info("Nenhum dado para exibir o gráfico.")

    except Exception as e:
        st.error(f"Não foi possível conectar ao banco de dados ou carregar os dados. Verifique suas configurações. Erro: {e}")

st.write("") # Adiciona um espaço vertical

# --- Projeto 2 (Exemplo) ---
with st.container(border=True):
    st.subheader("Pipeline de Sincronização Incremental de Documentos Fiscais")
    st.write("**Tecnologias usadas:** Python, PostgreSQL, Selenium, PowerBI.")
    st.write("""
        **Problema:** A consulta de notas fiscais era realizada manualmente em uma plataforma centralizadora, exigindo que diferentes operadores extraíssem repetidamente os mesmos relatórios ao longo do dia. Além do retrabalho e da demora na disponibilização das informações, a integração oficial via API possuía um custo que inviabilizava sua utilização na empresa.
        
        **Solução:** Desenvolvi um pipeline de sincronização incremental em Python que automatizava a extração das notas fiscais, validava os registros já existentes e realizava uma carga incremental apenas das novas notas fiscais. Os dados sincronizados eram disponibilizados em um dashboard com filtros dinâmicos, reduzindo a defasagem das informações para aproximadamente 2 minutos e eliminando a necessidade de consultas manuais recorrentes.
             
        **Impacto:** Eliminou consultas manuais repetitivas, reduziu o tempo de disponibilização das informações para aproximadamente 2 minutos e dispensou a contratação de uma API comercial para integração dos dados.
    """)

    # Use st.link_button para criar um botão que leva a um link externo
    st.link_button("Ver o código no GitHub", "https://github.com/IvanHenrique1/sincronizacao_incremental_de_documentos_fiscais") # <-- TROQUE PELO LINK REAL

    st.write(f"⏱️ Defasagem máxima: ~2 minutos • 🔄 Sincronização incremental • 🤖 Processo 100% automatizado • 📊 Dashboard em tempo real")

    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; font-family: sans-serif; margin-top: 20px;">
            <div style="border: 1px solid #4A4A4A; border-radius: 5px; padding: 10px 20px; margin-bottom: 10px; background-color: #262730; text-align: center;">🌐 Plataforma Fiscal. <br><small style="color: #9A9A9A;">ex: Jettax, Qive</small></div>
            <div style="font-size: 24px; color: #4A4A4A; line-height: 0.5;">↓</div>
            <div style="border: 1px solid #4A4A4A; border-radius: 5px; padding: 10px 20px; margin-top: 10px; margin-bottom: 10px; background-color: #262730; text-align: center;">🤖 Extração Automatizada<br><small style="color: #9A9A9A;">Selenium + PyAutoGUI</small></div>
            <div style="font-size: 24px; color: #4A4A4A; line-height: 0.5;">↓</div>
            <div style="border: 1px solid #4A4A4A; border-radius: 5px; padding: 10px 20px; margin-top: 10px; margin-bottom: 10px; background-color: #262730; text-align: center;">🔍 Validação Incremental<br><small style="color: #9A9A9A;">Pandas + PostgreSQL</small></div>
            <div style="font-size: 24px; color: #4A4A4A; line-height: 0.5;">↓</div>
            <div style="border: 1px solid #4A4A4A; border-radius: 5px; padding: 10px 20px; margin-top: 10px; margin-bottom: 10px; background-color: #262730; text-align: center;">💾 Inserção em Banco Interno<br><small style="color: #9A9A9A;">Pandas + PostgreSQL</small></div>
            <div style="font-size: 24px; color: #4A4A4A; line-height: 0.5;">↓</div>
            <div style="border: 1px solid #4A4A4A; border-radius: 5px; padding: 10px 20px; margin-top: 10px; margin-bottom: 10px; background-color: #262730; text-align: center;">📊 Dashboard Gerencial<br><small style="color: #9A9A9A;">Power BI conectado ao PostgreSQL</small></div>
        </div>
    """, unsafe_allow_html=True)

    st.caption("Execução automática agendada, garantindo atualização contínua dos dados sem intervenção manual.")
    

st.write("") # Adiciona um espaço vertical

st.divider()

# Contato
st.header("Bora trocar uma ideia?")
st.write("Me chame no [LinkedIn](https://www.linkedin.com/in/ivan-henrique-santos-616497190/) ou mande um e-mail para ivan.henrique.s.1406@gmail.com.")