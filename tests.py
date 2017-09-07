import unittest
from unittest import TestCase
# from main import get_names, yes_reg_exp, no_reg_exp, abstained_reg_exp, absent_reg_exp, get_rtf_files_list
# from main import get_names_kyiv, za_reg_exp, get_sirnames_kyiv_layout, has_sirname_duplicates, map_sirnames_to_pib_kyiv, get_names_kyiv_xls, get_minimal_unique_names, get_names_kyiv_layout, regs_dict_kyiv

# from main import rtf_to_txt, all_rtf_to_txt, doc_to_txt
# from main import vote_summary

from convert import get_rtf_files_list

from main import * 
from download import *
from common import *
import glob

import os 
names_kyiv = ['Бабій Ольга Андріївна', 'Багнюк Валентин Віталійович', 'Балагура Олег Вікторович', 'Бігарі Наталія Володимирівна', 'Боднар Володимир Михайлович', 'Бойко Галина Миколаївна', 'Борисенко Денис Валерійович', 'Боровська Наталя Вікторівна', 'Будюк Сергій Миколайович', 'Бунін Сергій Валерійович', 'Буковський Роман Володимирович', 'Береза Світлана Василівна', 'Волинець Олександр Леонідович', 'Глиняний Леонід Петрович', 'Горган Олександр Любомирович', 'Гринчук Віктор Васильович', 'Гунько Наталія Іванівна', 'Даниленко Анатолій Степанович', 'Дворник Микола Григорович', 'Джужик Леонід Петрович', 'Добрянський Ярослав Вікторович', 'Домбровський Ігор Ростиславович', 'Дорошенко Олексій Олександрович', 'Ерікян Давід Мартікович', 'Єрко Галина Георгіївна', 'Запаскін Максим Романович', 'Іваненко Олег Валерійович', 'Карлюк Віталій Іванович', 'Кармазін Сергій Вікторович', 'Киреєва Вікторія Станіславівна', 'Качний Олександр Сталіноленович', 'Кищук Олег Євгенович', 'Кудлай Іван Миколайович', 'Кузьменко Руслан Олександрович', 'Ксьонзенко Валерій Петрович', 'Леляк Олександр Іванович', 'Лисак Станіслав Володимирович', 'Лірник Гліб Андрійович', "Лук'яненко Мар'яна Анатоліївна", 'Луценко Віктор Миколайович', 'Ляшенко Микола Миколайович', 'Мазурко Максим Олександрович', 'Майбоженко Володимир Володимирович', 'Мороз Петро Микитови', 'Музиченко Наталія Анатоліївна', 'Нич Тимофій Михайлович', 'Нігруца Олександр Петрович', 'Одинець Владислав Іванович', 'Опенько Юрій Анатолійович', 'Павленко Олександр Іванович', 'Панченко Борис Максимович', 'Пещерін Андрій Євгенович', 'Парцхаладзе Лев Ревазович', 'Поліщук Станіслав Михайлович', 'Поляруш Олександр Олексійович', 'Сабій Ігор Михайлович', 'Світовенко Віктор Вікторович', 'Семенова Тетяна Миколаївна', 'Семеняка Микола Миколайович', 'Сімановський Олександр Володимирович', 'Сімутін Роман Вікторович', 'Сіренко Михайло Миколайович', 'Сіренко Олександр Олександрович', 'Скрипа Василь Ілліч', 'Соболєв Вячеслав Олександрович', 'Старикова Ганна Віталіївна', 'Стариченко Микола Анатолійович', 'Ступак Іван Іванович', 'Титикало Роман Сергійович', 'Тищенко Григорій Дмитрович', 'Удовиченко Володимир Петрович', 'Федорченко Сергій Миколайович', 'Фурдичка Микола Григорович', 'Хахулін Владислав Костянтинович', 'Хмельницький Вячеслав Вікторович', 'Цагареішвілі Жора', 'Цвик Василь Вікторович', 'Чубук Євген Олександрович', 'Чередніченко Юрій Анатолійович', 'Шандра Володимир Миколайович', "Шахар'янц Армен Мушегович", 'Швидкий Микола Андрійович', 'Юрович Наталія Миколаївна', 'Яременко Сергій Володимирович']

