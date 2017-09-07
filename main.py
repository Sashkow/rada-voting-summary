import re
import glob
import os
import ntpath

from datetime import datetime
from common import add_or_create_name_vote, update_voters

from xlrd import open_workbook
import xlrd

from convert import get_rtf_files_list, get_txt_files_list

import copy


# rivne_miskrada
yes_reg_exp = r'''(?s)(?:Так )(.*)(?:Ні )'''
no_reg_exp = r'''(?s)(?:Ні )(.*)(?:Утрималися )'''
abstained_reg_exp = r'''(?s)(?:Утрималися )(.*)(?:Не голосували)'''
absent_reg_exp = r'''(?s)(?:Не голосували)(.*)(?:[0-9]+\.)'''

# kyiv_oblrada
za_reg_exp = r'''(?s)За \( Голосование: (.*)Проти \( Голосование:'''
proty_reg_exp = r'''(?s)Проти \( Голосование: (.*)Утримався \( Голосование:'''
utr_reg_exp = r'''(?s)Утримався \( Голосование: (.*)Не голосував \('''
ne_reg_exp = r'''(?s)Не голосував \( (.*)'''
wordpair_reg_exp = r'''\b(?=([\w']+\W+[\w']+))'''
group_two_words_reg_exp = r'''([\w']+)\W+([\w']+)'''


datetime_reg_exp = r'''[0-3][0-9]\.[0-1][0-9]\.[1-2]([0-9]){3} [0-2][0-9]:[0-5][0-9]:[0-5][0-9]'''

# rivne_oblrada
name_value_reg_exp_str = r'.+ .\. .\. - .+'
name_value_reg_exp = re.compile(name_value_reg_exp_str)

# ternopil_misto
p_i_b_vote_reg_exp = r'''(?s)([\w'’-]+)[ ]+([\w'’-]+)[ ]+([\w'’-]+)\W+([-\w'’ "]+)'''
total_vote_reg_exp = r'''(?s)УСЬОГО:[\n \t]+([0-9]+)'''

# liviv_misto

total_vote_lviv_reg_exp = r'''(?s)[ВУ]СЬОГО.*?([0-9]+)'''

# kmel_obl

p_i_b_reg_exp = r'''(?s)[0-9]+[ ]*\n[ ]*([\w'’-]+)[ ]+([\w'’-]+)[ ]+([\w'’-]+)'''

# dnipro_obl

pib_vote_dnipro_reg_exp = r''''''








regs_dict = {
        'yes' : yes_reg_exp,
        'no' : no_reg_exp,
        'abstained': abstained_reg_exp,
        'absent': absent_reg_exp,
}

regs_dict_kyiv = {
        'yes' : za_reg_exp,
        'no' : proty_reg_exp,
        'abstained': utr_reg_exp,
        'absent': ne_reg_exp,
}

def get_date(txt_file):
    """Get first DD.MM.YYYY HH:MM:SS from file and return a list of [dd, mm, yyyy]"""
    p = re.compile(datetime_reg_exp)
    search = p.search(txt_file.read())
    if search:
        date_str = search.group().split(' ')[0]
        date = datetime.strptime(date_str, '%d.%m.%Y')
        return date
    else:
        return datetime.strptime('01.01.2000', '%d.%m.%Y')


def get_names(txt_file, reg_exp):
    """Rivne. Return list of who voted as in reg_exp at meeting txt_file."""
    p = re.compile(reg_exp)
    s = txt_file.read()
    search = p.search(s)
    if not search:
        
        print(s, reg_exp)
        # error!
        return -1
    else:
        names = search.group().split('\n')[1:-1]
        if not names:
            print("Error: did not match regexp at", 
                s[:100])

        # cut out empty lines
        names = [name for name in names if name]
        return names


def get_names_kyiv(txt_file, reg_exp):
    """Kyiv oblrada. Return list of who voted as in reg_exp at meeting txt_file."""

    p = re.compile(reg_exp)
    s = txt_file.read()
    search = p.search(s)


    names = []
    if not search:
        
        print("get Error:",s, reg_exp)
        # error!
        return -1
    else:

        lines = search.group().split('\n')[1:-1]

        # cut out empty lines
        lines = [line.strip() for line in lines if line]

        rest = ''
        for line in lines:
            words = line.split(' ')
            if len(words) > 3 or 'Предложение' in line or '(' in line:
                pass
            elif len(words) == 3:
                names.append(line)
                if rest:
                    names.append(rest)
                    rest = ''
            else:
                if rest:
                    name = ' '.join([rest, line])
                    if name in names:
                        print("!!!", name)
                    else:
                        names.append(name)
                    rest = ''
                else:
                    rest = line

        return names

