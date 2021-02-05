# Author: Gabriel Teixeira
# Github: GabTeixeira
import re
import os
import csv
import requests
from bs4 import BeautifulSoup


print("Welcome, this is a script that get players information from soFifa. The original script gets information from the last update")

print('\nYou can find the team id in the url, for example: \"https://sofifa.com/team/11/manchester-united/\".\n11 is the Man Utd id')

getTeam = input("\nPlease, enter the team id on the SoFifa:\n")

try:
    page = requests.get("https://sofifa.com/players?type=all&tm[]="+getTeam)
except:
    print("Error: please check your connection")
    exit()

if(page.status_code == 200):
    soup = BeautifulSoup(page.content,'html.parser')
    table = soup.find('table').find('tbody')
    all_a = table.find_all('a', {'class':'tooltip'})

    # List with player's href 
    players_list = ['https://sofifa.com'+ player['href'] for player in all_a]
    
    # List with player objects
    players = []

    if not len(players_list):
        print("Error: Please, check if your team has players")
        exit()

    print("Starting to get the players...\n")
    for player in players_list:
        try:
            page_player = requests.get(player)
        except:
            print("Error: please check your connection")
            exit()
        soup_player = BeautifulSoup(page_player.content, 'html.parser')
        team = soup_player.find_all('div',{'class':'card'})[2].find('h5').string

        foot = soup_player.find_all('div',{'class':'card'})[0].find('ul').find('li').get_text()
        foot = foot[foot.find('t')+1:]        

        name = soup_player.find('div',{'class':'info'}).find('h1').string

        # Main Position 
        position = soup_player.find('div',{'class':'info'}).find('div').find("span").string
        
        # Age, Height and Weight
        general = soup_player.find('div',{'class':'info'}).find('div').getText().split('o.')
        
        start_birthday = general[1].find("(")
        end_birthday = general[1].find(")")+1

        start_height = end_birthday+1
        end_height = general[1].find("\"")+1

        start_weight = end_height+1

        birthday = general[1][start_birthday:end_birthday]
        height = general[1][start_height:end_height]
        weight = general[1][start_weight:]

        # Get the player's overall and his potential
        ovr = soup_player.find('section',{'class':'card spacing'}).find_all('div', {'class':'column'})
        current_ovr = ovr[0].find('span').string
        potential_ovr = ovr[1].find('span').string

        print("Player: " + name)
        players.append({"name":name, "overall":current_ovr, "potential":potential_ovr,"position":position, "birthday":birthday,"height":height,"weight":weight,"foot":foot})

    print("\nYour team is: " + team)

    #filename without whitespace
    team = team.replace(" ","")

    try:
        if(not os.path.isdir('teams')):
            os.mkdir('teams')
        f = open('teams/'+team+'.csv','w')
    except:
        print("Error: An error has occurred while creating the file")
        exit()

    print("Starting to write your csv file...\n")
    with f:
        fnames = ['name','overall','potential','position','birthday','height','weight','foot']
        writer = csv.DictWriter(f,fieldnames = fnames)

        writer.writeheader()
        for player in players:
            writer.writerow({'name':player['name'],'overall':player['overall'],
            'potential':player['potential'],'position':player['position'],
            'birthday':player['birthday'],'height':player['height'],'weight':player['weight'],'foot':player['foot']})

    print("CSV is complete, the name of your file is: "+team+".csv\n"+"You can find it in \"teams\" folder. ")

else:
    print("An error has occurred, the page status code is: " + page.status_code)