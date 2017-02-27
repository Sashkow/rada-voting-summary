import re
import glob
import os
import ntpath

from datetime import datetime



yes_reg_exp = r'''(?s)(?:Так )(.*)(?:Ні )'''
no_reg_exp = r'''(?s)(?:Ні )(.*)(?:Утрималися )'''
abstained_reg_exp = r'''(?s)(?:Утрималися )(.*)(?:Не голосували)'''
absent_reg_exp = r'''(?s)(?:Не голосували)(.*)(?:[0-9]+\.)'''

datetime_reg_exp = r'''[0-3][0-9]\.[0-1][0-9]\.[1-2]([0-9]){3} [0-2][0-9]:[0-5][0-9]:[0-5][0-9]'''



regs_dict = {
        'yes' : yes_reg_exp,
        'no' : no_reg_exp,
        'abstained': abstained_reg_exp,
        'absent': absent_reg_exp,
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


def get_rtf_files_list(path):
    """Recursively search all rtf files in path, return list."""
    path_pattern = '/'.join([path, '**/*.rtf'])
    return glob.glob(path_pattern, recursive=True)

def get_txt_files_list(path):
    """Recursively search all txt files in path, return list."""
    path_pattern = '/'.join([path, '**/*.txt'])
    return glob.glob(path_pattern, recursive=True)

def rtf_to_txt(rtf_file_path, output_path, output_file_name=None):
    
    input_file_name = ntpath.basename(rtf_file_path)
    new_rtf_file_path = os.path.join(
            ntpath.dirname(rtf_file_path),
            input_file_name.replace(' ','_').replace('(','_').replace(')','_'),
    )


    os.rename(rtf_file_path, new_rtf_file_path)

    
    if output_file_name:
        file_name = output_file_name
    else:
        file_name = ntpath.basename(new_rtf_file_path)
        file_name = file_name.split('.')[0]

    output = os.path.join(output_path, file_name)
    

    command = "unoconv -o %s.txt \"%s\"" % (output, new_rtf_file_path)
    os.system(command)

def all_rtf_to_txt(inputs_path, output_path):
    fileslst = get_rtf_files_list(inputs_path)
    length = len(fileslst)
    i = 0
    for f in fileslst:
        i += 1
        print("converting file ", i, "of", length, ":", f)
        rtf_to_txt(f, output_path, str(i))        


def get_names(txt_file, reg_exp):
    """Return list of who voted as in reg_exp at meeting txt_file."""
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

def vote_summary(fileslst, output_file):
    """
    fill the following dict:
    {"voter's name":{'yes':1, 'no':2, ...}, ...}
    """
    voters = {}
    # fileslst = get_txt_files_list(path)
    print("here")
    print(len(fileslst))

    for f in fileslst:
        # print("processing:", f)
        for vote, reg in regs_dict.items():
            # print(" ", vote)
            with open(f, 'r') as meeting:
                names = get_names(meeting, reg)
                for name in names:
                    if name not in voters:
                        voters[name] = {vote : 1,}
                    else:
                        if vote not in voters[name]:
                            voters[name].update({vote:1})
                        else:
                            voters[name][vote] += 1

    # add zero values where no votes of certain type
    for voter in voters:
        for vote in regs_dict:
            if vote not in voters[voter]:
                voters[voter][vote] = 0


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
    print(len(date_dict['2016_01']), len(date_dict['2016_02']))

    print(len(file_list))
    vote_summary(file_list, "2016"+".tsv")
    # {halphyear:{voter:{'yes':1,...},...},...}
    # halphyear_dict = {}
    # for halphyear, fileslst in sorted(date_dict.items()):
    #     halphyear_dict[halphyear] = vote_summary(fileslst, halphyear+".tsv")


    # for halphyear, voters in sorted(halphyear_dict.items()):
    #     print(halphyear, len(voters))





    

# 2015-01-23 00:00:00
# 2017-01-24 00:00:00





def main():
    lst = get_rtf_files_list('inputs')
    i=1
    for item in lst:
        print(i, item)
        i+=1



    # all_rtf_to_txt('inputs', 'outputs')
    # vote_summary('outputs','2016.tsv')



    # vote_halphyear_summary('outputs')
    # with open('outputs/782.txt','r') as meeting:
    #     date = get_date(meeting)
    #     print(f, date)


# 
if __name__ == '__main__':
    main()

        






        # with open(f, 'r') as meeting:
        #     no_names = get_names(meeting, no_reg_exp)
        #     print("no    ", len(no_names))
        # with open(f, 'r') as meeting:
        #     abstained_names = get_names(meeting, abstained_reg_exp)
        #     print("hz    ", len(abstained_names))
        # with open(f, 'r') as meeting:
        #     absent_names = get_names(meeting, absent_reg_exp)
        #     print("out    ", len(absent_names))





    

# 3148 
# 2921




# def to_txt():


