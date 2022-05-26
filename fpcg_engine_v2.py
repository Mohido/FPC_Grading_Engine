import pandas as pd
import numpy as np
import re
import math


class FPCG_Engine(object):

    def __init__(self, configurations):
        self.m_configurations = configurations

    '''
        Loads the excel sheets, pre-process them, apply the evaluation and returns the results of the evaluation.
    '''
    def evaluate(self, index = -1):
        # What to evaluate?        
        print(self.m_configurations)
        configurations = self.m_configurations if (index == -1) else [self.m_configurations[index]]

        print("Processing the Configurations: ")
        # Run the engine on the configurations
        for ci, configuration in enumerate(configurations):
            table = self._load_configuration_data(configuration)     # Loading the CSV file
            table = self._pre_process_data(table, configuration)     # Renaming, Setting RowID
            print(table.info())
            print(table.head(5))
            # Process the data
            result_table = self._create_result_table(configuration)  # Creates an empty result table (Only id column is defined)
            print("--------------------------")
            print(result_table.info())
            print(result_table.head(5))
            print("--------------------------")

            for ei, evaluation in enumerate(configuration.evaluations):
                evaluation_results = _process(table, configuration, ei)     # Returns a list of the evaluation results object
                

                # TODO: Add the evaluation result to the table as a column



    '''
        Loads the data in a given configuration into a pandas dataframe.
    '''
    def _load_configuration_data(self, configuration):
        table = pd.DataFrame()
        for pi, path in enumerate(configuration['paths']):
            df = pd.read_csv(path, index_col=False)
            table = pd.concat([table, df], copy=False)
        return table


    '''
        Pre-Process the table. It renames the columns, set the RowIDs
    '''
    def _pre_process_data(self, table, configuration):
        # Renaming Table columns
        def maybe_rename(col_name):
            for pattern in configuration["rename_patterns"]: 
                if re.match(pattern[0], col_name):
                    return pattern[1]
            return col_name
        table.rename(columns=maybe_rename, errors="ignore", inplace=True, copy=False)
        table.set_index( configuration["rowIDs"], inplace=True, verify_integrity=True)
        return table


    '''
        Creates an empty table suitable for the configuration. 
        This function creates a template empty table holding the indices and empty evaluation results.
    '''
    def _create_result_table(self, configuration):
        cols = configuration["rowIDs"] + [eval["name"] for eval in configuration["evaluations"]]    # Columns of the empty table
        table = pd.DataFrame(columns=cols)                                                          # Empty table template creation
        table.set_index(configuration["rowIDs"], inplace=True, verify_integrity=True)               # Setting the index
        return table
        