
FILE_LL = "ll.txt"
FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"
ll_terminals=list()
ll_non_terminals=list()
is_ll_first_line=True
ll_table_dict=dict()
lr_table_dict=dict()

ll_input = []
lr_input = ""

def splitString(textToSplit,splitBy):# Split textToSplit string by splitBy list
    splitedList=list()
    while len(textToSplit) != 0:
        if textToSplit[0] in splitBy:
            splitedList.append(textToSplit[0])
            textToSplit=textToSplit[1:]
        elif textToSplit[:2] in splitBy:
            splitedList.append(textToSplit[:2])
            textToSplit=textToSplit[2:]
        elif textToSplit[:3] in splitBy:
            splitedList.append(textToSplit[:3])
            textToSplit=textToSplit[3:]
        elif textToSplit[:4] in splitBy:
            splitedList.append(textToSplit[:4])
            textToSplit=textToSplit[4:]
        elif textToSplit[:5] in splitBy:
            splitedList.append(textToSplit[:5])
            textToSplit=textToSplit[5:]

    return splitedList

def listToString(list):#convert the given list to a string
    str=""
    for i in list:
        str += i
    return str

def listToStringAmongSpace(list):#convert the given list to a string with space among each element
    str=""
    for i in list:
        str = str + i + " "
    return str

with open(FILE_LL,encoding = "utf-8") as file:
    
    for i in file:
        rows=i.split(";")
        
        temp_dict=dict()
        row_non_terminal_name=""
        for j in range(len(rows)):
            
            if is_ll_first_line :
                if j!=0:
                    ll_terminals.append(rows[j].strip())
            else:
                if j == 0:
                    row_non_terminal_name=rows[j].strip()
                    ll_non_terminals.append(row_non_terminal_name)
                else:
                    temp_dict[ll_terminals[j-1]]=rows[j].strip()
            
        if not is_ll_first_line:
            ll_table_dict[row_non_terminal_name]=temp_dict
        is_ll_first_line=False

lr_ter_and_nonter=list() 
count=0       

with open(FILE_LR,encoding = "utf-8") as file:
    
    for i in file:
        rows=i.split(";")

        temp_dict = dict()
        if count ==1:
            for j in rows:
                lr_ter_and_nonter.append(j.strip())
                
        elif count >= 2:
            state_name=""
            for j in range(len(rows)):
                if j == 0:
                    state_name=rows[j].strip()
                else:
                    temp_dict[lr_ter_and_nonter[j]]=rows[j].strip()

            lr_table_dict[state_name]=temp_dict

        count +=1       
    


def calculateLL(ll_input):
    count=1

    print("\n\nProcessing input string "+listToString(ll_input)+"  for LL(1) parsing table.\n\n")
    
    print("NO  | STACK      | INPUT          | ACTION")           
    ll_stack = []
    ll_stack.append('$')

    action=list(ll_table_dict.values())[0][ll_input[0]]
    if action == "":
        message="REJECTED ("+list(ll_table_dict.keys())[0]+" does not have an action/step for "+ll_input[0]+")"
        print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),message))
        return 

    #LL process    
    
    print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),action))

    while not (ll_stack[-1] == '$' and ll_input[0] == '$'):
        
        count += 1

        
        
        splitActionBy=ll_non_terminals+ll_terminals+["ϵ"]

        splitedAction=splitString(action.split("->")[1],splitActionBy)# get right hand side of action
        
        while len(splitedAction) > 0:# push element of right hand side of action
            if splitedAction[-1] != "ϵ":
                ll_stack.append(splitedAction[-1])
            del splitedAction[-1]

        if ll_stack[-1] == ll_input[0]: # 
            
            
            print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),"Match and remove "+ll_stack[-1]))#new
            count += 1

            del ll_stack[-1]
            del ll_input[0]

            # new action that the value where the last element of the stack in the table and the first element of the input intersect
            action=ll_table_dict[ll_stack[-1]][ll_input[0]] 

            if action == "":
                message="REJECTED ("+ll_stack[-1]+" does not have an action/step for "+ll_input[0]+" )"
                print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),message))
                return
            
            print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),action))
            

            if "->" in action and action.split("->")[1] == "ϵ":
                del ll_stack[-1] # if new action contains ϵ then pop stact again 
                # new action that the value where the last element of the stack in the table and the first element of the input intersect
                action=ll_table_dict[ll_stack[-1]][ll_input[0]]
                count +=1
                print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),action))

            del ll_stack[-1]
                
        else:
            # new action that the value where the last element of the stack in the table and the first element of the input intersect
            action=ll_table_dict[ll_stack[-1]][ll_input[0]]

            

            
            
            print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),action))
            del ll_stack[-1]

        if ll_stack[-1] == '$' and ll_input[0] == '$':#finish control
            count += 1
            print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),"ACCEPT"))
            break





        if action == "":
            message="REJECTED ("+ll_stack[-1]+" does not have an action/step for "+ll_input[0]+" )"
            print("{:<3} | {:<10} | {:>14} | {:<10}".format(str(count), listToString(ll_stack),listToString(ll_input),message))
            return

