[![Automated tests](https://github.com/Chifir31/testingLab2/actions/workflows/run_tests.yml/badge.svg)](https://github.com/Chifir31/testingLab2/actions/workflows/run_tests.yml)
# testingLab2
Класс <b>Professional_Standard</b> предназначен для обработки *docx*-файлов профессиональных стандартов.

Класс <b>Comparison_Of_Formulations</b> предназначен для нахождения схожих формулировок необходимых знаний или умений. 

# План тестирования
## Аттестационное тестирование
**Тест А1 (положительный)**
- Начальное состояние: В каталог *doc* загружены docx-файлы профессиональных стандартов (ПС), которые содержат схожие и идентичные необходимые знания и умения.
- Действие: Пользователь запускает программу.
- Ожидаемый результат: Программа вывела названия файлов сравниваемых ПС, список схожих и идентичных формулировок необходимых знаний, список схожих и идентичных формулировок необходимых умений.

**Тест А2 (положительный)**
- Начальное состояние: В каталог *doc* загружены docx-файлы профессиональных стандартов (ПС), которые не содержат схожие и идентичные необходимые знания и умения.
- Действие: Пользователь запускает программу.
- Ожидаемый результат: 
```
06.015.docx-06.016.docx
No found similar knowledge
No found identical knowledge
No found similar skills
No found identical skills
```

**Тест А3 (положительный)**
- Начальное состояние: В каталог *doc* загружены не *docx*-файл.
- Действие: Пользователь запускает программу.
- Ожидаемый результат: 
```
01.txt is not a docx file
07.json is not a docx file
```

## Блочное тестирование

## Класс Comparison_Of_Formulations

**Тест Б1 (положительный)**
- Описание: Проверка корректности метода-инициализатора.
- Метод: *\_\_init\_\_*.
- Входные данные: Отсутстувуют.
- Ожидаемый результат: Создан экземпляр класса, где свойства класса *formulations1* и *formulations2* равны {}.

**Тест Б2 (положительный)**
- Описание: Создан экземпляр класса, свойства класса *formulations1* и *formulations2* равны {}. Проверка корректности работы метода.
- Метод: *find_similar_formulationsV1()*.
- Входные данные: Отсутствуют.
- Ожидаемый результат: *ValueError*.

**Тест Б3 (положительный)**
- Описание: Создан экземпляр класса, свойства класса *formulations1* и *formulations2* равны {}. Проверка корректности работы метода.
- Метод: *find_similar_formulationsV1()*.
- Входные данные: *formulations1* = {"формулировка 1": *torch.empty(1, 2)*}, *formulations2* = {}
- Ожидаемый результат: *ValueError*.

**Тест Б4 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *find_similar_formulationsV1()*.
- Входные данные: *formulations1* = *f1*, *formulations2* = *f2*. [1] 
- Ожидаемый результат: Результат работы метода должен совпадать со значениями переменных *true_s*, *true_i*.[2]

[1] Значения переменных *f1* и *f2* содержатся в файле *comparison_of_formulation_test.json* под ключами *'f1'*, *'f2'*.

[2] Значения переменных *true_s* и *true_i* содержатся в файле *comparison_of_formulation_test.json* под ключами *'true_s'*, *'true_i'*. 

**Тест Б5 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *find_similar_formulationsV2()*.
- Входные данные: *formulation* = "Методы коммуникаций", *formulations* = ["Методы коммуникации и что-то там еще", "Средства коммуникаций и что-то там еще", "Языки программирования"]. 
- Ожидаемый результат: Метод должен вернуть список схожих формулировок.
```
["Методы коммуникации и что-то там еще", "Средства коммуникаций и что-то там еще"]
```

## Класс Professional_Standard
**Тест Б1 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *\_\_set_prof_standard_name()*.
- Входные данные: *docx* файл профессионального стандарта. 
- Ожидаемый результат: Значение свойства класса *\_\_prof_standard_name* равно "Программист".

**Тест Б2 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *\_\_set_prof_standard_kod()*.
- Входные данные: docx файл профессионального стандарта. 
- Ожидаемый результат: Значение свойства класса *\_\_prof_standard_kod* равно "06.001".

**Тест Б3 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *\_\_set_prof_standard_kod()*.
- Входные данные: docx файл профессионального стандарта. 
- Ожидаемый результат: Значение свойства класса *\_\_prof_standard_reg_num* равно "4".

**Тест Б4 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *\_\_set_gen_labor_funcs()*.
- Входные данные: docx файл профессионального стандарта. 
- Ожидаемый результат: Значение свойства класса *\_\_gen_labor_funcs* равно значению *gen_labor_funcs*[1].

[1] Значение переменной *gen_labor_funcs* хранится в файле *prof_standard_test.json* под ключом *'gen_labor_funcs'*.


**Тест Б5 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *\_\_set_other_params()*.
- Входные данные: docx файл профессионального стандарта. 
- Ожидаемый результат: Значение свойства класса *__professions* равно значению *professions*[1]. Значение свойства класса *__labor_action* равно значению *labor_action*[2]. Значение свойства класса *__knowledge* равно значению *knowledge*[3]. Значение свойства класса *__skills* равно значению *skills*[4].

[1] Значение переменной *professions* хранится в файле *prof_standard_test.json* под ключом *'professions'*.

[2] Значение переменной *labor_action* хранится в файле *prof_standard_test.json* под ключом *'labor_action'*.

[3] Значение переменной *knowledge* хранится в файле *prof_standard_test.json* под ключом *'knowledge'*.

[4] Значение переменной *skills* хранится в файле *prof_standard_test.json* под ключом *'skills'*.

**Тест Б6 (положительный)**
- Описание: Проверка корректности работы метода.
- Метод: *_get_embeddings()*.
- Входные данные: docx файл профессионального стандарта. 
- Ожидаемый результат: Значение свойства класса *__knowledge_embeddings* равно значению *knowledge_embeddings*[1]. Значение свойства класса *__skills_embeddings* равно значению *skills_embeddings*[2].

[1] Значение переменной *knowledge_embeddings* хранится в файле *prof_standard_test.json* под ключом *'knowledge_embeddings'*.

[2] Значение переменной *skills_embeddings* хранится в файле *prof_standard_test.json* под ключом *'skills_embeddings'*.

## Интеграционное тестирование
**Тест И1 (положительный)**
- Взаимодействие классов: *Comparison_Of_Formulations*, *Professional_Standard*.
- Описание: Тест проверяет, что свойство *__knowledge_embeddings* класса *Professional_Standard* подходит в качестве исходных данных для метода *find_similar_formulationsV1()  класса *Comparison_Of_Formulations**.
- Метод: *find_similar_formulationsV1()*.
- Входные данные: *formulations1* = *Professional_Standard.get_knowledge_with_embeddings*, *formulations2* = *Professional_Standard.get_knowledge_with_embeddings*.
- Ожидаемый результат: Списки схожих и идентичных формулировок.

**Тест И2 (положительный)**
- Взаимодействие классов: *Comparison_Of_Formulations*, *Professional_Standard*.
- Описание: Тест проверяет, что свойство *__skills_embeddings* класса *Professional_Standard* подходит в качестве исходных данных для метода *find_similar_formulationsV1()* класса *Comparison_Of_Formulations*.
- Метод: *find_similar_formulationsV1()*.
- Входные данные: *formulations1* = *Professional_Standard.get_skills_with_embeddings*, *formulations2* = *Professional_Standard.get_skills_with_embeddings*.
- Ожидаемый результат: Списки схожих и идентичных формулировок.

**Тест И3 (положительный)**
- Взаимодействие классов: *Comparison_Of_Formulations*, *Professional_Standard*.
- Описание: Тест проверяет, что свойство *__knowledges* класса *Professional_Standard* подходит в качестве исходных данных для метода *find_similar_formulationsV2()* класса *Comparison_Of_Formulations*.
- Метод: *find_similar_formulationsV2()*.
- Входные данные: *formulation* = "Языки программирования", *formulations* =  *Professional_Standard.get_knowledges()*.
- Ожидаемый результат: Список схожих формулировок.

**Тест И4 (положительный)**
- Взаимодействие классов: *Comparison_Of_Formulations*, *Professional_Standard*.
- Описание: Тест проверяет, что свойство *__skills* класса *Professional_Standard* подходит в качестве исходных данных для метода *find_similar_formulationsV2()* класса *Comparison_Of_Formulations*.
- Метод: *find_similar_formulationsV2()*.
- Входные данные: *formulation* = "Осуществлять коммуникации ", *formulations* =  *Professional_Standard.get_skills()*.
- Ожидаемый результат: Список схожих формулировок.
