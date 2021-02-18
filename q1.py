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
    # Question 1: 
    How did intakes trend over time and were there any sub populations that saw unusual trends when compared to the whole?

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
            ## Question 1
            """
            )
        st.write(
            """
            ### Species over time raw
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='species'))
        st.write(
            """
            ### Species over time normalized
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='species', as_percent=True))
        st.write(
            """
            It appears that the early months of the year have the greatest intake.  
            Also dogs are the overwhelming majority of intakes, and cats come in at second.  
            I am curious about "other" species are taken in...
            """
            )
        st.write(
            """
            ### src_intake_type over time raw
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_type'))
        st.write(
            """
            ### src_intake_type over time normalized
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_type', as_percent=True))
        st.write(
            """
            STRAY intakes appear to make up the majority of intakes, but it looks like after June, 
            STRAY intake decreases, while OWNER SUR increases.  
            We also notice that, although CONFISCATE has a cylclical behavior, it appears to be generally
            increasing (slightly) over time.
            """)
        st.write(
            """
            ### src_intake_subtype over time raw
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_subtype'))
        st.write(
            """
            ### src_intake_subtype over time normalized
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_subtype', as_percent=True))
        st.write(
            """
            Although OTC is the largest subtype, the trend is generally decreasing over over the year.  
            OTC OWNED decreases until about mid-year, then begins to increase again.  
            FIELD intakes appear to be increasing throughout the year.
            """)
        st.write(
            """
            ### src_intake_reason over time raw
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_reason'))
        st.write(
            """
            ### src_intake_reason over time normalized
            """
            )
        st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_intake_reason', as_percent=True))
        st.write(
            """
            STRAY and TOO MANY account for a large portion of intakes.  
            ILL showed an unusual increase in the middle 50% of the year.  
            OWNER PROB intakes increased in the second half of the year.
            """)
        # st.pyplot(plotOverTime(df, MA_days=movingAverageDays, hueCol='src_primary_breed')) 
        st.write(
            """
            ### age_at_intake (in years) over time
            """
            )
        st.pyplot(plotAge(df)) 
        st.write(
            """
            It looks like most intakes had and age less than 5 years.
            """)



if __name__ == "__main__":
    write()  