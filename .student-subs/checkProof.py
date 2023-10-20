# import re
import sys

rules = []
propositions = []
inputs = []
result = []
assumption_dict = {}

def scope_copy(curr_line, line1):
    ass_box = -1
    l1 = False
    for key in assumption_dict:
        for val in assumption_dict[key]:
            if(key <= curr_line <= val):
                ass_box = key
            if(key <= line1 <= val):
                l1 = True

    #Case 1 : current line is in some assumption box
    if(ass_box != -1):
        if( not l1 ):
            return True
        elif( l1):
            for key in assumption_dict:
                for val in assumption_dict[key]:
                    if(key <= line1 <= val and ( curr_line < key and curr_line > val)):
                        return False
    # Case 2: current line is outside assumption box
    else:
        for key in assumption_dict:
            for val in assumption_dict[key]:
                if(key <= line1 <= val):
                    return False
    return True


def check_scope(curr_line, line1, line2):
    
    ass_box = -1
    l1 = False
    l2 = False
    for key in assumption_dict:
        for val in assumption_dict[key]:
            if(key <= curr_line <= val):
                ass_box = key
            if(key <= line1 <= val):
                l1 = True
            if(key <= line2 <= val):
                l2 = True

    #Case 1 : current line is in some assumption box
    #If the two lines are in some assumption box, they must be in the same box
    # Note that we have the outermost nested box first in the list
    if(ass_box != -1):
        if( not l1 and not l2 ):
            return True
        elif( not l1  and l2):
            for key in assumption_dict:
                for val in assumption_dict[key]:
                    if(key <= line2 <= val and ( curr_line < key and curr_line > val)):
                        return False
        elif( not l2 and l1):
            for key in assumption_dict:
                for val in assumption_dict[key]:
                    if(key <= line1 <= val and ( curr_line < key and curr_line > val)):
                        return False
        elif( l1 and l2):
            for key in assumption_dict:
                for val in assumption_dict[key]:
                    if(key <= line1 <= val and ( curr_line < key and curr_line > val)):
                        return False
                    if(key <= line2 <= val and ( curr_line < key and curr_line > val)):
                        return False
    # Case 2: current line is outside assumption box
    else:
        for key in assumption_dict:
            for val in assumption_dict[key]:
                if(key <= line1 <= val or key <= line2 <= val):
                    return False
    return True


def check_lem(proposition):

    size = (len(proposition) - 7)//2
    clause = proposition[1:size+1]
    res = "(" + clause + "\\/" + "(" + "!" + clause + ")" + ")"
    # print(res)
    if(res!=proposition):
        return False
    return True
    
def check_mp(line1, line2, ans):

    prop1 = propositions[line1] #p
    prop2 = propositions[line2] #p ->q
    index = prop2.find(prop1)
    # Checking first term
    if(index != 1 or prop2[index:index+len(prop1)] != prop1):
        return False
    # print(prop2[index:index+len(prop1)])
    # print(prop2[3+len(prop1):-1])
    # Checking the second term
    if(prop2[3+len(prop1):-1] != ans):
        return False
    res = "(" + prop2[index:index+len(prop1)] + "->" + ans + ")"
    # Checking implication sign
    if(res != prop2):
        return False
    return True
    
def check_mt(line1, line2, ans):

    prop1 = propositions[line1] #p -> q
    prop2 = propositions[line2] #!q
    comp = prop2[2:-1]
    # print(prop1[-1-len(comp):-1])
    # print(prop1[-3-len(comp):-1-len(comp)])
    if(prop1[-1-len(comp):-1] != comp or prop1[-3-len(comp):-1-len(comp)] != "->"):
        return False
    res = "(" + "!" + prop1[1:-3-len(comp)] + ")"
    # print(res)
    if(res != ans):
        return False
    return True


