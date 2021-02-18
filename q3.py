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
        df = fullNull(df)
        return df


    st.write(
    """
    # Question 1: 
    Where are there holes in the data? hint: think about providing an analysis that a shelter operations director 
    might be able to use to try and tell how staff are doing with proper data input.

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
    

    uploaded_file = st.file_uploader("Step 1: Select a photo to upload.")

    st.write(
        """
        We apply a moving average in order to smooth out the data, and visualize trends more easily.  
        Using a moving Moving Average Days value of 1 will show the normal (un-smoothed) data. 
        """
        )
    movingAverageDays = st.number_input('Moving Average Days', 30)
    
      
    if st.button('Upload Data'):
        df = importDataNormalized(uploaded_file)
        st.write(
            """
            ## Example empty fields visuals
            """
            )
        st.write(
            """
            ### src_intake_subtype over time
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_subtype', as_percent=True))
        st.write(
            """
            ### src_intake_reason over time
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_reason', as_percent=True))
        st.write(
            """
            We see that src_intake_subtype and src_intake_reason are often left empty.  
            src_intake_reason is left empty around 50% of the time in the second half of the year.
            """)
        st.write(
            """
            ## tables of empty entries
            """
            )
        st.write(st.dataframe(getEmptyField(df, fieldName='dob'), width=0, height=0))
        st.write(st.dataframe(getEmptyField(df, fieldName='src_intake_subtype'), width=0, height=0))
        st.write(st.dataframe(getEmptyField(df, fieldName='src_intake_reason'), width=0, height=0))
        st.write(st.dataframe(getEmptyField(df, fieldName='src_found_zip_code'), width=0, height=0))
        # st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_primary_breed')) 
        st.write(
            """
            ## 0 value zip code
            """
            )
        st.write(st.dataframe(getZeroField(df, fieldName='src_finders_zip_code'), width=0, height=0))
        st.write(
            """
            ## Negative Age
            """
            )
        st.write(st.dataframe(getNegAge(df), width=0, height=0))
        st.write(
            """
            These are entries where the dob is greater than the intake date.  
            There are two possibilities:  
            + human error
            + intake animal was pregnant and had babies later on?
            """)



if __name__ == "__main__":
    write()  