from vynnicamisto import *
import chernihivobl

from xlutils.copy import copy



class TestGetYesNames(TestCase):
    def test_get_yes(self):
        with open('test_inputs/test1.txt') as f:
            re = ['Богатирчук-Кривко Світлана Кирил', 'Васильчук Сергій Миколайович', 'Виноградова Ірина Павлівна', 'Власенко  Василь Федорович', 'Галайчук Едуард Костянтинович', 'Грещук Андрій Васильович', 'Грудницький Володимир Миколайови', 'Демчук Валентин Вікторович', 'Жаровський Михайло Богданович', 'Зелінська Лариса Володимирівна', 'Зиль Володимир Васильович', 'Карпяк Олег Віталійович', 'Керницький Олексій Богданович', 'Конощук Марія Василівна', 'Лащук Олександр Іванович', 'Максименко Тарас Анатолійович', 'Нестерук Олександр Петрович', 'Першогуба Віталій Леонтійович', 'Радько Микола Олексійович', 'Сачук Антон Олександрович', 'Сачук Олександр Миколайович', 'Сидоришин Сергій Федорович', 'Смолярчук Ольга Аркадіївна', 'Туровська Людмила Валентинівна', 'Харковець Василь Степанович', 'Хмилецький Олексій Віталійович', 'Хомко Володимир Євгенович', 'Хорхолюк Артур Володимирович', 'Чугуєвець Анатолій Олександрович', 'Шамшин Павло Володимирович']
            self.assertEqual(get_names(f,yes_reg_exp), re)


    def test_get_no(self):
        with open('test_inputs/test1.txt') as f:
            re = []
            self.assertEqual(get_names(f, no_reg_exp), re)

    def test_get_abstained(self):
      with open('test_inputs/test1.txt') as f:
          re = ['Test Name', 'Another Test Name']
          self.assertEqual(get_names(f,abstained_reg_exp), re)

    def test_get_get_absent(self):
      with open('test_inputs/test1.txt') as f:
          re = ['Паладійчук Сергій Богданович', 'Шевчук Руслан Степанович']
          self.assertEqual(get_names(f,absent_reg_exp), re)

class TestRtf(TestCase):

    def test_get_rtfs(self):
        re = ['test_inputs/s10_3.rtf', 'test_inputs/48/1.rtf', 'test_inputs/48/2.rtf', 'test_inputs/48/5.rtf', 'test_inputs/48/3.rtf', 'test_inputs/48/7.rtf', 'test_inputs/48/6.rtf', 'test_inputs/48/4.rtf', 'test_inputs/46/z3/01pytannya_iz_zauv.rtf', 'test_inputs/46/z3/2_3pytannya_na_dovyvchennya.rtf', 'test_inputs/46/z3/02pytannya.rtf']
        self.assertEqual(get_rtf_files_list('test_inputs'), re)

    # def test_rtf_to_txt(self):
    #     rtf_to_txt('test_inputs/s10_3.rtf','test_inputs/txt')

    # def test_all_rtf_to_txt(self):
    #     all_rtf_to_txt('test_inputs', 'test_inputs/txt')

