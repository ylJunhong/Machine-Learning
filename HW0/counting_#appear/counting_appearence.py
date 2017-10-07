# By Junhong Yang
# read the words.txt file, count the number of appearance of the word and output it by this formal : <word><space><index><space><# of appearance>

with open("words.txt", 'r') as f:
    lines = f.read().split(' ')
dict_word_num = {}
for i in lines:
    if i not in dict_word_num:
        dict_word_num[i] = 1
    else:
        dict_word_num[i] += 1
b = 0
with open("output.text", 'w') as output:
    for i in dict_word_num:
        output.write(i + ' ' + str(b) + ' ' + str(dict_word_num[i]))
        output.write("\n")
        b += 1