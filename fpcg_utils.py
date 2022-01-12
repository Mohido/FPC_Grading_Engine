import pandas as pd
import re

'''
    Loading the Data as a pandas.DataFrame from teh given csv file. 

    Parameters:
        csvSheet        <-> string:                         ".csv" file path that holds the data.
        colAsId         <-> <Column header>:                The column name that you desire to refer the data by. Note that this is necessary for the purposes of this application. <Neptun codes> can be a good ID for instance.
        usecols         <-> [ints]:                         A list of columns indices that you desire to read. Note that if this is empty, all the columns will be loaded by default.
        renamePatterns  <-> [(re_pattern, string)]:         Used for converting column names that matches the pattern to the given alternative name.

    Returns:
        pandas.DataFrame that holds the desired data with the desired configuration.
'''
def loadDataframe(csvSheet, colAsId = None, usecols = [], renamePatterns = [], colsToDrop = []):    
    
    # --------------- Definitions + Declerations:
    df = pd.DataFrame()

    # Helper Anonymous function for renaming columns
    def maybe_rename(col_name):
        #print(csvSheet)
        for pattern in renamePatterns: 
            #print(pattern, col_name )
            if re.match(pattern[0], col_name):
                return pattern[1]
        return col_name
    
    # -- BEGIN 
    
    # Loading the dataset from the file.
    if( 0 < len(usecols) and len(usecols) < pd.read_csv(csvSheet).shape[1] ): # Simple error checking for the used columns lengths
        df = pd.read_csv(csvSheet, skiprows=[1], usecols=usecols)
    else:
        df = pd.read_csv(csvSheet, skiprows=[1])
        
    # cleaning the dataset.
    for i, col in enumerate(df.columns):

        # all strings to lowercase (Generalisation purposes.)
        if (df.dtypes[i] == 'object'):      
            df[col] = df[col].str.lower()
    
    df = df.fillna(0)                                               # filling messings with 0s
    df = df.rename(columns=maybe_rename, errors="ignore")           # Renaming the columns with the given patterns

    if(colAsId != None):
        df = df.set_index(colAsId)                                      # ID used in .loc[] is now set to the colAsId parameter
    
    return df 
    # -- END loadDataframe();



# ----------------------------------------------------------------------------------------


'''
    A "MS Teams" extension function that encapsulate the additional funcitonality of Loading the Data as a pandas.DataFrame from teh given csv file. 

    Parameters:
        csvSheet        <-> string:                         ".csv" file path that holds the data.
        colAsId         <-> <Column header>:                The column name that you desire to refer the data by. Note that this is necessary for the purposes of this application. <Neptun codes> can be a good ID for instance.
        usecols         <-> [ints]:                         A list of columns indices that you desire to read. Note that if this is empty, all the columns will be loaded by default.
        renamePatterns  <-> [(re_pattern, string)]:         Used for converting column names that matches the pattern to the given alternative name.

    Returns:
        pandas.DataFrame that holds the desired data with the desired configuration.
'''
def loadDataFrame_teams_ext(csvSheet, colAsId, colsToKeep = [], renamePatterns = [], colsToDrop = [], feedback=False):
    df = loadDataframe(csvSheet, None, colsToKeep, renamePatterns, colsToDrop) # Students' practice groups tables
    if(feedback):
        return df
    df = df[df.columns.drop(list(df.filter(regex='Feedback.*')))]
    df[colAsId] = df[colAsId].map(lambda value: str(value).split("@")[0])
    df = df.set_index(colAsId) 
    return df


'''
'''
def searchList(pattern, columns):
    result = []
    for i, element in enumerate(columns):
        if re.match(pattern, element):
            result.append(columns[i])
    return result



def printDetails(dataframe):
    print("--------- Head --------------------")
    print(dataframe.head())
    print("---------------------------------- ")
    print("--------- info --------------------")
    print(dataframe.info())
    print("---------------------------------- ")
    print("--------- describe --------------------")
    print(dataframe.describe())
    print("---------------------------------- ")
    print("--------- Maximums: Strings output are irrelevant. --------------------")
    print(dataframe.max())
    print("---------------------------------- ")


def logMessage(mtype, functionName, message):
    print("[%s]: [%s]: %s"  %(mtype, functionName, message) )
    pass
