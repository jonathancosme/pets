import streamlit as st
import pandas as pd
import seaborn as sns
from appFuncs import *

def write():
    @st.cache
    def importDataNormalized(dataFile):
        df = pd.read_csv(dataFile)
        df['intake_date'] = pd.to_datetime(df['intake_date'])
        df['dob'] = pd.to_datetime(df['dob'])
        df['count'] = 1
        df = getTotalDayCount(df)
        df = getDayOfWeek(df)
        df = getTotalWeekDayCount(df)
        df['percent'] = df['count'].values / df['date_count'].values
        df = dogAgeAtIntake(df)
        # df = fullNull(df)
        return df


    st.write(
    """
    # Instructions
    1. If you have NOT selected a file, select "Browse files" and chose the intake data csv file
    2. Select the "Upload Data" button!  

    (Please be patient while data and visuals load)

    """)

    uploaded_file = st.file_uploader("Step 1: Select a csv file to upload.")


    st.write(
    """
    ## Question 2: 
    Were there specific days of the week that saw higher intake volumes?

    """)
    
      
    if st.button('Upload Data'):
        df = importDataNormalized(uploaded_file)
        st.write(
        """
        ## Findings
        + Tuesdays and Wednesdays have the most intakes, both in raw numbers, and adjusted for the number of weekdays in the data 


        """)
        
        st.write(
            """
            ## Raw Data
            """
            )
        st.write(st.dataframe(df, width=0, height=0))
        st.write(
            """
            We added a few columns to the dataset above:  
            + count: this is just a value of 1 for each entry
            + date_count: the total number of entries for a particular date
            + weekday: the Sun-Sat value of a date
            + weekday_count: the total number of a Sun-Sat value in the dataset
            + percent: this is count / date_count
            + age_at_intake: this is intake_date - dob
            """
            )
        st.write(
            """
            ## Question 2
            """
            )
        st.write(
            """
            ### Raw intake by weekday
            """
            )
        st.pyplot(plotWeekdaysCountsRaw(df)) 
        st.write(
            """
            ### Average intake by weekday
            """
            )
        st.pyplot(plotWeekdayCountsNormalized(df)) 
        st.write(
            """
            Clearly Tuesday, and Wednesday have the highest intake.  
            I was surprised to see that Sunday was actually one of the lowest.
            """
            )


if __name__ == "__main__":
    write()  
