# FPC_Grading_Engine
An engine providing a simple framework to process `.csv` file/s. Since the justification for the engine creation is to help the demonstrators of the "Functional Programming Course" in grading the students' files, it was named "FPC Grading Engine".

---

## How to Use?
1) Create a list of configurations. Each configuration is a processing unit for a certain .csv file/s. The options of the configuration object are explained below.
E.G:

```
configurations = [
    {
        "paths" : ["file1.csv", "file2.csv"...],
        "rename_patterns" : [(r"regex1", "new_column_name"), ...],
        "rowIDs" : ["neptun-code", ...],
        "evaluations" : [
            {
                "name" : "column name of the evaluation",
                "nullfilter": True,
                "columns" : [r"column_name_regex1", ...],
                "callback" : lambda IDs, row: ...
            }
        ]
    }
]
```
2) Create an engine instance and pass the list of configuration to it.
E.G:
```
from fpcg_engine import FPCG_Engine

engine = FPC_Engine(configurations)
```
3) Call the evaluate method to start processing the data. The method outputs a new table with the columns named after the evaluations names. 
E.G:
```
# Evaluates all configurations and output tables respectively
tables = engine.evaluate() 
```
Note: If multiple configurations are given and only one need to be processed, you can pass the desired configuration to be evaluated in the evaluate method as an argument.
E.G:
```
tables = engine.evaluate(0) 
```
4) The `evaluate()` method returns a list of *pandas DataDrames*. To save the evaluated data into a .csv file, you can call the `.to_csv()` method provided inside the pandas dataframe objects.


---
## Configuration Explanation
Configuration contain multiple variables which define the behavior of the engine. Hereafter, these variables are explained:

* **paths** : The .csv file/s relative path which contain the data. Multiple paths can be given. The engine appends the rows of the file with respect to the *rowIDs*. 
* **rowIDs** : The column name/s which contain unique data so it can be used as an ID. Note, multiple IDs can be used, yet it is not recommended.
* **rename_patterns** : Comprises renaming tuples. First entry of each tuple is a regular expression, while the second one is a string. Providing this entry orders the engine to rename the given columns when the files are first loaded. Note that, the *renaming patterns* are applied before the *rowIDs* are processed.
* **evaluations** : Contains a list of evaluation objects. Each evaluation is a column in the output table of the engine for that specific configuration. For instance, if the configuration above is fed to the engine, the output table of the processed configuration will only contain the columns in the *rowIDs* and the *evaluation names* (in our previous configuration, the only provided evaluation name was: `"column name of the evaluation"`).

* **evaluation . name** : The name of the output column of this evaluation.

* **evaluation . nullfilter**: If null values should be passed to the evaluation function.
* **evaluation . columns** : A list of regular expressions defining the columns that their values are required for the process of this evaluation.
* **evaluation . callback** : A callback function in which the rowIDs and the data of the specified columns are passed to. The output of the function defines the value of the evaluation. This function is called for each row of the configuration. Function template : `def funcname(IDs, data)`. The IDs are values of the ID columns, while the data contain the values of the **evaluation . columns**. 



