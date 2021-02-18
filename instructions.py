import streamlit as st

def write():

    
    st.write(
    """
    # Instructions

    Go to one of the questions, upload the intake data csv file, and select the upload button!  

    Please give it a few minutes to finish loading (especially question 1); there are lots of visuals.

    In addition, you can find instructions for the following below:
    + enlarge tables and visuals
    + save an excel sheet as a csv file  

    Please note ONLY csv files can be uploaded into the app.  
    Please see below for instruction on how to convert an excel sheet into a csv file
    """)

    st.write(
    """
    ## Enlarge tables and visuals

    Tables and visuals can be expanded by hovering over the object, and selecting the
    arrows at the top right corver. 
    """)
    st.image('./images/visual.png', width=800)
    st.image('./images/table.png', width=800)

    st.write(
    """
    ## Save an excel sheet as a .csv file 
    """)
    st.image('./images/1.png', width=800)
    st.image('./images/2.png', width=800)
    st.image('./images/3.png', width=800)
    st.image('./images/4.png', width=800)
    st.image('./images/5.png', width=800)



if __name__ == "__main__":
    write()  
