import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from flask import Flask, render_template, url_for, flash, redirect, request
from sklearn.preprocessing import MinMaxScaler
import numpy as np

#---------------------------------------------------------------------------------------------------------------------------------

def greenPitch():
    data = pd.read_csv("dataset/green.csv")
    batsman=[]
    batsman=data[(data['Role'] == 'Batsman') & (data['Bat_Inns'] >= 14 )].sort_values(by=['Bat_Ave'], ascending=False)
    updated_batsman = batsman.sort_values(by=['Ct'],ascending=False)
    set1 = updated_batsman[:4]
    substitute1 = updated_batsman[4:6]
    wicket_keeper = [] 
    wicket_keeper = data[(data['Role'] == 'Wk') ].sort_values(by=['Bat_Ave'], ascending=False)
    updated_wicket_keeper = wicket_keeper.sort_values(by=['St'], ascending=False)
    set2 = updated_wicket_keeper[:1]
    substitute2 = updated_wicket_keeper[1:2]
    allrounder = [] 
    allrounder = data[(data['Role'] == 'Allrounder')].sort_values(by=['Wkts'], ascending=False)
    updated_allrounder = allrounder.sort_values(by=['Ct'], ascending=False)
    set3 = updated_allrounder[:2]
    substitute3 = updated_allrounder[2:3]
    bowler = [] 
    bowler = data[(data['Role'] == 'Bowler') & (data['Bow_Ave'] <=40) ].sort_values(by=['Wkts'], ascending=False)
    updated_bowler = bowler.sort_values(by=['Ct'], ascending=False)
    set4 = updated_bowler[:4]
    substitute4 = updated_bowler[4:6]
    final = [set1, set2, set3, set4]
    output = pd.concat(final)
    output.reset_index(inplace=True)
    output.drop("index",axis=1,inplace=True)
    sfinal = [substitute1,substitute2,substitute3,substitute4]
    soutput = pd.concat(sfinal)
    soutput.reset_index(inplace=True)
    soutput.drop("index",axis=1,inplace=True)

    return output, soutput

#---------------------------------------------------------------------------------------------------------------------------------

def deadPitch():
    data = pd.read_csv("dataset/dead.csv")
    batsman=[]
    batsman=data[(data['Role'] == 'Batsman') & (data['Bat_Inns'] >= 14 )].sort_values(by=['Bat_Ave'], ascending=False)
    updated_batsman = batsman.sort_values(by=['Ct'],ascending=False)
    set1 = updated_batsman[:5]
    substitute1 = updated_batsman[5:6]
    wicket_keeper = [] 
    wicket_keeper = data[(data['Role'] == 'Wk') ].sort_values(by=['Bat_Ave'], ascending=False)  #Run scored to Bat_Ave
    updated_wicket_keeper = wicket_keeper.sort_values(by=['St'], ascending=False)
    set2 = updated_wicket_keeper[:1]
    substitute2 = updated_wicket_keeper[1:2]
    allrounder = [] 
    allrounder = data[(data['Role'] == 'Allrounder')].sort_values(by=['Wkts'], ascending=False) #Removed Runs_scored 
    updated_allrounder = allrounder.sort_values(by=['Ct'], ascending=False)
    set3 = updated_allrounder[:2]
    substitute3 = updated_allrounder[2:3]
    bowler = [] 
    bowler = data[(data['Role'] == 'Bowler') & (data['Bow_Ave'] <=40) ].sort_values(by=['Wkts'], ascending=False)
    updated_bowler = bowler.sort_values(by=['Ct'], ascending=False)
    set4 = updated_bowler[:3]
    substitute4 = updated_bowler[3:6]
    final = [set1, set2, set3, set4]
    output = pd.concat(final)
    output.reset_index(inplace=True)
    output.drop("index",axis=1,inplace=True)
    sfinal = [substitute1,substitute2,substitute3,substitute4]
    soutput = pd.concat(sfinal)
    soutput.reset_index(inplace=True)
    soutput.drop("index",axis=1,inplace=True)

    return output, soutput

#---------------------------------------------------------------------------------------------------------------------------------

def dustyPitch():
    data = pd.read_csv("dataset/dusty.csv")
    batsman=[]
    batsman=data[(data['Role'] == 'Batsman') & (data['Bat_Inns'] >= 14 )].sort_values(by=['Bat_Ave'], ascending=False)
    updated_batsman = batsman.sort_values(by=['Ct'],ascending=False)
    set1 = updated_batsman[:4]
    substitute1 = updated_batsman[4:6]
    wicket_keeper = [] 
    wicket_keeper = data[(data['Role'] == 'Wk') ].sort_values(by=['Bat_Ave'], ascending=False)  #Run scored to Bat_Ave
    updated_wicket_keeper = wicket_keeper.sort_values(by=['St'], ascending=False)
    set2 = updated_wicket_keeper[:1]
    substitute2 = updated_wicket_keeper[1:2]
    allrounder = [] 
    allrounder = data[(data['Role'] == 'Allrounder')].sort_values(by=['Wkts'], ascending=False) #Removed Runs_scored
    updated_allrounder = allrounder.sort_values(by=['Ct'], ascending=False)
    set3 = updated_allrounder[:2]
    substitute3 = updated_allrounder[2:3]
    bowler = [] 
    bowler = data[(data['Role'] == 'Bowler') & (data['Bow_Ave'] <=40) ].sort_values(by=['Wkts'], ascending=False)
    updated_bowler = bowler.sort_values(by=['Ct'], ascending=False)
    set4 = updated_bowler[:4]
    substitute4 = updated_bowler[4:6]
    final = [set1, set2, set3, set4]
    output = pd.concat(final)
    output.reset_index(inplace=True)
    output.drop("index",axis=1,inplace=True)
    sfinal = [substitute1,substitute2,substitute3,substitute4]
    soutput = pd.concat(sfinal)
    soutput.reset_index(inplace=True)
    soutput.drop("index",axis=1,inplace=True)

    return output, soutput

