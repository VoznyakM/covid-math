import numpy as np
#import matplotlib.pyplot as plt
import requests
import sys
from datetime import datetime, timedelta

COUNTRY = "Ukraine"
DAYS_OF_SIMULATION = 366
COEF_BASE = 0.35
COEF_QUARANTINE = 0.135
DAY_QUARANTINE = 74
INCUBATION_PERIOD = 15
COVID_API_URL = 'http://localhost:3000/stats/'
START_DATE = datetime(2020, 8, 10, 17, 24, 49, 243497)
#datetime.now() # date(2019, 4, 13)

np.random.seed(0)

def get_coef(day):
    return COEF_BASE if day < DAY_QUARANTINE else COEF_QUARANTINE

if __name__ == "__main__":
    days = np.arange(1, DAYS_OF_SIMULATION)
    date = START_DATE

    infected = np.random.randint(1, INCUBATION_PERIOD, 1)

    infected_lst = []  
    new_cases_lst = []
    new_cases_total_lst = []

    for day in days:
        coef = get_coef(day)

        new_cases_idx = np.argwhere(infected == day).flatten()
        new_cases_count = new_cases_idx.size

        infected = np.delete(infected, new_cases_idx)

        new_infected_count = np.random.poisson(coef, infected.size).sum()
        new_infected = np.random.randint(1, INCUBATION_PERIOD, new_infected_count) + day
        infected = np.concatenate((infected, new_infected))

        infected_lst.append(infected.size)
        new_cases_lst.append(new_cases_count)
        new_cases_total_lst.append(sum(new_cases_lst))

        # print(day, infected.size)

        date = date + timedelta(days=1)
        stats = {
           "date":  datetime.strftime(date, "%Y-%m-%d"), 
           "cases": infected.size, 
           "deaths": round(np.random.poisson(coef, infected.size).sum() * 0.03), 
           "recovered": round(np.random.poisson(coef, infected.size).sum() * 0.06)
        }
#        print (stats)

        try:
          resp = requests.post(COVID_API_URL, json=stats)
          if resp.status_code != 201:
            raise ApiError('POST ' + COVID_API_URL + ' {}'.format(resp.status_code))
          print('Created stats. ID: {}'.format(resp.json()["id"]))
        except:
          print ('Cant connect to API server')
          sys.exit()

"""
    plt.figure(figsize=(16, 8))

    plt.subplot(311)
    plt.title(f"COVID-19 pandemic in {COUNTRY}")
    plt.plot(days, new_cases_total_lst)
    plt.grid(True)
    plt.legend(["Total cases"], loc='upper left')

    plt.subplot(312)
    plt.bar(days, new_cases_lst, alpha=0.7, color='y')
    plt.grid(True)
    plt.legend(["New cases"], loc='upper left')

    plt.subplot(313)
    plt.plot(days, infected_lst, color='r')
    plt.grid(True)
    plt.legend(["Infected"], loc='upper left')

    plt.show()
"""