# -*- coding: utf-8 -*-
import glob,os
import fnmatch
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import shutil
from sklearn.externals import joblib

arr_dados = []
arr_categoria = []
for arquivo in glob.iglob('C:\\armador\\faturamento\\*.txt'):
    caminho_arquivo = arquivo
    open_arq = open(caminho_arquivo,'r+')
    conteudo = unicode(open_arq.read(), errors='replace')
    arr_dados.append(conteudo)
    arr_categoria.append(1)

    open_arq.close()

for arquivo in glob.iglob('C:\\armador\\erros\\*.txt'):
    caminho_arquivo = arquivo
    open_arq = open(caminho_arquivo, 'r+')
    conteudo = unicode(open_arq.read(), errors='replace')
    arr_dados.append(conteudo)
    arr_categoria.append(0)

    open_arq.close()


# vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.8, stop_words=None)
vectorizer = TfidfVectorizer(analyzer='char_wb', sublinear_tf=False, max_df=0.8, stop_words=None)
treino_vetorizado = vectorizer.fit_transform(arr_dados)


tf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=False, smooth_idf=False).fit(treino_vetorizado)
X_train_tf = tf_transformer.transform(treino_vetorizado)

# clf = MultinomialNB().fit(treino_vetorizado, arr_categoria)
clf = MultinomialNB().fit(X_train_tf, arr_categoria)
# clf = SVC().fit(treino_vetorizado, arr_categoria)
# clf = SVC().fit(X_train_tf, arr_categoria)

joblib.dump(clf,'c:\\armador\\faturamento.pkl')

arr_descobrir = []

matches = []
for root, dirnames, filenames in os.walk('W:\\'):
    for filename in fnmatch.filter(filenames, '*.txt'):
        matches.append(os.path.join(root, filename))

for root, dirnames, filenames in os.walk('Y:\\'):
    for filename in fnmatch.filter(filenames, '*.txt'):
        matches.append(os.path.join(root, filename))

joblib.dump(matches,'c:\\armador\\arr_faturamento.pkl')

# matches = joblib.load('c:\\armador\\arr_faturamento.pkl')

for arquivo in matches:
    caminho_arquivo = arquivo
    open_arq = open(caminho_arquivo, 'r+')

    conteudo = unicode(open_arq.read(), errors='replace')
    arr_descobrir.append(conteudo)

    open_arq.close()
    X_new_counts = vectorizer.transform(arr_descobrir)
    X_new_tfidf = tf_transformer.transform(X_new_counts)
    print arquivo
    pred = clf.predict(X_new_tfidf)
    print(pred)
    if pred[0]==1:
        shutil.copy2(caminho_arquivo,"C:\\armador\\arq\\")
    arr_descobrir = []
