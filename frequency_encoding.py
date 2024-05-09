from math import ceil
from math import floor

import pandas as pd



def check_type(variable):
    if isinstance(variable, (int, float)):
        return "Number"
    elif isinstance(variable, str):
        return "String"
    else:
        return "Other type"


def frequency_encoding(data):
    bits=3
    encoder=['000','001','011','111']
    for col in data:
        if(check_type(data[col][0])=="Number"):
            col_arr=[]
            for element in data[col].values():
                col_arr.append(element)
            col_arr.sort()
            t=int(len(col_arr)/(bits+1))
            r=len(col_arr)%(bits+1)
            index_map={}
            j=0
            for i in range(len(col_arr)):
                if (i+1)%t==0:
                    index_map[col_arr[i]]=j
                    j+=1
                    j=min(j,3)
                else:
                    index_map[col_arr[i]]=j
            for i,(key,value) in enumerate(data[col].items()):
                temp=encoder[index_map[value]]
                data[col][i]=temp           

    return data        
