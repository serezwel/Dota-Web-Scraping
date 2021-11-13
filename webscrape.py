import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#NEED TO IMPLEMENT MORE THAN BO1
#NEED TO FIX FINDING WINNER

#function to get team agents and result
def get_match_data(match_url):
    match_data = []
    page = requests.get(match_url)
    match_src = page.content
    match_soup = BeautifulSoup(match_src, 'lxml')
    get_agents_tag = match_soup.find_all("td", attrs={"class" : "mod-agents"})
    #Get 10 agents in the game
    for agents in get_agents_tag:
        match_data.append(agents.find("img").attrs["alt"])
        match_data = match_data[:10]
    get_map = match_soup.find("div", attrs={"class" : "map"})
    #Clean map text
    game_map = re.sub("\s+", "", get_map.text)
    game_map = re.sub("[0-9]*:*[0-9]*:*[0-9]*", "", game_map)
    #Append map into match data
    match_data.append(game_map)
    #get_winner = match_soup.find("div", attrs={"class" : "team mod-right"})
    #if (get_winner.find("div", attrs={"class": "score "}).text == "13"):
    #    match_data.append("Team 2")
    #else:
    #    match_data.append("Team 1")
    return match_data




match_details = ["Team1Agent1", "Team1Agent2", "Team1Agent3", "Team1Agent4", "Team1Agent5",
 "Team2Agent1", "Team2Agent2", "Team2Agent3", "Team2Agent4", "Team2Agent5", "Map", "Victory"]
#create dataframe for matches
match_df = pd.DataFrame(columns = match_details)
#loop through pages
for i in range(1, 2):
    url = "https://www.vlr.gg/matches/results/?page=" + str(i)
    result_page = requests.get(url)
    src = result_page.content
    soup = BeautifulSoup(src, 'lxml')
    get_matches_div = soup.find_all("div", attrs={"class" : "wf-card"})[1:]
    for matches_list in get_matches_div:
        for match in matches_list:
            try:
                match_url = "https://www.vlr.gg" + match.attrs["href"]
                match_data = get_match_data(match_url)
                print(match_data)
            except:
                continue