def get_names_kyiv_xls(xls_file_path):
    """
    returns list of all full names in xls file
    """
    names = []
    with open_workbook(xls_file_path) as wb:
        s = wb.sheets()[0]
        for row_index in range(s.nrows):
            for col_index in range(s.ncols):
                if str(s.cell(row_index,col_index).value).strip() == 'Депутат':
                    dep_row = row_index
                    dep_col = col_index
                    for row_index in range(dep_row+1,s.nrows):
                        name = str(s.cell(row_index, dep_col).value).strip()
                        # present = str(s.cell(row_index, 5).value).strip()
                        names.append(name)
                    return names
        print('xls read error')        
        return None


def get_names_present_kyiv_xls(xls_file_path):
    """
    returns list of all full names in xls file
    """
    names = []
    with open_workbook(xls_file_path) as wb:
        s = wb.sheets()[0]
        for row_index in range(s.nrows):
            for col_index in range(s.ncols):
                if str(s.cell(row_index,col_index).value).strip() == 'Депутат':
                    dep_row = row_index
                    dep_col = col_index
                    for row_index in range(dep_row+1,s.nrows):
                        name = str(s.cell(row_index, dep_col).value).strip()
                        present = str(s.cell(row_index, dep_col+3).value).strip()
                        if present:
                            names.append(name)
                    return names
        print('xls read error')        
        return None
        


def has_sirname_duplicates(names):
    sirnames = [name.split(' ')[0] for name in names]
    # print(len(sirnames))
    # print(len(set(sirnames)))
    return len(sirnames) != len(set(sirnames))


def get_minimal_unique_names(names):
    min_names = []
    for name in names:
        sirname_name = ' '.join(name.split(' ')[:2])
        min_names.append(sirname_name)
    return min_names


def get_sirnames_kyiv_layout(txt_file, reg_exp):
    """
    get sirnames form txt file that is converted from pdf -layout
    """
    p = re.compile(reg_exp)
    s = txt_file.read()
    search = p.search(s)

    names = []
    if not search:
        print("Error at:", s, reg_exp)
        # error!
        return -1
    else:
        # lines with one two or three words
        lines = search.group().split('\n')[1:-1]
        pibs = '\n'.join(lines)
        name_sirnames = re.findall(re.compile(wordpair_reg_exp), pibs)

        for i in range(len(name_sirnames)):
            p_i = re.search(re.compile(group_two_words_reg_exp),name_sirnames[i])
            name_sirnames[i] = ' '.join([p_i.group(1), p_i.group(2)])

        # if 'Тимофій Михайлович' in name_sirnames:
        #     name_sirnames[name_sirnames.index('Тимофій Михайлович')] = 'Нич Тимофій'
        return name_sirnames

    
def map_sirnames_to_pib_kyiv(pis, pibs):
    """
    maps sirname-name pairs (pis) to sirname-name-fathername triplets (pibs)
    returns a list of pibs of the same length as pis
    """
    pi_b_map = {} 
    for pib in pibs:
        p_i_b = pib.split(' ')
        if len(p_i_b) == 3:
            pi = ' '.join(p_i_b[:2])
            b = p_i_b[-1]
        else:
            pi = pib
            b = ''
        pi_b_map[pi] = b

    
    some_pibs = []
    for pi in pis:
        if pi in pi_b_map:
            b = pi_b_map[pi]
            some_pibs.append(' '.join([pi, b]))
        # else:
        #     print("map error", pi)
    return some_pibs


def get_names_kyiv_layout(txt_file, xls_file_path, reg_exp):
    pis = get_sirnames_kyiv_layout(txt_file, reg_exp)
    pibs = get_names_kyiv_xls(xls_file_path)
    some_pibs = map_sirnames_to_pib_kyiv(pis, pibs)
    return some_pibs




def print_voters_to_xls(voters, output_file):
    with open(output_file, 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'Так', 'Ні', 'Утрималися', 'Не голосували','\n']))
        for voter, summary in voters.items():
            file_ln = '\t'.join([
                    voter,
                    str(summary['yes']),
                    str(summary['no']),
                    str(summary['abstained']),
                    str(summary['absent']),
                    '\n',]
            )
            output_file.write(file_ln)


