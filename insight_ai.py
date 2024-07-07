import getpass
import os
import sys
import time
import sqlite3
import pandas as pd
import streamlit as st
import pygwalker as pyg
from vizro_ai import VizroAI
import vizro.plotly.express as px
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain.chains import create_sql_query_chain
from langchain_community.vectorstores import FAISS
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
from pygwalker.api.streamlit import StreamlitRenderer

### Connect SQLite3 Database ###
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
conn = sqlite3.connect("Chinook.db")
cursor = conn.cursor()
table_info = db.table_info

# @st.cache_data
def generate_dataframe(question):
    ### Prompt Strategy ###
    examples = [
        {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
        {
            "input": "Find all albums for the artist 'AC/DC'.",
            "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
        },
        {
            "input": "List all tracks in the 'Rock' genre.",
            "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
        },
        {
            "input": "Find the total duration of all tracks.",
            "query": "SELECT SUM(Milliseconds) FROM Track;",
        },
        {
            "input": "List all customers from Canada.",
            "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
        },
        {
            "input": "How many tracks are there in the album with ID 5?",
            "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
        },
        {
            "input": "Find the total number of invoices.",
            "query": "SELECT COUNT(*) FROM Invoice;",
        },
        {
            "input": "List all tracks that are longer than 5 minutes.",
            "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
        },
        {
            "input": "Who are the top 5 customers by total purchase?",
            "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
        },
        {
            "input": "Which albums are from the year 2000?",
            "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
        },
        {
            "input": "How many employees are there",
            "query": 'SELECT COUNT(*) FROM "Employee"',
        },
    ]

    ### Find out the most semantically relevant examples ###
    # example_selector = SemanticSimilarityExampleSelector.from_examples(
    #     examples,
    #     # OpenAIEmbeddings(openai_api_key = openai_api_key, openai_api_base=selected_base_url),
    #     FAISS,
    #     k=5,
    #     input_keys=["input"],
    # )
    # example_selector.select_examples({"input": "how many artists are there?"})

    ### Dynamic Few-shot Strategy ###
    example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples[:5],
        example_prompt=example_prompt,
        prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
        suffix="User input: {input}\nSQL query: ",
        input_variables=["input", "top_k", "table_info"],
    )
    chain = create_sql_query_chain(llm, db, few_shot_prompt)

    ### Query Validation ###
    system = """Double check the user's {dialect} query for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins
    
    If there are any of the above mistakes, rewrite the query.
    If there are no mistakes, just reproduce the original query without any texting message.
    
    Output the final SQL query only."""

    valid_prompt = ChatPromptTemplate.from_messages(
        [("system", system, ), ("human", "{query}")]
    ).partial(dialect=db.dialect)
    validation_chain = valid_prompt | llm | StrOutputParser()
    full_chain = {"query": chain} | validation_chain
    final_query = full_chain.invoke({"question": question})

    ### Execute the SQL query & insert into dataframe ###
    cursor.execute(final_query)
    answer = cursor.fetchall()

    ### Create a DataFrame from the rows and column names ###
    column_names = [desc[0] for desc in cursor.description]
    answer = pd.DataFrame(answer, columns=column_names)
    st.success('Data is generated successfully!', icon="✅")
    with st.expander(":bookmark_tabs: Data Result", expanded=True):
        st.write(answer)
    st.session_state.df = answer
def stream_data(code_string):
    for word in code_string.split(" "):
        yield word + " "
        time.sleep(0.05)
def generate_answer(prompt):
    vizro_ai = VizroAI(model=llm)
    code_string = vizro_ai._run_plot_tasks(df, prompt, explain=True)
    code_string = code_string['business_insights']
    st.write_stream(stream_data(code_string))
    fig = vizro_ai.plot(df, prompt)
    st.plotly_chart(fig)

### Streamlit UI Configuration ###
st.set_page_config(
    page_title="Insight AI",
    layout="wide"
)
tab1, tab2, tab3 = st.tabs(["Data Agent", "Visual Analyzer", "BI Wizard"])

with st.sidebar:
    st.title("Insight AI :chains:")
    ### Connect OpenAI ###
    user_api_key = st.sidebar.text_input('OpenAI API Key', type='password', placeholder='Open API Key')
    # selected_base_url = st.sidebar.text_input('Proxy', placeholder='Base URL path for API requests')
    if user_api_key:
        openai_api_key = user_api_key
        selected_base_url = "https://api.openai.com/v1"
    else:
        st.warning('Please input OpenAI API key!', icon='⚠')
        openai_api_key = st.secrets["openai_api_key"]
        selected_base_url = st.secrets["selected_base_url"]
        # os.environ["OPENAI_API_KEY"] = getpass.getpass()
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a ChatGPT model', ['gpt-3.5-turbo', 'gpt-4'], key='selected_model')
    selected_temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    selected_top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    llm = ChatOpenAI(openai_api_key=openai_api_key, base_url=selected_base_url, model=selected_model,
                     temperature=selected_temperature, top_p=selected_top_p)
    #####################
    st.write('© 2024 Micky Wong, All Rights Reserved')
    st.markdown("""---""")
    st.sidebar.header("About")
    st.markdown("Transforming natural language into structured data and stunning BI visualizations.")
    st.markdown("Unlock insights from data effortlessly, streamlining analysis workflow and empowering data-driven decision making.")
    st.markdown("Experience the future of data exploration today with innovative GenAI tool.")
    st.markdown("""---""")

with tab1:
    with st.form('data_agent'):
        st.markdown("### Data Agent :open_file_folder: ###")
        question = st.text_area('Enter text:', 'What data you want to extract?')
        submitted = st.form_submit_button('Submit')
        if submitted and openai_api_key.startswith('sk-'):
            generate_dataframe(question)

with tab2:
    st.markdown("### Visual Analyzer :bar_chart: ###")
    uploaded_file = st.file_uploader("Generate Dataset from Data Agenet or Upload your data by CSV file below", type=['csv'])
    if 'df' in st.session_state is not None:
        df = st.session_state.df
        st.success('Data is imported from Data Agent successfully! Please preview from below.', icon="✅")
        pyg_app = StreamlitRenderer(df)
        pyg_app.explorer()
    elif uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success('Data is uploaded successfully! Please preview from below.', icon="✅")
        pyg_app = StreamlitRenderer(df)
        pyg_app.explorer()
        st.session_state.df2 = df

with tab3:
    with st.form('bi_wizard'):
        st.markdown("### BI Wizard :crystal_ball: ###")
        prompt = st.text_area('Enter text:', 'What diagram you want to generate?')
        generated = st.form_submit_button('Generate')

        if 'df' in st.session_state is not None:
            df = st.session_state.df
            st.success('Data is imported from Data Agent successfully! Please preview from below.', icon="✅")
            with st.expander (":mag: Dataframe Preview (10 rows)"):
              st.write(df.head(10))
        elif 'df2' in st.session_state is not None:
            df = st.session_state.df2
            st.success('Data is uploaded successfully! Please preview from below.', icon="✅")
            with st.expander(":mag: Dataframe Preview (10 rows)"):
             st.write(df.head(10))
        else:
            st.warning("No dataset from Data Agent or upload file.", icon='⚠')

        if generated and openai_api_key.startswith('sk-'):
            if prompt:
                with st.spinner('Wait for it...'):
                    generate_answer(prompt)
            else:
                st.warning("Please enter a prompt.", icon='⚠')