class KyivOblrada(TestCase):
    
    def test_get_all_pib_from_txt(self):
        with open('test_inputs/kyiv_test.txt', 'r') as f:
            names = get_names_kyiv(f, r'(?s).*')
            self.assertEqual(len(names), 62)

    def test_get_all_pib_from_xls(self):
        file_path = 'test_inputs/kyiv_test.xls'
        names = get_names_kyiv_xls(file_path)
        self.assertEqual(len(names), 84)

    def test_no_sirname_duplicates(self):
        lst = names_kyiv
        self.assertFalse(has_sirname_duplicates(lst))

    def test_no_sirname_duplicates(self):
        lst = names_kyiv
        self.assertEqual(len(get_minimal_unique_names(lst)),len(names_kyiv))

    def test_get_za_sirnames(self):
        with open('test_inputs/kyiv_test_layout.txt', 'r') as f:
            pi = get_sirnames_kyiv_layout(f, za_reg_exp)
            pi_expected = ['Бігарі Наталія', 'Наталія Володимирівна', 'Володимирівна Бабій', 'Бабій Ольга', 'Ольга Андріївна', 'Андріївна Багнюк', 'Багнюк Валентин', 'Валентин Віталійович', 'Віталійович Балагура', 'Балагура Олег', 'Олег Вікторович', 'Вікторович Боднар', 'Боднар Володимир', 'Володимир Михайлович', 'Михайлович Бойко', 'Бойко Галина', 'Галина Миколаївна', 'Миколаївна Борисенко', 'Борисенко Денис', 'Денис Валерійович', 'Валерійович Боровська', 'Боровська Наталя', 'Наталя Вікторівна', 'Вікторівна Будюк', 'Будюк Сергій', 'Сергій Миколайович', 'Миколайович Буковський', 'Буковський Роман', 'Роман Бунін', 'Бунін Сергій', 'Сергій Валерійович', 'Валерійович Волинець', 'Волинець Олександр', 'Олександр Леонідович', 'Леонідович Володимирович', 'Володимирович Гунько', 'Гунько Наталія', 'Наталія Іванівна', 'Іванівна Даниленко', 'Даниленко Анатолій', 'Анатолій Степанович', 'Степанович Дворник', 'Дворник Микола', 'Микола Григорович', 'Григорович Добрянський', 'Добрянський Ярослав', 'Ярослав Вікторович', 'Вікторович Домбровський', 'Домбровський Ігор', 'Ігор Ростиславович', 'Ростиславович Дорошенко', 'Дорошенко Олексій', 'Олексій Ерікян', 'Ерікян Давід', 'Давід Мартікович', 'Мартікович Запаскін', 'Запаскін Максим', 'Максим Романович', 'Романович Олександрович', 'Олександрович Кармазін', 'Кармазін Сергій', 'Сергій Вікторович', 'Вікторович Киреєва', 'Киреєва Вікторія', 'Вікторія Станіславівна', 'Станіславівна Кищук', 'Кищук Олег', 'Олег Євгенович', 'Євгенович Кудлай', 'Кудлай Іван', 'Іван Миколайович', 'Миколайович Лисак', 'Лисак Станіслав', 'Станіслав Володимирович', "Володимирович Лук'яненко", "Лук'яненко Мар'яна", "'яненко Мар'яна", "яненко Мар'яна", "Мар'яна Анатоліївна", "'яна Анатоліївна", 'яна Анатоліївна', 'Анатоліївна Луценко', 'Луценко Віктор', 'Віктор Миколайович', 'Миколайович Ляшенко', 'Ляшенко Микола', 'Микола Миколайович', 'Миколайович Майбоженко', 'Майбоженко Володимир', 'Володимир Мороз', 'Мороз Петро', 'Петро Микитови', 'Микитови Нігруца', 'Нігруца Олександр', 'Олександр Петрович', 'Петрович Володимиров', 'Володимиров Нич', 'Нич Тимофій', 'Тимофій Михайлович', 'Михайлович Опенько', 'Опенько Юрій', 'Юрій Анатолійович', 'Анатолійович Павленко', 'Павленко Олександр', 'Олександр Іванович', 'Іванович Поляруш', 'Поляруш Олександр', 'Олександр Олексійович', 'Олексійович Сіренко', 'Сіренко Михайло', 'Михайло Миколайович', 'Миколайович Сабій', 'Сабій Ігор', 'Ігор Михайлович', 'Михайлович Світовенко', 'Світовенко Віктор', 'Віктор Вікторович', 'Вікторович Семеняка', 'Семеняка Микола', 'Микола Миколайович', 'Миколайович Стариченко', 'Стариченко Микола', 'Микола Анатолійович', 'Анатолійович Удовиченко', 'Удовиченко Володимир', 'Володимир Петрович', 'Петрович Хмельницький', 'Хмельницький Вячеслав', 'Вячеслав Чубук', 'Чубук Євген', 'Євген Олександрович', "Олександрович Шахар'янц", "Шахар'янц Армен", "'янц Армен", 'янц Армен', 'Армен Мушегович', 'Мушегович Вікторович', 'Вікторович Швидкий', 'Швидкий Микола', 'Микола Андрійович']
            self.assertEqual(pi, pi_expected)

    def test_map_sirnames_to_pib(self):
        xls_file_path = 'test_inputs/kyiv_test.xls'
        with open('test_inputs/kyiv_test_layout.txt', 'r') as f:
            pis = get_sirnames_kyiv_layout(f, za_reg_exp)
            pibs = get_names_kyiv_xls(xls_file_path)
            some_pibs = map_sirnames_to_pib_kyiv(pis, pibs)
            expected_some_pibs = ['Бігарі Наталія Володимирівна', 'Бабій Ольга Андріївна', 'Багнюк Валентин Віталійович', 'Балагура Олег Вікторович', 'Боднар Володимир Михайлович', 'Бойко Галина Миколаївна', 'Борисенко Денис Валерійович', 'Боровська Наталя Вікторівна', 'Будюк Сергій Миколайович', 'Буковський Роман Володимирович', 'Бунін Сергій Валерійович', 'Волинець Олександр Леонідович', 'Гунько Наталія Іванівна', 'Даниленко Анатолій Степанович', 'Дворник Микола Григорович', 'Добрянський Ярослав Вікторович', 'Домбровський Ігор Ростиславович', 'Дорошенко Олексій Олександрович', 'Ерікян Давід Мартікович', 'Запаскін Максим Романович', 'Кармазін Сергій Вікторович', 'Киреєва Вікторія Станіславівна', 'Кищук Олег Євгенович', 'Кудлай Іван Миколайович', 'Лисак Станіслав Володимирович', "Лук'яненко Мар'яна Анатоліївна", 'Луценко Віктор Миколайович', 'Ляшенко Микола Миколайович', 'Майбоженко Володимир Володимирович', 'Мороз Петро Микитови', 'Нігруца Олександр Петрович', 'Нич Тимофій Михайлович', 'Опенько Юрій Анатолійович', 'Павленко Олександр Іванович', 'Поляруш Олександр Олексійович', 'Сіренко Михайло Миколайович', 'Сабій Ігор Михайлович', 'Світовенко Віктор Вікторович', 'Семеняка Микола Миколайович', 'Стариченко Микола Анатолійович', 'Удовиченко Володимир Петрович', 'Хмельницький Вячеслав Вікторович', 'Чубук Євген Олександрович', "Шахар'янц Армен Мушегович", 'Швидкий Микола Андрійович']
            self.assertEqual(some_pibs, expected_some_pibs)
            self.assertEqual(len(some_pibs), 45)

    def test_get_names_kyiv_layout(self):
        xls_file_path = 'test_inputs/kyiv_test.xls'
        with open('test_inputs/kyiv_test_layout.txt', 'r') as f:
            self.assertEqual(len(get_names_kyiv_layout(f, xls_file_path, za_reg_exp)), 45)

    def test_get_arrival_time(self):
        xls_folder_path = 'test_inputs/kyiv_oblrada_registry_xls'
        output_file = 'arrival_kyiv.xls'
        get_arrival_time(xls_folder_path, output_file)


    def test_add_or_create_name_vote(self):
        name = "Jane Doe"
        vote = "yes"
        voters = {}
        self.assertFalse(voters)
        add_or_create_name_vote(voters, name, vote)
        self.assertEqual(voters[name][vote], 1)

