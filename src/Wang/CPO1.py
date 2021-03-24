import copy
class Hashdic:
    def __init__(self,Hashcode=1024):
        self.code=Hashcode
        self.key=[-1 for i in range(self.code)]
        self.value=[-1 for i in range(self.code)]
        self.size=0

    def __eq__(self, other):
        if other is None:
            return False
        for x in range(0,len(self.key)):
            if self.key[x]==-1:
                if self.key[x] != other.key[x]:
                    return False
                if self.value[x]!= other.value[x]:
                    return False
            else:
                if self.key[x][0] != other.key[x][0]:
                    return False
                if self.value[x][0] != other.value[x][0]:
                    return False


        return True

def cons(Hd, key,value):
    new=Hashdic()
    new.size=Hd.size
    k=int(key) % new.code
    for x in range(0,len(Hd.key)):
        new.key[x]=Hd.key[x]
        new.value[x]=Hd.value[x]
    if key==None:
        print("key cant be NULL")
        return new
    if new.key[k]==-1:
        new.key[k]=[key,-1]
        new.value[k] = [value, -1]
        new.size += 1
    else:
        temp=new.key[k]
        tempv=new.value[k]
        if temp[0]==key:
            tempv[0]=value
        else:
            while temp[1] != -1:

                temp = temp[1]
                tempv = tempv[1]
                if temp[0] == key:
                    tempv[0] = value
                    break
            temp[1] = [key, -1]
            tempv[1] = [value, -1]
            new.size+=1
    return new

def remove(Hd, key):
    if not key:
        print("NULL")
        return -1
    new=Hashdic()
    new.size = Hd.size
    k=int(key) % new.code
    for x in range(0,len(Hd.key)):
        new.key[x]=Hd.key[x]
        new.value[x]=Hd.value[x]
    if key==None:
        print("key cant be NULL")
        return new
    if new.key[k]==-1:
        print("now such key")
    else:
        temp=new.key[k]
        tempv=new.value[k]
        if temp[0]==key:
            new.key[k]=-1
            new.value[k]=-1
            new.size -= 1
        else:
            while temp[1] != -1:

                btemp = temp[1]
                btempv = tempv[1]
                if btemp[0] == key:
                    temp[1]=btemp[1]
                    tempv[1]=btempv[1]
                    new.size -= 1
                    break
                else:
                    temp=btemp
                    tempv=btempv
    return new

def size(Hd):
    if Hd:
        return Hd.size
    else:
        return -1



def to_list(h):
    outlist=[]
    if not h:
        return outlist
    for i in range(0,len(h.key)):
        if h.key[i]==-1:
            continue
        else:
            temp=h.key[i]
            tempv=h.value[i]
            outlist.append([temp[0],tempv[0]])
            while temp[1]!=-1:
                temp=temp[1]
                tempv=tempv[1]
                outlist.append([temp[0], tempv[0]])
    return outlist

def from_list(list):
    p=Hashdic()

    for st in list:
        if len(st)<2:
            return -1
        p=cons(p,st[0],st[1])

    return  p


def find(mp,key):
    if not key:
        return -1
    fin=key%mp.code
    find=0
    if mp.key[fin] == -1:
        print("no such value")
        return -1
    else:
        temp=mp.key[fin]
        tempv=mp.value[fin]
        if temp[0]==key:
            return [temp[0],tempv[0]]
        while temp[1]!=-1:
            temp=temp[1]
            tempv=tempv[1]
            if temp[0] == key:
                return [temp[0], tempv[0]]
    print("no such value")
    return -1

def mempty(h):
    return Hashdic()


def mconcat(a,b):
    if not a and not b:
        return None
    new = Hashdic()
    if not a:
        new.size = b.size
        for x in range(0, len(b.key)):
            new.key[x] = b.key[x]
            new.value[x] = b.value[x]
        return new
    elif not b:
        new.size = a.size
        for x in range(0, len(a.key)):
            new.key[x] = a.key[x]
            new.value[x] = a.value[x]
        return new
    else:
        list=to_list(b)
        for st in list:
            a=cons(a,st[0],st[1])

        return a

def iterator(hp):
    iterator_list=[]
    for i in range(0, len(hp.key)):
        if hp.key[i] == -1:
            continue
        else:
            temp = hp.key[i]
            tempv = hp.value[i]
            iterator_list.append([temp[0], tempv[0]])
            while temp[1] != -1:
                temp = temp[1]
    na=0
    def next():
        nonlocal na
        t=na
        na=na+1
        if t>=len(iterator_list):
            return -1
        return iterator_list[t]
    return next

def map(a,f):
    new = Hashdic()
    new.size = a.size
    for x in range(0, len(a.key)):
        new.key[x] = a.key[x]
        new.value[x] = a.value[x]

    for i in range(0, len(new.key)):
        if new.key[i] == -1:
            continue
        else:
            temp = new.key[i]
            tempv = new.value[i]
            tempv[0]=f(tempv[0])
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                tempv[0]=f(tempv[0])

    return new


def add(a):
    return a + 1

def reduce(a,f,state):
    instate=state
    for i in range(0, len(a.key)):
        if a.key[i] == -1:
            continue
        else:
            temp = a.key[i]
            tempv = a.value[i]
            instate=f(tempv[0],instate)
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                tempv[0]=f(tempv[0])
                instate = f(tempv[0], instate)
    return instate

def filter(a,is_even):
    result=[]
    for i in range(0, len(a.key)):
        if a.key[i] == -1:
            continue
        else:
            temp = a.key[i]
            tempv = a.value[i]
            if is_even and tempv[0]%2==0:
                result.append([temp[0],tempv[0]])
            elif not is_even and tempv[0]%2==1:
                result.append([temp[0], tempv[0]])

            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                if is_even and tempv[0] % 2 ==0:
                    result.append([temp[0], tempv[0]])
                elif not is_even and tempv[0] % 2 == 1:
                    result.append([temp[0], tempv[0]])
    return result


p=Hashdic()
p=cons(p,1,5)
p=cons(p,1025,6)
p=cons(p,2049,9)
map(p,add)
lc= to_list(p)
print(to_list(p))
p=from_list(lc)
p=remove(p,1025)




