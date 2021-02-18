

import streamlit as st
import awesome_streamlit as ast
import pandas as pd

import instructions
import q1
import q2
import q3
import q4

PAGES = {
    "Instructions": instructions,
    "Question 1": q1,
    "Question 2": q2,
    "Question 3": q3,
    "Question 4": q4,
    }


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Steps", list(PAGES.keys()))
    
    page = PAGES[selection]
    
    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    

if __name__ == "__main__":
    main()
