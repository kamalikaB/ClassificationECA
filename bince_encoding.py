
data={
    'Age':{0:10,1:20,2:25,3:35}
}
from math import ceil
from math import floor

def decimal_to_binary(number,n):
    binary=bin(number)
    binary=binary[2:]
    if len(binary) is not n:
        for i in range(n-len(binary)):
            binary='0'+binary
    return binary

def check_type(variable):
    if isinstance(variable, (int, float)):
        return "Number"
    elif isinstance(variable, str):
        return "String"
    else:
        return "Other type"


def bince_encoding(data):
    bits=3
    for col in data:
        if(check_type(data[col][0])=="Number"):
            max_element=0
            min_element=10000000
            for element in data[col].values():
                max_element=max(max_element,element)
                min_element=min(min_element,element)
            range1=max_element-min_element
            range_array=[]
            index=0
            for item in data[col].values():
                item=(item-min_element)/range1
                item=ceil(item*(2**bits))-1
                item=max(0,item)
                item=decimal_to_binary(item,bits)
                data[col][index]=item
                index=index+1
    return data        


