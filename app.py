import streamlit as st

pages = {
    "Калькулятори": [
        st.Page("./pages/article.py", title="Авторська стаття"),
        st.Page("./pages/translation.py", title="Переклад"),
    ],
}

pg = st.navigation(pages)
pg.run()
