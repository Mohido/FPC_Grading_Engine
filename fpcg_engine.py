# import pandas as pd
# import re 
from fpcg_utils import loadDataframe
from fpcg_utils import loadDataFrame_teams_ext



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
        self.m_teams_df = self._load_teams_data()
        self.m_cvLab_df = self._load_canvas_lab_data()
        self.m_cvLec_df = self._load_canvas_lab_data()

    # -- Getters
    def getTeamsData(self):
        return self.m_teams_df
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
            "Neptun Code",
            "Fullname", 
            "Theory Percentage", 
            "Quizes Percentage", 
            "Midterm Exam Percentage",
            "Endterm Exam Percentage",
            "Progress Tasks Percentage",
            "Homeworks Percentage",
            "Final Grade"
        ]

        self.m_studentsResults = pd.DataFrame(columns = studentColumns)

        
        # 1) get the Students Theory result.

        # 2) get the Student mini quizes grade. Red-dots can compensate on that.

        # 3) get the Students Midterm exam results

        # 4) get the Students Endterm exam results

        # 5) get the Students Progress Tasks (Check if red-dots is replacable)

        # 6) get the Students HWs (Check if red-dots can replace the zero ones as well.)



    # --- Private: 
    def _load_teams_data(self):
        t_conf = self.m_configuration["MSTeamsConf"]
        tsps = t_conf["paths"]                               # <-> [string]:      Teams Sheet Paths

        # Loading the data of the teams dataframe and returns it.
        teams_df = loadDataFrame_teams_ext(
            tsps[0],
            t_conf["columnAsId"], 
            t_conf["usecols"],
            t_conf["renamePatterns"]
        )
        for path in tsps[1:]:
            teams_df = teams_df.append(
                loadDataFrame_teams_ext(
                    path,
                    t_conf["columnAsId"], 
                    t_conf["usecols"],
                    t_conf["renamePatterns"]
                )   
            )

        return teams_df




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

