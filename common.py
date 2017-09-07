import copy

def add_or_create_name_vote(voters, name, vote):
    """
    modiffies voters
    """
    if name not in voters:
        voters[name] = {vote : 1,}
    else:
        if vote not in voters[name]:
            voters[name].update({vote:1})
        else:
            voters[name][vote] += 1


def update_voters(voters, new_voters):
    for new_voter in new_voters:
        if new_voter not in voters:
            voters[new_voter] = copy.deepcopy(new_voters[new_voter])
        else:
            for vote in new_voters[new_voter]:
                if vote not in voters[new_voter]:
                    voters[new_voter][vote] = new_voters[new_voter][vote]
                else:
                    voters[new_voter][vote] += new_voters[new_voter][vote]


def update_voters_with_zeros(voters, votings):
    for voter in voters:
        for voting in votings:
            if voting not in voters[voter]:
                voters[voter][voting] = 0


def voters_to_xls(voters, votings, xlsfilename):
    with open(xlsfilename, 'w') as output_file:
        output_file.write('\t'.join(['ПІБ'] + votings) + '\n')
        for voter, summary in voters.items():
            summary_values = [str(summary[voting]) for voting in votings]
            file_ln = '\t'.join([voter] + summary_values) + '\n'
            output_file.write(file_ln)


