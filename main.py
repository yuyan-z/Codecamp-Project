import os
import argparse

from mylog import Log


class Command:
    def __init__(self, args_dict):
        self.args = args_dict
        self.file_name = args_dict['file_name']

        self.fields = ['id', 'description'] + sub_attrs
        self.tasks = []  # [{'id': , 'description', ...}, ...]
        self.cols_max_len = {field: len(field) for field in self.fields}

        self.log = Log()

    def do_command(self):
        if self.get_tasks() == 1:
            print("File name error!")
            return

        getattr(self, self.args['op'])()

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

    def add(self):
        id = len(self.tasks) + 1
        description = ' '.join(self.args['description'])
        task = {'id': str(id), 'description': description}

        # Input sub-attributes
        for field in self.fields[2:]:
            attr = input(field + ': ')
            task[field] = attr

        self.tasks.append(task)

        with open(self.file_name, 'a') as f:
            task_str = ','.join(task.values())
            f.write(task_str + '\n')

        print('Task id =', id, 'added')
        self.log.add_log('Task id = ' + str(id) + ' added')

        return id

    def find_task(self):
        res = -1
        for i, task in enumerate(self.tasks):
            if str(task['id']) == str(self.args['id']):
                res = i
                break
        return res

    def modify(self):
        id = self.args['id']
        i = self.find_task()
        if i > -1:
            print(self.tasks[i])

            for field, attr in self.args.items():
                if attr is not None and field != 'id' and field in self.fields:
                    self.tasks[i][field] = ' '.join(attr)

            with open(self.file_name, 'w') as f:
                f.write(','.join(self.fields) + '\n')

                for task in self.tasks:
                    task_str = ','.join(task.values())
                    f.write(task_str + '\n')

            print('Task id =', id, 'modified')
            self.log.add_log('Task id = ' + str(id) + ' modified')
        else:
            print('Task id =', id, " can't be found")
            self.log.add_log('Task id = ' + id + " can't be found")

    def rm(self):
        id = self.args['id']
        i = self.find_task()
        if i > -1:
            self.tasks.pop(i)

            for task in self.tasks[i:]:
                task['id'] = str(int(task['id']) - 1)

            with open(self.file_name, "w") as f:
                f.write(','.join(self.fields) + '\n')

                for task in self.tasks:
                    task_str = ','.join(task.values())
                    f.write(task_str + '\n')

            print('Task id =', id, 'removed')
            self.log.add_log('Task id = ' + str(id) + ' removed')

        else:
            print('Task id =', id, " can't be found")
            self.log.add_log('Task id = ' + str(id) + " can't be found")

    def show(self):
        print_table(self.fields, self.tasks, self.cols_max_len)
        self.log.add_log('show')


def print_table(heads: list, data: list, cols_max_len: dict):
    border_str = '+'
    for head in heads:
        border_str = border_str + '-'.center(cols_max_len[head] + 2, '-') + '+'
    print(border_str)

    field_str = '|'
    for head in heads:
        field_str = field_str + head.center(cols_max_len[head] + 2, ' ') + '|'
    print(field_str)
    print(border_str)

    for item in data:
        item_str = '|'
        for i, head in enumerate(heads):
            item_str = item_str + item[head].center(cols_max_len[head] + 2, ' ') + '|'

        print(item_str)

    print(border_str)


if __name__ == '__main__':
    sub_attrs = [
        'project',
        'state',
        'priority',
        'context',
        'tag',
        'user',
        'estimated_duration',
        'actual_duration'
    ]

    # command_str = 'task lestaches.txt modify 2 --description task 2 modified --project codecamp 4'
    # command_str = 'task lestaches.txt show'
    command_str = 'task lestaches.txt add task 1'
    # command_str = 'task lestaches.txt rm 2'

    parser = argparse.ArgumentParser(prog='task', description="Input a command to manage task")
    parser.add_argument("task", choices=['task'], help="Task")
    parser.add_argument("file_name", type=str, help="File name")

    subparsers = parser.add_subparsers(dest='op', title='Operations')

    # add description
    parser_add = subparsers.add_parser('add', help='Add a task')
    parser_add.add_argument('description', nargs='+', help='Description of the task')

    # modify id
    parser_modify = subparsers.add_parser('modify', help='Modify a task by id')
    parser_modify.add_argument('id', type=int, help='Task id')
    parser_modify.add_argument('--description', nargs='+')
    for sub_attr in sub_attrs:
        parser_modify.add_argument('--' + sub_attr, nargs="+")

    # rm id
    parser_rm = subparsers.add_parser('rm', help='Remove a task by id')
    parser_rm.add_argument('id', type=int, help='Task id')

    # show
    parser_show = subparsers.add_parser('show', help='Show tasks')

    args = parser.parse_args(command_str.split())

    command = Command(vars(args))
    command.do_command()

    # while True:
    #     command_str = input("Input a command, q for quit: ")
    #     if command_str == "q":
    #         break
    #     else:
    #         parser = argparse.ArgumentParser(prog='task', description="Input a command")
    #         parser.add_argument("task", type=str, help="Task")
    #         parser.add_argument("file_name", type=str, help="File name")
    #         parser.add_argument("op", choices=["add", "modify", "rm", "show"], help="Operation for the task")
    #         parser.add_argument("params", nargs="*", help="Other parameters for the operation")
    #
    #         args = parser.parse_args(command_str.split())
    #         print(args)
    #
    #         command = Command(args)
    #         command.do_command()