#LR process
def calculateLR(lr_input):
    print("\n\nProcessing input string "+listToString(lr_input) +" for LR(1) parsing table.\n\n")
    lr_process_dict=dict()

    lr_process_dict[""]="State_1"

    print("NO  | STATE STACK | READ   | INPUT    | ACTION")
    no=0

    read=''
    
    action=""
    input_split_index = 0

    splited_lr_input=splitString(lr_input,lr_ter_and_nonter)

    action=list(lr_table_dict.values())[0][splited_lr_input[0]]
    if action == "":

        message="REJECTED (State 1 does not have an action/step for "+splited_lr_input[0]+")"
        print("{:<3} | {:<11} | {:<5}  | {:>8} | {:<10}".format(str(no), str(1),splited_lr_input[0],listToString(splited_lr_input),message))
        return

    str_input=""
    while True:

        
        
        no += 1


        
        
        lr_process_dict_list=list(lr_process_dict.values())
        
        read=splited_lr_input[input_split_index]
        

        table_result=lr_table_dict[lr_process_dict_list[-1]][read]

        if table_result == "":

            message="REJECTED ( "+lr_process_dict_list[-1]+" does not have an action/step for "+splited_lr_input[0]+")"
            print("{:<3} | {:<11} | {:<5}  | {:>8} | {:<10}".format(str(no), str(1),splited_lr_input[-2],listToString(splited_lr_input),message))
            return

        lr_state_list=list(lr_process_dict.values())
        if len(lr_state_list) > 0:
            for i in range(len(lr_state_list)):
                lr_state_list[i] = lr_state_list[i][-1]

        if table_result.startswith("State"):
            if splited_lr_input[input_split_index+1] =="$":
                action="Change to "+table_result
            else:
                action="Shift to "+table_result

            lr_process_dict[splited_lr_input[input_split_index]]=table_result
            input_split_index += 1
            str_input=listToString(splited_lr_input)
        
        elif table_result == "Accept":# finish control
            print("{:<3} | {:<11} | {:<5}  | {:>8} | {:<10}".format(str(no), listToStringAmongSpace(lr_state_list),read,listToString(splited_lr_input),"Accept"))
            break

        else:
            action = "Reverse " +table_result
            rule=table_result.split("->")
            splited_rule_right_side=splitString(rule[1],lr_ter_and_nonter)# get right side of state

            deleted_count =0
            str_input=listToString(splited_lr_input)
            while len(splited_rule_right_side) > 0:
                
                if splited_rule_right_side[-1] == splited_lr_input[-2]:
                    del lr_process_dict[splited_rule_right_side[-1]]
                    del splited_rule_right_side[-1]
                    del splited_lr_input[-2]
                    deleted_count += 1
                else:
                    print("REJECTED THE RULE "+splited_rule_right_side[-1] +" DOES NOT MATCH WITH "+splited_lr_input[-2])
                    return

            splited_lr_input= splited_lr_input[:-1] + [rule[0]] + splited_lr_input[-1:]
            
            input_split_index -= deleted_count
            
        print("{:<3} | {:<11} | {:<5}  | {:>8} | {:<10}".format(str(no), listToStringAmongSpace(lr_state_list),read,str_input,action))

print("Read LL(1) parsing table from file "+FILE_LL)
print("Read LR(1) parsing table from file "+FILE_LR)
print("Read input strings from file"+FILE_INPUT)

with open(FILE_INPUT,encoding = "utf-8") as file:
    for i in file:
        rows=i.split(";")
        for j in range(len(rows)):
            if rows[j].strip()=="LL":
                
                ll_input=splitString(rows[1].strip(),ll_terminals)
                try:
                    calculateLL(ll_input)
                except:
                    print("REJECTED")
                

            elif rows[j].strip()=="LR":
                lr_input=rows[1].strip()
                try:
                    calculateLR(lr_input)
                except:
                    print("REJECTED")
                
