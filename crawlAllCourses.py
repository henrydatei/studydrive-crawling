from studydrive import studydriveapi
from datetime import datetime
import multiprocessing

def produceOutput(universityID):
    print(universityID)
    totalResult = ""
    for course in api.getUniversityCourses(universityID)[0:5]:
        totalResult += produceOutput2(course) + "\n"
    return totalResult
        

def produceOutput2(course):
    moreData = api.getCourseDetails(course["course_id"])["course"]
    currentDate = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
    if course["qlearningid"] is None:
        ql = ""
    else:
        ql = course["qlearningid"]
    if course["originator"] is None:
        ori = ""
    else:
        ori = str(course["originator"])
    try:
        spo = str(moreData["sponsoring"]["company"]["id"])
    except:
        spo = "NULL"
    try:
        spoName = moreData["sponsoring"]["company"]["company_name"]
    except:
        spoName = ""
    return str(course["course_id"]) + ",\"" + course["number"] + "\",\"" + course["name"] + "\",\"" + ql + "\",\"" + ori + "\"," + str(course["active"]) + "," + str(course["copyright_warning"]) + "," + str(course["users_count"]) + "," + str(int(course["has_joined"])) + ",\"" + course["share_link"][:len(course["share_link"]) - 12] + "\",\"" + course["email_body"] + "\",\"" + course["email_subject"] + "\"," + str(course["university_id"]) + "," + str(int(moreData["is_sponsored"])) + ",\"" + moreData["image_url"] + "\",\"" + moreData["description_text"] + "\",\"" + moreData["course_description"]["exam_date"] + "\"," + spo + ",\"" + spoName + "\"," + currentDate

api = studydriveapi.StudydriveAPI()
api.login("studydrive-crawl@web.de", "qwertzuiop")

p = multiprocessing.Pool(20)
unis = [university["university_id"] for university in api.getUniversities()[0:1]]
with open("output_2.csv", "w") as f:
    for result in p.imap(produceOutput, unis):
        f.write(result + "\n")