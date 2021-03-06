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
        print("Processing the Configurations: ")
        print(self.m_configurations)
        configurations = self.m_configurations if (index == -1) else [self.m_configurations[index]]

        # Run the engine on the configurations
        tables = []
        for ci, configuration in enumerate(configurations):
            table = self._load_configuration_data(configuration)     # Loading the CSV file

            # Process the data
            result_table = self._create_result_table(configuration)  # Creates an empty result table (Only columns names are defined)
            for ei, evaluation in enumerate(configuration["evaluations"]):
                result_table = self._process(table, configuration, evaluation, result_table)     # Returns a list of the evaluation results object
            tables.append(result_table)
        return tables


    '''
        Loads the data of a given configuration into a pandas dataframe. It loads the csv file and returns it.
    '''
    def _load_configuration_data(self, configuration):
        table = pd.DataFrame()
        for pi, path in enumerate(configuration['paths']):
            df = pd.read_csv(path, index_col=False)
            df = self._pre_process_data(df, configuration)     # Renaming columns, and setting RowID
            table = pd.concat([table, df], verify_integrity=True)
        return table


    '''
        Pre-Process the table. It renames the columns, and set the RowIDs
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
        This function creates a template empty table holding the indices and the columns.
    '''
    def _create_result_table(self, configuration):
        cols = configuration["rowIDs"] + [eval["name"] for eval in configuration["evaluations"]]    # Columns of the empty table
        table = pd.DataFrame(columns=cols)                                                          # Empty table template creation
        table.set_index(configuration["rowIDs"], inplace=True, verify_integrity=True)               # Setting the index
        return table
        

    '''
        Process the data according to the given evaluation object and fills the result_table and returns it.
    '''
    def _process(self, table, configuration, evaluation, result_table):
        # Get the columns matching the pattern
        desired_columns = []
        for eval_col in evaluation["columns"]:
            for table_col in table.columns:
                if re.match(eval_col, table_col):
                    desired_columns.append(table_col)
        desired_columns = list(set(desired_columns)) # Removing duplications
        
        # Create a new table with desired columns to process, and the indices
        temp = table.loc[:, desired_columns]                                                        # Extract the desired columns to process
        indices = temp.index.to_frame().dropna().index if evaluation["nullfilter"] else temp.index  # Filter out null indices
        
        # Loop through the rows and extract the desired columns
        for rowID in indices:
            row_data = temp.loc[rowID, :].dropna() if evaluation["nullfilter"] else temp.loc[rowID, :]
            if(len(row_data) == 0):
                continue
            data = [ (row_data.index[x], row_data[x])  for x in range(0, len(row_data))]                 # [(index, [values])]
            result_table.loc[rowID, evaluation["name"]] = evaluation["callback"](list(rowID), data)      # Evaluate and store it in its entry      
        return result_table




