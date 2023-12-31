import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# Read data from the CSV into a dataframe
folder='Datasets'
raw_data_1 = pd.read_csv(folder +'2000-01.csv')
raw_data_2 = pd.read_csv(folder +'2001-02.csv')
raw_data_3 = pd.read_csv(folder +'2002-03.csv')
raw_data_4 = pd.read_csv(folder +'2003-04.csv')
raw_data_5 = pd.read_csv(folder +'2004-05.csv')
raw_data_6 = pd.read_csv(folder +'2005-06.csv')
raw_data_7 = pd.read_csv(folder +'2006-07.csv')
raw_data_8 = pd.read_csv(folder +'2007-08.csv')
raw_data_9 = pd.read_csv(folder +'2008-09.csv')
raw_data_10 = pd.read_csv(folder +'2009-10.csv')
raw_data_11 = pd.read_csv(folder +'2010-11.csv')
raw_data_12 = pd.read_csv(folder +'2011-12.csv')
raw_data_13 = pd.read_csv(folder +'2012-13.csv')
raw_data_14 = pd.read_csv(folder +'2013-14.csv')
raw_data_15 = pd.read_csv(folder +'2014-15.csv')
raw_data_16 = pd.read_csv(folder +'2015-16.csv')
raw_data_17 = pd.read_csv(folder +'2016-17.csv')
raw_data_18 = pd.read_csv(folder +'2017-18.csv')

#Gets all the statistics related to gameplay
                      
columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','HTHG','HTAG','FTR', 'HTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR', 'Referee']

playing_statistics_1 = raw_data_1[columns_req]                      
playing_statistics_2 = raw_data_2[columns_req]
playing_statistics_3 = raw_data_3[columns_req]
playing_statistics_4 = raw_data_4[columns_req]
playing_statistics_5 = raw_data_5[columns_req]
playing_statistics_6 = raw_data_6[columns_req]
playing_statistics_7 = raw_data_7[columns_req]
playing_statistics_8 = raw_data_8[columns_req]
playing_statistics_9 = raw_data_9[columns_req]
playing_statistics_10 = raw_data_10[columns_req]
playing_statistics_11 = raw_data_11[columns_req]   
playing_statistics_12 = raw_data_12[columns_req]
playing_statistics_13 = raw_data_13[columns_req]
playing_statistics_14 = raw_data_14[columns_req]
playing_statistics_15 = raw_data_15[columns_req]
playing_statistics_16 = raw_data_16[columns_req]
playing_statistics_17 = raw_data_17[columns_req]
playing_statistics_18 = raw_data_18[columns_req]
playing_statistics = [playing_statistics_1,playing_statistics_2,playing_statistics_3,playing_statistics_4,playing_statistics_5,
                      playing_statistics_6,playing_statistics_7,playing_statistics_8,playing_statistics_9,playing_statistics_10,
                      playing_statistics_11,playing_statistics_12,playing_statistics_13,playing_statistics_14,playing_statistics_15,
                      playing_statistics_16,playing_statistics_17,playing_statistics_18]
df = pd.concat(playing_statistics)
#
### Changing value H, A, D, in column FTR (Full Time Result) in Home, Away, Draw
df['FTR'] = np.where(df['FTR'] == 'H',"HOME",
                          np.where(df['FTR'] == 'A',"AWAY", "DRAW"))

### To identify the winner of each match: if "H"- the home team was the winner, if "A" the away team was the winner, else draw:
df['Winner'] = np.where(df['FTR'] == 'HOME',df['HomeTeam'],
                          np.where(df['FTR'] == 'AWAY', df['AwayTeam'], "Draw"))


### To identify the result of each match: whether the home team won, the away team won, or drew:
df['Result'] = np.where(df['FTR'] == 'HOME','Home Team Win',
                          np.where(df['FTR'] == 'AWAY', 'Away Team Win', "Draw"))

### To identify how many goals did the winner had:
df['Result'] = np.where(df['FTR'] == 'HOME','Home Team Win',
                          np.where(df['FTR'] == 'AWAY', 'Away Team Win', "Draw"))

### To get the "Year" of each match:
df['Year']=pd.DatetimeIndex(df['Date']).year

### To get the total number of goals in each match and the goal differences:
df['TotalGoal'] = df['FTHG'] + df['FTAG']
df['GoalDif']= df['FTHG']- df['FTAG']

### Drop the results which were "Draw" as this data was not required for the visualisation
### Group by Winner
df2 = df[df.FTR != 'DRAW']
avgWinning = df2.groupby('Winner')['Winner'].count().reset_index(name = "Count")
avgWinning.rename(columns = {'Winner':'Team', 'Count':'Victories'}, inplace=True)

###Costruendo dataset con statistiche per ogni team
teamStatistics = df.groupby('HomeTeam')['HST'].agg('sum').reset_index(name = 'Home Shots on Target')
teamStatistics = teamStatistics.rename(columns={"HomeTeam": "Team"})
AST = df.groupby('AwayTeam')['AST'].agg('sum').reset_index(name = 'Away Shots on Target')
teamStatistics["Away Shots on Target"] = AST["Away Shots on Target"]
teamStatistics["Total Shots on Target"] = teamStatistics["Home Shots on Target"] + teamStatistics["Away Shots on Target"]

