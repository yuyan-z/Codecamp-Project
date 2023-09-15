from command import Command
from config import Config
from utils import get_args

if __name__ == '__main__':
    config = Config()

    """ debug """
    # command_str = 'task lestaches.txt add task 1'
    # command_str = 'task lestaches.txt modify 2 --description task 2 modified --project codecamp 4'
    # command_str = 'task lestaches.txt show'
    # command_str = 'task lestaches.txt rm 2'
    # args_dict = get_args(command_str)
    # command = Command(args_dict)
    # command.do_command()

    """ run """
    while True:
        command_str = input('Input a command, q for quit: ')
        if command_str == 'q':
            break
        else:
            args_dict = get_args(command_str, config)
            # print('args_dict:', args_dict)
            command = Command(args_dict, config)
            command.do_command()
        print()





