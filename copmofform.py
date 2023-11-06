import re
from sentence_transformers import util
import pymorphy2
from torch import Tensor
from flashtext import KeywordProcessor


Synonyms = {
    "испытание": ["тестирование", "проведение испытание", "натурные испытания"],
    "сбор данные": ["сбор информация"],
    "управление": ["управлять"],
    "метод": ["методика", "способ", "методология", "технология", "средство"],
    "бд": ["субд"],
    "программный продукт": ["программный обеспечение", "программный проект"],
    "программный система": ["интегрированный программный обеспечение"],
    "проверка": ["верификация"],
    "тестирование по": ["тестирование разработать по"],
    "ведение переговоры": ["проведение переговоры"],
    "управление проект": ["проектный управление", "менеджмент проект"],
    "правовой акт": ["локальный правовой акт", "нормативный правовой акт"],
    "отношение": ["взаимоотношение"],

    "использовать": ["применять"],
    "оценивать": ["производить оценка", "проводить оценка"],
    "анализировать риск": ["оценивать риск"],
    "проводить ": ["выполнять", "осуществлять", "производить", "осуществление"],
    "проводить интервью": ["проводить интервьюирование"],
    "входной дать": ["входной информация"],
    "составлять": ["подготавливать", "pазрабатывать", "документировать"],
    "документ": ["документация"],
    "выполнение": ["исполнение"],
    "строить прогноз": ["составлять прогноз"],
    "опрашивать": ["проводить опрос"],
    "контроль": ["контролировать"],
    "система управление версия": ["система контроль версия"],
    "безопасность информация": ["информационный безопасность"],
    "по": [" программного обеспечения"],
    "инфокоммуникационный": ["информационно коммуникационный"],
    "автоматизированный система": ["ИАС"],
    "понятие": ["содержание понятие"],
    "к файл и папка": ["на файл и папка"],
    "действовать стандарт": ["современный стандарт"],
    "локализовать": ["локализовывать"],
    "на основа": ["с использование"],
    "находить": ["вести поиск"]
}


class Comparison_Of_Formulations:
    def __init__(self, formulations1: dict[str, Tensor] = None, formulations2: dict[str, Tensor] = None):
        self._cos_const = 0.95
        self._keyword_processor = KeywordProcessor()
        self._keyword_processor.add_keywords_from_dict(Synonyms)
        self._morph = pymorphy2.MorphAnalyzer()
        if formulations1 is None:
            self.formulations1 = {}
        else:
            self.formulations1 = formulations1
        if formulations2 is None:
            self.formulations2 = {}
        else:
            self.formulations2 = formulations2

    def update_formulations(self, formulations1: dict[str, Tensor], formulations2: dict[str, Tensor]):
        self.formulations1 = formulations1
        self.formulations2 = formulations2

    def find_similar_formulationsV1(self, formulations1: dict[str, Tensor] = None,
                                    formulations2: dict[str, Tensor] = None) -> [list[dict[str, str], list[str]]]:
        if formulations1 is None:
            if self.formulations1 == {}:
                raise ValueError('Missing argument: formulations1 is None')
            else:
                formulations1 = self.formulations1
        if formulations2 is None:
            if self.formulations2 == {}:
                raise ValueError('Missing argument: formulations2 is None')
            else:
                formulations2 = self.formulations2

        similar_formulations: list[tuple[str, str]] = []
        identical_formulations, repeats = [], []
        for formulation1 in formulations1.keys():
            for formulation2 in formulations2.keys():
                if formulation1 != formulation2:
                    lemmas_formulations12 = self.__preprocessing([formulation1, formulation2])
                    value1 = self.__Jacquard(lemmas_formulations12[0], lemmas_formulations12[1])
                    if value1 == 1 and formulation1 not in identical_formulations and \
                            formulation2 not in identical_formulations and formulation1 not in repeats\
                            and formulation2 not in repeats:
                        identical_formulations.append(formulation1)
                        repeats.append(formulation1)
                        repeats.append(formulation2)
                        continue
                    value2 = round(
                        util.cos_sim(a=formulations1[formulation1], b=formulations2[formulation2]).item(), 2)
                    if value2 >= self._cos_const:
                        if self.__subset_check(lemmas_formulations12):
                            similar_formulations.append((formulation1, formulation2))
                        else:
                            _formulation1 = self._keyword_processor.replace_keywords(
                                ' '.join(lemmas_formulations12[0]))
                            _formulation2 = self._keyword_processor.replace_keywords(
                                ' '.join(lemmas_formulations12[1]))
                            if self.__subset_check([_formulation1.split(" "), _formulation2.split(" ")]):
                                similar_formulations.append((formulation1, formulation2))
                else:
                    if formulation1 not in identical_formulations and formulation1 not in repeats:
                        identical_formulations.append(formulation1)
        update_similar_formulations = self._get_similar_formulations(similar_formulations, identical_formulations)
        return update_similar_formulations, identical_formulations

    def find_similar_formulationsV2(self, formulation: str, formulations: list[str]) -> list[str]:
        similar_formulations = []
        for formulation2 in formulations:
            lemmas_formulations12 = self.__preprocessing([formulation, formulation2])
            if self.__subset_check(lemmas_formulations12):
                similar_formulations.append(formulation2)
            else:
                _formulation1 = self._keyword_processor.replace_keywords(
                    ' '.join(lemmas_formulations12[0]))
                _formulation2 = self._keyword_processor.replace_keywords(
                    ' '.join(lemmas_formulations12[1]))
                if self.__subset_check([_formulation1.split(" "), _formulation2.split(" ")]):
                    similar_formulations.append(formulation2)
        return similar_formulations

    @staticmethod
    def __Jacquard(formulations1: list[str], formulations2: list[str]) -> float:
        formulations1 = set(formulations1)
        shared = formulations1.intersection(formulations2)
        total = formulations1.union(formulations2)
        return len(shared) / len(total)

    def __preprocessing(self, formulations: list[str]) -> list[list[str]]:
        bad_words = ["и"]
        new_data = []
        for form in formulations:
            sent_lemmas = []
            words = re.findall(r'\w+|\d+', form)
            for word in words:
                lemmas = self._morph.normal_forms(word[0:len(word)])
                if lemmas[0] not in bad_words:
                    sent_lemmas.append(lemmas[0])
            new_data.append(sent_lemmas)
        return new_data

    @staticmethod
    def __subset_check(formulations) -> bool:
        if len(formulations[1]) > len(formulations[0]):
            formulation1, formulation2 = formulations[0], formulations[1]
        else:
            formulation1, formulation2 = formulations[1], formulations[0]
        for formulation in formulation1:
            if formulation not in formulation2:
                return False
        return True

    @staticmethod
    def _get_similar_formulations(formulations: list[tuple[str, str]],
                                  identical_formulations: list[str]) -> list[dict[str, str]]:
        new_formulations = []
        for formulation12 in formulations:
            if formulation12[0] not in identical_formulations and formulation12[1] not in identical_formulations:
                new_formulations.append({"form1": formulation12[0], "form2": formulation12[1]})
        return new_formulations
