import streamlit as st

#### PAGE SETUP ####

pages = {
    "App Navigation": [
        # st.Page("./app.py", title="Home"),
    ],
    "front page": [
        # st.Page("./pages/filename here.py", title="page title here"),
        ],
    "calculate / adjust recipes": [
        # st.Page("./pages/filename here..py", title="page title her"),
    ],
    "others ": [
        # st.Page("./pages/page_approach.py", title="Approach"),
        # st.Page("./pages/page_resources.py", title="Resources"),,
        # st.page_link("https://github.com/yukaberry/ai_gen_recipe", label="Github repo")
    ],
}

pg = st.navigation(pages)
pg.run()

st.sidebar.page_link(
    page="https://github.com/yukaberry/ai_gen_recipe",
    label="Github repo "
)
