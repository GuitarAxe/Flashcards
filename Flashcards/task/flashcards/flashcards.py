from constants import *
from actions import *
import argparse


while True:
    parser = argparse.ArgumentParser(description="Import and export argument parser.")
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()

    if args.import_from is not None:
        import_quizzes(args)

    print_save('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
    action = save_log(input())

    if action == ADD:
        add_card()
    elif action == REMOVE:
        remove_card()
    elif action == IMPORT:
        import_file()
    elif action == EXPORT:
        export_file()
    elif action == ASK:
        ask()
    elif action == EXIT:
        exit_quizzes(args)
        break
    elif action == LOG:
        log()
    elif action == HARDEST_CARD:
        hardest_card()
    elif action == RESET_STATS:
        reset_status()
    else:
        print('Invalid action')
