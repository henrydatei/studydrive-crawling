preLine = ""
preNumber = 0
minLine = ""
minLength = 5000
with open("course_4_output_questions.csv") as f:
    for line in f.readlines():
        # if not line.split(",")[0][0].isdigit():
        #     newLine = preLine.strip() + line
        #     print(newLine, end = "")
        # else:
        #     print(line, end = "")
        # preLine = line
        # number = line.split(",")[0]
        # if (number != preNumber) and ("2022-06-10" in line.split(",")[-1]) and (len(line) > 50):
        #     print(line, end = "")
        # preNumber = number
        if len(line) < minLength and len(line) > 1:
            minLength = len(line)
            minLine = line
    print(minLine)
