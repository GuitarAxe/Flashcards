from os.path import exists
import json
import ast

term_to_definition_dict = {}
wrong_answers_dict = {}
log_list = []


def get_log_list():
    return log_list


def save_log(msg: str):
    log_list.append(msg)
    return msg


def print_save(msg: str):
    print(msg)
    return save_log(msg)


def add_card():
    print_save('The card:')
    while True:
        term = save_log(input())
        if term in term_to_definition_dict.keys():
            print_save('The card "{}" already exists. Try again:'.format(term))
            continue
        break
    print_save('The definition of the card:')
    while True:
        definition = save_log(input())
        if definition in term_to_definition_dict.values():
            print_save('The definition "{}" already exists. Try again:'.format(definition))
            continue
        break
    print_save('The pair ("{0}":"{1}") has been added.'.format(term, definition))
    term_to_definition_dict.update({term: definition})


def remove_card():
    print_save('Which card?')
    card = save_log(input())
    if card in term_to_definition_dict.keys():
        term_to_definition_dict.pop(card)
        print_save('The card has been removed.')
    else:
        print_save('Can\'t remove "{}": there is no such card.'.format(card))


def import_file():
    print_save('File name:')
    file_name = save_log(input())
    import_from_file(file_name)


def import_quizzes(args):
    if args.import_from is not None:
        file_name = save_log(args.import_from)
        import_from_file(file_name)


def import_from_file(file_name: str):
    if not exists(file_name):
        print_save('File not found.')
        return term_to_definition_dict

    with open(file_name, 'r') as file:
        new_term_to_definition_dict = dict(ast.literal_eval(file.read()))
    print_save('{} cards have been loaded.'.format(len(new_term_to_definition_dict)))
    term_to_definition_dict.clear()
    term_to_definition_dict.update(new_term_to_definition_dict)


def export_file():
    print_save('File name:')
    file_name = save_log(input())
    export_to_file(file_name)


def exit_quizzes(args):
    if args.export_to is not None:
        file_name = save_log(args.export_to)
        export_to_file(file_name)
    print('Bye bye!')


def export_to_file(file_name: str):
    with open(file_name, 'w') as file:
        file.write(json.dumps(term_to_definition_dict))
    print_save('{} cards have been saved.'.format(len(term_to_definition_dict)))


def ask():
    print_save('How many times to ask?')
    attempts_number = int(save_log(input()))

    while True:
        for key, value in term_to_definition_dict.items():
            print_save('Print the definition of "{}"'.format(key))
            answer = save_log(input())

            if answer == value:
                print_save('Correct!')
            elif answer in term_to_definition_dict.values():
                correct_key = [k for k, v in term_to_definition_dict.items() if v == answer][0]
                print_save('Wrong. The right answer is "{0}", but your definition is correct for "{1}".'
                           .format(value, correct_key))
            else:
                add_wrong_answer(key)
                print_save('Wrong. The right answer is {}'.format(value))
            attempts_number -= 1
            if attempts_number == 0:
                return


def log():
    print_save('File name:')
    file_name = save_log(input())
    with open(file_name, 'a') as file:
        for item in log_list:
            file.write(str(item) + '\n')
    print('The log has been saved.')


def hardest_card():
    invalid_answer = get_most_invalid_answers()
    if invalid_answer is None:
        print_save('There are no cards with errors.')
        return
    (key, value), = invalid_answer.items()
    print_save('The hardest card is "{0}". You have {1} errors answering it'.format(key, str(value)))


def add_wrong_answer(definition: str):
    if definition not in wrong_answers_dict.keys():
        wrong_answers_dict.update({definition: 1})
    else:
        wrong_answers = wrong_answers_dict.get(definition)
        wrong_answers += 1
        wrong_answers_dict.update({definition: wrong_answers})


def get_most_invalid_answers():
    invalid_definition = []
    invalid_number = 0
    if not wrong_answers_dict:
        return None
    for key, value in wrong_answers_dict.items():
        if value > invalid_number:
            invalid_definition.append(key)
            invalid_number = value
    return {' '.join(invalid_definition): invalid_number}


def reset_status():
    wrong_answers_dict.clear()
    print_save('Card statistics have been reset.')
