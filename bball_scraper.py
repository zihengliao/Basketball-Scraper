"""
The goal is to find if the 3 point shot has made the league into a higher scoring league
and how has the 3 point shot affect a team
"""



import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd



home_url = 'https://www.basketball-reference.com'



# open the file in the write mode
# f = open('csv_file.csv', 'w')

# create the csv writer
# writer = csv.writer(f)




# print(teams.prettify())

total_three_pointer = {}
total_points = {}

condition = True
for year in range(2023, 2020, -1):

    url = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'
    r = requests.get(url).text

    soup = BeautifulSoup(r, 'lxml')

    teams = soup.find('div',id = 'switcher_totals_team-opponent').tbody
    # print(teams.prettify())
    teams = teams.find_all('tr')

    average = 0     # three pointer
    average_points = 0
    team_amount = 0
    for i in teams:
        team_url = i.td.a['href']
        team_url = re.sub('\d+', f'{year}', team_url)

        team = i.td.a.text
        # print(team)
        # write a row to the csv file
        
        # print(home_url + team_url)
        team_r = requests.get(home_url + team_url).text
        soup = BeautifulSoup(team_r, 'lxml')
        # print(soup.prettify())
        data_stuff = soup.find('div', id = 'all_team_and_opponent') 
        # data_stuff = soup.find('div', class_ = 'table_container is_setup')
        data_stuff = str(data_stuff)
        tpa = re.findall('fg3a" >\d+', data_stuff)
        tpa = tpa[0].split('>')[1]
        average += int(tpa)
        
        points = re.findall('pts" >\d+', data_stuff)
        points = points[2].split('>')[1]
        average_points += int(points)
        # print(points)
        # writer.writerow([team, tpa])
        if condition:
            total_three_pointer[f'{team}'] = [tpa]
            

            total_points[f'{team}'] = [points]
            
        else:
            lst_tpa = total_three_pointer[f'{team}']
            lst_tpa.append(tpa)
            

            total_points[f'{team}'].append(points)
            
            # print(lst_tpa)
        # the amount of teams playing that season
        team_amount += 1


    
    average = round(average / team_amount, 2)        # 30 teams in the nba
    average_points = round(average_points / team_amount, 2)
    if condition:
        total_three_pointer['average'] = [average]
        total_three_pointer['year'] = [year]

        total_points['average'] = [average_points]
        total_points['year'] = [year]
    else:
        total_three_pointer['average'].append(average)
        total_three_pointer['year'].append(year)

        total_points['average'].append(average_points)
        total_points['year'].append(year)

    condition = False
    print(total_three_pointer)
    print('\n \n')
    print(total_points)



# close the file
# f.close()

# df = pd.read_csv('csv_file.csv')
# print(df)

df = pd.DataFrame(total_three_pointer)
df.set_index('year', inplace = True)
df.to_csv('csv_file.csv')

print(df)

points_df = pd.DataFrame(total_points)
points_df.set_index('year', inplace = True)
points_df.to_csv('points.csv')






