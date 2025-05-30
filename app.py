import streamlit as st

pages = {
    "Калькулятори": [
        st.Page("./pages/translation.py", title="Переклад"),
        st.Page("./pages/article.py", title="Авторська стаття"),
    ],
}

pg = st.navigation(pages)
pg.run()
