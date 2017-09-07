import re
import os, glob
from common import add_or_create_name_vote, update_voters, update_voters_with_zeros

import datetime

import xlrd, xlwt
from xlutils.copy import copy

# question_reg = r'''(?s)№ п/п[ ]*Прізвище, Ім'я, По-батькові[ ]*Вибір(.*?)ВСЬОГО: *([0-9]*)'''
"""
groups are: datetime, question, question_number, voters_list, voted_total 
"""
question_reg = r'''(?s)від   (.*?)\n\s*(.*?)\s*Питання № (\d+).*?№ п/п[ ]*Прізвище, Ім'я, По-батькові[ ]*Вибір(.*?)ВСЬОГО: *([0-9]*)'''

voter_reg  = r'''[0-9]+ *([\w'-]* *[\w'-]* *[\w'-]*) *([\w ]*)'''

question_number_reg = r'''Питання № ([0-9]*)'''


session_name_reg = r'''ПОІМЕННЕ ГОЛОСУВАННЯ\s+(.*)\n'''


def get_highest_question_number(filepath):
    question_number_pat = re.compile(question_number_reg)
    with open(filepath, 'r') as f:
        text = f.read()
    numbers = question_number_pat.findall(text)
    return int(numbers[-1])


def get_voters(filepath):
    question_pat = re.compile(question_reg)
    voter_pat = re.compile(voter_reg)
    questions = []
    voters = {}
    with open(filepath, 'r') as f:
        text = f.read()
        questions = question_pat.findall(text)
        assert(len(questions) == get_highest_question_number(filepath))
        for question in questions:
            question_voters = voter_pat.findall(question[0])
            assert(len(question_voters) == int(question[1]))
            for voter in question_voters:
                add_or_create_name_vote(voters,voter[0],voter[1])
    return voters


def session_to_xls(inputpath, outputpath, council_name, convocation_number):
    question_pat = re.compile(question_reg)
    voter_pat = re.compile(voter_reg)
    session_name_pat = re.compile(session_name_reg)
    questions = []
    
    rb = xlrd.open_workbook(outputpath, formatting_info=True)
    r_sheet = rb.sheet_by_index(0) 
    r = r_sheet.nrows + 1
    wb = copy(rb) 
    sheet = wb.get_sheet(0) 
 
    with open(inputpath, 'r') as f:
        text = f.read()
        session_name = session_name_pat.findall(text)[0]
        questions = question_pat.findall(text)
        assert(len(questions) == get_highest_question_number(inputpath))
        thing = True
        for question in questions:
            d = datetime.datetime.strptime(question[0], '%d.%m.%Y %H:%M')
            voting_date = str(d.date())
            voting_time = str(d.time())
            question_text = question[1]
            question_number = question[2]
            question_voters = voter_pat.findall(question[3])
            assert(len(question_voters) == int(question[4]))

            for voter in question_voters:
                pib = voter[0]
                answer = voter[1]
                lst = [
                        pib,
                        council_name,
                        convocation_number,
                        session_name,
                        "",
                        "",
                        question_text,
                        answer,
                        voting_date,
                        voting_time
                ]

                for i in range(len(lst)):
                    sheet.write(r, i, lst[i])
                r+=1

    wb.save(outputpath)



    # return voters


def get_all_voters(folderpath):
    path_pattern = '/'.join([folderpath, '**/*.txt'])
    filepaths = glob.glob(path_pattern, recursive=True)
    voters = {}
    for filepath in filepaths:
        current_voters = get_voters(filepath)
        update_voters(voters, current_voters)
    votings = ['ЗА','ПРОТИ','УТРИМАВСЯ', 'НЕ ГОЛОСУВАВ','відсутній']
    update_voters_with_zeros(voters, votings)
    return voters
    # for voter in voters:
    #     print(voter, voters[voter])


def all_sessions_to_xls(folderpath, outputpath, council_name, convocation_number):
    path_pattern = '/'.join([folderpath, '**/*.txt'])
    filepaths = glob.glob(path_pattern, recursive=True)

    for filepath in filepaths:
        print(filepath)
        session_to_xls(
                filepath,
                outputpath,
                council_name,
                convocation_number
        )
        











