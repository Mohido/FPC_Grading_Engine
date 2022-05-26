from fpcg_engine import FPCG_Engine
import re



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

    theory_score = (max((midterm + endterm) * 2, bigterm) / 100) * 15
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

def homework_score(rowIDs, row_data):
    homework_sum = sum([data[1] for data in row_data])
    return min((homework_sum / 1000) * 15, 15)



# ------------------------ Configuration Area

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
    },
    {
        "paths" : ["res/FP Lab Gr1 Thu 2-3.30 pm grades - 05-26-2022, 04-39 AM.csv"],
        "rename_patterns" : [],
        "rowIDs" : ["Email Address", "First Name", "Last Name"],
        "evaluations" : [
            {
                "name" : "progress-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": progress_fulfilled
            },
            {
                "name" : "homework-percentage",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_score
            },
        ]
    }
    ,
    {
        "paths" : ["res/FP Lab Gr2 Fri 12-1.30 pm grades - 05-26-2022, 04-38 AM.csv"],
        "rename_patterns" : [],
        "rowIDs" : ["Email Address", "First Name", "Last Name"],
        "evaluations" : [
            {
                "name" : "progress-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": progress_fulfilled
            },
            {
                "name" : "homework-percentage",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_score
            },
        ]
    }
    ,
    {
        "paths" : ["res/FP Lab Gr3 Thu 4-5.30 pm grades - 05-26-2022, 04-29 AM.csv"],
        "rename_patterns" : [],
        "rowIDs" : ["Email Address", "First Name", "Last Name"],
        "evaluations" : [
            {
                "name" : "progress-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": progress_fulfilled
            },
            {
                "name" : "homework-percentage",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_score
            },
        ]
    },
    {
        "paths" : ["res/FP Lab Gr4 Fri 10.15-11.45 am grades - 05-26-2022, 04-36 AM.csv"],
        "rename_patterns" : [],
        "rowIDs" : ["Email Address", "First Name", "Last Name"],
        "evaluations" : [
            {
                "name" : "progress-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": progress_fulfilled
            },
            {
                "name" : "homework-percentage",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_score
            },
        ]
    }
]

# ----------------------------------- Processing Area
fpc = FPCG_Engine(configurations)
evaluation_tables = fpc.evaluate()

# Save the results
for i, ev in enumerate(evaluation_tables):
    ev.to_csv("res/configuration_output_" + str(i) + ".csv")