def vote_summary(fileslst, output_file):
    """
    fill the following dict:
    {"voter's name":{'yes':1, 'no':2, ...}, ...}
    """
    voters = {}

    # fileslst = get_txt_files_list(path)

    for f in fileslst:
        # print("processing:", f)
        for vote, reg in regs_dict.items():
            # print(" ", vote)
            with open(f, 'r') as meeting:
                names = get_names(meeting, reg)
                for name in names:
                    add_or_create_name_vote(voters, name, vote)

    # add zero values where no votes of certain type
    for voter in voters:
        for vote in regs_dict:
            if vote not in voters[voter]:
                voters[voter][vote] = 0


    print_voters_to_xls(voters, output_file)

    return voters


def vote_summary_kyiv(folders_path, output_file):
    """
    fill the following dict:
    {"voter's name":{'yes':17, 'no':25а, ...}, ...}
    """
    voters = {}

    folders = glob.glob(os.path.join(folders_path, '*/'))
    files_count = 0
    for folder in folders:
        xls_file_path = glob.glob(os.path.join(folder, '*.xls'))[0]
        pibs = get_names_kyiv_xls(xls_file_path)
        
        fileslst = glob.glob(os.path.join(folder, '*.txt'))

        for pib in pibs:
            if not pib in voters:
                voters[pib] = {}

        
        # fileslst = get_txt_files_list(path)

        for f in fileslst:
            files_count += 1
            # print("processing:", f)
            for vote, reg in regs_dict_kyiv.items():
                # print(" ", vote)
                with open(f, 'r') as desidion:
                    names = get_names_kyiv_layout(desidion, xls_file_path, reg)
                    
                    for name in names:
                        add_or_create_name_vote(voters, name, vote)

        # add zero values where no votes of certain type
        for voter in voters:
            for vote in regs_dict_kyiv:
                if vote not in voters[voter]:
                    voters[voter][vote] = 0

    # print('total files:', files_count)
    with open(output_file, 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'Так', 'Ні', 'Утрималися', 'Не голосували','\n']))
        for voter, summary in voters.items():
            file_ln = '\t'.join([
                    voter,
                    str(summary['yes']),
                    str(summary['no']),
                    str(summary['abstained']),
                    str(summary['absent']),
                    '\n',]
            )
            output_file.write(file_ln)

    return voters



def vote_summary_present_but_not_voted_kyiv(folders_path, output_file):
    """
    fill the following dict:
    {"voter's name":{'yes':17, 'no':25а, ...}, ...}
    """
    voters = {}

    folders = glob.glob(os.path.join(folders_path, '*/'))
    files_count = 0
    
    for folder in folders:
        current_folder_files_count = 0
        xls_file_path = glob.glob(os.path.join(folder, '*.xls'))[0]
        # print("here", xls_file_path)
        pibs = get_names_kyiv_xls(xls_file_path)
        present_pibs = get_names_present_kyiv_xls(xls_file_path)
        
        fileslst = glob.glob(os.path.join(folder, '*.txt'))

        for pib in pibs:
            if not pib in voters:
                voters[pib] = {}

        
        # fileslst = get_txt_files_list(path)

        for f in fileslst:
            current_folder_files_count +=1
            files_count += 1
            # print("processing:", f)
            desidion_pibs_lst = []
            for vote, reg in regs_dict_kyiv.items():
                # print(" ", vote)
                with open(f, 'r') as desidion:
                    names = get_names_kyiv_layout(desidion, xls_file_path, reg)

                    for name in names:
                        if name not in desidion_pibs_lst:
                            desidion_pibs_lst.append(name)

                    for name in names:
                        add_or_create_name_vote(voters, name, vote)

            #if present but did not vote -> just_present
            for present_pib in present_pibs:
                if present_pib not in desidion_pibs_lst:
                    vote = 'just_present'
                    if present_pib not in voters:
                        voters[present_pib] = {vote : 1,}
                    else:
                        if vote not in voters[present_pib]:
                            voters[present_pib].update({vote:1})
                        else:
                            voters[present_pib][vote] += 1
                    


        # add zero values where no votes of certain type
        for voter in voters:
            for vote in regs_dict_kyiv:
                if vote not in voters[voter]:
                    voters[voter][vote] = 0
            if 'just_present' not in voters[voter]:
                voters[voter]['just_present'] = 0


    # print('total files:', files_count)
    with open(output_file, 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'Так', 'Ні', 'Утрималися', 'Не голосували', 'Просто присутній', '\n']))
        for voter, summary in voters.items():
            file_ln = '\t'.join([
                    voter,
                    str(summary['yes']),
                    str(summary['no']),
                    str(summary['abstained']),
                    str(summary['absent']),
                    str(summary['just_present']),
                    '\n',]
            )
            output_file.write(file_ln)

    return voters


