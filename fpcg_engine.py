# import pandas as pd
# import re 
#from fpcg_utils import loadDataframe
#from fpcg_utils import loadDataFrame_teams_ext
from fpcg_utils import *
import pandas as pd
import numpy as np

'''

Configuration struct....


FPCG_config  : {

    MSTeamsConf <-> {              #  the teams sheets configurations.
        paths <-> [string],                        # desired file paths
        renamePatterns <-> [(regex, string)],      # column renaming patterns
        usecols <-> [Int],                         # columns that you want to use in the files. Leave it empty to make the engine handles it internally.
        columnAsId <-> <column name>               # column to be used as an ID to refer to the students. Should be a column that have similar details in both Teams and Canvas sheets.

    },

    CanvasLabConf <-> {                #  the teams sheets configurations
        paths  <-> [string],                       # desired file paths
        renamePatterns <-> [(regex, string)],      # column renaming patterns
        usecols <-> [Int],                         # columns that you want to use in the files. Leave it empty to make the engine handles it internally.
        columnAsId <-> <column name>               # column to be used as an ID to refer to the students. Should be a column that have similar details in both Teams and Canvas sheets.
    },


    CanvasLecConf <-> {                #  the teams sheets configurations
        paths  <-> [string],                       # desired file paths
        renamePatterns <-> [(regex, string)],      # column renaming patterns
        usecols <-> [Int],                         # columns that you want to use in the files. Leave it empty to make the engine handles it internally.
        columnAsId <-> <column name>               # column to be used as an ID to refer to the students. Should be a column that have similar details in both Teams and Canvas sheets.
    }
}

'''



