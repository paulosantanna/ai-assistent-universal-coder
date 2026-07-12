import math,re
from collections import Counter
from dataclasses import dataclass
TOKEN_RE=re.compile(r"\b\w+\b",re.UNICODE)
def tokenize(text:str)->list[str]: return [t.lower() for t in TOKEN_RE.findall(text)]
@dataclass
class BM25Index:
    documents:list[str]; k1:float=1.5; b:float=.75
    def __post_init__(self):
        self.tokens=[tokenize(d) for d in self.documents]; self.lengths=[len(x) for x in self.tokens]
        self.avgdl=sum(self.lengths)/max(len(self.lengths),1); self.df=Counter()
        for x in self.tokens:self.df.update(set(x))
    def score(self,q:str,i:int)->float:
        terms=tokenize(q); tokens=self.tokens[i]; f=Counter(tokens); dl=self.lengths[i]; n=len(self.documents); s=0.
        for term in terms:
            df=self.df.get(term,0); idf=math.log(1+(n-df+.5)/(df+.5)); tf=f.get(term,0)
            den=tf+self.k1*(1-self.b+self.b*dl/max(self.avgdl,1e-9)); s+=idf*(tf*(self.k1+1))/max(den,1e-9)
        return s
    def search(self,q:str,top_k:int=5): return sorted([(i,self.score(q,i)) for i in range(len(self.documents))],key=lambda x:x[1],reverse=True)[:top_k]
