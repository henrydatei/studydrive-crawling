from studydrive import studydriveapi
from datetime import datetime
import multiprocessing
import pandas as pd
import csv
from copy import deepcopy
import os

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

def produceOutput(questionID):
    print(questionID)
    try:
        data = api.getInformationAboutQuestion(questionType = questionType, questionID = questionID)
        
        ########################################
        # question
        ########################################
        
        dataCopy = deepcopy(data["data"])
        del dataCopy["answers"]
        del dataCopy["user_data"]
        del dataCopy["files"]
        if "fileLink" in dataCopy:
            del dataCopy["fileLink"]
        if "poll" in dataCopy:
            del dataCopy["poll"]
        data_df = pd.DataFrame(dataCopy, index = [0])
        if "file_id" in data_df.columns:
            file_id = data_df["file_id"].iloc[0]
            data_df.drop(columns = ["file_id"], inplace = True)
            data_df["belongs_to_type"] = "document"
            data_df["belongs_to_id"] = file_id
        if "course_id" in data_df.columns:
            course_id = data_df["course_id"].iloc[0]
            data_df.drop(columns = ["course_id"], inplace = True)
            data_df["belongs_to_type"] = "course"
            data_df["belongs_to_id"] = course_id
        if "group_id" in data_df.columns:
            group_id = data_df["group_id"].iloc[0]
            data_df.drop(columns = ["group_id"], inplace = True)
            data_df["belongs_to_type"] = "group"
            data_df["belongs_to_id"] = group_id
        data_df.loc[0, "text"] = data_df.loc[0, "text"].replace("\n", " ")
        data_df.loc[0, "emailBody"] = data_df.loc[0, "emailBody"].replace("\n", " ")
        data_df.rename(columns = {"id": "question_id"}, inplace = True)

        userData_df = pd.DataFrame(data["data"]["user_data"], index = [0])
        userData_df.rename(columns = {"id": "user_data_id", "identity_id": "user_data_identity_id", "name": "user_data_name", "link": "user_data_link", "picture": "user_data_picture", "profile_picture": "user_data_profile_picture", "karma_points": "user_data_karma_points", "time": "user_data_time"}, inplace = True)

        dataCopy2 = deepcopy(data)
        del dataCopy2["data"]
        del dataCopy2["user_identity"]
        if "course" in dataCopy2:
            del dataCopy2["course"]
        if "group" in dataCopy2:
            del dataCopy2["group"]
        if "file_name" in dataCopy2:
            del dataCopy2["file_name"]
        del dataCopy2["type"]
        question_df = pd.DataFrame(dataCopy2, index = [0])
        question_df.rename(columns = {"questionType": "type"}, inplace = True)

        full_df = pd.concat([data_df, userData_df, question_df], axis = 1)
        full_df["added"] = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
        newColOrder = ["question_id", "time", "type", "pin", "is_edited", "text", "is_anonymous", "is_reported", "can_edit", "is_owner", "is_admin", "created_at", "updated_at", "belongs_to_type", "belongs_to_id", "upvotes", "downvotes", "has_poll", "has_marking", "answered", "user_data_id", "user_data_identity_id", "user_data_name", "user_data_link", "user_data_picture", "user_data_profile_picture", "user_data_karma_points", "user_data_time", "answersCount", "maxAnswersShown", "uservote", "user_report", "is_favored", "is_muted", "shareLink", "emailBody", "emailSubject", "added"]
        full_df = full_df[newColOrder]
        full_df.to_csv("output_questions.csv", mode = "a", encoding = 'utf-8', index = False, quoting = csv.QUOTE_NONNUMERIC, escapechar = "\\", float_format = "%0.0f", header = not os.path.exists("output_questions.csv"))

        ########################################
        # files
        ########################################
        
        if len(data["data"]["files"]) > 0:
            files_df = pd.DataFrame(data["data"]["files"])
            files_df.rename(columns = {"id": "file_id"}, inplace = True)
            files_df["belongs_to_type"] = data["questionType"]
            files_df["belongs_to_id"] = data["data"]["id"]
            files_df["added"] = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
            files_df.to_csv("output_files.csv", mode = "a", encoding = 'utf-8', index = False, quoting = csv.QUOTE_NONNUMERIC, escapechar = "\\", float_format = "%0.0f", header = not os.path.exists("output_files.csv"))

        ########################################
        # answers
        ########################################

        answer_df = pd.DataFrame()
        for answer in data["data"]["answers"]:
            answerCopy = deepcopy(answer)
            del answerCopy["user_data"]
            del answerCopy["files"]
            singleAnswer_df = pd.DataFrame(answerCopy, index = [0])
            if singleAnswer_df["is_author"].iloc[0] == False:
                singleAnswer_df.loc[0, "is_author"] = 0
            if singleAnswer_df["is_author"].iloc[0] == True:
                singleAnswer_df.loc[0, "is_author"] = 1
            singleAnswer_df.loc[0, "text"] = singleAnswer_df.loc[0, "text"].replace("\n", " ")
            singleAnswer_df.rename(columns = {"id": "answer_id"}, inplace = True)

            userDataAnswer_df = pd.DataFrame(answer["user_data"], index = [0])
            userDataAnswer_df.rename(columns = {"id": "user_data_id", "identity_id": "user_data_identity_id", "name": "user_data_name", "link": "user_data_link", "picture": "user_data_picture", "profile_picture": "user_data_profile_picture", "karma_points": "user_data_karma_points", "time": "user_data_time"}, inplace = True)

            singleAnswer_df = pd.concat([singleAnswer_df, userDataAnswer_df], axis = 1)
            singleAnswer_df["belongs_to_type"] = data["questionType"]
            singleAnswer_df["belongs_to_id"] = data["data"]["id"]
            singleAnswer_df["added"] = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
            newColOrder = ["answer_id", "text", "upvotes", "downvotes", "is_reported", "is_anonymous", "created_at", "updated_at", "is_edited", "time", "can_edit", "is_owner", "is_best", "user_data_id", "user_data_identity_id", "user_data_name", "user_data_link", "user_data_picture", "user_data_profile_picture", "user_data_karma_points", "user_data_time", "is_author", "is_admin", "uservote", "user_report", "is_nsfw", "belongs_to_type", "belongs_to_id", "added"]
            singleAnswer_df = singleAnswer_df[newColOrder]

            answer_df = pd.concat([answer_df, singleAnswer_df], ignore_index = True)
        answer_df.to_csv("output_answers.csv", mode = "a", encoding = 'utf-8', index = False, quoting = csv.QUOTE_NONNUMERIC, escapechar = "\\", float_format = "%0.0f", header = not os.path.exists("output_answers.csv"))

        ########################################
        # polls
        ########################################

        if data["data"]["has_poll"] == 1:
            poll = deepcopy(data["data"]["poll"])
            del poll["options"]
            del poll["question_id"]
            poll_df = pd.DataFrame(poll, index = [0])
            poll_df["belongs_to_type"] = data["questionType"]
            poll_df["belongs_to_id"] = data["data"]["id"]
            poll_df["added"] = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
            poll_df.to_csv("output_polls.csv", mode = "a", encoding = 'utf-8', index = False, quoting = csv.QUOTE_NONNUMERIC, escapechar = "\\", float_format = "%0.0f", header = not os.path.exists("output_polls.csv"))

        ########################################
        # polloptions
        ########################################

        if data["data"]["has_poll"] == 1:
            pollOptions = data["data"]["poll"]["options"]
            pollOptions_df = pd.DataFrame(pollOptions)
            pollOptions_df["poll_id"] = data["data"]["poll"]["poll_id"]
            pollOptions_df["added"] = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
            pollOptions_df.to_csv("output_polloptions.csv", mode = "a", encoding = 'utf-8', index = False, quoting = csv.QUOTE_NONNUMERIC, escapechar = "\\", float_format = "%0.0f", header = not os.path.exists("output_polloptions.csv"))
    except:
       pass

questionType = "course"
#produceOutput(1986487)
ids = range(500000)
#ids = range(500000, 1000000)
#ids = range(1000000, 1500000)
#ids = range(1500000, 2000000)

#questionType = "group"
#ids = range(500000)
#ids = range(500000, 1000000)
#ids = range(1000000, 1100000)

#questionType = "document"
#ids = range(500000)
#ids = range(500000, 800000)

p = multiprocessing.Pool(20)
p.map(produceOutput, ids)