class TernopilMistoTestCase(TestCase):
    def test_get_voters_one_file(self):
        file_path = 'test_inputs/ternopil_test.txt'
        voters = get_voters_ternopil(file_path)
        self.assertTrue(len(voters),43)

    def test_get_voters_all_files(self):
        files_path = '/home/sashko/Python/rada/data/ternopyl_misto'
        voters = get_voters_ternopil_all_files(files_path)
        

class UtilsTestCase(TestCase):
    def test_voters_update(self):
        voters = {'Anya':{'yes':1}}
        new_voters = {'Anya':{'yes':1,'no':1},'Hera':{'abstained':3}}
        update_voters(voters, new_voters)
        new_voters = {}
        expected_voters = {'Hera': {'abstained': 3}, 'Anya': {'yes': 2, 'no': 1}}
        self.assertEqual(voters, expected_voters)


class KhmelRegionTestCase(TestCase):
    def test_get_session_links(self):     
        url = 'http://km-oblrada.gov.ua/rishennya-sesij/vii-sklikannya/'
        links = get_session_links(url)
        self.assertEqual(len(links), 7)

    def test_get_voting_links(self):        
        session_link = 'http://km-oblrada.gov.ua/rishennya-sesij/vii-sklikannya/devyata-sesiya-23-12-2016/'
        voting_links = get_voting_links(session_link)
        self.assertEqual(len(voting_links), 78)

    # def test_download_files(self):       
    #     output_folder = 'test_outputs/khmel_obl/'
    #     session_link = 'http://km-oblrada.gov.ua/rishennya-sesij/vii-sklikannya/devyata-sesiya-23-12-2016/'
    #     voting_links = get_voting_links(session_link)
    #     os.system('rm -r ' + output_folder + '*')
    #     # download_files(voting_links, output_folder)
    #     # print(len(os.listdir(output_folder)))

    # def test_get_voters_khmel(self):
    #     file_path = 'test_inputs/khmel_obl_test.txt'
    #     get_voters_khmel(file_path)

    # def test_get_voters_khmel_all(self):
    #     get_voters_khmel_all()

    # def test_get_session_votings_count(self):
    #     path = '/home/sashko/Python/rada/data/khmel_obl/chetverta-sesiya-17-02-2016'
    #     get_session_votings_count(path)


    # def test_get_all_session_votings_count(self):
    #     path = '/home/sashko/Python/rada/data/khmel_obl/'
    #     get_all_session_votings_count(path)

    # def test_fill_registry(self):
    #     voters = get_voters_khmel()
    #     fill_registy(voters, sessions_path)

    # def test_get_voters_regisrty(self):
    #     path = '/home/sashko/Python/rada/data/khmel_obl/chetverta-sesiya-17-02-2016'
    #     get_voters_registry(path)
        