#---------------------------------------------------------------------------------------------------------------------------------

def player_stats(player_name, player_role, pitch_type, method):
    players_and_role = {}
    player_role = player_role
    SheetNames = pd.ExcelFile('dataset/stats.xlsx').sheet_names
    if player_name in SheetNames:

        if(player_role == 'None'):
            proles = pd.read_excel("dataset/player_role.xlsx")
            for i in range(proles.shape[0]):
                players_and_role.update({proles.iloc[i][0]:proles.iloc[i][1]})
            
            if player_name in players_and_role.keys():
                player_role = players_and_role[player_name]
            else:
                return False


        #print("\nPLAYER_NAME:--------------------------------", player_name, "\n")
        df = pd.read_excel("dataset/stats.xlsx", player_name)

        df.drop(df.tail(1).index,inplace=True)
        df = df.sort_values('Year')
        #total_rows = df.shape[0]

        if(player_role == 'Batsman' or player_role == 'Wk'):
            stat_data_desc = {}

            year = df['Year']
            runs = df['Runs']
            plt.figure(figsize=(12,6))
            plt.xticks(rotation=75)
            plt.title(player_name+"'s "+'Runs Scored Per Year')
            runs_per_year = sns.barplot(x = year, y = runs)
            runs_per_year.set(xlabel = 'Year', ylabel = 'No. of Runs')
            runs_per_year.figure.savefig('static/stat/'+player_name+'_1.png')
            desc_1 = "Runs Scored Per Year.\n\nYear (Horizontal) and Total Runs Scored (Vertical)"

            avg = df['Avg']
            plt.figure(figsize=(8,8))
            plt.title(player_name+"'s "+'Average Per Year')
            pie_chart = plt.pie(avg,labels=df['Year'], autopct='%1.2f%%')
            plt.savefig('static/stat/'+player_name+'_3.png')
            desc_2 = "Average Per Year"
        
            year = df['Year']
            half_centuries = df[50]
            centuries = df[100]
            combined_centuries = pd.concat([year,half_centuries,centuries], axis = 1)
            combined_centuries.columns = ['Year', 'Half Centuries','Centuries']
            c = combined_centuries.set_index(combined_centuries.columns[0])
            c.plot(kind = 'bar', figsize=(12,6), title = player_name+"'s "+'50s & 100s Per Year', xlabel = 'Year', ylabel = 'No. of 50s & 100s').figure.savefig('static/stat/'+player_name+'_2.png')
            desc_3 = "50s & 100s Scored Per Year.\n\nTotal number of 50s and 100s (Horizontal) and Year (Vertical)"

            plt.figure(figsize=(12,6))
            plt.title(player_name+"'s "+'Innings Played Per Year')
            innings_per_year = sns.barplot(y=df['Year'], x=df['Innings'], orient = 'h')
            innings_per_year.set(ylabel = 'Year',xlabel = 'No. of Innings')
            innings_per_year.figure.savefig('static/stat/'+player_name+'_4.png')
            desc_4 = "Innings Played Per Year.\n\nTotal number of Innings (Horizontal) and Year (Vertical)"

            stat_data_desc.update({"desc_1":desc_1, "desc_2":desc_2,"desc_3":desc_3,"desc_4":desc_4})

            return stat_data_desc
        
        elif(player_role == 'Bowler'):
            stat_data_desc = {}

            year = df['Year']
            wickets = df['Wickets']
            plt.figure(figsize=(12,6))
            plt.xticks(rotation=75)
            plt.title(player_name+"'s "+'Wickets Per Year')
            wickets_per_year = sns.barplot(x = year, y = wickets)
            wickets_per_year.set(xlabel = 'Year', ylabel = 'No. of Wickets')
            wickets_per_year.figure.savefig('static/stat/'+player_name+'_1.png')
            desc_1 = "Wickets Taken Per Year.\n\nYear (Horizontal) and Total Number of Wickets Taken (Vertical)"

            avg = df['Avg']
            plt.figure(figsize=(8,8))
            plt.title(player_name+"'s "+'Bowling Average Over The Years')
            pie_chart = plt.pie(avg,labels=df['Year'],autopct='%1.2f%%')
            plt.savefig('static/stat/'+player_name+'_3.png')
            desc_2 = "Bowling Average Per Year"

            plt.figure(figsize=(12,6))
            x = df['Year']
            y = df['Econ']
            plt.title(player_name+"'s "+'Economy Over The Years')
            plt.xlabel("Year") 
            plt.ylabel("Economy")
            plt.plot(x,y)
            plt.savefig('static/stat/'+player_name+'_2.png')
            desc_3 = "Bowling Economy Per Year.\n\nYear (Horizontal) and Economy (Vertical)"

            plt.figure(figsize=(12,6))
            plt.title(player_name+"'s "+'Overs Bowled Per Year')
            overs_per_year = sns.barplot(y=df['Year'],x=df['Overs'], orient = 'h')
            overs_per_year.set(ylabel = 'Year',xlabel = 'No. of Overs')
            overs_per_year.figure.savefig('static/stat/'+player_name+'_4.png')
            desc_4 = "Total Overs Bowled Per Year.\n\nTotal Number of Overs (Horizontal) and Year (Vertical)"

            stat_data_desc.update({"desc_1":desc_1, "desc_2":desc_2,"desc_3":desc_3,"desc_4":desc_4})

            return stat_data_desc
        
        elif(player_role == 'Allrounder'):
            stat_data_desc = {}

            year = df['Year']
            runs = df['Runs_Scored']
            plt.figure(figsize=(12,6))
            plt.xticks(rotation=75)
            plt.title(player_name+"'s "+'Runs Scored Per Year')
            runs_per_year = sns.barplot(x = year, y = runs)
            runs_per_year.set(xlabel = 'Year', ylabel = 'No. of Runs')
            runs_per_year.figure.savefig('static/stat/'+player_name+'_1.png')
            desc_1 = "Total Runs Scored Per Year.\n\nYear (Horizontal) and Total Runs Scored (Vertical)"

            year = df['Year']
            half_centuries = df[50]
            centuries = df[100]
            combined_centuries = pd.concat([year,half_centuries,centuries], axis = 1)
            combined_centuries.columns = ['Year', 'Half Centuries','Centuries']
            c = combined_centuries.set_index(combined_centuries.columns[0])
            c.plot(kind = 'bar', figsize=(12,6), title = player_name+"'s "+'50s & 100s Per Year', xlabel = 'Year', ylabel = 'No. of 50s & 100s').figure.savefig('static/stat/'+player_name+'_2.png')
            desc_2 = "50s & 100s Scored Per Year.\n\nTotal number of 50s and 100s (Horizontal) and Year (Vertical)"

            year = df['Year']
            wickets = df['Wickets']
            plt.figure(figsize=(12,6))
            plt.xticks(rotation=75)
            plt.title(player_name+"'s "+'Wickets Per Year')
            wickets_per_year = sns.barplot(x = year, y = wickets)
            wickets_per_year.set(xlabel = 'Year', ylabel = 'No. of Wickets')
            wickets_per_year.figure.savefig('static/stat/'+player_name+'_3.png')
            desc_3 = "Wickets Taken Per Year.\n\nYear (Horizontal) and Total Number of Wickets Taken (Vertical)"

            plt.figure(figsize=(12,6))
            x = df['Year']
            y = df['Econ']
            plt.title(player_name+"'s "+'Bowling Economy Over The Years')
            plt.xlabel("Year") 
            plt.ylabel("Economy")
            plt.plot(x,y)
            plt.savefig('static/stat/'+player_name+'_4.png')
            desc_4 = "Bowling Economy Per Year.\n\nYear (Horizontal) and Economy (Vertical)"

            stat_data_desc.update({"desc_1":desc_1, "desc_2":desc_2,"desc_3":desc_3,"desc_4":desc_4})

            return stat_data_desc

        else:
             return 'invalid category'
    else:
        return False

