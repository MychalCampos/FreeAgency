# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 20:57:59 2015
scraping data on NBA free agency transactions from www.sportrac.com
@author: Mychal
"""
# import os
# os.getcwd() # get current working directory

from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

years = range(2011, 2016)

for y in years:
    # this website has nicer tables, but each cell in the table has its
    # own separate tag
    base_url = "http://www.spotrac.com/nba/free-agents/" + str(y) + "/signed/"
    soup = BeautifulSoup(urlopen(base_url).read(), 'lxml')

    player_bs4e = soup.find_all("td", " player")

    player_info = soup.find_all("td", "center")
    position = []
    age = []
    agency_type = []
    team_from = []
    team_to = []
    years_contract = []
    i = 0
    while i < len(player_info):
        position.append(str(player_info[i].string))
        age.append(str(player_info[i+1].string))
        agency_type.append(str(player_info[i+2].string))
        team_from.append(str(player_info[i+3].string))
        team_to.append(str(player_info[i+4].string))
        years_contract.append(str(player_info[i+5].string))
        i = i + 6
        if len(position) == len(player_bs4e):
            break

    amounts = soup.find_all("td", "right")
    i = 0
    total_amount = []
    avg_amount = []
    while i < len(amounts):
        total_amount.append(str(amounts[i].string))
        avg_amount.append(str(amounts[i+1].string))
        i = i + 2
        if len(total_amount) == len(player_bs4e):
            break

    with open("freeagency" + str(y) + ".tsv", "w") as f:
        fieldnames = ("player", "position", "age", "agency_type", "team_from",
            "team_to", "years_contract", "total_amount", "avg_amount")
        output = csv.writer(f, delimiter="\t")
        output.writerow(fieldnames)

        for i in range(0, len(player_bs4e)):
            player = str(player_bs4e[i].string)
            position_i = position[i]
            age_i = age[i]
            agency_type_i = agency_type[i]
            team_from_i = team_from[i]
            team_to_i = team_to[i]
            years_contract_i = years_contract[i]
            total_amount_i = total_amount[i]
            avg_amount_i = avg_amount[i]

            output.writerow([player, position_i, age_i, agency_type_i,
                             team_from_i, team_to_i, years_contract_i,
                             total_amount_i, avg_amount_i])

    f.close()