def check_or_el(line1, line2, line3, line4, line5, ans):
    prop1 = propositions[line2]
    prop2 = propositions[line4]
    prop = propositions[line1]
    res = "(" + prop1 + "\\/" + prop2 + ")"
    if(res != prop):
        return False
    if(propositions[line3] != propositions[line5]):
        return False
    if(rules[line2] != "[assumption]" or rules[line4] != "[assumption]"):
        return False
    if(ans != propositions[line3]):
        return False
    return True


def check_and_in(line1, line2, ans):

    prop1 = propositions[line1]
    prop2 = propositions[line2]
    res = "(" + prop1 + "/\\" + prop2 + ")"
    # print(res)
    if(res != ans): 
        return False
    return True
    
def check_and_e1(line1, ans):

    prop1 = propositions[line1]
    index = prop1.find(ans)
    if(index != 1):
        return False
    if(prop1[1:1+len(ans)] != ans):
        return False
    if(prop1[1+len(ans):3+len(ans)] != "/\\"):
        return False
    return True
    
def check_and_e2(line1, ans):

    prop1 = propositions[line1]
    index = -1 - len(ans)
    # print(prop1[index:-1])
    if(prop1[index:-1] != ans or prop1[index-2:index] != "/\\"):
        return False
    return True
    
    
def check_or_i1(line1, ans):

    prop1 = propositions[line1]
    comp = "(" + prop1 + "\\/"
    # print(ans[0:3+len(prop1)])
    if(ans[0:3+len(prop1)] != comp):
        return False
    return True
    
def check_or_i2(line1, ans):

    prop1 = propositions[line1]
    comp = "\\/" + prop1 + ")"
    # print(ans[-3-len(prop1):])
    if(ans[-3-len(prop1):] != comp):
        return False
    return True
    
def check_dneg_in(line1, ans):
    prop1 = propositions[line1]
    res = "(" + "!" + "(" + "!" + prop1 + ")" + ")"
    # print(res)
    if(res != ans):
        return False
    return True
    
def check_dneg_el(line1, ans):
    prop1 = propositions[line1]
    if(prop1[4:-2] != ans):
        return False
    return True
    
def check_imp_in(line1, line2, ans):
    if(rules[line1] != "[assumption]"):
        return False
    if(rules[line2] == "[assumption]"):
        return False
    prop1 = propositions[line1]
    prop2 = propositions[line2]
    comp = "(" + prop1 + "->" + prop2 + ")"
    if(comp != ans):
        return False
    return True
    
def check_neg_in(line1, line2, ans):

    prop2 = propositions[line2]

    # \bot denotes bottom operator i.e contradiction
    if(rules[line1] != "[assumption]" or prop2 != "\\bot"):
        return False
    if(rules[line2] == "[assumption]"):
        return False
    prop1 = propositions[line1]
    res = "(" + "!" + prop1 + ")"
    if(res != ans):
        return False
    return True
    
def check_neg_el(line1, line2, ans):

    prop1 = propositions[line1]
    prop2 = propositions[line2]
    if(ans != "\\bot"):
        return False
    res = "(" + "!" + prop1 + ")"
    if(res != prop2):
        return False
    return True

def check_bot_el(line1, ans):

    prop1 = propositions[line1]
    if(prop1 != "\\bot"):
        return False
    return True
    
def check_pbc(line1, line2, ans):
    prop1 = propositions[line1]
    prop2 = propositions[line2]
    if(rules[line1] != "[assumption]"):
        return False
    if(rules[line2] == "[assumption]"):
        return False
    if(prop2 != "\\bot"):
        return False
    if(prop1[2:-1] != ans):
        return False
    


