import numpy as np
from scipy import sparse
import pagerank as pr  

def transpose(a):
    """Transpose helper function for pr_matrix"""
    aT=np.array([[a[j,k] for j in range(len(a))] for k in range(len(a[0]))])
    return aT

def pr_matrix(fname, alpha):
    """Enters P entries interatively based off adj. 
        Applies formula to get pagerank matrix"""
    adj,n,names=pr.read_graph_file(fname)
    mat=np.zeros((n,n))
    #creating p
    for i in range(n):
        outs=len(adj[i])
        for j in range(outs):
            mat[i,adj[i][j]]=(1/outs)
    #transpose
    matT=transpose(mat)
    #modifying pagerank matrix
    added=((1-alpha)/4)*np.ones((n,n))
    M=np.add(matT*alpha, added)
    return M

def pr_ranking(fname, alpha):
    """Takes in file name and alpha, calling read_graph_file
        and pr_matrix to get pagerank matrix. Matrix is then
        input into ranking function. Printing function identifies
        the maximum value in ranked array, prints it in the right
        place and then sets it to zero so that it is not counted 
        again in the next iteration. Allows for tied pages. in ranking"""
        
    adj,n,names=pr.read_graph_file(fname)
    M=pr_matrix(fname, alpha)
    ranked=pr.ranking(M)
    tempcheck=np.zeros(n)
    print("___PAGE_RANKING___" )
    counter=1
    while not np.array_equal(ranked,tempcheck):
        print("{}. " .format(counter), end="")
        maxval=max(ranked)
        maxind=[i for i in range(n) if ranked[i] == maxval]
        for i in range(len(maxind)):
            print(names[maxind[i]], end="")
            ranked[maxind[i]]=0
            if i!=(len(maxind)-1):
                print(", ", end="")
        print ("") #allows to go to next line
        counter+=1
    
def sparse_matrix(adj,n):
    """Uses adj to construct sparse matrix. Input n needed to have
        record of max node which is used to determine sparse matrix size
        Iteratively, from 0 to n, function checks if key exists in adj
        and if it does will append proper data and coordinates."""
    data=[]
    r=[]
    c=[]
    #directly building tranpose matrix
    for i in range(n):
        if i in adj:
            outs=len(adj[i])
            for j in range(outs):
                data.append(1/outs)
                c.append(i) #transposed from row
                r.append(adj[i][j]) #transposed from column
    spmat=sparse.coo_matrix((data,(r,c)), shape=(n,n))
    return spmat

def sparse_ranking(fname, alpha):
    """Runs read_graph_file, sparse_matrix and ranking_sparse consecutively
        to obtain spranked array. Similar to pr_ranking, the funciton ranks
        by iteratively finding the max value in spranked, printing, then
        setting to zero. Allows for tied pages in ranking and top URL comment."""
    adj,n,names=pr.read_graph_file(fname)
    spmat=sparse_matrix(adj,n)
    spranked=pr.ranking_sparse(spmat, alpha)
    firstcheck=True
    print("_____________PAGE_RANKING_____________" )
    for k in range(5):#prints top 5 URLs
        print("{}. " .format(k+1), end="")
        maxval=max(spranked)
        maxind=[i for i in range(n) if spranked[i] == maxval]
        if firstcheck==True:
            top=[0]*len(maxind)
            for i in range(len(maxind)):
                top[i]=names[maxind[i]]
            firstcheck=False
        for i in range(len(maxind)):
            print(names[maxind[i]], end="")
            spranked[maxind[i]]=0
            if i!=(len(maxind)-1):
                print(", ", end="")
        print ("") #allows to go to next line
    if len(top)==1:
        print("The top URL is: ", end="")
    else:
        print("The top URLs are: ", end="")
    for i in range(len(top)):
        if i==0:
            print(top[i], end="")
        else:
            print(", {}" .format(top[i]), end="")

