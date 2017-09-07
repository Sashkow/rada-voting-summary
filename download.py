import requests 
import re
import os
import glob

# lviv_misto

domain = 'http://www.lvivrada.gov.ua'

def get_2016_only(hrefs):
    hrefs_2016 = []
    for href in hrefs:
        if '2016' in href:
            hrefs_2016.append(href)
    return hrefs_2016


def get_meeting_links():
    meeting_links = []
    meeting_href_reg = re.compile(r'href="(/zasidannia/rezultaty-golosuvan/item/.*)">')
    common_link_template = 'https://www.lvivrada.gov.ua/zasidannia/rezultaty-golosuvan?tmpl=component&start='
    start = 5
    for i in range(5):
        common_link = ''.join([common_link_template, str(start)])
        page = requests.get(common_link).text
        meeting_hrefs = meeting_href_reg.findall(page)
        meeting_hrefs = [''.join([domain,href]) for href in meeting_hrefs]
        meeting_hrefs_2016 = get_2016_only(meeting_hrefs)
        if not meeting_hrefs_2016:
            break
        else:
            meeting_links += meeting_hrefs_2016         
        start += 10

    return meeting_links


def download_all_rtfs_from_meeting(meeting_link, data_folder):
    r = requests.get(meeting_link)
    page = r.text
    href = re.compile(r'href="(.*\.rtf)')
    all_href = href.findall(page)

    urls = []
    for ref in all_href:
        urls.append(''.join([domain, ref]))
    
    
    folder_name = meeting_link.split('/')[-1]
    path = os.path.join(data_folder, folder_name)
    if not os.path.exists(path):
        os.system('mkdir '+ data_folder + '/'+folder_name)
    
    for url in urls:
        # print("-->",url)
        os.system('wget -P ' + path + ' "' + url +'"')








# meeting_links = get_meeting_links()

# # meeting_link = 'https://www.lvivrada.gov.ua/zasidannia/rezultaty-golosuvan/item/6285-rezulytaty-golosuvannya-plenarnogo-zasidannya-22-12-2016-26-12-2016'
# data_folder = '/home/sashko/Python/rada/data/lviv_misto'

# for meeting_link in meeting_links:
#     print("------>", meeting_link)
#     download_all_rtfs_from_meeting(meeting_link, data_folder)

#end lviv_misto

# khmel region

# kmel_oblrada

session_link_khmel_obl_reg =r'<a href="(http://km-oblrada.gov.ua/[/\w-]*-2016/)"'

voting_link_kmel_obl_reg1 = r'(?<=href=")([^"]*?)(?=">Результати поіменного голосування)'
voting_link_kmel_obl_reg2 = r'(?<=href=")([^"]*?)(?=">Поіменне голосування)'
voting_link_kmel_obl_reg3 = r'(?<=href=")([^"]*?)(?=">Результати голосування)'
voting_link_kmel_obl_reg4 = r'(?<=href=")([^"]*?)(?="><u>Результати поіменного голосування)'
voting_link_kmel_obl_regs = [
        voting_link_kmel_obl_reg1,
        voting_link_kmel_obl_reg2,
        voting_link_kmel_obl_reg3,
        voting_link_kmel_obl_reg4,
]



def get_session_links(link):
    page = requests.get(link).text
    session_links_re = re.compile(session_link_khmel_obl_reg)
    links = session_links_re.findall(page)
    return links
    

def get_voting_links(session_link):
    page = requests.get(session_link).text
    for reg in voting_link_kmel_obl_regs:
        voting_links_re = re.compile(reg)
        voting_links = voting_links_re.findall(page)
        if voting_links:
            # print("Caught with:", reg)
            return voting_links
    print("Uncaught")
    return []
    

def download_files(voting_links, output_folder):
    prev = os.getcwd()
    os.chdir(output_folder)
    os.system('cd ' + output_folder)
    for link in voting_links:
        os.system('wget -m -p -E -k -K -np -nd --restrict-file-names=nocontrol ' + link)
        # os.system('curl -s -O -o ' + output_folder + ' "' + link +'"')
    os.chdir(prev)


# output_folder = '/home/sashko/Python/rada/data/khmel_obl'
# url = 'http://km-oblrada.gov.ua/rishennya-sesij/vii-sklikannya/'
# # session_link = 'http://km-oblrada.gov.ua/rishennya-sesij/vii-sklikannya/chetverta-sesiya-17-02-2016/' # get_session_links(url)
# session_links = get_session_links(url)
# for session_link in session_links:
    
#     session_folder = os.path.join(
#         output_folder,
#         session_link.split('/')[-2]
#     )

#     if not os.path.exists(session_folder):
#         os.mkdir(session_folder)
#     voting_links = get_voting_links(session_link)
#     download_files(voting_links, session_folder)
#     input("Press Enter to continue...")


















