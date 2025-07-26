import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Для чтения PDF и DOCX
import pdfplumber
import docx

# Функция для чтения PDF
def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    # Пример: разбить текст на строки и сделать DataFrame
    lines = [line for line in text.split('\n') if line.strip()]
    df = pd.DataFrame({'text': lines})
    return df

# Функция для чтения DOCX
def read_docx(file):
    doc = docx.Document(file)
    lines = [para.text for para in doc.paragraphs if para.text.strip()]
    df = pd.DataFrame({'text': lines})
    return df

st.title("Анализ данных в разных форматах (csv, xlsx, pdf, docx)")

uploaded_file = st.file_uploader("Загрузите файл (csv, xlsx, pdf, docx)", type=["csv", "xlsx", "pdf", "docx"])

df = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.pdf'):
            df = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            df = read_docx(uploaded_file)
        else:
            st.error("Неподдерживаемый формат файла")
    except Exception as e:
        st.error(f"Ошибка при чтении файла: {e}")

if df is not None:
    st.write("Первые строки данных:")
    st.write(df.head())
    try:
        # Не передаем config_file вообще!
        pr = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
        st_profile_report(pr)
    except Exception as e:
        st.error(f"Ошибка при генерации отчета: {e}")