# class VynnicaTestCase(TestCase):
#     # def test_get_voters(self):
#     #     filepath = 'test_inputs/vynnica_misto.txt'
#     #     get_voters(filepath)

#     def test_get_highest_question_number(self):
#         filepath = 'test_inputs/vynnica_misto.txt'
#         self.assertEqual(get_highest_question_number(filepath), 51)

#     # def test_get_all_voters(self):
#     #     folderpath = '/home/sashko/Python/rada/data/vynnica_misto'
#     #     voters = get_all_voters(folderpath)
#     #     votings = ['ЗА','ПРОТИ','УТРИМАВСЯ', 'НЕ ГОЛОСУВАВ','відсутній']
#     #     voters_to_xls(voters, votings, 'vynnica_misto.xls')

#     def test_session_to_xls(self):
#         # inputpath = 'test_inputs/vynnica_misto.txt'
#         folderpath = '/home/sashko/Python/rada/data/vynnica_misto'
#         inputpath = '/home/sashko/Python/rada/data/vynnica_misto/Результати поіменного голосування 7 сесії 7 скликання.pdf.txt'

#         outputpath = 'test_outputs/voting_by_deputy.xls'
#         council_name = 'Вінницька міська рада'
#         convocation_number = '7'

#         # session_to_xls(
#         #         inputpath,
#         #         outputpath,
#         #         council_name,
#         #         convocation_number)


#         all_sessions_to_xls(
#                 folderpath,
#                 outputpath,
#                 council_name,
#                 convocation_number)





class ChernihivTestCase(TestCase):
    def test_get_voters(self):
        filepath = 'test_inputs/chernihivobl_test.txt'
        chernihivobl.get_voters(filepath)

    # def test_get_highest_question_number(self):
    #     filepath = 'test_inputs/vynnica_misto.txt'
    #     self.assertEqual(get_highest_question_number(filepath), 51)

    def test_get_all_voters(self):
        folderpath = '/home/sashko/Python/rada/data/chernihiv_obl'
        voters = chernihivobl.get_all_voters(folderpath)
        votings = ['ЗА','ПРОТИ','УТРИМАВСЯ', 'Не голосував']
        voters_to_xls(voters, votings, 'chernihiv_obl.xls')




if __name__ == '__main__':
    unittest.main()



