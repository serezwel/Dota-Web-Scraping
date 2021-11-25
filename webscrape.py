import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#function to get team agents and result
def get_match_data(match_url):
    game_data = []
    page = requests.get(match_url)
    match_src = page.content
    match_soup = BeautifulSoup(match_src, 'lxml')
    get_matches = match_soup.find("div", attrs = {"class": "vm-stats-container"})
    get_matches = get_matches.find_all("div", attrs = {"data-game-id" : re.compile('[0-9]+')})
    for matches in get_matches:
        match_data = []
        try: 
            get_agents_tag = matches.find_all("td", attrs={"class" : "mod-agents"})
            #Get 10 agents in the game
            for agents in get_agents_tag:
                match_data.append(agents.find("img").attrs["alt"])
            get_map = matches.find("div", attrs={"class" : "map"})
            #Clean map text
            game_map = re.search("Split|Bind|Ascent|Icebox|Haven|Breeze|Fracture", get_map.text).group()
            #Append map into match data
            match_data.append(game_map)
            get_team2score = matches.find("div", attrs={"class" : "team mod-right"})
            get_team2score = get_team2score.find("div", class_ = "score")
            get_team1score = matches.find("div", attrs={"class": "team"})
            get_team1score = get_team1score.find("div", class_= "score")
            if (int(get_team2score.text) > int(get_team1score.text)):
                match_data.append("Team 2")
            else:
                match_data.append("Team 1")
            game_data.append(match_data)
        except AttributeError:
            continue
    return game_data




match_details = ["Team1Agent1", "Team1Agent2", "Team1Agent3", "Team1Agent4", "Team1Agent5",
 "Team2Agent1", "Team2Agent2", "Team2Agent3", "Team2Agent4", "Team2Agent5", "Map", "Victory"]
#create dataframe for matches
match_df = pd.DataFrame()
#loop through pages

for i in range(1, 151):
    url = "https://www.vlr.gg/matches/results/?page=" + str(i)
    result_page = requests.get(url)
    src = result_page.content
    soup = BeautifulSoup(src, 'lxml')
    get_matches_div = soup.find_all("div", attrs={"class" : "wf-card"})[1:]
    for div in get_matches_div:
        matches_list = div.find_all('a')
        for match in matches_list:
            match_url = "https://www.vlr.gg" + match.attrs["href"]
            match_data = get_match_data(match_url)
            match_df = match_df.append(match_data, ignore_index = True)
    print(f"Opening page: {i}")
match_df.columns = match_details
print(match_df)
match_df.to_csv("matches.csv", index=False)