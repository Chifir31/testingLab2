import json
import os

from copmofform import Comparison_Of_Formulations
import profstandard as ps


if __name__ == '__main__':
    cof = Comparison_Of_Formulations()
    docs = os.listdir(path='doc', )
    true_i = ['Языки, утилиты и среды программирования и средства пакетного выполнения процедур', 'Модели коммуникаций']
    print()

