import os
import argparse


class Commend:
    def __init__(self, args):
        self.task = args.task
        self.file_name = args.file_name
        self.op = args.op
        self.params = args.params

        self.description = ""
        self.id = 0
        self.tasks = {}

    def check_grammar(self):
        """
        check the grammar of the command
        """
        res = 0  # 1 for error

        if self.task == "task":
            if self.op == "add" and len(self.params) >= 1:  # description
                self.description = " ".join(self.params)
            elif self.op == "modify" and len(self.params) >= 2:  # id, description
                self.id = int(self.params[0])
                self.description = " ".join(self.params[1:])
            elif self.op == "rm" and len(self.params) == 1:  # id
                self.id = int(self.params[0])
            elif self.op == "show" and len(self.params) == 0:
                pass
            else:
                res = 1
        else:
            res = 1

        return res

    def get_tasks(self):
        """
        read tasks from file
        """
        res = 0
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                data = f.readlines()
            for d in data:
                id, description = d.split(",")
                self.tasks[int(id)] = description.strip()
        else:
            to_create = input(self.file_name + " can't find, create? (y/n) : ")
            if to_create == "y":
                with open(self.file_name, "w") as f:
                    print(self.file_name, "created")
            else:
                res = 1

        return res

    def add(self):
        self.id = len(self.tasks) + 1
        self.tasks[self.id] = self.description
        with open(self.file_name, "a") as f:
            f.write(str(self.id) + "," + self.description + "\n")

        print(self.id, "added")

        return self.id

    def modify(self):
        if self.tasks.get(self.id):
            self.tasks[self.id] = self.description

            with open(self.file_name, "w") as f:
                for task in self.tasks.items():
                    f.write(str(task[0]) + "," + task[1] + "\n")

            print(self.id, "modified")
        else:
            print(self.id, " can't be found")

    def rm(self):
        if self.tasks.get(self.id):
            self.tasks.pop(self.id)

            with open(self.file_name, "w") as f:
                for task in self.tasks.items():
                    f.write(str(task[0]) + "," + task[1] + "\n")
        else:
            print(self.id, " can't be found")

    def show(self):
        print("+-----+----------+")
        print("| id | description |")
        print("+-----+----------+")
        if self.tasks:
            for task in self.tasks.items():
                print("| ", task[0], " | ", task[1].strip(), " |")
        print("+-----+----------+")

    def do_command(self):
        if self.check_grammar() == 1:
            print("Grammar error!")
            return
        if self.get_tasks() == 1:
            print("File name error!")
            return

        getattr(self, self.op)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Input a command")
    parser.add_argument("task", type=str, help="Task")
    parser.add_argument("file_name", type=str, help="File name")
    parser.add_argument("op", type=str, choices=["add", "modify", "rm", "show"], help="Operation")
    parser.add_argument("params", nargs="*", help="Other parameters")
    args = parser.parse_args()

    # print(args.task, args.file_name, args.op, args.params)

    commend = Commend(args)
    commend.do_command()



