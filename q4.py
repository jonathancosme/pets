import streamlit as st
import pandas as pd
import seaborn as sns
from appFuncs import *

def write():
    @st.cache
    def getWeatherMerged(dataFile):
        df = pd.read_csv(dataFile)
        df['intake_date'] = pd.to_datetime(df['intake_date'])
        df['dob'] = pd.to_datetime(df['dob'])
        df['count'] = 1
        df = mergeWithWeatherDF(df)
        return df


    st.write(
    """
    # Question 4: 
    Surprise us! Using the data, please provide a visualization that gives a unique insight into the data.

    """)

    st.write(
    """
    ## Analysis
    Given the recent snow debacle of Austin, I am curious about the impact of weather on intakes!  
    I'm also from Florida and personally I didn't like going out in the rain.  


    I've downloaded historic daily weather data for 2020 for Austin, and I'm going to run a simple regression
    on daily intakes vs temperature, humidity, and precipiation.  
    Since I imagine the relationship to be of degree order 2 (i.e. not an exact linear relationship), I will include
    squared terms for each variable.
    
    """)
    

    uploaded_file = st.file_uploader("Step 1: Select a photo to upload.")
    
      
    if st.button('Upload Data'):
        df = getWeatherMerged(uploaded_file)
        st.write(
            """
            ### Daily intake total merged with Austin weather data
            """
            )
        st.write(st.dataframe(df, width=0, height=0))
        st.write(
            """
            ### OLS model results
            + x1: daily avg temperature
            + x2: daily avg humidity
            + x3: daily avg precipitation
            + x4: daily avg temperature^2
            + x5: daily avg humidity^2
            + x6: daily avg precipitation^2
            """
            )
        st.code(getOLSResults(df))
        st.write(
            """
            According to our OLS model, it appears temperature has a statistically significant 
            impact on daily intake.  
            The same cannot be said of humidity, which does not seem to have an impact at all.  
            Precipitation might have an impact, but the evidence is not strong. 
            """
            )
        st.write(
            """
            ### Residual plot
            """
            )
        st.pyplot(plotResids(getUpdatedResults(df)))
        st.write(
            """
            ### Conclusion
            Although temperature does seem to have an impact, the impact itself seems to be negligible.  
            It looks like month and day of week have a more significant effect.   
            If I were to explore this particular relationship further, I'd try to obtain hourly data (both for intake, 
            and weather data), and explore that relationship. 
            """
            )



if __name__ == "__main__":
    write()  