def vote_halphyear_summary(path):
    """
    fill the following dict:
    {"voter's name":{'yes':1, 'no':2, ...}, ...}
    """
    fileslst = get_txt_files_list(path)
    dateslst = []
    date_dict = {}
    for f in fileslst:
        with open(f,'r') as meeting:
            date = get_date(meeting)
            if date.month < 7:
                halphyear = str(date.year)+"_01"
            else:
                halphyear = str(date.year)+"_02"
            if halphyear not in date_dict:
                date_dict[halphyear]=[f,]
            else:
                date_dict[halphyear].append(f)

    file_list = date_dict['2016_01']+date_dict['2016_02']
    # print(len(date_dict['2016_01']), len(date_dict['2016_02']))

    # print(len(file_list))
    vote_summary(file_list, "2016"+".tsv")
    # {halphyear:{voter:{'yes':1,...},...},...}
    # halphyear_dict = {}
    # for halphyear, fileslst in sorted(date_dict.items()):
    #     halphyear_dict[halphyear] = vote_summary(fileslst, halphyear+".tsv")


    # for halphyear, voters in sorted(halphyear_dict.items()):
    #     print(halphyear, len(voters))


def poltava_summary():
    """
    exclude blank lines
        filtered = filter(lambda x: not re.match(r'^\s*$', x), original)

    match desidion title i.e. more than three words in a row 
    match voter_vote
    match all_voters
    """
    pass

def make_replacements(file_lines):
    new_lines = []
    for line in file_lines:
        new_line = line.replace('Не гол.*', 'Не гол.')
        new_lines.append(new_line)
    return new_lines

def rivne_oblrada_summary():
    path = 'outputs/rivne_oblrada'
    files = os.listdir(path)
    filepaths = [os.path.join(path,f) for f in files]

    name_value_dict = {}
    voting_count = 0
    #gather name-vote-amount info
    for filepath in filepaths:
        with open(filepath, 'r') as f:
            file_lines = f.readlines()
            file_lines = make_replacements(file_lines)
            for line in file_lines:
                if 'За:' in line:
                    voting_count += 1
                if 'За: 0' in line:
                    print(line)

                search = name_value_reg_exp.search(line)
                if search:
                    name_value = search.group().strip()
                    name = name_value.split(' - ')[0].strip()
                    value = name_value.split(' - ')[1].strip()
                    if name in name_value_dict:
                        if value in name_value_dict[name]:
                            name_value_dict[name][value] += 1
                        else:
                            name_value_dict[name][value] = 1
                    else:
                        name_value_dict[name] = {value:1}

    
    votes = ['За', 'Проти', 'Утрим.', 'Не гол.']

    #check for unusual votes
    for name in name_value_dict:
        values = name_value_dict[name]
        for value in values:
            if value not in votes:
                print(value,values[value])

    # zeroes
    for name in name_value_dict:
        values = name_value_dict[name]
        for vote in votes:
            if vote not in values:
                values[vote] = 0

    for name in name_value_dict:
        print(name, name_value_dict[name])
    print(voting_count)

    #check voting_sum > voting_count
    for name in name_value_dict:
        values = name_value_dict[name]
        voting_sum = sum([values[value] for value in values])
        if voting_sum > voting_count:
            print(name, values, voting_sum, voting_count)

    voters = name_value_dict
    with open('results.tsv', 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'За', 'Проти', 'Утрим.', 'Не гол.','\n']))
        for voter, summary in voters.items():
            file_ln = '\t'.join([
                    voter,
                    str(summary['За']),
                    str(summary['Проти']),
                    str(summary['Утрим.']),
                    str(summary['Не гол.']),
                    '\n',]
            )
            output_file.write(file_ln)


