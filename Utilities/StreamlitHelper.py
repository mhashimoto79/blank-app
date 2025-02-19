import streamlit as st
from streamlit_js_eval import streamlit_js_eval

def update_windows_size():
    with st.empty():
        windows_height = 800
        value = streamlit_js_eval(js_expressions='windows.parent.innerHeight', key='HEIGHT', want_output = True,)
        if value is not None:
            windows_height = value
        st.session_state["WINDOW_HEIGHT"] = windows_height

def get_windows_height():
    return st.session_state.get("WINDOW_HEIGHT", 800)

def hide_top_bar():
    css = f'''
<style>
    .stApp > header {{
        padding-top:0rem;
        height:0rem;
    }}
    div.block-container{{
        padding-top:0rem;
        padding-buttom:0rem;
    }}
    h1 {{
        padding:0.25rem 0px 0rem;
    }}
    .st-emotion-cache-1jicfl2 {{
        padding-left:1rem;
        padding-right:1rem;
    }}
    #MainMenu {{visibility:hidden;}}
    .stAppDeployButton {{display:none;}}
    footer {{visibility:hidden;}}
    #stDecoration {{display:none;}}
</style>
'''
    st.markdown(
        css,
        unsafe_allow_html=True,
    )

def initialize_page(page_title:str, page_icon:str, layout:str="wide"):
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    hide_top_bar()
    col1, col2, col3 = st.columns([4,2,1])
    with col1:
        st.markdown(f"# {page_title}")