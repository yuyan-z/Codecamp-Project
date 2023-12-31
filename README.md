# Codecamp-Project
The github link https://github.com/yuyan-z/Codecamp-Project/tree/main
# Libraries used
argparse, datetime, os

# Commands
| Command | Description |  
| --- | --- |
| `task <file_name> add <description>` | Add a task in the task file, given description and other attributes |  
| `task <file_name> modify <id> <--attribute> <value>` | Modify the task with the given id and the given attributes |  
| `task <file_name> rm <id>` | Remove the task with the given id |  
| `task <file_name> show` | Show tasks in tabular form |  
| `task <file_name> find <--attribute> <value>` | Find the task with the given attributes |  
| `task -h` | Get help |

# Functions
## get_args(command: str, config)
Get arguments from the input command string `command`, given the configuration `config`.

Return a `dict` `args_dict` with the format of `{arg_name: arg_value}`

Author: EL BEZ Oumayma, HENI Yahia, LOBATO Felipe, ZHAO Yuyan

## class Command
Read and run the command, given `args_dict` and the configuration `config`

Author: EL BEZ Oumayma, HENI Yahia, LOBATO Felipe, ZHAO Yuyan

### __init__(self, args_dict, config)
Initial the object's attributes, including `self.file_name` the file name to store the tasks data, `self.fields` the fields for the task,      `self.tasks` the list to store the tasks data, `cols_max_len` the maximum length of each column

### do_command(self)
First read tasks data from task file `self.file_name`. If it does not exist then create one.
Next, run the operation function. Finally save a history file

### add(self)
Add a task in the task file `self.file_name`, given description and other attributes

### modify(self)
Modify the task with the given id and the given attributes

### rm(self)
Remove the task with the given id

### show(self)
Show tasks in tabular form

### find(self)
Find the task with the given attributes

## class Log
Manage log file. 

Author: LOBATO Felipe, ZHAO Yuyan

### get_logs(self)
First read the log file from the given log file path, if it does not exist then create one.

### add_log(self, action: str)
Add a new log string at the end of log file after doing a command, with the format of '%Y/%m/%d %H:%M:%S_action'



## class Config
The configuration can be modified in `class Config`, including the attributes of task `self.sub_attrs`, the range of choice `self.choices` and help text for attributes `self.helps`

Author: ZHAO Yuyan


## print_table(heads: list, data: list, cols_max_len: dict)
Display the list `data` in tabular form, given a list of header fields `heads` and the maximum length of each column `cols_max_len`.

Author: ZHAO Yuyan


## attr2str(attr)
Convert the input variable `attr` to string type. The type of `attr` can be `str`, `int`, or `list`.

Author: ZHAO Yuyan

# Example
1. Run main.py  
2. First time add a task in the task file `lestaches.txt` with the description `group meeting 1`
   
   `task lestaches.txt add group meeting 1`
   
   Set values for other parameters according to the help text

![image](https://github.com/yuyan-z/Codecamp-Project/assets/64955334/03b7a39c-c8e2-4db1-9eda-fef34e5ee95f)

2. Similarly, add other tasks. The result is as follows.

![image](https://github.com/yuyan-z/Codecamp-Project/assets/64955334/139387cb-c07a-48bf-9a22-ae79b4bec089)

3. Modify the task with the given id `2` and the given parameters `--state completed --actual_duration 1h`
   
   `task lestaches.txt modify 2 --state completed --actual_duration 1h`  

![image](https://github.com/yuyan-z/Codecamp-Project/assets/64955334/4f4c7be2-45af-4997-b8ee-71267bf33179)

4. Remove the task with the given id `3` (lunch). The id of the following rest tasks is decreased by one automatically
   
   `task lestaches.txt rm 3`

![image](https://github.com/yuyan-z/Codecamp-Project/assets/64955334/d3771a94-09e7-49a3-ba01-1f1540752e83)

5. Find the task with the given parameters `--context classroom --tag dcl`
   
   `task lestaches.txt find --context classroom --tag dcl`

![image](https://github.com/yuyan-z/Codecamp-Project/assets/64955334/98264966-4cf8-41d1-98e6-22d32fe52c40)

6. We can see that, after each operation, a log string is generated in `log.txt`, and a history file is generated in `.\history\`

![image](https://github.com/yuyan-z/Codecamp-Project/assets/64955334/3a4d18a3-6f93-4ed0-b51e-051ecb9ffef5)







