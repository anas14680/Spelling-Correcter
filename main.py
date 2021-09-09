import re
import numpy as np
 
##### MY CODE STARTS

with open("austen-sense-corrupted.txt") as f:
    para = f.read()                             ##opens the corrupted file

with open("/Users/mohammadanas/Desktop/Duke MIDS/Fall 2021/NLP/Assignment 2/dictionary.txt") as f:
    dict_list=[]
    for line in f:
        dict_list.append(line.strip())        ##took the dictionary and created a list of it


 
 

pattern = re.compile('\W?(\w*[-]?\w*)(\W?)').  ##define a parttern of regex to extract the words from a word
                                                ## group1 extracts word and group2 extracts anything after like ", or ."

def w_char(pattern, text):
    for i in re.finditer(pattern, text):
        return i.group(1)
    
def r_char(pattern, text):
    for i in re.finditer(pattern, text):
        return i.group(2)
    

def lev_dis(target, source):                  ## defines levensthein distance
    target = '@' + target
    source = '@' + source
    lst_target = [k for k in target]
    lst_source = [k for k in source]
    arr = np.zeros((len(source), len(target)))
    arr[0] = [i for i in range(len(lst_target))]
    arr[:,0] = [j for j in range(len(lst_source))]
    
    if target[1] != source[1]:
        arr[1,1] = 1
    for col in range(1, len(target)):
        for row in range(1, len(source)):


            if target[col] != source[row]:
                arr[row, col] = min(arr[row-1,col],arr[row,col -1],arr[row-1,col-1]) + 1 

            else:
                arr[row, col] = arr[row-1, col-1]

    return int(arr[-1,-1])




def correcter(text):                                            


    tok_lst = text.split()   ## split the list into words


    final_lst = []

    for i in tok_lst:
        word = w_char(pattern, i)
        lower_word = word.lower()
        
        if word not in dict_list:
            dist = []

            for j in dict_list:
                dist.append(lev_dis(j,lower_word))
            index = dist.index(min(dist))
            if word[0].isupper():
                final_lst.append(dict_list[index].capitalize())            ## this chunk of code works on creating a new list to put the correct words either from 
            else:                                                          ## dictionary or from the text itself. This code does not change the capitalization of words
                final_lst.append(dict_list[index])                         ## insted it check the lower case of each word
                
        
        elif lower_word in dict_list:
            final_lst.append(word)


    punc_lst = []                                                           ## creates a list of punctutation marks with the same length as the previous one
    for i in tok_lst:
        puc = r_char(pattern, i)
        punc_lst.append(puc)


    for i in range(len(punc_lst)):                                          ## adds punctuation marks back to the list in the same order
        if len(punc_lst[i]) > 0:
            final_lst[i] = final_lst[i] + punc_lst[i]

    final_text = ''
    for i in final_lst:
        final_text = final_text + i + ' '                                  ## makes the text out of that list and returns that.

    final_text = final_text[:-1]

    return final_text