HG = df.groupby('HomeTeam')['FTHG'].agg('sum').reset_index(name = 'Home Goal')
teamStatistics["Home Goal"] = HG['Home Goal']
AG = df.groupby('AwayTeam')['FTAG'].agg('sum').reset_index(name = 'Away Goal')
teamStatistics["Away Goal"] = AG['Away Goal']

HHG = df.groupby('HomeTeam')['HTHG'].agg('sum').reset_index(name = 'Half Home Goal')
teamStatistics["Half Home Goal"] = HHG['Half Home Goal']
HAG = df.groupby('AwayTeam')['HTAG'].agg('sum').reset_index(name = 'Half Away Goal')
teamStatistics["Half Away Goal"] = HAG['Half Away Goal']

HGC = df.groupby('HomeTeam')['FTAG'].agg('sum').reset_index(name = 'Home Goal Conceded')
teamStatistics["Home Goal Conceded"] = HGC['Home Goal Conceded']
AGC = df.groupby('AwayTeam')['FTHG'].agg('sum').reset_index(name = 'Away Goal Conceded')
teamStatistics["Away Goal Conceded"] = AGC['Away Goal Conceded']
teamStatistics["Total Goal"] = teamStatistics["Home Goal"] + teamStatistics['Away Goal']
teamStatistics["Total Goal Conceded"] = teamStatistics["Home Goal Conceded"] + teamStatistics['Away Goal Conceded']
teamStatistics["Goal/ST"] = teamStatistics['Total Goal'] / teamStatistics['Total Shots on Target']

participations =  df.groupby('HomeTeam')['HomeTeam'].count().reset_index(name = "Count")
participations["Count"] = participations["Count"] * 2
teamStatistics["Games"] = participations["Count"]

#DF2 NON CONSIDERA I PAREGGI -->
victories = df2.groupby('Winner')['Winner'].count().reset_index(name = "Count")
teamStatistics["Victories"] = victories['Count']
teamStatistics["Wins/Games"] = teamStatistics['Victories'] / teamStatistics['Games']
teamStatistics["avgGoals"] = teamStatistics['Total Goal'] / teamStatistics['Games']
teamStatistics["avgGoals Conceded"] = teamStatistics['Total Goal Conceded'] / teamStatistics['Games']

HF =  df.groupby('HomeTeam')['HF'].agg('sum').reset_index(name = "Count")
AF =  df.groupby('AwayTeam')['AF'].agg('sum').reset_index(name = "Count")
teamStatistics["Home Fouls"] = HF['Count']
teamStatistics["Away Fouls"] = AF['Count']
teamStatistics["Total Fouls"] = teamStatistics["Home Fouls"] + teamStatistics["Away Fouls"]

HY =  df.groupby('HomeTeam')['HY'].agg('sum').reset_index(name = "Count")
AY =  df.groupby('AwayTeam')['AY'].agg('sum').reset_index(name = "Count")
teamStatistics["Home Yellow Cards"] = HY['Count']
teamStatistics["Away Yellow Cards"] = AY['Count']
teamStatistics["Total Yellow Cards"] = teamStatistics["Home Yellow Cards"] + teamStatistics["Away Yellow Cards"]

HR =  df.groupby('HomeTeam')['HR'].agg('sum').reset_index(name = "Count")
AR =  df.groupby('AwayTeam')['AR'].agg('sum').reset_index(name = "Count")
teamStatistics["Home Red Cards"] = HR['Count']
teamStatistics["Away Red Cards"] = AR['Count']
teamStatistics["Total Red Cards"] = teamStatistics["Home Red Cards"] + teamStatistics["Away Red Cards"]
teamStatistics["Cards/Fouls"] = (teamStatistics['Total Yellow Cards'] + teamStatistics['Total Red Cards'] ) / teamStatistics['Total Fouls']

### Group the data by Result:
general = df.groupby('Result')['Result'].count().reset_index(name = "count")
### Apply px.pie:
fig1 = px.pie(general, values ='count', names ='Result', title='Premier League - results from 2000 - 2018', color = 'Result',
             color_discrete_map={'Home Team Win':'royalblue',
                                 'Away Team Win':'orangered',
                                 'Draw':'lightgreen'})

### Add text and define text information:
fig1.update_traces(textposition='inside', textinfo='label+percent', textfont_size=9)
fig1.update_layout(showlegend=False) 
fig1.show()

goal_first_time = teamStatistics["Half Home Goal"].sum() + teamStatistics["Half Away Goal"].sum()
total_goal = teamStatistics["Home Goal"].sum() + teamStatistics["Away Goal"].sum()
goal_second_time = total_goal - goal_first_time
fig3 = go.Figure(data=[go.Pie(labels=["Goal first time","Goal second time"], values=[goal_first_time,goal_second_time])])
fig3.update_traces(textposition='inside', textinfo='label+percent', textfont_size=9)
fig3.update_layout(title = "Goals scored in the two halves", showlegend=False) 
fig3.show()

