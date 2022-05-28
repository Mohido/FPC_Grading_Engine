from fpcg_engine import FPCG_Engine
import re
import pandas as pd



# ----------------------------------------  Callbacks AREA
def mini_quiz_fulfilled(rowIDs, row_data):
    mini_quiz_sum = sum([score[1] for score in row_data])
    return mini_quiz_sum >= 25  

def mini_quiz_score(rowIDs, row_data):
    mini_quiz_sum = sum([score[1] for score in row_data])
    return mini_quiz_sum 

def theoritical_score(rowIDs, row_data):
    midterm = [score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]
    midterm = midterm[0] if len(midterm) > 0 else 0

    endterm = [score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]
    endterm = endterm[0] if len(endterm) > 0 else 0

    bigterm = [score[1] for score in row_data if re.match(r".*[Bb]ig.*", score[0])]
    bigterm = bigterm[0] if len(bigterm) > 0 else 0

    theory_score = max((midterm + endterm) * 2, bigterm)
    return theory_score

def programming_score(rowIDs, row_data):
    midterm = [score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]
    midterm = max(midterm) if len(midterm) > 0 else 0

    endterm = [score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]
    endterm = max(endterm) if len(endterm) > 0 else 0

    programming_score = ((midterm / 100) + (endterm/100)) * 35 # 35% endterm and 35% midterm
    return programming_score


def progress_fulfilled(rowIDs, row_data):
    accum = 0
    for pt in row_data:
        pt_score = pt[1]
        while (pt_score >= 50):
            accum += 1
            pt_score -= 100
    return accum >= 5 

def progress_count(rowIDs, row_data):
    accum = 0
    for pt in row_data:
        pt_score = pt[1]
        while (pt_score >= 50):
            accum += 1
            pt_score -= 100
    return accum


def homework_score(rowIDs, row_data):
    homework_sum = sum([data[1] for data in row_data])
    return min((homework_sum / 1000) * 15, 15)


def neptun_code(rowIDs, row_data):
    return "".join(rowIDs).split("@")[0].upper()
    


# ------------------------ Configuration Area

configurations = [
     {
        "paths" : [
            "res/FP Lab Gr1 Thu 2-3.30 pm grades - 05-26-2022, 04-39 AM.csv",
            "res/FP Lab Gr2 Fri 12-1.30 pm grades - 05-26-2022, 04-38 AM.csv", 
            "res/FP Lab Gr3 Thu 4-5.30 pm grades - 05-26-2022, 04-29 AM.csv",
            "res/FP Lab Gr4 Fri 10.15-11.45 am grades - 05-26-2022, 04-36 AM.csv"],
        "rename_patterns" : [],
        "rowIDs" : ["Email Address"],
        "evaluations" : [
            {
                "name" : "first-name",
                "nullfilter": True,
                "columns" : [r".*[Ff]irst.*[Nn]ame.*"],
                "callback": lambda rowIDs, row_data: row_data[0][1] 
            },
            {
                "name" : "last-name",
                "nullfilter": True,
                "columns" : [r".*[Ll]ast.*[Nn]ame.*"],
                "callback": lambda rowIDs, row_data: row_data[0][1] 
            },
            {
                "name" : "passed-progress-task-count",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": progress_count
            },
            {
                "name" : "progress-task-precondition-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": progress_fulfilled
            },
            {
                "name" : "homework-raw-sum",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": lambda IDs, row_data: sum([data[1] for data in row_data])
            },
            {
                "name" : "homework-percentage-15%",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_score
            },
            {
                "name" : "neptun-code",
                "nullfilter": True,
                "columns" : [r".*"],
                "callback": neptun_code 
            }
        ]
    },
    {
        "paths" : ["res/2022-05-24T0507_Grades-2021_22_2_IP-18fFUNPEG_90_-_Functional_programming_L+Pr..csv"],
        "rename_patterns" : [("SIS Login ID", "neptun-code")],
        "rowIDs" : ["Student"],
        "evaluations" : [
            {
                "name" : "mini-quiz-raw-sum",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*")],
                "callback": mini_quiz_score
            },
            {
                "name" : "mini-quiz-precondition-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*")],
                "callback": mini_quiz_fulfilled
            },
            {
                "name" : "theory-score",
                "nullfilter": True,
                "columns" : [re.compile(".*[Mm]id.*[Qq]uiz.*"), re.compile(".*[Ee]nd.*[Qq]uiz.*"), re.compile(".*[Bb]ig.*[Qq]uiz.*")],
                "callback": theoritical_score
            },
            {
                "name" : "theory-percentage-15%",
                "nullfilter": True,
                "columns" : [re.compile(".*[Mm]id.*[Qq]uiz.*"), re.compile(".*[Ee]nd.*[Qq]uiz.*"), re.compile(".*[Bb]ig.*[Qq]uiz.*")],
                "callback": lambda IDs, row_data: (theoritical_score(IDs, row_data) / 100) * 15
            },
            {
                "name" : "midterm-score",
                "nullfilter": True,
                "columns" : [re.compile(".*[Mm]id.*[Pp]rogramming.*")],
                "callback": lambda IDs, row_data: max([score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]) if len([score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]) > 0 else 0
            },
            {
                "name" : "endterm-score",
                "nullfilter": True,
                "columns" : [re.compile(".*[Ee]nd.*[Pp]rogramming.*")],
                "callback": lambda IDs, row_data: max([score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]) if len([score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]) > 0 else 0
            },
            {
                "name" : "programming-exam-contribution-70%",
                "nullfilter": True,
                "columns" : [re.compile(".*[Mm]id.*[Pp]rogramming.*"), re.compile(".*[Ee]nd.*[Pp]rogramming.*")],
                "callback": programming_score
            },
            {
                "name" : "neptun-code",
                "nullfilter": True,
                "columns" : ["neptun-code"],
                "callback": lambda rowIDs, row_data : row_data[0][1]
            }
        ]
    }
]

# ----------------------------------- Processing Area
fpc = FPCG_Engine(configurations)
evaluation_tables = fpc.evaluate()

# Canvas evaluation
# evaluation_tables[0].to_csv("res/canvas_evaluation.csv")

# Teams evaluation
evaluation_tables[1].set_index("neptun-code", inplace=True, verify_integrity=True)
evaluation_tables[0].set_index("neptun-code", inplace=True, verify_integrity=True)

final_table = pd.concat([evaluation_tables[0], evaluation_tables[1]], verify_integrity=True, axis=1)

final_table.to_csv("res/main_evaluation.csv")