#---------------------------------------------------------------------------------------------------------------------------------

def kmeans_green():
    df = pd.read_csv("dataset/Batting.csv")
    df = df.loc[df['Role']=='Batsman']
    
    #Batting Average
    BattingStats = pd.DataFrame()
    BattingStats.insert(0,'Player',df['Player'],True)
    ba = round((df['Runs'])/((df['Innings'])-(df['NotOut'])), 2)
    BattingStats.insert(1,"Batting Average",ba,True)
    #Batting Strike Rate
    bs = round(((df['Runs'])*100)/(df['BF']), 2)
    BattingStats.insert(2,"Batting SR",bs,True)
    #MRA
    mra = round((((df['Fifties'])+(df['Hundreds']))*100)/(df['Innings']), 2)
    BattingStats.insert(3,"MRA",mra,True)
    #Outrate
    outrate = round((((df['Innings'])-(df['NotOut']))*100)/(df['BF']), 2)
    BattingStats.insert(4,"Outrate",outrate,True)
    #Boundry Rate per Innings
    bpri = round((4*(df['Fours']))/(df['Innings']), 2)
    BattingStats.insert(5,"Boundary Rate",bpri,True)
    BattingStats = BattingStats.dropna()
    BattingStats.insert(6,'Catches',df['Ct'],True)
    BattingStats.insert(7,'Stumpings',df['St'],True)
    plt.scatter(BattingStats['MRA'],BattingStats['Batting SR'])
    sse = []
    for k in range(1,12):
        km = KMeans(n_clusters=k)
        km.fit(BattingStats[['MRA','Batting SR']])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,12),sse)
    km = KMeans(n_clusters=3)
    y_predicted = km.fit_predict(BattingStats[['MRA','Batting SR']])
    BattingStats['Cluster'] = y_predicted
    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    df3 = BattingStats[BattingStats.Cluster==2]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting SR'],color='green')
    plt.scatter(df2.MRA,df2['Batting SR'],color='blue')
    plt.scatter(df3.MRA,df3['Batting SR'],color='red')
    plt.xlabel('MRA')
    plt.ylabel('Batting SR')
    plt.legend()
    km.cluster_centers_
    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    df3 = BattingStats[BattingStats.Cluster==2]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting SR'],color='green')
    plt.scatter(df2.MRA,df2['Batting SR'],color='blue')
    plt.scatter(df3.MRA,df3['Batting SR'],color='red')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('MRA')
    plt.ylabel('Batting SR')
    plt.legend()

    x = len(df1)
    y = len(df2)
    z = len(df3)
    if x > y and x > z:
        out = df1
    elif y > x and y > z:
        out = df2
    else:
        out = df3

    batsman = out

    updated_batsman = batsman.sort_values(by=['MRA'],ascending=False)
    updated_batsman = updated_batsman.sort_values(by=['Catches'],ascending=False)
    set1 = updated_batsman[:4]
    substitute1 = updated_batsman[4:6]


    df = pd.read_csv("dataset/Batting.csv")
    df2 = df.loc[df['Role']=='Wicket Keeper Batsman']
    
    
    BattingStats = pd.DataFrame()
    BattingStats.insert(0,'Player',df2['Player'],True)
    ba = round((df2['Runs'])/((df2['Innings'])-(df2['NotOut'])), 2)
    BattingStats.insert(1,"Batting Average",ba,True)
    bs = round(((df2['Runs'])*100)/(df2['BF']), 2)
    BattingStats.insert(2,"Batting SR",bs,True)
    mra = round((((df2['Fifties'])+(df2['Hundreds']))*100)/(df2['Innings']), 2)
    BattingStats.insert(3,"MRA",mra,True)
    outrate = round((((df2['Innings'])-(df2['NotOut']))*100)/(df2['BF']), 2)
    BattingStats.insert(4,"Outrate",outrate,True)
    bpri = round((4*(df2['Fours']))/(df2['Innings']), 2)
    BattingStats.insert(5,"Boundary Rate",bpri,True)
    BattingStats = BattingStats.dropna()
    BattingStats.insert(6,'Catches',df['Ct'],True)
    BattingStats.insert(7,'Stumpings',df['St'],True)

    plt.scatter(BattingStats['MRA'],BattingStats['Batting Average'])
    sse = []
    for k in range(1,4):
        km = KMeans(n_clusters=k)
        km.fit(BattingStats[['MRA','Batting Average']])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,4),sse)
    km = KMeans(n_clusters=2)
    y_predicted = km.fit_predict(BattingStats[['MRA','Batting Average']])
    BattingStats['Cluster'] = y_predicted
    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting Average'],color='red')
    plt.scatter(df2.MRA,df2['Batting Average'],color='blue')
    plt.xlabel('MRA')
    plt.ylabel('Batting Average')
    plt.legend()

    km.cluster_centers_
    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting Average'],color='red')
    plt.scatter(df2.MRA,df2['Batting Average'],color='blue')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('MRA')
    plt.ylabel('Batting Average')
    plt.legend()

    x = len(df1)
    y = len(df2)
    if x > y:
        out = df1
    else:
        out = df2

    wk = out
    wk

    updated_wk = wk.sort_values(by=['MRA'],ascending=False)
    updated_wk = updated_wk.sort_values(by=['Stumpings'],ascending=False)
    set2 = updated_wk[:1]
    substitute2 = updated_wk[1:2]

    df = pd.read_csv("dataset/Bowling.csv")
    df3 = df.loc[df['Role']=='Bowler']
    df3=df3[(df3['BowlingStyle'] == 'Left-arm Medium') | (df3['BowlingStyle'] == 'Right-arm Medium') | (df3['BowlingStyle'] == 'Right-arm Fast')]
    BowlingStats = pd.DataFrame()
    BowlingStats.insert(0,'Player',df3['Player'],True)
    BowlingStats.insert(1,'Wickets',df3['Wickets'],True)
    ba = round((df3['Runs'])/(df3['Wickets']), 2)
    BowlingStats.insert(2,"Bowling Average",ba,True)

    bs = round(((df3['Overs'])*6)/(df3['Wickets']), 2)
    BowlingStats.insert(3,"Bowling SR",bs,True)

    er = round((df3['Runs'])/(df3['Overs']), 2)
    BowlingStats.insert(4,"Economy",df3['Economy'],True)

    outrate = round((((df3['Wickets'])*100)/((df3['Overs'])*6)), 2)
    BowlingStats.insert(5,"Outrate",outrate,True)
    BowlingStats.insert(6,'Catches',df3['Ct'],True)
    BowlingStats.insert(7,'Stumpings',df3['St'],True)

    sse = []
    for k in range(1,8):
        km = KMeans(n_clusters=k)
        km.fit(BowlingStats[['Economy','Wickets']])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,8),sse)

    scaler = MinMaxScaler()

    scaler.fit(BowlingStats[['Wickets']])
    BowlingStats['Wickets'] = scaler.transform(BowlingStats[['Wickets']])

    scaler.fit(BowlingStats[['Economy']])
    BowlingStats['Economy'] = scaler.transform(BowlingStats[['Economy']])
    plt.scatter(df3.Economy,df3['Wickets'])

    km = KMeans(n_clusters=2)
    y_predicted = km.fit_predict(BowlingStats[['Economy','Wickets']])
    y_predicted

    BowlingStats['Cluster']=y_predicted
    BowlingStats.head(10)

    km.cluster_centers_
    df1 = BowlingStats[BowlingStats.Cluster==0]
    df2 = BowlingStats[BowlingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.Economy,df1['Wickets'],color='green')
    plt.scatter(df2.Economy,df2['Wickets'],color='red')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('Economy')
    plt.ylabel('Wickets')
    plt.legend()

    x = len(df1)
    y = len(df2)
    if x < y:
        out = df1
    else:
        out = df2

    bowler = out
    bowler

    updated_bowler = bowler.sort_values(by=['Economy'],ascending=False)

    updated_bowler = updated_bowler.sort_values(by=['Catches'],ascending=False)
    set3 = updated_bowler[:4]
    x = len(df1)
    y = len(df2)
    if x > y:
        out = df1
    else: 
        out = df2
    substitute_bowler = out
    substitute_bowler

    updated_substitute_bowler = substitute_bowler.sort_values(by=['Economy'],ascending=False)
    substitute3 = updated_substitute_bowler[0:2]
    df4 = pd.read_csv('dataset/Allrounder.csv')
    df4 = df4.dropna()

    allrounder = df4.sort_values(by=['Wickets'], ascending=False)

    updated_allrounder = allrounder.sort_values(by=['Runs'], ascending=False)

    updated_allrounder = allrounder.sort_values(by=['Ct'], ascending=False)
    set4 = updated_allrounder[:2]
    substitute4 = updated_allrounder[2:3]
    #---------------------final output----------------------------------
    final = [set1, set2, set4, set3]
    output = pd.concat(final)

    output.reset_index(inplace=True)
    output.drop("index",axis=1,inplace=True)

    sfinal = [substitute1,substitute2,substitute3,substitute4]
    soutput = pd.concat(sfinal)

    soutput.reset_index(inplace=True)
    soutput.drop("index",axis=1,inplace=True)

    output.fillna('0.0', inplace=True)
    soutput.fillna('0.0', inplace=True)

    return output, soutput



