import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import math,csv
import scipy

semcor_ic = wordnet_ic.ic('ic-semcor.dat')

def sim_lin(syns1,syns2):
    maxSim=None
    for s1 in syns1:
        for s2 in syns2:
            sim=s1.lin_similarity(s2,semcor_ic)
            if maxSim==None or maxSim<sim:
                maxSim=sim
    return maxSim

def sim_resnik(syns1,syns2):
    maxSim=None
    for s1 in syns1:
        for s2 in syns2:
            sim=s1.res_similarity(s2,semcor_ic)
            if maxSim==None or maxSim<sim:
                maxSim=sim
    return maxSim

train = csv.reader(open("combined.csv",'rb'))

word1=[]
word2=[]
hr=[]
LinS=[]

for row in train:
    word1.append(row[0])
    word2.append(row[1])
    hr.append(row[2])

#f=open("SemcorIC.txt","w")

for i in range(1,len(hr)):
    a=wn.synsets(word1[i],pos="n")
    b=wn.synsets(word2[i],pos="n")
    LinS.append(sim_lin(a,b))
    #f.write("%s\t%s\t%.5s\t%.5s\t%.5s\n"%(word1[i],word2[i],sim_lin(a,b),sim_resnik(a,b),hr[i]))

#f.close()
hr.pop(0)
print scipy.stats.spearmanr(LinS,hr)