class FPCG_Engine(object):

    # -- Constructor: 
    def __init__(self, FPCG_config):
        self.m_configuration = FPCG_config

    # -- Public: 
    def start(self):
        self.m_teams_dfs = self._load_teams_data()
        self.m_cvLab_df = self._load_canvas_lab_data()
        self.m_cvLec_df = self._load_canvas_lab_data()

    # -- Getters
    def getTeamsData(self, index):
        return self.m_teams_dfs[index]
    def getCanvasLabData(self):
        return self.m_cvLab_df
    def getCanvasLecData(self):
        return self.m_cvLec_df



    '''
        Creates self.students Dataframe by calculating the grades in the teams/canvas tables.

        Canvas tables have the Midterm/Endterm theory Quizes + the Mini quizes.
        Teams tables have the PTS, HWs, Midterm/Endterm practical exam, and extra red-dots assignment.
    '''
    def run(self):
        studentColumns = [
            ("Neptun Code", self._fill_neptun_column),
            ("Fullname", self._fill_name_column), 
            ("Theory Percentage", self._fill_theory_column),
            ("Passed Quizes Percentage", self._fill_quizes_column), 
            ("Midterm Exam Percentage", self._fill_practice_exams_columns),
            ("Endterm Exam Percentage", None), # loaded withen the midterm percentage initializer.
            ("Progress Tasks Percentage", None),
            ("Homeworks Percentage", None),
            ("Final Grade", None)
        ]

        columnsNames = [ col[0] for col in studentColumns]
        self.m_studentsResults = pd.DataFrame(columns = columnsNames)

        for column, initializer in studentColumns:
            if initializer != None:
                initializer()

        printDetails(self.m_studentsResults)



    '''
    '''
    def _fill_neptun_column(self):
        print("------------------ FILLING Student Neptun Column")
        # Initializing the neptun code columns and fullname columns
        neptunColumnName = searchList(re.compile("[Nn]eptun.*"), list(self.m_cvLec_df.columns))[0]
        self.m_studentsResults["Neptun Code"] = self.m_cvLec_df[neptunColumnName]
        print("---------------------------------- Done  ")


    '''
    '''
    def _fill_name_column(self):
        print("------------------ FILLING Student Name Column")
        fullnameColumnName = searchList(re.compile("[Ff]ull.*[Nn]ame.*"), list(self.m_cvLec_df.columns))[0]
        self.m_studentsResults["Fullname"] = self.m_cvLec_df[fullnameColumnName]
        print("---------------------------------- Done  ")



    '''
        Fill the theory column of the students. Note that the canvas ID of the Lab and Lecture is the one used here as a primery key that conencts all the tables.
    '''
    def _fill_theory_column(self):
        # Get the data columns names of the lecture canvas sheets.
        bigQuizColumnName = searchList(re.compile("^[Bb]ig.*[Qq]uiz.*"), list(self.m_cvLec_df.columns))[0]
        endtermQuizColumnName = searchList(re.compile("^[Ee]nd.*[Qq]uiz.*"), list(self.m_cvLec_df.columns))[0]
        l_midtermQuizColumnName = searchList(re.compile("^[Mm]id.*[Qq]uiz.*"), list(self.m_cvLec_df.columns))[0] # This is the lecture sheet sheet column name

        # Get the data columns names of the practice canvas sheets
        p_midtermQuizColumnName = searchList(re.compile("^[Mm]id.*[Qq]uiz.*"), list(self.m_cvLab_df.columns))[0] # this is the practice lab sheet name

        # The column that we desire to fill in the students table.
        stdTheoryColumnName = searchList(re.compile(".*[Tt]heory.*"), list(self.m_studentsResults.columns))[0]

        # Filling the students theory data
        for stdInd, studentRow in self.m_studentsResults.iterrows():
            labRow = self.m_cvLab_df.loc[stdInd]
            lecRow = self.m_cvLec_df.loc[stdInd]
            
            # highest since students who attended online did not attend the offline of the midterm. Therefore, highest is the simplest way to get the result
            midtermTheoryResult = max(labRow[p_midtermQuizColumnName], lecRow[l_midtermQuizColumnName])
            endtermTheoryResult = lecRow[endtermQuizColumnName]
            bigquizTheoryResult = lecRow[bigQuizColumnName]

            self.m_studentsResults.loc[stdInd][stdTheoryColumnName] = max(bigquizTheoryResult, (midtermTheoryResult + endtermTheoryResult) )



    '''
    '''
    def _fill_quizes_column(self):
        # Getting the column names of the quizes data.
        miniQuizColumns = searchList(re.compile("^[Qq]uiz.*"), list(self.m_cvLec_df.columns))
        stdQuizesColumnName = searchList(re.compile(".*[Qq]uizes.*"), list(self.m_studentsResults.columns))[0]

        # the extra quiz index. It is a replacable quiz.
        extraQuizIndex = len(miniQuizColumns) - 1
        extraQuizScore = 10
        extraQuizColumnName = miniQuizColumns[extraQuizIndex]

        # quizes main columns. 
        mainQuizesColumns = miniQuizColumns[0:extraQuizIndex] + miniQuizColumns[extraQuizIndex + 1:]
        miniQuizScore = 5

        # Filling the students quizes data
        for stdInd, studentRow in self.m_studentsResults.iterrows():
            lecRow = self.m_cvLec_df.loc[stdInd]
            currentExtraScore = lecRow[extraQuizColumnName]    

            studentScores = list(lecRow[mainQuizesColumns])

            # Distributing last column (quiz9,10 into seperate entries.)
            quiz9 = min(studentScores[-1], miniQuizScore)
            quiz10 = studentScores[-1] - quiz9
            studentScores = studentScores[0:len(studentScores)-1] + [quiz9] + [quiz10]

            # substitute minimums with the extra quiz score:
            logMessage("INFO", "_fill_quizes_column", "Starting filling missing quizes.")
            logMessage("INFO", "_fill_quizes_column", "Final Scores Data: Canvas ID: " + str(stdInd) + ", Student Quizes Score: " + str(studentScores) +",  Leftover Extra Quiz Score " + str(currentExtraScore))
            minInd = np.argmin(studentScores)
            while( currentExtraScore > 0 and studentScores[minInd] < currentExtraScore):
                scoreToTransfer = min(currentExtraScore, miniQuizScore)
                currentExtraScore -= scoreToTransfer
                studentScores[minInd] = scoreToTransfer
                minInd = np.argmin(studentScores)
            logMessage("INFO", "_fill_quizes_column", "Final Scores Data: Canvas ID: " + str(stdInd) + ", Student Quizes Score: " + str(studentScores) +",  Leftover Extra Quiz Score " + str(currentExtraScore))
            logMessage("INFO", "_fill_quizes_column", "Done filling missing quizes.")
            logMessage("INFO", "_fill_quizes_column", "Starting calculating the Quiz score.")
            # calculating the sum of the quizes. in percentage.
            minimumPassingScorePerQuiz = 3
            passed_quizes = [ s for s in studentScores if s >= minimumPassingScorePerQuiz]
            
            self.m_studentsResults.loc[stdInd][stdQuizesColumnName] = (len(passed_quizes) / len(studentScores)) * 100
            logMessage("INFO", "_fill_quizes_column", "Done calculating the Quiz score.")
            logMessage("INFO", "_fill_quizes_column", "Conclusion: Student Passed Quizes Percentage: "+ str(self.m_studentsResults.loc[stdInd][stdQuizesColumnName]))
            # self.m_studentsResults.loc[stdInd][stdQuizesColumnName] = (sum(studentScores) / (len(studentScores) * miniQuizScore)) * 100



    ''''''
    def _fill_practice_exams_columns(self):
        # Get the table in which the student midterm, endterm grade are stored.
        def _get_teams_index(neptun_code):
            for index, df in enumerate(self.m_teams_dfs):
                
                if(neptun_code in df.index):
                    return (index, df)
            return (None, None)
                
        # Filling the students quizes data
        neptun_code_col = searchList(re.compile(".*[Nn]eptun.*"), list(self.m_studentsResults.columns))[0]
        stdMidtermColumn = searchList(re.compile(".*[Mm]id.*term.*"), list(self.m_studentsResults.columns))[0]
        stdEndtermColumn = searchList(re.compile(".*[Ee]nd.*term.*"), list(self.m_studentsResults.columns))[0]

        for stdInd, studentRow in self.m_studentsResults.iterrows():
            neptun_code = studentRow[neptun_code_col]
            logMessage("INFO", "_fill_practice_exams_columns", f"Processing Student: {neptun_code}...")
            (i, df) = _get_teams_index(neptun_code)
            
            if( i == None):
                logMessage("WARNGING", "_fill_practice_exams_columns", f"Student: {neptun_code} has no MS teams data.")
            #     raise Exception(f'No student with id: {neptun_code} is NOT found in the MS teams files...')
                continue
            logMessage("INFO", "_fill_practice_exams_columns", f"Found Student Teams Dataframe: {neptun_code} Belongs to dataframe: {i}")
            
            midterm_columns = searchList(re.compile("^[Mm]id.*term.*"), list(df.columns))
            midterm_scores = list(df.loc[neptun_code][midterm_columns])
            bestMidterm = np.max(midterm_scores)
            self.m_studentsResults.loc[stdInd][stdMidtermColumn] = bestMidterm

            logMessage("INFO", "_fill_practice_exams_columns", f"Midterm columns are: {midterm_columns}")
            logMessage("INFO", "_fill_practice_exams_columns", f"{neptun_code} midterm scores are: {midterm_scores}. Best Score: {bestMidterm}")

            endterm_columns = searchList(re.compile("^[Ee]nd.*term.*"), list(df.columns))
            endterm_scores = list(df.loc[neptun_code][endterm_columns])
            bestEndterm = np.max(endterm_scores)
            self.m_studentsResults.loc[stdInd][stdEndtermColumn] = bestEndterm

            logMessage("INFO", "_fill_practice_exams_columns", f"Endterm columns are: {endterm_columns}")
            logMessage("INFO", "_fill_practice_exams_columns", f"{neptun_code} endterm scores are: {endterm_scores}. Best Score: {bestEndterm}")
            logMessage("INFO", "_fill_practice_exams_columns", f"Done processing: {neptun_code}")
            


            
                

            
    


    # --- Private: 
    def _load_teams_data(self):
        t_conf = self.m_configuration["MSTeamsConf"]
        tsps = t_conf["paths"]                               # <-> [string]:      Teams Sheet Paths
        teams_dfs = []

        # Loading the data of the teams dataframe and returns it.
        teams_dfs = [loadDataFrame_teams_ext(
            tsps[0],
            t_conf["columnAsId"], 
            t_conf["usecols"],
            t_conf["renamePatterns"]
        )]
        for path in tsps[1:]:
            teams_dfs = teams_dfs.append(
                loadDataFrame_teams_ext(
                    path,
                    t_conf["columnAsId"], 
                    t_conf["usecols"],
                    t_conf["renamePatterns"]
                )
            )

        return teams_dfs




    def _load_canvas_lab_data(self):
        t_conf = self.m_configuration["CanvasLabConf"]
        tsps = t_conf["paths"]                               # <-> [string]:      Teams Sheet Paths

        # Loading the data of the teams dataframe and returns it.
        df = loadDataframe(
            tsps[0],
            t_conf["columnAsId"], 
            t_conf["usecols"],
            t_conf["renamePatterns"]
        )
        for path in tsps[1:]:
            df = df.append(
                loadDataframe(
                    path,
                    t_conf["columnAsId"], 
                    t_conf["usecols"],
                    t_conf["renamePatterns"]
                )   
            )

        return df



    def _load_canvas_lab_data(self):
        t_conf = self.m_configuration["CanvasLecConf"]
        tsps = t_conf["paths"]                               # <-> [string]:      Teams Sheet Paths

        # Loading the data of the teams dataframe and returns it.
        df = loadDataframe(
            tsps[0],
            t_conf["columnAsId"], 
            t_conf["usecols"],
            t_conf["renamePatterns"]
        )
        for path in tsps[1:]:
            df = df.append(
                loadDataframe(
                    path,
                    t_conf["columnAsId"], 
                    t_conf["usecols"],
                    t_conf["renamePatterns"]
                )   
            )

        return df