def get_arrival_time(xls_folder_path, output_file):
    files = os.listdir(xls_folder_path)
    files = sorted(files)
    # filepaths = [ for fname in files]
    # {name: {session1:arrival_time, session2: arrival_time,...}, ...}
    deputy = {}
    for fname in files:
        with open_workbook(os.path.join(xls_folder_path,fname)) as wb:
            s = wb.sheets()[0]
            for row_index in range(s.nrows):
                for col_index in range(s.ncols):
                    if str(s.cell(row_index,col_index).value).strip() == 'Депутат':
                        dep_row = row_index
                        dep_col = col_index
                        for row_index in range(dep_row+1,s.nrows):
                            name = str(s.cell(row_index, dep_col).value).strip()

                            arrival_time = str(s.cell(row_index, dep_col+2).value).strip()
                            if not arrival_time:
                                arrival_time = 'absent'
                            if name not in deputy:
                                deputy[name]= {fname[2:-4]:arrival_time}
                            else:
                                if fname[2:-4] not in deputy[name]:
                                    deputy[name][fname[2:-4]] = arrival_time
                                else:
                                    print('Error: arrival time twice in same doc')


    with open(output_file, 'w') as output_file:
        first_heading = ['Депутат_ка']
        headings = []
        
        for i in range(len(files)):
            heading = files[i][2:-4]
            headings.append(heading)
            

        all_headings = first_heading + headings + ['\n']

        output_file.write('\t'.join(all_headings))

        for name in deputy:
            line = [name]
            for heading in headings:
                if heading in deputy[name]:
                    line.append(deputy[name][heading])
            line.append('\n')
            output_file.write('\t'.join(line))


def get_voters_ternopil(filepath):
    voters = {}
    exp = re.compile(p_i_b_vote_reg_exp)
    total_exp = re.compile(total_vote_reg_exp)
    with open(filepath, 'r') as f:
        contents = f.read()
    total = total_exp.findall(contents)

    delimiter = "Прізвище, Ім'я, По-батькові"
    contents = contents.split(delimiter)[1]
    delimiter2 = "УСЬОГО:"
    new_contents = contents.split(delimiter2)
    if len(new_contents)==2:
        contents = new_contents[0]
    else:
        print("Usyoho not found")


    
    all_pairs = exp.findall(contents)
    
    assert(len(total) == 1)
    total = int(total[0])
    for pair in all_pairs:
        pib = ' '.join(pair[:3])
        vote = pair[-1]
        add_or_create_name_vote(voters, pib, vote)
    if len(voters) != total:
        print(filepath, len(voters), total)
    # assert(len(voters)==total)
    votes = ['ЗА','УТРИМАВСЯ','ПРОТИ','НЕ ГОЛОСУВАВ','відсутній']
    #add zeroes
    for voter in voters:
        for vote in votes:
            if vote not in voters[voter]:
                voters[voter][vote] = 0



    return voters


def get_voters_ternopil_all_files(files_path):
    """
    takes folder with txt files to process. Subfolders allowed
    """
    voters = {}
    files_lst = get_txt_files_list(files_path)

    votings_count = 0

    for fname in files_lst:
        current_voters = get_voters_ternopil(fname)
        if current_voters:
            votings_count += 1
        update_voters(voters, current_voters)

    # print('total files:', votings_count)
    with open('ternopil_misto.xls', 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'Так', 'Ні', 'Утрималися', 'Не голосували', 'Відсутні', '\n']))
        for voter, summary in voters.items():
            file_ln = '\t'.join([
                    voter,
                    str(summary['ЗА']),
                    str(summary['ПРОТИ']),
                    str(summary['УТРИМАВСЯ']),
                    str(summary['НЕ ГОЛОСУВАВ']),
                    str(summary['відсутній']),
                    '\n',]
            )
            output_file.write(file_ln)

# lviv_misto    


