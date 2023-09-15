import datetime
import os

from utils import Log, print_table, attr2str


class Command:
    def __init__(self, args_dict, config):
        self.args = args_dict
        self.file_name = args_dict['file_name']

        self.fields = ['id', 'description'] + config.sub_attrs
        self.tasks = []  # [{'id': , 'description', ...}, ...]
        self.cols_max_len = {field: len(field) for field in self.fields}

        self.log = Log()

        self.config = config

    def do_command(self):
        # read tasks from file
        if self.get_tasks() == 1:
            print("Error file name!")
            return

        # run the operation function
        getattr(self, self.args['op'])()

        # save history file
        if self.args['op'] != 'show':
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S_')
            history_path = './history/' + time_str + self.file_name
            self.write_tasks(history_path)

    def add(self):
        id = len(self.tasks) + 1
        description = ' '.join(self.args['description'])
        task = {'id': str(id), 'description': description}

        # input attributes
        print("Add attributes...")
        for field in self.fields[2:]:
            # check if the input attr in the given choices
            choices = self.config.choices.get(field)
            if choices:
                attr = input('--' + field + ' ' + str(choices) + ' ')
                while attr not in choices:
                    print("Error choice!")
                    attr = input('--' + field + ' ' + str(choices) + ' ')
            else:
                help_str = self.config.helps.get(field, '')
                attr = input('--' + field + ' ' + help_str + ' ')

            task[field] = attr

        # add new task in the file
        self.tasks.append(task)
        with open(self.file_name, 'a') as f:
            task_str = ','.join(task.values())
            f.write(task_str + '\n')

        # log result
        res = 'Task id = ' + str(id) + ' added'
        print(res)
        self.log.add_log(res)

        return id

    def modify(self):
        id = self.args['id']
        i = self.find_task_by_id()
        if i > -1:
            print('find task:', self.tasks[i])

            for field, attr in self.args.items():
                if attr is not None and field != 'id' and field in self.fields:
                    self.tasks[i][field] = attr2str(attr)

            self.write_tasks(self.file_name)

            res = 'Task id = ' + str(id) + ' modified'
        else:
            res = 'Task id = ' + str(id) + ' not found'

        # log result
        print(res)
        self.log.add_log(res)
        return

    def rm(self):
        id = self.args['id']
        i = self.find_task_by_id()
        if i > -1:
            self.tasks.pop(i)

            for task in self.tasks[i:]:
                task['id'] = str(int(task['id']) - 1)

            self.write_tasks(self.file_name)

            res = 'Task id = ' + str(id) + ' removed'
        else:
            res = 'Task id = ' + str(id) + ' not found'

        # log result
        print(res)
        self.log.add_log(res)
        return

    def show(self):
        print_table(self.fields, self.tasks, self.cols_max_len)
        # log result
        self.log.add_log('show')

    def find(self):
        found_tasks = []

        for i, task in enumerate(self.tasks):
            is_found = False
            # check all the fields and attrs
            for field, attr in self.args.items():
                if attr is not None and field in self.fields:
                    if attr2str(attr) in task[field]:
                        is_found = True
                    else:
                        is_found = False
                        break

            if is_found:
                found_tasks.append(task)

        if found_tasks:
            res = 'Tasks found, ' + str(self.args)
            print('Tasks found')
            print_table(self.fields, found_tasks, self.cols_max_len)
        else:
            print('Tasks not found')
            res = 'Tasks not found, ' + str(self.args)

        # log result
        self.log.add_log(res)
        return

    def get_tasks(self):
        """
        read tasks from file
        """
        res = 0

        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                data = f.readlines()
                data = data[1:]  # first line is fields

            for d in data:
                task = {}
                attrs = d.strip('\n').split(',')
                for i, attr in enumerate(attrs):
                    field = self.fields[i]
                    task[field] = attr

                    if len(attr) > self.cols_max_len[field]:
                        self.cols_max_len[field] = len(attr)

                self.tasks.append(task)

            # print('self.tasks:', self.tasks)
            # print('self.cols_max_len:', self.cols_max_len)
        else:
            to_create = input(self.file_name + " can't find, create? (y/n) : ")
            if to_create == "y":
                with open(self.file_name, "w") as f:
                    f.write(','.join(self.fields) + '\n')
                    print(self.file_name, "created")
            else:
                res = 1

        return res

    def write_tasks(self, file_name):
        with open(file_name, 'w') as f:
            f.write(','.join(self.fields) + '\n')

            for task in self.tasks:
                task_str = ','.join(task.values())
                f.write(task_str + '\n')

    def find_task_by_id(self):
        """
        find the index of the task with the given id
        """
        idx = -1
        for i, task in enumerate(self.tasks):
            if str(task['id']) == str(self.args['id']):
                idx = i
                break
        return idx


