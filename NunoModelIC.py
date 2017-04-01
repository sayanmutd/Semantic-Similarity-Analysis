from nltk.corpus import wordnet as wn
import math,csv,Hyponym
import scipy

global node_max

node_max=206941

def hypernym_paths(c):
    paths=[]
    k=0
    a=[]
    hypernyms = c.hypernyms() + c.instance_hypernyms()
    if len(hypernyms) == 0:
        paths = [c]
    for hypernym in hypernyms:
        for ancestor_list in hypernym.hypernym_paths():
            ancestor_list.append(c)
            paths.append(ancestor_list)
            k=k+1
    for i in range(0,k):
        for j in paths[i]:
            a.append(j)
    return a

def LCS(a,b):
    dpt=-1
    it2=0
    it1=0
    item=''
    for i in range(0,len(a)):
        for j in range(0,len(b)):
            for i1 in hypernym_paths(a[i]):
                for i2 in hypernym_paths(b[j]):
                    if i1==i2:
                        if len(hypernym_paths(i1))>dpt:
                            dpt=len(hypernym_paths(i1))
                            item=i1
                            it1=i
                            it2=j             
    return item,a[it1],b[it2]
                
def IC(a):
    if (Hyponym.hyponym_paths(a))==[]:
        return 1-(math.log10(1)/math.log10(node_max))
    return 1-(math.log10(len(Hyponym.hyponym_paths(a)))/math.log10(node_max))
    
def Prob(a):
    if (Hyponym.hyponym_paths(a))==[]:
        return 1-(math.log10(1)/math.log10(node_max))
    return (math.log10(len(Hyponym.hyponym_paths(a))+1)/math.log10(node_max+1))
    """(1/(1-(math.log10(len(Hyponym.hyponym_paths(a))+2)/math.log10(node_max+1))))
    """

def Lin_Sim(item,it1,it2):
    return 2*IC(item)/(IC(it1)+IC(it2))

def Res_Sim(item):
    return IC(item)

train = csv.reader(open("rg.csv",'rb'),delimiter=';')

word1=[]
word2=[]
hr=[]
LinS=[]

for row in train:
    word1.append(row[0])
    word2.append(row[1])
    hr.append(row[2])    

#f=open("NunoModel.txt","w")

for i in range(1,len(hr)):
    a=wn.synsets(word1[i])
    b=wn.synsets(word2[i])
    [item,it1,it2]=LCS(a,b)
    LinS.append(Res_Sim(item))
    #print Prob(item),Lin_Sim(item,it1,it2)
    #f.write("%s\t%s\t%.5s\t%.5s\t%.5s\n"%(word1[i],word2[i],Lin_Sim(item,it1,it2),Res_Sim(item),hr[i]))
    
#f.close()
hr.pop(0)    
#print len(LinS), len(hr1)
print scipy.stats.spearmanr(LinS,hr)
