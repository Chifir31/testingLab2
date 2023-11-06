import os
from copmofform import Comparison_Of_Formulations
import profstandard as ps


if __name__ == '__main__':
    cof = Comparison_Of_Formulations()
    docs = os.listdir(path='doc', )
    start = 1
    for i in range(0, len(docs) - 1):
        if not docs[i].endswith('.docx'):
            print("{} is not a docx file".format(docs[i]))
            start += 1
            continue
        for j in range(start, len(docs)):
            if not docs[j].endswith('.docx'):
                print("{} is not a docx file".format(docs[j]))
                continue
            print("{}-{}".format(docs[i], docs[j]))
            p1 = ps.Professional_Standard('doc/' + docs[i])
            p2 = ps.Professional_Standard('doc/' + docs[j])
            s, ii = cof.find_similar_formulationsV1(p1.get_knowledge_with_embeddings(),
                                                    p2.get_knowledge_with_embeddings())

            if len(s) != 0:
                print("similar knowledge:")
                for ss in s:
                    print("\t{} - {}".format(ss['form1'], ss['form2']))
            else:
                print("No found similar knowledge")

            if len(ii) != 0:
                print("identical knowledge:")
                for i1 in ii:
                    print("\t", i1)
            else:
                print("No found identical knowledge")
            s, ii = cof.find_similar_formulationsV1(p1.get_skills_with_embeddings(),
                                                    p2.get_skills_with_embeddings())

            if len(s) != 0:
                print("similar skills:")
                for ss in s:
                    print("\t{} - {}".format(ss['form1'], ss['form2']))
            else:
                print("No found similar skills")
            if len(ii) != 0:
                print("identical skills:")
                for i1 in ii:
                    print("\t", i1)
            else:
                print("No found identical skills")
        start += 1
