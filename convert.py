import glob

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


def doc_to_txt(doc_file_path):

    new_doc_file_path = \
            doc_file_path.replace(' ','_').replace('(','_').replace(')','_')


    input_file_name = ntpath.basename(new_doc_file_path)
    
    output_file_name = '.'.join(input_file_name.split('.')[:-1]) + '.txt'

    os.rename(doc_file_path, new_doc_file_path)



    output_path = 'outputs/rivne_oblrada'
    output_file_path = os.path.join(output_path,output_file_name)
    command = 'unoconv -o \"%s\" \"%s\"' % (output_file_path, doc_file_path)
    os.system(command)


def all_rtf_to_txt(inputs_path, output_path):

    fileslst = get_rtf_files_list(inputs_path)
    length = len(fileslst)
    i = 0
    for f in fileslst:
        i += 1
        print("converting file ", i, "of", length, ":", f)
        rtf_to_txt(f, output_path, str(i))        
