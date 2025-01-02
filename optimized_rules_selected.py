import random
def solve(number, rulenumber):
    if ((1 << number) & rulenumber) > 0:
        return 1
    return 0

m = {
    0: [(12, 1), (3, 1), (6, 3), (9, 3)],
    1: [(204, 1), (51, 1),(85, 2),(54, 5),(57, 5), (99, 5), (108, 5), (147, 5), (156, 5), (198, 5), (201, 5)],
    2: [(15, 1)],
    3: [ (204, 1), (85, 2), (27, 5),(39, 5), (78, 5), (114, 5), (141, 5), (177, 5), (216, 5), (228, 5)],
    5: [(51, 1), (204, 1), (85, 2)]
   
}

training_data={
    '0000':1,
    '1111':0,
    '0010':1,
    '0001':0,
    '0011':1,
    '0100':0, 
    '0101':1,
    '0111':0
}

endround = {
    1: [ 20, 65, 68],
    2: [5, 20, 65, 80],
    3: [5, 68, 80],
    4: [20, 65],
    5: [ 68],
    
}

def rule_to_binary(rule, num_states):
    return format(rule, '0' + str(num_states**3) + 'b')

def evolve_cell(left, center, right, rule_number):
    index = int(str(left)+str(center)+str(right), 2)
    if((1<<index)&rule_number)>0:
        return '1'
    return '0'

def evolve_ca(row, rule_numbers):
    num_cells = len(row)
    next_row =""

    for i in range(num_cells):
        if(i-1<0):
            left=0
        else:
            left = int(row[(i - 1) % num_cells])
        center = int(row[i])
        if(i+1==num_cells):
            right=0
        else:
            right = int(row[(i + 1) % num_cells])
        next_row+= evolve_cell(left, center, right, rule_numbers[i])
    return next_row

def binary_to_decimal(binary):
    decimal=int(binary,2)
    return decimal

def decimal_to_binary(number,n):
    binary=bin(number)
    binary=binary[2:]
    if len(binary) is not n:
        for i in range(n-len(binary)):
            binary='0'+binary
    return binary

def binatodeci(binary):
    return int(binary,2)

def generate_ca(number, rule_numbers, all_numbers,n):
    initial_row=decimal_to_binary(number,n)
    ca_history = [initial_row]
    # print(initial_row)
    s=set()
    all_numbers[number]=1
    while True:
        new_row = evolve_ca(ca_history[-1], rule_numbers)
        # print(new_row)
        if new_row in s:
            return -1
        if new_row==initial_row:
            ca_history.append(new_row)
            break
        s.add(new_row)
        ca_history.append(new_row)
        # print(new_row)
        number=binatodeci(new_row)
        all_numbers[number]=1
    return ca_history

def get_index(arr):
    return arr[1]

def classification(data,testing_data,n):
    t=2**n
    max_rule_number=[]
    max_ans=0
    #for times in range(10000):
    while(max_ans<0.90):
        rule_numbers=[] 
        # [10, 180, 197, 90, 165, 165, 195, 172, 150, 204, 106, 5]
        initial_class=0
        for i in range(n-1):
            random_num=random.choice(m[initial_class])
            rule_numbers.append(random_num[0])
            initial_class=random_num[1]

        random_num=random.choice(endround[initial_class])
        rule_numbers.append(random_num) 

        all_numbers=[0]*t
        ca_history=[]
        for i in range(t):
            if(all_numbers[i]==0):
                history = generate_ca(i, rule_numbers,all_numbers,n)
                ca_history.append(history)
                if history==-1:
                    ca_history=[]
                    break
        
        map_to_cycle={}

        # print(ca_history)
        xor_values_for_each_cycle=[]
        for i in range(len(ca_history)):
            xor_label_index_dict=[]
            xor_a=0
            for j in range(len(ca_history[i])):
                num=binary_to_decimal(ca_history[i][j])
                xor_a=xor_a^num
                map_to_cycle[ca_history[i][j]]=i
            xor_label_index_dict.append(i)
            xor_label_index_dict.append(xor_a)
            xor_values_for_each_cycle.append(xor_label_index_dict)
        # print(1)


        count_majority_for_each_cycle={}
        for i in range(len(ca_history)):
            count_majority_for_each_cycle[i]=[0,0,0]
        for i,(key,value) in enumerate(data.items()):
            cycle_index=map_to_cycle[key]
            count_majority_for_each_cycle[cycle_index][value]+=1
        
        cycle_label={}
        for i,(key,value) in enumerate(count_majority_for_each_cycle.items()):
            label=value.index(max(value))
            c=0
            for j in range(len(value)):
                if (value[label]==value[j]):    
                    c+=1
            if c>1:
                cycle_label[i]=3
                xor_values_for_each_cycle[i].append(3)
            else:
                cycle_label[i]=label
                xor_values_for_each_cycle[i].append(label)


        sorted_array=sorted(xor_values_for_each_cycle,key=get_index)
        # for i in range(len(sorted_array)):
        #     print(sorted_array[i][1])
        # print(sorted_array)

        gap_index_arr=[]
        gap_index_arr.append(0)
        curr_diff=sorted_array[1][1]-sorted_array[0][1]
        for i in range(2,len(sorted_array),1):
            if curr_diff==0:
                curr_diff=sorted_array[i][1]-sorted_array[i-1][1]
            elif sorted_array[i][1]-sorted_array[i-1][1]>10*curr_diff:
                gap_index_arr.append(i)
                curr_diff=0
                continue
            curr_diff=sorted_array[i][1]-sorted_array[i-1][1]
        
        gap_index_arr.append(len(sorted_array))

        # print(gap_index_arr)
        # print(sorted_array)

        j=1
        label_0=0
        label_1=0
        label_2=0
        for i in range(len(sorted_array)+1):
            if i==gap_index_arr[j]:
                max_val=max(label_0,label_1,label_2)
                label_0=0
                label_1=0
                label_2=0
                for k in range(gap_index_arr[j-1],gap_index_arr[j],1):
                    if sorted_array[k][2]==3:
                        # sorted_array[k][2]=max_val
                        if max_val==label_0:
                            cycle_label[sorted_array[k][0]]=0
                            sorted_array[k][2]=0
                        elif max_val==label_1:
                            cycle_label[sorted_array[k][0]]=1
                            sorted_array[k][2]=1
                        else:
                            cycle_label[sorted_array[k][0]]=2
                            sorted_array[k][2]=2
                        # print(cycle_label[sorted_array[k][0]],sorted_array[k][0])   
                j+=1

           
            if i<len(sorted_array):
                if sorted_array[i][2]==0:
                    label_0+=1
                elif sorted_array[i][2]==1:
                    label_1+=1
                elif sorted_array[i][2]==2:
                    label_2+=1
             
        # print(cycle_label)
        count=0
        for i,(key,value) in enumerate(testing_data.items()):
            cycle_index=map_to_cycle[key]
            label=cycle_label[cycle_index]
            if value==label:
                count+=1
            # else:
            #     print(value,label,count_majority_for_each_cycle[cycle_index])
        
        accuracy=count/len(testing_data)
        print(accuracy)
        if(accuracy>max_ans):
            max_ans=accuracy
            max_rule_number=rule_numbers
            # if (accuracy>0.96):
            #     break

        
    print(max_rule_number)
    return max_ans