df3 = df[['HTR', 'FTR']].copy()
df3['FTR'] = np.where(df['FTR'] == 'HOME',"H",
                          np.where(df3['FTR'] == 'AWAY',"A", "D"))
df3['Change'] = 'FALSE'
df3['Change'] = df3['HTR'] == df3['FTR']

### Group the data by the changinf of the result:
changing = df3.groupby('Change')['Change'].count().reset_index(name = "count")

fig16 = px.pie(changing, values ='count', names ='Change', title='What percentage of Results Changed after Half Time', color = 'Change',
              )
fig16.update_traces(textposition='inside', textinfo='label+percent', textfont_size=9)
fig16.update_layout(showlegend=False) 
fig16.show()

### Group total goals by year
total_goal = df.groupby('Year')['TotalGoal'].agg('sum').reset_index(name = 'Sum of Goals')
### Remove the data for 2000 and 2018 as it seemed that the data for those years were not complete
total_goal = total_goal[(total_goal.Year != 2018) & (total_goal.Year != 2000)]
### Visualise histogram
fig5 = px.bar(total_goal, x="Year", y="Sum of Goals",  title = "Total Goal by Year", text_auto=True)
fig5.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig5.update_xaxes(type='category')
fig5.update(layout_yaxis_range = [900,1120])
fig5.show()

### To get the total number of fouls in each match:
df['TotalFouls'] = df['HF'] + df['AF']
### Group total fouls by year
total_fouls =df.groupby('Year')['TotalFouls'].agg('sum').reset_index(name = 'Sum of Fouls')
### Remove the data for 2000 and 2018 as it seemed that the data for those years were not complete
total_fouls = total_fouls[(total_fouls.Year != 2018) & (total_fouls.Year != 2000)]
### Visualise by line chart
fig6 = px.bar(total_fouls, x = 'Year', y = 'Sum of Fouls', title = 'Total Fouls by Year', text_auto='0.3s')
fig6.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig6.update_xaxes(type='category')
fig6.update(layout_yaxis_range = [7500,10500])
fig6.show()

#Numero di goal per partita
fig15 = px.histogram(df, x=(df['FTHG']+df['FTAG']), title="Number of Goals per Match",text_auto=True)
fig15.update_layout(
    xaxis_title="Number of Goals",
    yaxis_title="Number of Matches",
)
fig15.show()

##Squadra più precisa GOAL/TIRI IN PORTA
goal_on_shots = teamStatistics.sort_values(by ='Goal/ST', ascending=True)
fig8 = px.bar(goal_on_shots, x='Goal/ST', y='Team', text_auto=True, title='The most accurate teams')
fig8.update_layout(yaxis_tickformat = '.1%')
fig8.show()
##Squadra con Vittorie/Partite giocate
wins_on_games = teamStatistics.sort_values(by ='Wins/Games', ascending=True)
fig9 = px.bar(wins_on_games, x='Wins/Games', y='Team', text_auto=True, title='The most efficent teams')
fig9.update_layout(yaxis_tickformat = '.0%')
fig9.show()
##Squadra con Cartellini/Falli giocate
cards_on_fouls = teamStatistics.sort_values(by ='Cards/Fouls', ascending=True)
fig10 = px.bar(cards_on_fouls, x='Cards/Fouls', y='Team', text_auto=True, title='The most aggresive teams')
fig10.update_layout(yaxis_tickformat = '.1%')
fig10.show()

##Squadra con media Goal più alta
avgGoals = teamStatistics.sort_values(by ='avgGoals', ascending=True)
fig11 = px.bar(avgGoals, x='avgGoals', y='Team', text_auto='0.3', title='Goal average')
fig11.update_traces(textangle=0, textposition="outside", cliponaxis=False)
fig11.show()
##Squadra con media Goal più alta
avgGoalsConceded = teamStatistics.sort_values(by ='avgGoals Conceded', ascending=True)
fig12 = px.bar(avgGoalsConceded, x='avgGoals Conceded', y='Team', title='Goal conceded average')
fig12.show()

topTeam = teamStatistics.sort_values(by ='Games', ascending=False).head(6)
fig17 = px.histogram(topTeam, x = 'Team',y =['Home Goal','Away Goal'], text_auto=True)
fig17.update_layout(bargap=0.1)
fig18 = px.histogram(topTeam, x = 'Team', y='Victories', text_auto=True)
fig18.update_layout(bargap=0.1)
fig19 = go.Figure()
fig19.add_trace(go.Bar(
    x=topTeam['Team'],
    y=topTeam['Total Goal'],
    texttemplate = "%{value}",
    name='Total Goal', 
))
fig19.add_trace(go.Bar(
    x=topTeam['Team'],
    y=topTeam['Total Goal Conceded'],
    texttemplate = "%{value}",
    name='Total Goal Conceded'
))
fig19.update_layout(width =1200, height=600)
fig17.show()
fig18.show()
fig19.show()
