from studydrive import studydriveapi
from datetime import datetime
import pandas as pd
import csv

try:
    file = open("main-account.txt")
    loginData = file.read()
    mainUsername = loginData.split(":")[0]
    mainPassword = loginData.split(":")[1]
except:
    print("main-account.txt not found")
    print("I'll create the file main-account.txt with your credentials.")
    file = open("main-account.txt", "w+")
    mainUsername = input('Email: ')
    mainPassword = input('Password: ')
    file.write(str(mainUsername) + ":" + str(mainPassword))
finally:
    file.close()

api = studydriveapi.StudydriveAPI()
api.login(mainUsername, mainPassword)

df = pd.DataFrame(api.getUniversities())
df["added"] = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
df.to_csv("output_universities.csv", encoding = 'utf-8', index = False, quoting = csv.QUOTE_NONNUMERIC, escapechar = "\\", float_format = "%0.0f")