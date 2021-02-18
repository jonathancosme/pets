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

    # @st.cache
    # def importDataRaw(dataFile):
    #     df = pd.read_csv(dataFile)
    #     df['intake_date'] = pd.to_datetime(df['intake_date'])
    #     df['dob'] = pd.to_datetime(df['dob'])
    #     df['count'] = 1
    #     df = getTotalDayCount(df)
    #     df = getDayOfWeek(df)
    #     df = getTotalWeekDayCount(df)
    #     df = dogAgeAtIntake(df)
    #     # df = fullNull(df)
    #     return df


    st.write(
    """
    # Instructions
    1. Select "Browse files" and chose the intake data csv file
    2. Select the "Upload Data" button!  

    """)

    uploaded_file = st.file_uploader("Step 1: Select a csv file to upload.")

#    st.write(
#        """
#        We apply a moving average in order to smooth out the data, and visualize trends more easily.  
#        Using a moving Moving Average Days value of 1 will show the normal (un-smoothed) data. 
#        """
#        )
#    movingAverageDays = st.number_input('Moving Average Days', 30)

    st.write(
    """
    ## Question 1: 
    Were there specific days of the week that saw higher intake volumes?

    """)


    st.write(
    """
    ## Analysis
    Wherever possible, we display two data plots:  
    + raw
    + normalized  

    The raw plot is just that: raw data.  
    The normalized plot displays items as a percent of the day's intake.  
    For example if 20 dogs were taken in on a certain date, and there were 
    40 total intakes for that date, then the value for dog intakes would be 0.5   


    """)
    
      
    if st.button('Upload Data'):
        df = importDataNormalized(uploaded_file)
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
            + date_count: he total number of entries for a particular date
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
