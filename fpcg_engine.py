# import pandas as pd
# import re 
from fpcg_utils import loadDataframe
from fpcg_utils import loadDataFrame_teams_ext



'''
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


    CanvasLectureConf <-> {                #  the teams sheets configurations
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
        self.teams_df = self._load_teams_data()
        self.cvLab_df = self._load_canvas_lab_data()


    def getTeamsData(self):
        return self.teams_df

    def getCanvasLabData(self):
        return self.cvLab_df

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

