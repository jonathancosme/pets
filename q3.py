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
    # Instructions
    1. If you have NOT selected a file, select "Browse files" and chose the intake data csv file
    2. (optional) change Moving Average value
    3. Select the "Upload Data" button!  

    (Please be patient while data and visuals load)

    """)

    uploaded_file = st.file_uploader("Step 1: Select a csv file to upload.")

    st.write(
        """
        We apply a moving average in order to smooth out the data, and visualize trends more easily.  
        Using a moving Moving Average Days value of 1 will show the normal (un-smoothed) data. 
        """
        )
    movingAverageDays = st.number_input('Moving Average Days', value=30)

    st.write(
    """
    ## Question 3: 
    Where are there holes in the data? hint: think about providing an analysis that a shelter operations director 
    might be able to use to try and tell how staff are doing with proper data input.

    """)


      
    if st.button('Upload Data'):
        df = importDataNormalized(uploaded_file)
        st.write(
            """
            ## Findings
            + src_intake_subtype being left as an empty field occured lease frequently around the 2nd quarter of the year, increased during the middle of the year, 
            and slowly stared decreasing towards the end of the year.
            + src_intake_reason being left as an empty field has increased since inception, and has remained high (a little under 50%).
            + dob and src_found_zip_code are also sometimes left empty.
            + There are some 0 valued entries for src_finders_zip_code. This might be because:  
                + human error
                + unknown zip code, but field is required, so 0 was entered 
            + There are entries where age is negative (dob occurs later than intake date). This might be because:  
                + human error
                + intake animal was pregnant and had babies later on?
            """)
        
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
