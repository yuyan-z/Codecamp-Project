import datetime
from prettytable import PrettyTable, from_csv
import argparse
import os

class Todo:
    def __init__(self):
        self.last_row = 0 #Iniciate index with zero

        self.field_names = ["id", "task"]
        self.sub_attrs = ["project", "state", "priority", "context", "tag", "creator"]

        self.field_names = self.field_names + self.sub_attrs

        self.read_existing_data()
        self.iniciate_parser()

        self.l = Log()

        if self.args:

            if self.args.add:
                
                self.adding_all_attrs()

                #Saves immediately
                self.save_file(self.mytable)
                print(self.mytable)

                self.l.add_log(f'added task {self.args.add}')

            elif self.args.clear:
                self.mytable.clear_rows()
                self.save_file(self.mytable)
                print(self.mytable)

                self.l.add_log(f'table cleared')


            elif self.args.show:
                print(self.mytable)

                self.l.add_log(f'table showed')

            elif self.args.delete:
                index = self.find_index_from_id(self.args.delete)

                if index is not None:
                    self.mytable.del_row(index)
                    self.save_file(self.mytable)
                    print(self.mytable)

                    self.l.add_log(f'task with id {self.args.delete} deleted')

                else:
                    print('id does not exist')

            elif self.args.modify:
                self.modify_row(self.args.modify)

            if self.args.log:
                self.l.show()
    
    def iniciate_parser(self):
        parser = argparse.ArgumentParser(prog='task', usage='%(prog)s [options]')
        parser.add_argument('--add', help='adding a task', metavar=('task'))
        parser.add_argument('--clear', help='clear all tasks', action='store_true')
        parser.add_argument('--show', help='show all tasks', action='store_true')
        parser.add_argument('--delete', help='delete task by id', type=int, metavar=('id'))
        parser.add_argument('--modify', help='modify task by id', nargs=3, metavar=('id', 'column', 'value'))
        parser.add_argument('--log', help='show log', action='store_true')

        self.args = parser.parse_args()

    def read_existing_data(self):
        try:
            self.read_file()
            self.get_last_row()

        except:
            x = PrettyTable()
            x.field_names = self.field_names

            self.mytable = x
            self.save_file(table=x)

    def save_file(self, table):
        with open('file.txt', 'w') as f:
            data = table.get_csv_string()
            f.write(data)

    def read_file(self):
        with open("file.txt", "r") as fp:
            self.mytable = from_csv(fp)

    def get_last_row(self):
        self.last_row = self.mytable.rows[-1][0]

    def find_index_from_id(self, id):
        rows = self.mytable.rows
        for i, r in enumerate(rows):
            if id == int(r[0]):
                return i
            
    def modify_row(self, args):

        id = args[0]
        column = args[1]
        value = args[2]

        index = self.find_index_from_id(id)
        rows = self.mytable.rows
        
        #add modifying by column name

        for i, r in enumerate(rows):
            if int(id) == int(r[0]):
                self.l.add_log(f'column {column} of task with id {id} has been modified from {rows[i][1]} to {value}')   
                rows[i][1] = value

        self.mytable.clear_rows()
        self.mytable.add_rows(rows)
        self.save_file(self.mytable)
        print(self.mytable)

    def adding_all_attrs(self):
        attrs_array = []
        for attr in self.sub_attrs:
            attrs_array.append(input(attr+': '))

        self.mytable.add_row([int(self.last_row)+1, self.args.add] + attrs_array)

class Log:
    def __init__(self) -> None:
        self.check_if_exists_log_file()

    def check_if_exists_log_file(self):
        if os.path.exists('./backup/.log'):
            self.read_file()
        else:
            try:
                os.mkdir('backup')
            except:
                x = PrettyTable()
                x.field_names = ['datetime', 'action']

                self.mylog = x
                print(x)
                self.save_file(table=x)

    def read_file(self):
        with open("./backup/.log", "r") as fp:
            self.mylog = from_csv(fp)

    def save_file(self, table):
        with open("./backup/.log", 'w') as f:
            data = table.get_csv_string()
            f.write(data)

    def add_log(self, action:str):
        self.mylog.add_row([datetime.datetime.now(), action])
        self.save_file(self.mylog)

    def show(self):
        print(self.mylog)

if __name__ == '__main__':
    t = Todo()