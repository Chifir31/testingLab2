import json
import os
import unittest
import profstandard as ps
from torch import empty
from copmofform import Comparison_Of_Formulations
import warnings

TESTDATA_FILENAME1 = os.path.join(os.path.dirname(__file__), 'test_docs/comparison_of_formulation_test.json')
TESTDATA_FILENAME2 = os.path.join(os.path.dirname(__file__), 'test_docs/prof_standard_test.json')
TESTDATA_FILENAME3 = os.path.join(os.path.dirname(__file__), 'test_docs/06.001.docx')


class CompOfFormTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        with open(TESTDATA_FILENAME1) as f:
            templates = json.load(f)
        cls.true_s = templates['true_s']
        cls.true_i = templates['true_i']
        cls.f1 = templates['f1']
        cls.f2 = templates['f2']
        cls.compOfForm = Comparison_Of_Formulations({}, {})

    def test__init__(self):
        cof = Comparison_Of_Formulations()
        self.assertEqual(cof.formulations1, {})
        self.assertEqual(cof.formulations2, {})

    def test_find_similar_formulationsV1(self):
        self.compOfForm.update_formulations({}, {})
        with self.assertRaises(ValueError):
            self.compOfForm.find_similar_formulationsV1()
        v1 = empty(1, 2)
        self.compOfForm.update_formulations({"формулировка1": v1}, {})
        with self.assertRaises(ValueError):
            self.compOfForm.find_similar_formulationsV1()

        self.compOfForm.update_formulations(self.f2, self.f1)
        s, i = self.compOfForm.find_similar_formulationsV1()
        self.assertEqual(i, self.true_i)
        self.assertEqual(s, self.true_s)

    def test_find_similar_formulationsV2(self):
        s = self.compOfForm.find_similar_formulationsV2("Методы коммуникаций",
                                                        ["Методы коммуникации и что-то там еще",
                                                         "Средства коммуникаций и что-то там еще",
                                                         "Языки программирования"])
        self.assertEqual(s, ["Методы коммуникации и что-то там еще", "Средства коммуникаций и что-то там еще"])


class ProfStandardTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = ps.Professional_Standard(TESTDATA_FILENAME3)
        with open(TESTDATA_FILENAME2, 'r') as f:
            templates = json.load(f)
        cls.gen_labor_funcs = templates['gen_labor_func']
        cls.professions = templates['professions']
        cls.labor_action = templates['labor_actions']
        cls.knowledge = templates['knowledge']
        cls.skills = templates['skills']
        cls.knowledge_embeddings = templates['knowledge_embeddings']
        cls.skills_embeddings = templates['skills_embeddings']

    def test_set_prof_standard_name(self):
        self.assertEqual(self.p.get_prof_standard_name(), "Программист")

    def test_set_prof_standard_kod(self):
        self.assertEqual(self.p.get_prof_standard_kod(), "06.001")

    def test_set_prof_standard_reg_num(self):
        self.assertEqual(self.p.get_prof_standard_reg_name(), "4")

    def test_set_gen_labor_funcs(self):
        self.assertEqual(self.p.get_gen_labor_funcs(), self.gen_labor_funcs)

    def test_set_other_params(self):
        self.assertEqual(self.p.get_professions(), self.professions)
        self.assertEqual(self.p.get_labor_actions(), self.labor_action)
        self.assertEqual(self.p.get_knowledge(), self.knowledge)
        self.assertEqual(self.p.get_skills(), self.skills)

    def test_get_embeddings(self):
        self.assertEqual(len(self.p.get_knowledge_with_embeddings()), len(self.knowledge_embeddings))
        self.assertEqual(len(self.p.get_skills_with_embeddings()), len(self.skills_embeddings))


class IntegrationTestsCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = ps.Professional_Standard(TESTDATA_FILENAME3)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        cls.cof = Comparison_Of_Formulations()

    def test_find_similar_formulationsV1(self):
        res = self.cof.find_similar_formulationsV1(self.p.get_knowledge_with_embeddings(),
                                                   self.p.get_knowledge_with_embeddings())
        self.assertEqual(len(res[0]), 0)
        self.assertNotEqual(len(res[1]), 0)

        res = self.cof.find_similar_formulationsV1(self.p.get_skills_with_embeddings(),
                                                   self.p.get_skills_with_embeddings())
        self.assertEqual(len(res[0]), 0)
        self.assertNotEqual(len(res[1]), 0)

    def test_find_similar_formulationsV2(self):
        res = self.cof.find_similar_formulationsV2('Языки программирования',
                                                   self.p.get_knowledge())
        self.assertNotEqual(len(res), 0)

        res1 = self.cof.find_similar_formulationsV2('Осуществлять коммуникации',
                                                    self.p.get_skills())
        self.assertEqual(len(res1), 0)


if __name__ == '__main__':
    unittest.main()