#---------------------------------------------------------------------------------------------------------------------------------

def kmeans_dusty():
    df = pd.read_csv("dataset/Batting.csv")
    df = df.loc[df['Role']=='Batsman']

    BattingStats = pd.DataFrame()
    BattingStats.insert(0,'Player',df['Player'],True)
    ba = round((df['Runs'])/((df['Innings'])-(df['NotOut'])))
    BattingStats.insert(1,"Batting Average",ba,True)

    bs = round(((df['Runs'])*100)/(df['BF']), 2)
    BattingStats.insert(2,"Batting SR",bs,True)

    mra = round((((df['Fifties'])+(df['Hundreds']))*100)/(df['Innings']), 2)
    BattingStats.insert(3,"MRA",mra,True)

    outrate = round((((df['Innings'])-(df['NotOut']))*100)/(df['BF']), 2)
    BattingStats.insert(4,"Outrate",outrate,True)

    bpri = round((4*(df['Fours']))/(df['Innings']), 2)
    BattingStats.insert(5,"Boundary Rate",bpri,True)
    BattingStats = BattingStats.dropna()
    BattingStats.insert(6,'Catches',df['Ct'],True)
    BattingStats.insert(7,'Stumpings',df['St'],True)

    plt.scatter(BattingStats['MRA'],BattingStats['Batting SR'])

    sse = []
    for k in range(1,12):
        km = KMeans(n_clusters=k)
        km.fit(BattingStats[['MRA','Batting SR']])
        sse.append(km.inertia_)
    
    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,12),sse)

    km = KMeans(n_clusters=3)
    y_predicted = km.fit_predict(BattingStats[['MRA','Batting SR']])
    BattingStats['Cluster'] = y_predicted

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    df3 = BattingStats[BattingStats.Cluster==2]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting SR'],color='green')
    plt.scatter(df2.MRA,df2['Batting SR'],color='blue')
    plt.scatter(df3.MRA,df3['Batting SR'],color='red')
    plt.xlabel('MRA')
    plt.ylabel('Batting SR')
    plt.legend()

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    df3 = BattingStats[BattingStats.Cluster==2]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting SR'],color='green')
    plt.scatter(df2.MRA,df2['Batting SR'],color='blue')
    plt.scatter(df3.MRA,df3['Batting SR'],color='red')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('MRA')
    plt.ylabel('Batting SR')
    plt.legend()

    x = len(df1)
    y = len(df2)
    z = len(df3)
    if x > y and x > z:
        out = df1
    elif y > x and y > z:
        out = df2
    else:
        out = df3

    batsman = out

    updated_batsman = batsman.sort_values(by=['MRA'],ascending=False)
    updated_batsman = updated_batsman.sort_values(by=['Catches'],ascending=False)

    set1 = updated_batsman[:4]
    substitute1 = updated_batsman[4:6]

    df = pd.read_csv("dataset/Batting.csv")
    df2 = df.loc[df['Role']=='Wicket Keeper Batsman']

    BattingStats = pd.DataFrame()
    BattingStats.insert(0,'Player',df2['Player'],True)
    ba = round((df2['Runs'])/((df2['Innings'])-(df2['NotOut'])), 2)
    BattingStats.insert(1,"Batting Average",ba,True)

    bs = round(((df2['Runs'])*100)/(df2['BF']), 2)
    BattingStats.insert(2,"Batting SR",bs,True)

    mra = round((((df2['Fifties'])+(df2['Hundreds']))*100)/(df2['Innings']), 2)
    BattingStats.insert(3,"MRA",mra,True)

    outrate = round((((df2['Innings'])-(df2['NotOut']))*100)/(df2['BF']), 2)
    BattingStats.insert(4,"Outrate",outrate,True)

    bpri = round((4*(df2['Fours']))/(df2['Innings']), 2)
    BattingStats.insert(5,"Boundary Rate",bpri,True)
    #BattingStats = BattingStats.dropna()
    BattingStats.insert(6,'Catches',df['Ct'],True)
    BattingStats.insert(7,'Stumpings',df['St'],True)

    plt.scatter(BattingStats['MRA'],BattingStats['Batting Average'])
    sse = []
    for k in range(1,4):
        km = KMeans(n_clusters=k)
        km.fit(BattingStats[['MRA','Batting Average']])
        sse.append(km.inertia_)
    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,4),sse)

    km = KMeans(n_clusters=2)
    y_predicted = km.fit_predict(BattingStats[['MRA','Batting Average']])
    BattingStats['Cluster'] = y_predicted
    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting Average'],color='red')
    plt.scatter(df2.MRA,df2['Batting Average'],color='blue')
    plt.xlabel('MRA')
    plt.ylabel('Batting Average')
    plt.legend()

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting Average'],color='red')
    plt.scatter(df2.MRA,df2['Batting Average'],color='blue')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('MRA')
    plt.ylabel('Batting Average')
    plt.legend()

    x = len(df1)
    y = len(df2)
    if x > y:
        out = df1
    else:
        out = df2

    wk = out
    updated_wk = wk.sort_values(by=['MRA'],ascending=False)
    updated_wk = updated_wk.sort_values(by=['Stumpings'],ascending=False)
    set2 = updated_wk[:1]
    substitute2 = updated_wk[1:2]


    df3 = pd.read_csv('dataset/Bowling.csv')
    df3 = df3.loc[df3['Role']=='Bowler']
    BowlingStats = pd.DataFrame()
    BowlingStats.insert(0,'Player',df3['Player'],True)
    BowlingStats.insert(1,'Wickets',df3['Wickets'],True)
    ba = round((df3['Runs'])/(df3['Wickets']), 2)
    BowlingStats.insert(2,"Bowling Average",ba,True)

    bs = round(((df3['Overs'])*6)/(df3['Wickets']), 2)
    BowlingStats.insert(3,"Bowling SR",bs,True)

    er = round((df3['Runs'])/(df3['Overs']), 2)
    BowlingStats.insert(4,"Economy",df3['Economy'],True)

    outrate = round((((df3['Wickets'])*100)/((df3['Overs'])*6)), 2)
    BowlingStats.insert(5,"Outrate",outrate,True)
    BowlingStats.insert(6,'Catches',df3['Ct'],True)
    BowlingStats.insert(7,'Stumpings',df3['St'],True)

    sse = []
    for k in range(1,8):
        km = KMeans(n_clusters=k)
        km.fit(BowlingStats[['Economy','Wickets']])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,8),sse)

    scaler = MinMaxScaler()

    scaler.fit(BowlingStats[['Wickets']])
    BowlingStats['Wickets'] = scaler.transform(BowlingStats[['Wickets']])

    scaler.fit(BowlingStats[['Economy']])
    BowlingStats['Economy'] = scaler.transform(BowlingStats[['Economy']])

    plt.scatter(df3.Economy,df3['Wickets'])
    km = KMeans(n_clusters=2)
    y_predicted = km.fit_predict(BowlingStats[['Economy','Wickets']])

    BowlingStats['Cluster']=y_predicted

    df1 = BowlingStats[BowlingStats.Cluster==0]
    df2 = BowlingStats[BowlingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.Economy,df1['Wickets'],color='green')
    plt.scatter(df2.Economy,df2['Wickets'],color='red')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('Economy')
    plt.ylabel('Wickets')
    plt.legend()

    x = len(df1)
    y = len(df2)
    if x > y:
        out = df1
    else:
        out = df2

    bowler = out

    updated_bowler = bowler.sort_values(by=['Economy'],ascending=False)
    set3 = updated_bowler[:4]
    x = len(df1)
    y = len(df2)
    if x < y:
        out = df1
    else:
        out = df2
    substitute_bowler = out

    updated_substitute_bowler = substitute_bowler.sort_values(by=['Economy'],ascending=False)
    substitute3 = updated_substitute_bowler[0:2]

    df4 = pd.read_csv('dataset/Allrounder.csv')
    df4 = df4.dropna()
    allrounder = df4.sort_values(by=['Wickets'], ascending=False)
    updated_allrounder = allrounder.sort_values(by=['Bowling Average'], ascending=True)
    set4 = updated_allrounder[:2]
    substitute4 = updated_allrounder[2:3]

    final = [set1, set2, set4, set3]
    output = pd.concat(final)

    output.reset_index(inplace=True)
    output.drop("index",axis=1,inplace=True)

    sfinal = [substitute1,substitute2,substitute3,substitute4]
    soutput = pd.concat(sfinal)

    soutput.reset_index(inplace=True)
    soutput.drop("index",axis=1,inplace=True)

    output.fillna('0.0', inplace=True)
    soutput.fillna('0.0', inplace=True)
    
    return output, soutput
    
