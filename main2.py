from fpcg_engine_v2 import FPCG_Engine
import re



def callback_1(rowIDs, row_data):
    print(rowIDs[0], row_data)
    return 1

configurations = [
    {
        "paths" : ["res/2022-05-24T0507_Grades-2021_22_2_IP-18fFUNPEG_90_-_Functional_programming_L+Pr..csv"],
        "rename_patterns" : [("SIS Login ID", "neptun-code")],
        "rowIDs" : ["neptun-code", "Student"],
        "evaluations" : [
            {
                "name" : "quiz-score",
                "nullfilter": True,
                "columns" : [re.compile("^[qQ]uiz.*")],
                "callback": callback_1
            }
        ]
    }
]


fpc = FPCG_Engine(configurations)
evaluation_tables = fpc.evaluate()