def get_voters_lviv(filepath):
    voters = {}
    exp = re.compile(p_i_b_vote_reg_exp)
    total_exp = re.compile(total_vote_lviv_reg_exp)
    with open(filepath, 'r') as f:
        contents = f.read()
    total = total_exp.findall(contents)

    delimiter = "Прізвище, Ім'я, По-батькові"
    contents = contents.split(delimiter)[-1]
    delimiter2 = "ВСЬОГО:"
    new_contents = contents.split(delimiter2)
    if len(new_contents)==2:
        contents = new_contents[0]
    else:
        delimiter2 = "УСЬОГО:"
        new_contents = contents.split(delimiter2)
        if len(new_contents)==2:
            contents = new_contents[0]
        else:
            print("Usyoho not found", filepath)



    
    all_pairs = exp.findall(contents)
    for item in total:
        assert(item==total[0])
    # assert(len(total) == 1)
    # if len(total) > 1:
    #     print("More than 1 voting in file:", filepath)
        # return {}


    total = int(total[0])
    for pair in all_pairs:
        pib = ' '.join(pair[:3])
        vote = pair[-1]
        add_or_create_name_vote(voters, pib, vote)
    if len(voters) != total:
        print(filepath, len(voters), total)
    assert(len(voters)==total)
    votes = ['ЗА','УТРИМАВСЯ','ПРОТИ','НЕ ГОЛОСУВАВ','відсутній']
    #add zeroes
    for voter in voters:
        for vote in votes:
            if vote not in voters[voter]:
                voters[voter][vote] = 0



    return voters


def get_voters_lviv_all_files(files_path):
    """
    takes folder with txt files to process. Subfolders allowed
    """
    voters = {}
    files_lst = get_txt_files_list(files_path)

    votings_count = 0

    for fname in files_lst:
        current_voters = get_voters_lviv(fname)
        if current_voters:
            votings_count += 1
        update_voters(voters, current_voters)

    print(voters)

    # print('total files:', votings_count)
    vote_types = ['ЗА','УТРИМАВСЯ','ПРОТИ','НЕ ГОЛОСУВАВ','відсутній']
    with open('lviv_misto.xls', 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'Партія', 'Так', 'Ні', 'Утрималися', 'Не голосували', 'Відсутні', '\n']))
        for voter, summary in voters.items():
            party = [vote for vote in summary if vote not in vote_types]
            if len(party) == 0:
                party = ''
            elif len(party) == 1:
                party = party[0]
            else:
                print("Multiple parties:", party)
                party = ', '.join(party)

            file_ln = '\t'.join([
                    voter,
                    party,
                    str(summary['ЗА']),
                    str(summary['ПРОТИ']),
                    str(summary['УТРИМАВСЯ']),
                    str(summary['НЕ ГОЛОСУВАВ']),
                    str(summary['відсутній']),
                    '\n',]
            )
            output_file.write(file_ln)

# khmel_obl


def get_voters_khmel(filepath):
    if 'РЕЄСТРАЦІЯ' in filepath:
        print('REGISTRY', filepath)
        return {}
    voters = {}
    exp = re.compile(p_i_b_vote_reg_exp)
    total_exp = re.compile(total_vote_lviv_reg_exp)
    with open(filepath, 'r') as f:
        contents = f.read()
    total = total_exp.findall(contents)
    if not total:
        print("Total voters not found at:", filepath)


    delimiter = "Прізвище"
    contents = contents.split(delimiter)[-1]
    delimiter2 = "ВСЬОГО:"
    new_contents = contents.split(delimiter2)
    if len(new_contents)==2:
        contents = new_contents[0]
    else:
        delimiter2 = "УСЬОГО:"
        new_contents = contents.split(delimiter2)
        if len(new_contents)==2:
            contents = new_contents[0]
        else:
            print("Usyoho not found", filepath)


    # print("_________-")
    # print(contents)
    # print("_________-")
    all_pairs = exp.findall(contents)
    for item in total:
        assert(item==total[0])

    # assert(len(total) == 1)
    # if len(total) > 1:
    #     print("More than 1 voting in file:", filepath)
        # return {}


    total = int(total[0])
    for pair in all_pairs:
        pib = ' '.join(pair[:3])
        vote = pair[-1]
        if vote == 'УТРИМАВСЯ':
            vote = 'УТРИМАЛОСЬ'
        if vote == 'НЕ ГОЛОСУВАВ':
            vote = 'НЕ ГОЛОСУВАЛО'
        add_or_create_name_vote(voters, pib, vote)

    
    votes = ['ЗА','УТРИМАЛОСЬ','ПРОТИ','НЕ ГОЛОСУВАЛО']
    #add zeroes
    for voter in voters:
        for vote in votes:
            if vote not in voters[voter]:
                voters[voter][vote] = 0

    all_zeros = True
    for voter in voters:
        for vote in votes:
            if voters[voter][vote] != 0:
                all_zeros = False
    if all_zeros:
        print('No votes at:', filepath)
        return {}


    if len(voters) != total:
    # for voter in voters:
    #     print(voter, voters[voter])
        print(filepath, len(voters), total)
    assert(len(voters)==total)

    return voters


