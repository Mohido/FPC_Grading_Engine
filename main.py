from fpcg_engine import FPCG_Engine
import re

# Canvas Practice channel configuration.
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


# Canvas Lecture channel configuration.
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


# Teams Configuration.

# Canvas Lecture channel configuration.
teamsSheetPaths = [ 
    "res/FP Practice Gr 1. Monday 6.15-7.45 p.m. 00-524 marks - 12-01-2022, 20-33.csv",
    "res/FP Practice Gr 2. Friday 12.15-1.45 p.m. 2-107 marks - 12-01-2022, 20-34.csv",
    "res/FP Practice Gr 3. Friday 2-3.30 p.m. 00-524 marks - 12-01-2022, 20-34.csv",
    "res/FP Practice Gr 4. Friday 3.45-5.15 p.m. 00-524 marks - 12-01-2022, 20-34.csv",
    "res/FP Practice Gr 5. Wed 8.30-10 a.m. 2-107 marks - 12-01-2022, 20-35.csv",
    "res/FP Practice Gr 6. Thursday 6-7.30 p.m. 00-524 marks - 12-01-2022, 20-35.csv",
    "res/FP Practice Gr 7. Wed 12-1.30 p.m. 2-107 marks - 12-01-2022, 20-35.csv",
]
teamsRenamePatterns = [
    (re.compile(".*mid.*term.*retake", re.IGNORECASE),          "Mid-term-retake"),
    (re.compile(".*mid.*term.*online", re.IGNORECASE),          "Mid-term-online"),
    (re.compile(".*mid.*term.*", re.IGNORECASE),                "Mid-term"),
    (re.compile(".*end.*term.*retake", re.IGNORECASE),          "End-term-retake"),
    (re.compile(".*end.*term.*online", re.IGNORECASE),          "End-term-online"),
    (re.compile(".*end.*term.*", re.IGNORECASE),                "End-term"),
    (re.compile(".*red.*dots$", re.IGNORECASE),                 "Red-dots-0"),
    (re.compile("^additional hw 1", re.IGNORECASE),             "Homework-extra-1"),
    (re.compile("^extra2", re.IGNORECASE),                      "Homework-extra-2"),
    (re.compile("^home.*work.*11", re.IGNORECASE),                "Homework-extra-1"),
    (re.compile("^home.*work.*12", re.IGNORECASE),                "Homework-extra-2"),
    (re.compile("^extra.*progress.*task.*", re.IGNORECASE),     "Progress-task-extra-1"),
    (re.compile("^exrtra.*progress.*task.*", re.IGNORECASE),    "Progress-task-extra-1"),
    (re.compile(".*progress.*task.*extra.*", re.IGNORECASE),    "Progress-task-extra-1"),
    (re.compile("Extra homework 2", re.IGNORECASE),             "Homework-extra-2"),
    (re.compile("Extra homework", re.IGNORECASE),               "Homework-extra-1"),
    (re.compile("^Progress Task $", re.IGNORECASE),             "Progress-task-1")
    ] + [
        (re.compile(".*[rR]ed.*[dD]ots.*" + str(x) +"[a-z ]*$", re.IGNORECASE), "Red-dots-" + str(x)) for x in range(0,5)
    ] + [
        (re.compile("^progress.*" + str(x) +"[a-z ]*$", re.IGNORECASE), "Progress-task-" + str(x)) for x in range(1,11)
    ] + [ 
        (re.compile("home.*work.*" + str(x) +"[a-z ]*$", re.IGNORECASE), "Homework-" + str(x)) for x in range(1,11)
    ]
teamsUseCols = []


# ________________


conf = {
    "MSTeamsConf" : 
        { 
            "paths" : teamsSheetPaths,
            "renamePatterns" : teamsRenamePatterns,
            "usecols" : teamsUseCols,
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
df = engine.getTeamsData(0)




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