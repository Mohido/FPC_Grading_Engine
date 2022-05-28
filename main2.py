from fpcg_engine import FPCG_Engine
import re
import pandas as pd


# ------------------- Callbacks area

def final_grade(IDs, row_data):
    theory_perc = [x[1] for x in row_data if x[0] == "theory-percentage-15%"]
    prog_perc = [x[1] for x in row_data if x[0] == "programming-exam-contribution-70%"]
    home_perc = [x[1] for x in row_data if x[0] == "homework-percentage-15%"]
    quiz_pass = [x[1] for x in row_data if x[0] == "mini-quiz-precondition-fulfilled"]
    pt_pass = [x[1] for x in row_data if x[0] == "progress-task-precondition-fulfilled"]
    mid_score = [x[1] for x in row_data if x[0] == "midterm-score"]
    end_score = [x[1] for x in row_data if x[0] == "endterm-score"]

    print(theory_perc,prog_perc, home_perc, quiz_pass,  pt_pass)

    # Check if data are null (Havenot attended)
    if(len(mid_score) <= 0 or len(end_score) <= 0 or len(theory_perc) <= 0 or len(prog_perc) <= 0 or len(home_perc) <= 0 or len(quiz_pass) <= 0 or len(pt_pass) <= 0):
        return 

    # Check preconditions
    if(home_perc[0] < 7.5 or mid_score[0] < 50 or end_score[0] < 50 or quiz_pass[0] == False or pt_pass[0] == False):
        return (1, -1)

   # Calculate grade
    final = theory_perc[0] + prog_perc[0] + home_perc[0] 
    if (final > 85 ):
        return (5, final)
    elif(final > 70 ):
        return (4, final)
    elif(final > 60 ):
        return (3, final)
    elif(final >= 50 ):
        return (2, final)
    else:
        return (1, final)


# ------------------------------ Configuration Area
configuration = [
    {
        "paths" : ["res/main_evaluation.csv"],
        "rename_patterns" : [],
        "rowIDs" : ["neptun-code"],
        "evaluations" : [
            {
                "name" : "final-grade",
                "nullfilter": True,
                "columns" : [
                    "theory-percentage-15%", 
                    "programming-exam-contribution-70%",
                    "homework-percentage-15%", 
                    "progress-task-precondition-fulfilled", 
                    "mini-quiz-precondition-fulfilled",
                    "midterm-score",
                    "endterm-score"
                    ],
                "callback" : lambda IDs, data: final_grade(IDs, data)[0] if (final_grade(IDs, data) != None) else None
            },
            {
                "name" : "final-percentage",
                "nullfilter": True,
                "columns" : [
                    "theory-percentage-15%", 
                    "programming-exam-contribution-70%",
                    "homework-percentage-15%", 
                    "progress-task-precondition-fulfilled", 
                    "mini-quiz-precondition-fulfilled",
                    "midterm-score",
                    "endterm-score"
                    ],
                "callback" : lambda IDs, data: final_grade(IDs, data)[1] if (final_grade(IDs, data) != None)  else None
            }
    ]
}]


# ------------------- Process Area
engine = FPCG_Engine(configuration)
table = engine.evaluate()[0]

df = pd.read_csv("res/main_evaluation.csv")
df.set_index("neptun-code", inplace=True, verify_integrity=True)


final_table = pd.concat([ df, table], verify_integrity=True, axis=1)
final_table.to_csv("res/final.csv")