def get_voters_khmel_all_files(files_path):
    """
    takes folder with txt files to process. Subfolders allowed
    """

    voters = {}
    files_lst = get_txt_files_list(files_path)

    votings_count = 0

    for fname in files_lst:
        current_voters = get_voters_khmel(fname)
        if current_voters:
            votings_count += 1
        else:
            print("Empty:", fname)
        update_voters(voters, current_voters)


    print("Votings count:", votings_count)



    fill_registry(voters, files_path)
    for voter in sorted(voters):
        print('\t'.join([voter, str(voters[voter]['registered'])]))

    # print('total files:', votings_count)
    vote_types = ['ЗА','УТРИМАЛОСЬ','ПРОТИ','НЕ ГОЛОСУВАЛО']
    with open('khmel_obl.xls', 'w') as output_file:
        output_file.write('\t'.join(['ПІБ', 'Партія', 'Так', 'Ні', 'Утрималися', 'Не голосували', 'Зареєструвалося', '\n']))
        for voter, summary in voters.items():

            party = [vote for vote in summary if vote not in vote_types]
            if len(party) == 0:
                party = ''
            elif len(party) == 1:
                party = party[0]
            else:
                print("Multiple parties:", party)
                party = ', '.join(party)

            

            file_ln = '\t'.join([
                    voter,
                    party,
                    str(summary['ЗА']),
                    str(summary['ПРОТИ']),
                    str(summary['УТРИМАЛОСЬ']),
                    str(summary['НЕ ГОЛОСУВАЛО']),
                    '\n',]
            )
            output_file.write(file_ln)


def get_session_votings_count(session_path):
    files_lst = get_txt_files_list(session_path)
    votings_count = 0
    for fname in files_lst:
        current_voters = get_voters_khmel(fname)
        if current_voters:
            votings_count += 1
        else:
            print("Empty:", fname)
    return votings_count

def get_all_session_votings_count(sessions_path):
    folders = os.listdir(sessions_path)
    folder_paths = [os.path.join(sessions_path, folder) for folder in folders]
    session_votings_dict = {}
    for folder in folder_paths:
        fldr = folder.split('/')[-1]
        session_votings_dict[fldr] = get_session_votings_count(folder)
    return session_votings_dict

