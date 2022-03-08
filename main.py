import yaml
from yaml.loader import SafeLoader

from bin import flow, task 


with open('.\DataSet\Examples\Milestone1\Milestone1_Example.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    print(data)
    
    for  key in data:


    main_workFlow = flow.Flow(list(data.keys())[0], data[list(data.keys())[0]]['Execution'])
    # print(main_workFlow.execution)
    sample_task1 = task.Task(list(data[main_workFlow.name].keys())[0], data[list(data[main_workFlow.name].keys())[0]]['Function'], data[list(data[main_workFlow.name].keys())[0]]['Inputs'])
    sample_task2 = task.Task(list(data[main_workFlow.name].keys())[1], data[list(data[main_workFlow.name].keys())[1]]['Function'], data[list(data[main_workFlow.name].keys())[1]]['Inputs'])
    sample_subflow = flow.Flow(list(data[main_workFlow.name].keys())[2], data[list(data[main_workFlow.name].keys())[2]]['Execution'])
    sample_subtask1 = task.Task(list(data[sample_subflow.name].keys())[0], data[list(data[sample_subflow.name].keys())[0]]['Function'], data[list(data[sample_subflow.name].keys())[0]]['Inputs'])
    sample_subtask2 = task.Task(list(data[sample_subflow.name].keys())[1], data[list(data[sample_subflow.name].keys())[1]]['Function'], data[list(data[sample_subflow.name].keys())[1]]['Inputs'])

    
