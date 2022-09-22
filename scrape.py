import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import requests

nba_team = ["ATL", "BRK", "BOS", "CHI", "CHO", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM",
           "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
seasons = ["2017","2018", "2019", "2020", "2021", "2022"]
path = "/Users/Alex/Desktop/new/bell_curve_model/game_logs/"

for i in range(len(nba_team)):
    for j in range(len(seasons)):
        page = requests.get("https://www.basketball-reference.com/teams/{}/{}/gamelog-advanced/".format(nba_team[i], seasons[j]))
        soup = BeautifulSoup(page.content, "html.parser") 
        column_headers = [th.getText() for th in
                          soup.findAll('tr')[1].findAll('th')] # Column headers for our dataframe
        data_rows = soup.findAll('tr')[2:] # tr defines a row in HTML table
        # Data rows for our dataframe
        team_data = [[td.getText() for td in data_rows[i].findAll('td')]
                    for i in range(len(data_rows))] # list for team datas
        team = []
        for l in range(len(team_data)):
            if(len(team_data[l]) > 0):
                team.append(team_data[l][:23])
            else:
                continue
        team_df = pd.DataFrame(team, columns=column_headers[1:24])
        input_team = []
        for m in range(len(team_df)):
            input_team.append(nba_team[i]) # "BOS" can be change to index in a list
        team_df.insert(2, "Team", input_team) # dataframe for TEAM ONLY
        opponent = [] 
        for n in range(len(team_data)):
            if(len(team_data[n]) > 0):
                opponent.append(team_data[n][24:41])
            else:
                continue
        opponent_df = pd.DataFrame(opponent, columns= column_headers[25:41]) # dataframe for OPPONENT ONLY
        df = team_df.join(opponent_df, lsuffix="_for", rsuffix="_against") 
        df = df.set_index("G")
        # add joint dataframe to overall dataframe
        df.to_csv(path + "{}_{}.csv".format(nba_team[i], seasons[j]))
        time.sleep(1)