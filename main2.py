from fpcg_engine_v2 import FPCG_Engine
import re

def mini_quiz_fulfilled(rowIDs, row_data):
    mini_quiz_sum = sum([score[1] for score in row_data])
    # print(rowIDs[0], mini_quiz_sum)
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

    theory_score = (max((midterm + endterm) * 2, bigterm) / 100) * 15
    return theory_score

def programming_score(rowIDs, row_data):
    midterm = [score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]
    midterm = max(midterm) if len(midterm) > 0 else 0

    endterm = [score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]
    endterm = max(endterm) if len(endterm) > 0 else 0

    programming_score = ((midterm / 100) + (endterm/100)) * 35 # 35% endterm and 35% midterm
    return programming_score



configurations = [
    {
        "paths" : ["res/2022-05-24T0507_Grades-2021_22_2_IP-18fFUNPEG_90_-_Functional_programming_L+Pr..csv"],
        "rename_patterns" : [("SIS Login ID", "neptun-code")],
        "rowIDs" : ["neptun-code", "Student"],
        "evaluations" : [
            {
                "name" : "mini-quiz-score",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*")],
                "callback": mini_quiz_score
            },
            {
                "name" : "mini-quiz-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*")],
                "callback": mini_quiz_fulfilled
            },
            {
                "name" : "theory-percentage",
                "nullfilter": True,
                "columns" : [re.compile(".*[Mm]id.*[Qq]uiz.*"), re.compile(".*[Ee]nd.*[Qq]uiz.*"), re.compile(".*[Bb]ig.*[Qq]uiz.*")],
                "callback": theoritical_score
            },
            {
                "name" : "programming-percentage",
                "nullfilter": True,
                "columns" : [re.compile(".*[Mm]id.*[Pp]rogramming.*"), re.compile(".*[Ee]nd.*[Pp]rogramming.*")],
                "callback": programming_score
            }
        ]
    }
]


fpc = FPCG_Engine(configurations)
evaluation_tables = fpc.evaluate()
evaluation_tables[0].fillna(0).to_csv("res/canvas_process.csv")


