from fpcg_engine import FPCG_Engine
import re


cSheetsPathsPrs = [ 
    "res/2022-01-10T1609_Grades-2021_22_1_IP-18fFUNPEG_6_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1609_Grades-2021_22_1_IP-18fFUNPEG_7_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1610_Grades-2021_22_1_IP-18fFUNPEG_4_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1610_Grades-2021_22_1_IP-18fFUNPEG_5_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1611_Grades-2021_22_1_IP-18fFUNPEG_1_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1611_Grades-2021_22_1_IP-18fFUNPEG_2_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1611_Grades-2021_22_1_IP-18fFUNPEG_3_-_Functional_programming_L+Pr..csv"
]




renamePatterns = [
    (r"^Mid-term.*", "Mid-term-quiz"),
    (r".*SIS.*", "neptun-code"),
    (r"^Student", "full-name")
]


cSheetPathsLts = [ 
    "res/2022-01-10T1612_Grades-2021_22_1_IP-18fFUNPEG_90_-_Functional_programming_L+Pr..csv",
    "res/2022-01-10T1613_Grades-2021_22_1_IP-18fFUNPEG_91_-_Functional_programming_L+Pr..csv"
]
lectureRenamePatterns = [
    (r"^Mid-term.*", "Mid-term-quiz"),
    (r"^Endterm Quiz.*", "End-term-quiz"),
    (r"^Big_Quiz_Retake.*", "Big_Quiz_Retake"),
    (r".*SIS.*", "neptun-code"),
    (r"^Student", "full-name"),
    (r"^Quiz_Extra.*", "Quiz-extra")
] + [ (re.compile("^Quiz" + str(x)), "Quiz-" + str(x)) for x in range(1,10)]
lectureUseCols = [0,1,2] + [x for x in range(4,17)]

# ________________
conf = {
    "MSTeamsConf" : 
        { 
            "paths" : ["res/FP Practice Gr 5. Wed 8.30-10 a.m. 2-107 marks - 11-01-2022, 13-05.csv"],
            "renamePatterns" : [],
            "usecols" : [],
            "columnAsId" : "Email Address"
        },

    "CanvasLabConf" : {                
        "paths"  :               cSheetsPathsPrs,             
        "renamePatterns":        renamePatterns, 
        "usecols" :              [0,1,2,4],
        "columnAsId":            "ID"     # Both the canvas ones should have this Canvas ID which refer to the students.
    },

    "CanvasLecConf" : {                
        "paths"  :               cSheetPathsLts,             
        "renamePatterns":        lectureRenamePatterns, 
        "usecols" :              lectureUseCols,
        "columnAsId":            "ID"     # This should be in the lab channel as well.
    },
}




engine = FPCG_Engine(conf)
engine.start()
df = engine.getCanvasLecData()

print("______________________________")
print(df.info())
print("______________________________")
print(df.head())
print("______________________________")
print(df.describe())
print("______________________________")
print(df.shape)
print("______________________________")


engine.run()