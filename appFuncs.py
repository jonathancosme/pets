import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm  
sns.set_style("darkgrid")
sns.set_context("paper")
sns.set(rc={'figure.figsize':(15, 10)})

weekdayDict = { 0: 'monday',
1: 'tuesday',
2: 'wednesday',
3: 'thursday',
4: 'friday',
5: 'saturday',
6: 'sunday',
}

def fullNull(df):
    for cur_col in df.columns.values:
        temp_mask = df[cur_col].isnull().values
        if any(temp_mask):
            df[cur_col].iloc[temp_mask] = '(EMPTY)'
    return df

def getTotalDayCount(df):
	dateDicts = df.groupby('intake_date').sum()['count'].to_dict()
	df['date_count'] = df.apply(lambda x: dateDicts[x['intake_date']], axis=1)
	return df

def getDayOfWeek(df):
	df['weekday'] = pd.to_datetime(df['intake_date']).dt.weekday
	df['weekday'] = df.apply(lambda x: weekdayDict[x['weekday']], axis=1)
	return df

def getTotalWeekDayCount(df):
	dayDicts = pd.to_datetime(df['intake_date'].unique()).weekday.value_counts().to_dict()
	df['weekday_count'] = df.apply(lambda x: dayDicts[x['intake_date'].weekday()], axis=1)
	return df

def dogAgeAtIntake(df):
    df['age_at_intake'] = df['intake_date'] - df['dob']
    df['age_at_intake'] = df['age_at_intake'] / pd.Timedelta(365, 'day')
    return df

def plotOverTime(df, MA_days=1, hueCol='species', as_percent=False):
	if as_percent:
		yCol = 'percent'
		
	else:
		yCol = 'count'
	rolling_df = df.groupby([hueCol, 'intake_date']).sum()[yCol].rolling(MA_days).mean().reset_index()
	fig, ax1 = plt.subplots(1)
	sns.lineplot(data=rolling_df, x='intake_date', y=yCol, hue=hueCol, ax=ax1)
	plt.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1)
	return fig

def plotWeekdaysCountsRaw(df):
	weekday_df = df.groupby(['weekday']).sum()['count'].reset_index()
	fig, ax1 = plt.subplots(1)
	sns.barplot(data=weekday_df, y='weekday', x='count', ax=ax1, color='gray', order=['sunday',
                                                                 'monday',
                                                                 'tuesday',
                                                                 'wednesday',
                                                                 'thursday',
                                                                 'friday',
                                                                 'saturday',])
	return fig

def plotWeekdayCountsNormalized(df):
	weekday_df = df.groupby(['weekday']).sum()['count']
	weekday_counts = df.groupby(['weekday']).mean()['weekday_count']
	weekday_df = weekday_df / weekday_counts
	weekday_df = weekday_df.reset_index()
	weekday_df.columns = ['weekday', 'Avg Count']
	fig, ax1 = plt.subplots(1)
	sns.barplot(data=weekday_df, y='weekday', x='Avg Count', ax=ax1, color='gray', order=['sunday',
                                                                 'monday',
                                                                 'tuesday',
                                                                 'wednesday',
                                                                 'thursday',
                                                                 'friday',
                                                                 'saturday',])
	return fig

def plotAge(df):
    fig, ax1 = plt.subplots(1)
    sns.scatterplot(data=df, x='intake_date', y='age_at_intake', alpha=0.1, ax=ax1)
    return fig

def getNegAge(df):
    tempMask = df['age_at_intake'] != '(EMPTY)'
    df_negAge = df.loc[tempMask]
    tempMask = df_negAge['age_at_intake'] < 0
    df_negAge = df_negAge.loc[tempMask]
    df_negAge = df_negAge[['animal_id', 'dob', 'intake_date', 'age_at_intake']]
    return df_negAge

def getEmptyField(df, fieldName='dob'):
    tempMask = df[fieldName] == '(EMPTY)'
    df_empty = df.loc[tempMask]
    df_empty = df_empty[['animal_id', fieldName]]
    return df_empty


def getZeroField(df, fieldName='src_finders_zip_code'):
    tempMask = df[fieldName] == 0
    df_empty = df.loc[tempMask]
    df_empty = df_empty[['animal_id', fieldName]]
    return df_empty

def mergeWithWeatherDF(df):
    filename2 = './AustinWeather2020.csv'
    df_weather = pd.read_csv(filename2)
    df_weather['date'] = pd.to_datetime(df_weather['date'])
    # df_weather = df_weather.drop(['humid', 'precip'], axis=1)
    df_weather['tempSqrd'] = df_weather['temp'] ** 2
    df_weather['humidSqrd'] = df_weather['humid'] ** 2
    df_weather['precipSqrd'] = df_weather['precip'] ** 2
    df_countByDate = df.groupby(['intake_date']).sum()['count'].reset_index().copy()
    df_countByDate = df_countByDate.merge(df_weather, 'left', left_on='intake_date', right_on='date')
    df_countByDate = df_countByDate.drop(['date'], axis=1)
    return df_countByDate

def getUpdatedResults(df_weather):
    y = df_weather['count'].copy()
    x = df_weather.drop(['intake_date', 'count'], axis=1).copy()
    reg = LinearRegression().fit(x, y)
    df_out = df_weather.copy()
    df_out['pred'] = reg.predict(x)
    df_out['resids'] = df_out['count'] - df_out['pred']
    return df_out

def getOLSResults(df_weather):
    y = df_weather['count'].copy()
    x = df_weather.drop(['intake_date', 'count'], axis=1).copy()
    x = x.values
    x = sm.add_constant(x)
    y = y.values
    model = sm.OLS(y, x)
    results = model.fit()
    return results.summary()

def plotResids(df_weather):
    fig, ax1 = plt.subplots(1)
    sns.scatterplot(data=df_weather, x='intake_date', y='resids', ax=ax1)
    plt.axhline(0, color='red')
    return fig