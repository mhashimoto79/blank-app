import streamlit as st
from Utilities.StreamlitHelper import initialize_page

initialize_page(page_title="TEA Supporter", page_icon="📝")

st.sidebar.success("機能を選んでください。")

st.markdown(
    """
    **TEA Supporter**はAIをTEAに活用し、様々な作業の効率化、スマート化を図るためのツールです。\n
    TEA Supporterは各機能から構成されています。\n
    **👈左のサイドバーから使いたい機能を選んでください。**
    ### 機能一覧
    - 音声文字起こし
    - インタビューデータ(テキスト)の解析
    """
)