def get_voters_registry(folder):
    registry = []
    folder_contents = os.listdir(folder)
    registry_file_name = ''
    for contetnt in folder_contents:
        if "РЕЄСТРАЦІЯ" in contetnt and '.txt' in contetnt:
            registry_file_name = contetnt
            
    if registry_file_name == '':
        return ['ВИШНІВСЬКА Наталія Миколаївна', 'ЖВАЛЮК Микола Володимирович', 'НІКУЛІШИН Ігор Анатолійович', 'НОВОСЕЛЬСЬКА Надія Яківна', 'ПОБІЯНСЬКИЙ Валентин Іванович', 'ЛЕСКОВ Валерій Олександрович', 'ДЕХТЯРУК Олександр Миколайович', 'МИШКО Володимир Васильович', 'ПОВОРОЗНИК Володимир Васильович', 'БАНДИРСЬКИЙ Віталій Анатолійович', 'ШУТЯК Андрій Васильович', 'ПРИСЯЖНИЙ Володимир Броніславович', 'КИРИЛЮК Іван Іванович', 'МОВСІСЯН Врам Македонович', 'КОВАЛЬ Людмила Миколаївна', 'ГОНЧАР Іван Ярославович', 'ПАВЛЮК Петро Миколайович', 'РОМАСЮКОВ Артем Євгенійович', 'ЦУГЛЕВИЧ Яків Миколайович', 'ПАЛІЙ Олександр Володимирович', 'ГЛАДІЙ Валентина Євгенівна', 'МИКЛУШ Олександр Петрович', 'ПЕТЛЬОВАНИЙ Руслан Федорович', 'ОЛУЙКО Віталій Миколайович', 'ТКАЧЕНКО Уляна Юріївна', 'СКРИМСЬКИЙ Руслан Францович', 'ЛОЗОВИЙ Вадим Миколайович', 'БІЛЯВЕЦЬ Олег Петрович', 'БУРЛИК Віктор Вікторович', 'БРУХНОВА Лілія Степанівна', 'ОЛІЙНИК Анатолій Антонович', 'СПІВАК Олександр Михайлович', 'ПАНЧУК Анатолій Анатолійович', 'ЛАТИНСЬКИЙ Едуард Владиславович', 'САВЧУК Олександр Петрович', 'ОСТРОВСЬКА Ніла Василівна', 'ЯЦКОВ Борис Олександрович', 'ДРАЛЮК Микола Іванович', 'СТЕПАНЮК Леонід Адамович', 'ЛЕБЕДИНСЬКИЙ Віктор Вікторович', 'ОЛИЦЬКИЙ Микола Васильович', 'КОВАЛЬ Наталія Михайлівна', 'БОЙКО Михайло Дмитрович', 'ДРАГАН Олександр Васильович', 'ПЕРЕЙМА Анатолій Анатолійович', 'ФРІДМАН Артур Давидович', 'АНТОНЮК Вячеслав Вікторович', 'ХАРКАВИЙ Микола Олександрович', 'КУХАРУК Наталія Леонідівна', 'ІВАЩУК Сергій Петрович', 'ТЕРЛЕЦЬКА Галина Василівна', 'ЯЩУК Інна Петрівна', 'ЗЕЛЕНКО Тетяна Іванівна', 'АНДРІЙЧУК Неоніла Вячеславівна', 'ЯНЧУК Микола Андрійович', 'ЗАВРОЦЬКИЙ Олександр Іванович', 'СКРИНЧУК Олег Леонідович', 'МИКУЛЬСЬКИЙ Сергій Володимирович', 'СТРОЯНОВСЬКИЙ Василь Станіславович', 'ТКАЧ Борис Васильович', 'МАСТІЙ Василь Васильович', 'ДЯЧУК Микола Миколайович', 'ФЕДОРЧУК Володимир Володимирович', 'ЛУЧКОВ Дмитро Олександрович', 'БЕРЕГОВА Оксана Віталіївна', 'МОЦНИЙ Микола Іванович', 'ГЛАДУНЯК Іван Васильович', 'ЧУБАР Віктор Миколайович', 'ЗАВАЛЬНЮК Юрій Анатолійович', 'САЛАНСЬКИЙ Анатолій Миколайович', 'ПРОЦЮК Василь Васильович', 'СМАЛЬ Юрій Валентинович', 'СЛОБОДЯН Олександр Станіславович']


    print(">>", registry_file_name)
    with open(os.path.join(folder,registry_file_name), 'r') as f:
        registry_text = f.read()

    compiled_pib = re.compile(p_i_b_reg_exp)
    regisrtry = compiled_pib.findall(registry_text)


    united_regisrty = [' '.join(p_i_b) for p_i_b in regisrtry]
    
    return united_regisrty




def fill_registry(voters, sessions_path):
    """
    modiffies voters
    """
    folders = os.listdir(sessions_path)
    folder_paths = [os.path.join(sessions_path, folder) for folder in folders]
    session_votings_dict = get_all_session_votings_count(sessions_path)
    all_registered_voters = {}
    for folder in folder_paths:
        fldr = folder.split('/')[-1]
        registered_voters = get_voters_registry(folder)
        for voter in registered_voters:
            if 'registered' not in voters[voter]:
                voters[voter]['registered'] = session_votings_dict[fldr]
            else:
                voters[voter]['registered'] += session_votings_dict[fldr]

    for voter in voters:
        if 'registered' not in voters[voter]:
            voters[voter]['registered'] = 0


    
# vynnica_misto








def main():
    # vote_summary_present_but_not_voted_kyiv('/home/sashko/Python/rada/data/kyiv/results_layout/','kyiv.xls')
    # filepath = '/home/sashko/Python/rada/data/lviv_misto/5475-rezulytaty-golosuvannya-plenarnogo-zasidannya-14-01-2016/1.txt'
    folderpath = '/home/sashko/Python/rada/data/khmel_obl/'
    # voters = get_voters_khmel(filepath)
    # for voter in voters:
    #     print(voter, voters[voter])







    # all_rtf_to_txt('inputs', 'outputs')
    # vote_summary('outputs','2016.tsv')



    # vote_halphyear_summary('outputs')
    # with open('outputs/782.txt','r') as meeting:
    #     date = get_date(meeting)
    #     print(f, date)



if __name__ == '__main__':
    main()

    



