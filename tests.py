import unittest
from unittest import TestCase
from main import get_names, yes_reg_exp, no_reg_exp, abstained_reg_exp, absent_reg_exp, get_rtf_files_list
from main import rtf_to_txt, all_rtf_to_txt
from main import vote_summary


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

class VoteSummary(TestCase):

    def test_vote_summary(self):
        vote_summary('test_inputs/txt')




if __name__ == '__main__':
    unittest.main()

