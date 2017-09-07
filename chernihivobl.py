
import re
import os, glob
from common import add_or_create_name_vote, update_voters, update_voters_with_zeros

# question_reg = r'''(?s)№ п/п[ ]*Прізвище, Ім'я, По-батькові[ ]*Вибір(.*?)ВСЬОГО: *([0-9]*)'''
voter_reg  = r'''[0-9]{1,3}\. *([\w'-]* *[\w'-]* *[\w'-]*) *- *([\w ]*)'''
question_reg = r'''(?s)[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}(.*?)(?=[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}|\Z)'''
last_question = ''


question_number_reg = r'''Питання № ([0-9]*)'''


# def get_highest_question_number(filepath):
#     question_number_pat = re.compile(question_number_reg)
#     with open(filepath, 'r') as f:
#         text = f.read()
#     numbers = question_number_pat.findall(text)
#     return int(numbers[-1])



def get_voters(filepath):
    question_pat = re.compile(question_reg)
    voter_pat = re.compile(voter_reg)
    questions = []
    voters = {}
    with open(filepath, 'r') as f:
        text = f.read()
        questions = question_pat.findall(text)
        for question in questions:            
            question_voters = voter_pat.findall(question)
            # assert(len(question_voters) == int(question[1]))
            for voter in question_voters:
                add_or_create_name_vote(voters,voter[0],voter[1])
        print(len(voters))
        return voters
        # for voter in voters:
        #     print(voter, voters[voter])
        # print(len(voters))


def get_all_voters(folderpath):
    path_pattern = '/'.join([folderpath, '**/*.txt'])
    filepaths = glob.glob(path_pattern, recursive=True)
    voters = {}
    for filepath in filepaths:
        current_voters = get_voters(filepath)
        update_voters(voters, current_voters)
    votings = ['ЗА','ПРОТИ','УТРИМАВСЯ', 'Не голосував']
    update_voters_with_zeros(voters, votings)
    return voters
    # for voter in voters:
    #     print(voter, voters[voter])









