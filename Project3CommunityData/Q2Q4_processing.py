import os
import csv
import statistics
import numpy as np
import matplotlib.pyplot as plt 

team = {}

for t in range(1, 9):
    tr = ['Team'+str(t)+'/clean_data/seq3/'+x for x in os.listdir('Team'+str(t)+'/clean_data/seq3') if 'tr1' in x]
    teamid = "Team"+str(t)
    team[teamid] = {}
    for r in tr:
        with open(r, 'r') as csvfile:
            website = r.split("_")[2]
            if not(website in team[teamid]):
                team[teamid][website] = {}

            dat = csv.reader(csvfile)
            delays = [] # [[date, time, ip, avg delay]]
            for row in dat:
                # website, date, time, traceroute hop index, IP of hop,  
                # delay1, delay2, delay3, average delay
                if (len(row) > 7 and row[7] != 'N/A' and row[7] != -1):
                    delays.append([row[1], row[2], row[4], row[7]])
            avg_delays = [float(x[3]) for x in delays]
            a = np.array(avg_delays)
            threshold = 1.5 * (np.percentile(a, 75) - np.percentile(a, 25))
            ips_past = [x[2] for x in delays if float(x[3]) > threshold]
            team[teamid][website]["threshold"] = threshold
            team[teamid][website]["bottlenecks"] = ips_past

all_websites = []
for t in team:
    webs = team[t].keys()
    all_websites.append(webs)


timey = {'amazon':{}, 'bbc':{}, 'youtube':{}, 'walmart':{}}
# websites = ['amazon', 'bbc', 'youtube', 'walmart']
websites = ['wikipedia', 'reddit', 'youtube']
weekend_days = ['05-16-2020', '05-17-2020', '05-23-2020', '05-24-2020']
weekday_days = []
for i in range(13, 27):
    day = '05-'+str(i)+'-2020'
    if not(day in weekend_days):
        weekday_days.append(day)

weekday = [0]*4
weekend = [0]*4
index = -1
for web in websites:
    index += 1
    for t in team:
        for w in team[t]:
            if w == web:
                print(w, t, team[t][w]['bottlenecks'])
                

                
