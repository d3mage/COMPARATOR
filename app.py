import streamlit as st

pages = {
    "Калькулятори": [
        st.Page("./pages/article.py", title="Авторська стаття"),
        st.Page("./pages/translation.py", title="Переклад"),
        st.Page("./pages/editor.py", title="Редактор"),
    ],
}

pg = st.navigation(pages)
pg.run()