#---------------------------------------------------------------------------------------------------------------------------------

def kmeans_dead():
    df = pd.read_csv('dataset/Batting.csv')
    df = df.loc[df['Role']=='Batsman']

    BattingStats = pd.DataFrame()
    BattingStats.insert(0,'Player',df['Player'],True)
    ba = round((df['Runs'])/((df['Innings'])-(df['NotOut'])), 2)
    BattingStats.insert(1,"Batting Average",ba,True)

    bs = round(((df['Runs'])*100)/(df['BF']), 2)
    BattingStats.insert(2,"Batting SR",bs,True)

    mra = round((((df['Fifties'])+(df['Hundreds']))*100)/(df['Innings']), 2)
    BattingStats.insert(3,"MRA",mra,True)

    outrate = round((((df['Innings'])-(df['NotOut']))*100)/(df['BF']), 2)
    BattingStats.insert(4,"Outrate",outrate,True)

    bpri = round((4*(df['Fours']))/(df['Innings']), 2)
    BattingStats.insert(5,"Boundary Rate",bpri,True)
    BattingStats = BattingStats.dropna()
    BattingStats.insert(6,'Catches',df['Ct'],True)
    BattingStats.insert(7,'Stumpings',df['St'],True)

    plt.scatter(BattingStats['MRA'],BattingStats['Batting SR'])
    sse = []
    for k in range(1,12):
        km = KMeans(n_clusters=k)
        km.fit(BattingStats[['MRA','Batting SR']])
        sse.append(km.inertia_)
    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,12),sse)

    km = KMeans(n_clusters=3)
    y_predicted = km.fit_predict(BattingStats[['MRA','Batting SR']])
    BattingStats['Cluster'] = y_predicted

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    df3 = BattingStats[BattingStats.Cluster==2]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting SR'],color='green')
    plt.scatter(df2.MRA,df2['Batting SR'],color='blue')
    plt.scatter(df3.MRA,df3['Batting SR'],color='red')
    plt.xlabel('MRA')
    plt.ylabel('Batting SR')
    plt.legend()

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    df3 = BattingStats[BattingStats.Cluster==2]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting SR'],color='green')
    plt.scatter(df2.MRA,df2['Batting SR'],color='blue')
    plt.scatter(df3.MRA,df3['Batting SR'],color='red')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('MRA')
    plt.ylabel('Batting SR')
    plt.legend()

    x = len(df1)
    y = len(df2)
    z = len(df3)
    if x > y and x > z:
        out = df1
    elif y > x and y > z:
        out = df2
    else: 
        out = df3

    batsman = out

    updated_batsman = batsman.sort_values(by=['MRA'],ascending=False)
    updated_batsman = updated_batsman.sort_values(by=['Catches'],ascending=False)
    set1 = updated_batsman[:5]
    substitute1 = updated_batsman[5:7]

    df = pd.read_csv('dataset/Batting.csv')
    df2 = df.loc[df['Role']=='Wicket Keeper Batsman']
    BattingStats = pd.DataFrame()
    BattingStats.insert(0,'Player',df2['Player'],True)
    ba = round((df2['Runs'])/((df2['Innings'])-(df2['NotOut'])), 2)
    BattingStats.insert(1,"Batting Average",ba,True)

    bs = round(((df2['Runs'])*100)/(df2['BF']), 2)
    BattingStats.insert(2,"Batting SR",bs,True)

    mra = round((((df2['Fifties'])+(df2['Hundreds']))*100)/(df2['Innings']), 2)
    BattingStats.insert(3,"MRA",mra,True)

    outrate = round((((df2['Innings'])-(df2['NotOut']))*100)/(df2['BF']), 2)
    BattingStats.insert(4,"Outrate",outrate,True)

    bpri = round((4*(df2['Fours']))/(df2['Innings']), 2)
    BattingStats.insert(5,"Boundary Rate",bpri,True)
    #BattingStats = BattingStats.dropna()
    BattingStats.insert(6,'Catches',df['Ct'],True)
    BattingStats.insert(7,'Stumpings',df['St'],True)

    plt.scatter(BattingStats['MRA'],BattingStats['Batting Average'])

    sse = []
    for k in range(1,4):
        km = KMeans(n_clusters=k)
        km.fit(BattingStats[['MRA','Batting Average']])
        sse.append(km.inertia_)
    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,4),sse)
    km = KMeans(n_clusters=2)

    y_predicted = km.fit_predict(BattingStats[['MRA','Batting Average']])
    BattingStats['Cluster'] = y_predicted

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting Average'],color='red')
    plt.scatter(df2.MRA,df2['Batting Average'],color='blue')
    plt.xlabel('MRA')
    plt.ylabel('Batting Average')
    plt.legend()

    df1 = BattingStats[BattingStats.Cluster==0]
    df2 = BattingStats[BattingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.MRA,df1['Batting Average'],color='red')
    plt.scatter(df2.MRA,df2['Batting Average'],color='blue')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('MRA')
    plt.ylabel('Batting Average')
    plt.legend()

    x = len(df1)
    y = len(df2)
    if x > y:
        out = df1
    else: 
        out = df2

    wk = out
    updated_wk = wk.sort_values(by=['MRA'],ascending=False)
    updated_wk = updated_wk.sort_values(by=['Stumpings'],ascending=False)
    set2 = updated_wk[:1]
    substitute2 = updated_wk[1:2]

    df3 = pd.read_csv('dataset/Bowling.csv')
    df3 = df3.loc[df3['Role']=='Bowler']

    BowlingStats = pd.DataFrame()
    BowlingStats.insert(0,'Player',df3['Player'],True)
    BowlingStats.insert(1,'Wickets',df3['Wickets'],True)
    ba = round((df3['Runs'])/(df3['Wickets']), 2)
    BowlingStats.insert(2,"Bowling Average",ba,True)

    bs = round(((df3['Overs'])*6)/(df3['Wickets']), 2)
    BowlingStats.insert(3,"Bowling SR",bs,True)

    er = round((df3['Runs'])/(df3['Overs']), 2)
    BowlingStats.insert(4,"Economy",df3['Economy'],True)

    outrate = round((((df3['Wickets'])*100)/((df3['Overs'])*6)), 2)
    BowlingStats.insert(5,"Outrate",outrate,True)
    BowlingStats.insert(6,'Catches',df3['Ct'],True)
    BowlingStats.insert(7,'Stumpings',df3['St'],True)

    sse = []
    for k in range(1,8):
        km = KMeans(n_clusters=k)
        km.fit(BowlingStats[['Economy','Wickets']])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error')
    plt.plot(range(1,8),sse)

    scaler = MinMaxScaler()

    scaler.fit(BowlingStats[['Wickets']])
    BowlingStats['Wickets'] = scaler.transform(BowlingStats[['Wickets']])

    scaler.fit(BowlingStats[['Economy']])
    BowlingStats['Economy'] = scaler.transform(BowlingStats[['Economy']])
    km = KMeans(n_clusters=2)
    y_predicted = km.fit_predict(BowlingStats[['Economy','Wickets']])

    BowlingStats['Cluster']=y_predicted

    df1 = BowlingStats[BowlingStats.Cluster==0]
    df2 = BowlingStats[BowlingStats.Cluster==1]
    plt.figure(figsize=(12,6))
    plt.scatter(df1.Economy,df1['Wickets'],color='green')
    plt.scatter(df2.Economy,df2['Wickets'],color='red')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*')
    plt.xlabel('Economy')
    plt.ylabel('Wickets')
    plt.legend()

    x = len(df1)
    y = len(df2)
    if x > y:
        out = df1
    else: 
        out = df2

    bowler = out

    updated_bowler = bowler.sort_values(by=['Economy'],ascending=False)
    updated_bowler = bowler.sort_values(by=['Catches'],ascending=False)
    set3 = updated_bowler[:3]
    substitute3 = updated_bowler[3:6]

    df4 = pd.read_csv('dataset/Allrounder.csv')
    df4 = df4.dropna()
    allrounder = df4.sort_values(by=['Wickets'], ascending=False)
    updated_allrounder = allrounder.sort_values(by=['Ct'], ascending=False)

    set4 = updated_allrounder[:2]
    substitute4 = updated_allrounder[2:3]

    final = [set1, set2, set4, set3]
    output = pd.concat(final)

    output.reset_index(inplace=True)
    output.drop("index",axis=1,inplace=True)

    sfinal = [substitute1,substitute2,substitute3,substitute4]
    soutput = pd.concat(sfinal)

    soutput.reset_index(inplace=True)
    soutput.drop("index",axis=1,inplace=True)

    output.fillna('0.0', inplace=True)
    soutput.fillna('0.0', inplace=True)

    return output, soutput