import argparse
import datetime
import os


class Log:
    def __init__(self):
        self.logs = []
        self.log_file = 'log.txt'
        self.fields = ['time', 'action']

        self.get_logs()

    def get_logs(self):
        """
        read logs from file
        """
        # if log_file doesn't exist create, else read
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.logs = f.readlines()
        else:
            with open(self.log_file, "w") as f:
                f.write(','.join(self.fields) + '\n')

    def add_log(self, action: str):
        time_str = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        log_str = time_str + ',' + str(action)
        self.logs.append(log_str)

        with open(self.log_file, 'a') as f:
            f.write(log_str + '\n')


def get_args(command: str, config):
    parser = argparse.ArgumentParser(prog='task', description="Input a command to manage task")
    parser.add_argument("task", choices=['task'], help="Task")
    parser.add_argument("file_name", type=str, help="File name")

    subparsers = parser.add_subparsers(dest='op', title='Operations')

    # add description
    parser_add = subparsers.add_parser('add', help='Add a task')
    parser_add.add_argument('description', nargs='+', help='Description of the task')

    # modify id --description ...
    parser_modify = subparsers.add_parser('modify', help='Modify a task by id')
    parser_modify.add_argument('id', type=int, help='Task id')
    parser_modify.add_argument('--description', nargs='+')
    for sub_attr in config.sub_attrs:
        # load choices config
        choices = config.choices.get(sub_attr)
        if choices:
            parser_modify.add_argument('--' + sub_attr, choices=choices)
        else:
            parser_modify.add_argument('--' + sub_attr, nargs="+")

    # rm id
    parser_rm = subparsers.add_parser('rm', help='Remove a task by id')
    parser_rm.add_argument('id', type=int, help='Task id')

    # show
    parser_show = subparsers.add_parser('show', help='Show tasks')

    # find --id --description ...
    parser_find = subparsers.add_parser('find', help='Find a task by the given attributes')
    parser_find.add_argument('--id', type=int, help='Task id')
    parser_find.add_argument('--description', nargs='+')
    for sub_attr in config.sub_attrs:
        parser_find.add_argument('--' + sub_attr, nargs="+")

    args = parser.parse_args(command.split())
    return vars(args)


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


def attr2str(attr):
    if isinstance(attr, str):
        attr_str = attr
    else:
        attr_str = ' '.join(attr)

    return attr_str

