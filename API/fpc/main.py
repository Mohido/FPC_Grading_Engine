from fpcg_engine import FPCG_Engine
import re
import pandas as pd



# ----------------------------------------  Callbacks AREA
def mini_quiz_fulfilled(rowIDs, row_data):
    mini_quiz_sum =  mini_quiz_score(rowIDs, row_data)
    return mini_quiz_sum >= 20  

def mini_quiz_score(rowIDs, row_data):
    mini_quiz_sum = sum([score[1] for score in row_data])
    return mini_quiz_sum 

def theoritical_score(rowIDs, row_data):
    midterm = [score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]
    midterm = max(midterm) if len(midterm) > 0 else 0

    endterm = [score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]
    endterm = max(endterm) if len(endterm) > 0 else 0

    theory_score = midterm  + endterm
    return theory_score

def programming_score(rowIDs, row_data):
    midterm = [score[1] for score in row_data if re.match(r".*[Mm]id.*", score[0])]
    midterm = max(midterm) if len(midterm) > 0 else 0
    midterm = 100 if midterm > 100 else midterm

    endterm = [score[1]  for score in row_data if re.match(r".*[Ee]nd.*", score[0])]
    endterm = max(endterm) if len(endterm) > 0 else 0
    endterm = 100 if endterm > 100 else endterm    

    programming_score_1 = ((midterm/100)) * 35 # 35% endterm and 35% midterm
    programming_score_2 = ((endterm/100)) * 35 # 35% endterm and 35% midterm
    return programming_score_1 + programming_score_2

def progress_fulfilled(rowIDs, row_data):
    return total_of_pts_points(rowIDs, row_data) >= 400 

def total_of_pts_points(rowIDs, row_data):
    total_sum = 0  
    for pt in row_data:
        total_sum += pt[1]
    return total_sum 


def homework_score(rowIDs, row_data):
    homework_s = homework_sum(rowIDs, row_data)
    return min((homework_s / 800) * 15, 15)


def neptun_code(rowIDs, row_data):
    return "".join(rowIDs).split("@")[0].upper()
    
def homework_sum(rowIDs, row_data):
    hws_points_without_extra = [] 
    extra_points = 0
    for data in row_data:
        if data[0] != "HW additional":
            hws_points_without_extra.append(data[1])
        else:
            extra_points = data[1]
    hws_points_without_extra.sort()
    if(hws_points_without_extra[0] < extra_points  and extra_points <= 100):
        hws_points_without_extra[0] = extra_points
        extra_points = 0 
    elif(hws_points_without_extra[0] < extra_points  and extra_points > 100):  
        hws_points_without_extra[0] = 100 
        extra_points -= 100
    
    if(hws_points_without_extra[1] < extra_points ):
        hws_points_without_extra[1] = extra_points
        extra_points = 0 
    
    return sum([points for points in hws_points_without_extra])

# ------------------------ Configuration Area

configurations = [
     {

        "paths" : [
            "res\FP GR1 Wed 12.00-13.30 PC2 2.107 marks - 14-12-2022, 07-11.csv"
            ,"res\FP GR2 Fri 8.30-10 PC2 2.107 marks - 14-12-2022, 07-11.csv"
            ,"res\FP GR3 Fri 12.00-13.30 PC2 2.107 marks - 14-12-2022, 07-11.csv"
            ,"res\FP GR4 Wed 10.15-11.45 PC2 2.107 marks - 14-12-2022, 07-12.csv"
            ,"res\FP GR5 Thu 4-5.30 PC2 2.107 marks - 14-12-2022, 07-12.csv"
            ,"res\FP GR 6 Thu 12-13.30 PC4 00.524 marks - 14-12-2022, 07-13.csv"
            ,"res\GR7 Fri 10.15-11.45 PC2 2.107 South Build_ marks - 14-12-2022, 07-13.csv"
            ],
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
                "name" : "total progress task points",
                "nullfilter": True,
                "columns" : [re.compile(".*[Pp][Tt].*"), re.compile(".*[Pp]rogres.*"), re.compile(".*[Pp]rogres.*")],
                "callback": total_of_pts_points
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
                "columns" : [re.compile(".*[Hh]W.*"), re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_sum 
            },
            {
                "name" : "homework-percentage-15%",
                "nullfilter": True,
                "columns" : [re.compile(".*[Hh]W.*"), re.compile(".*[Hh]om.*"), re.compile(".*[Ee].xtr.*[Hh]om.*"),re.compile(".*[Hh]om.*[Ee].xtr.*") ,re.compile("^extra_.*")],
                "callback": homework_score
            },
            {
                "name" : "neptun-code",
                "nullfilter": True,
                "columns" : [r".*"],
                "callback": neptun_code 
            }
        ]
    }
    ,
    {
        "paths" : ["res\canvas.csv"],
        "rename_patterns" : [("SIS Login ID", "neptun-code")],
        "rowIDs" : ["Student"],
        "evaluations" : [
            {
                "name" : "mini-quiz-raw-sum",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*") , re.compile("^Extra_[qQ]uiz.*")  ],
                "callback": mini_quiz_score
            },
            {
                "name" : "mini-quiz-precondition-fulfilled",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*") , re.compile("^Extra_[qQ]uiz.*") ],
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
                "callback": lambda IDs, row_data: (theoritical_score(IDs, row_data) / 40) * 15
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

final_table = pd.concat([evaluation_tables[0],evaluation_tables[1]], verify_integrity=True, axis=1)

final_table.to_csv("res/main_evaluation.csv")
