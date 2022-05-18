from datetime import datetime
from numpy import equal
import pandas as pd

""" Function to get the list of the late employees """
def WhoIsLate():
    df = pd.read_csv('Attendance.csv')
    now = datetime.today().strftime('%Y-%d-%B')
    print(now)
    with open('TodayLateList.csv', 'r+') as f:
        for i in range(len(df)):
            name = df.values[i][0]
            time = df.values[i][1]
            date = df.values[i][2]
            if str(time) > "10:03:00.0" and str(date) == str(now):
                f.writelines(f'\n {name},{time}')

               
   

func = WhoIsLate()
