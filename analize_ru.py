import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Анализ данных", layout="wide")
st.title("Интерактивный анализ данных (на русском)")

uploaded_file = st.file_uploader("Загрузите файл (csv, xlsx)", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.write("Первые строки данных:")
    st.dataframe(df.head())

    # 1. Тепловая карта корреляций
    st.subheader("Тепловая карта корреляций (числовые переменные)")
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.info("Недостаточно числовых переменных для корреляционной матрицы.")

    # 2. Интерактивный анализ зависимостей
    st.subheader("График зависимости переменных")
    cols = df.columns.tolist()
    x_var = st.selectbox("Выберите переменную по оси X", cols)
    y_var = st.selectbox("Выберите переменную по оси Y", cols, index=1 if len(cols) > 1 else 0)
    if x_var and y_var:
        fig, ax = plt.subplots()
        if pd.api.types.is_numeric_dtype(df[x_var]) and pd.api.types.is_numeric_dtype(df[y_var]):
            ax.scatter(df[x_var], df[y_var], alpha=0.7)
            ax.set_xlabel(x_var)
            ax.set_ylabel(y_var)
            ax.set_title(f"Зависимость {y_var} от {x_var}")
        else:
            df_grouped = df.groupby(x_var)[y_var].mean().reset_index()
            ax.bar(df_grouped[x_var].astype(str), df_grouped[y_var])
            ax.set_xlabel(x_var)
            ax.set_ylabel(f"Среднее {y_var}")
            ax.set_title(f"Среднее {y_var} по {x_var}")
            plt.xticks(rotation=45)
        st.pyplot(fig)

    # 3. Столбчатые графики по каждой переменной
    st.subheader("Столбчатые графики по переменным")
    for col in df.columns:
        st.markdown(f"**{col}**")
        fig, ax = plt.subplots()
        if pd.api.types.is_numeric_dtype(df[col]):
            ax.hist(df[col].dropna(), bins=20, color='skyblue')
            ax.set_xlabel(col)
            ax.set_ylabel("Частота")
        else:
            df[col].value_counts().head(20).plot(kind='bar', ax=ax, color='orange')
            ax.set_xlabel(col)
            ax.set_ylabel("Частота")
            plt.xticks(rotation=45)
        st.pyplot(fig)