def checkProof(filename):
    # Reading the input file and storing the rules and propositional logic formulas in lists
    line_index = -1
    with open(filename, 'r') as file:
        # Read the file line by line
        first_line = file.readline()
        clause = first_line.split("|-")
        final = clause[-1].replace("\n","")
        result.append(final.replace(" ",""))
        clause.pop()

        # Storing the premises
        for expression in clause:
            premises = expression.split(',')
            for premise in premises:
                if(premise != ' '):
                    inputs.append(premise.replace(" ",""))
        # Iterating over the proof
        for line in file:
            # Split the line into words using whitespace as the delimiter
            words = line.split("]")
            # print(words)
            # Iterate through the words and process them as needed
            for word in words:
                word = word.split('\n')
                for w in word:
                    if(w != ''):
                        if(w[0] == '['):
                            rule = w + ']'
                            # print(line_index)
                            # print(rule)
                            if(rule == "[assumption]"):
                                assumption_dict[line_index] = []
                            if(rule[0:8] == "[impl-in"):
                                lines = rule[9:-1]
                                line_nums = lines.split('-')
                                line1 = int(line_nums[0].replace(" ","")) - 3
                                line2 = int(line_nums[1].replace(" ","")) - 3
                                # if(assumption_dict[line1] == -1):
                                #     assumption_dict[line1] = line2
                                # else:
                                #     return "incorrect"
                                if line1 in assumption_dict:
                                    assumption_dict[line1].append(line2)
                                else:
                                    return "incorrect"
                            if(rule[0:6] == "[or-el"):
                                lines = rule[7:-1]
                                line_nums = lines.split(',')
                                para1 = line_nums[1].split('-')
                                para2 = line_nums[2].split('-')
                                line2 = int(para1[0].replace(" ","")) - 3
                                line3 = int(para1[1].replace(" ","")) - 3
                                line4 = int(para2[0].replace(" ","")) - 3
                                line5 = int(para2[1].replace(" ","")) - 3
                                # if(assumption_dict[line2] == -1):
                                #     assumption_dict[line2] = line3
                                # else:
                                #     return "incorrect"
                                if line2 in assumption_dict:
                                    assumption_dict[line2].append(line3)
                                else:
                                    return "incorrect"
                                # if(assumption_dict[line4] == -1):
                                #     assumption_dict[line4] = line5
                                # else:
                                #     return "incorrect"
                                if line4 in assumption_dict:
                                    assumption_dict[line4].append(line5)
                                else:
                                    return "incorrect"
                            if(rule[0:7] == "[neg-in"):
                                lines = rule[8:-1]
                                line_nums = lines.split('-')
                                line1 = int(line_nums[0].replace(" ","")) - 3
                                line2 = int(line_nums[1].replace(" ","")) - 3
                                if line1 in assumption_dict:
                                    assumption_dict[line1].append(line2)
                                else:
                                    return "incorrect"
                                # if(assumption_dict[line1] == -1):
                                #     assumption_dict[line1] = line2
                                # else:
                                #     return "incorrect"
                            if(rule[0:4] == "[pbc"):
                                lines = rule[5:-1]
                                line_nums = lines.split('-')
                                line1 = int(line_nums[0].replace(" ","")) - 3
                                line2 = int(line_nums[1].replace(" ","")) - 3
                                if line1 in assumption_dict:
                                    assumption_dict[line1].append(line2)
                                else:
                                    return "incorrect"
                                # if(assumption_dict[line1] == -1):
                                #     assumption_dict[line1] = line2
                                # else:
                                #     return "incorrect"
                            # print(rule)
                            rules.append(rule)
                        else:
                            w = w.replace(" ","")
                            if(w != ""):
                                propositions.append(w)
            line_index+=1
        for key in assumption_dict:
            if(assumption_dict[key] == []):
                # print("incorrect")
                # return -1
                return "incorrect"
        # print(inputs)
        # print(rules)
        # print(result)
        # print(propositions)
        # print(assumption_dict)

    if(propositions[-1] != result[0]):
        return "incorrect"
    # flag = True
    for i in range(len(rules)):
        # print(i)
        if(rules[i] == "[premise]"):
            if propositions[i] not in inputs:
                return "incorrect"
        elif(rules[i]=="[assumption]"):
            # Should not assume the result
            # if(propositions[i] == result[0]):
            #     return "incorrect" 
            pass
        elif(rules[i][0:5]=="[copy"):
            # rule is of the form [copy i] where i is the line number
            # line number is as in the text file, we want list index
            line_num = int(rules[i].split()[1][:-1]) - 3
            if(line_num >= i):
                return "incorrect"
            # print(line_num)
            if(propositions[line_num] != propositions[i]):
               return "incorrect"
            if(not scope_copy(i, line_num)):
                return "incorrect"
        elif(rules[i] == "[lem]"):
            if(not check_lem(propositions[i])):
                return "incorrect"
        elif(rules[i][0:3] == "[mp"):
            # rule is of the form [mp i, j]
            lines = rules[i][4:-1]
            line_nums = lines.split(',')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i):
                return "incorrect"
            if(check_scope(i, line1, line2)):
                if(not check_mp(line1, line2, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:3] == "[mt"):
            # rule is of the form [mt i, j]
            lines = rules[i][4:-1]
            line_nums = lines.split(',')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i):
                return "incorrect"
            if(check_scope(i, line1, line2)):
                if(not check_mt(line1, line2, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:7] == "[and-in"):
            lines = rules[i][8:-1]
            line_nums = lines.split(',')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i):
                return "incorrect"
            if(check_scope(i, line1, line2)):
                if(not check_and_in(line1, line2, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:7] == "[and-e1"):
            line1 = int(rules[i][8:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_and_e1(line1, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:7] == "[and-e2"):
            line1 = int(rules[i][8:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_and_e2(line1, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:7] == "[or-in1"):
            line1 = int(rules[i][8:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_or_i1(line1, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:7] == "[or-in2"):
            line1 = int(rules[i][8:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_or_i2(line1, propositions[i]) ):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:8] == "[dneg-in"):
            line1 = int(rules[i][9:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_dneg_in(line1, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:8] == "[dneg-el"):
            line1 = int(rules[i][9:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_dneg_el(line1, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:8] == "[impl-in"):
            lines = rules[i][9:-1]
            line_nums = lines.split('-')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i or line2 < line1):
                return "incorrect"
            if(not check_imp_in(line1, line2, propositions[i])):
                return "incorrect"
        elif(rules[i][0:7] == "[neg-in"):
            lines = rules[i][8:-1]
            line_nums = lines.split('-')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i or line2 < line1):
                return "incorrect"
            if(not check_neg_in(line1, line2, propositions[i])):
                return "incorrect"
        elif(rules[i][0:7] == "[neg-el"):
            lines = rules[i][8:-1]
            line_nums = lines.split(',')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i ):
                return "incorrect"
            if(check_scope(i, line1, line2)):
                if(not check_neg_el(line1, line2, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:7] == "[bot-el"):
            line1 = int(rules[i][8:-1]) - 3 
            if(line1 >= i):
                return "incorrect"
            if(check_scope(i, line1, line1)):
                if(not check_bot_el(line1, propositions[i])):
                    return "incorrect"
            else:
                return "incorrect"
        elif(rules[i][0:4] == "[pbc"):
            lines = rules[i][5:-1]
            line_nums = lines.split('-')
            line1 = int(line_nums[0].replace(" ","")) - 3
            line2 = int(line_nums[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i or line2 < line1):
                return "incorrect"
            if(not check_pbc(line1, line2, propositions[i])):
                return "incorrect"
        elif(rules[i][0:6] == "[or-el"):
            lines = rules[i][7:-1]
            line_nums = lines.split(',')
            line1 = int(line_nums[0].replace(" ","")) - 3
            para1 = line_nums[1].split('-')
            para2 = line_nums[2].split('-')
            line2 = int(para1[0].replace(" ","")) - 3
            line3 = int(para1[1].replace(" ","")) - 3
            line4 = int(para2[0].replace(" ","")) - 3
            line5 = int(para2[1].replace(" ","")) - 3
            if(line1 >= i or line2 >= i or line3 >= i or line4 >= i or line5 >= i):
                return "incorrect"
            if(not check_or_el(line1, line2, line3, line4, line5, propositions[i])):
                return "incorrect"
        else:
            return "incorrect"
        
    return "correct"

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        result = checkProof(filename)
        print(result)
    else:
        print("No command-line argument provided.")
            
if __name__ == "__main__":
    main()
                        