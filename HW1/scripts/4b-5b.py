import numpy as np
import matplotlib.pyplot as plt
msg = "Лапин Алексей Александрович"
x_standard = []

ch_dict = {
    "А": 192,
    "Б": 193,
    "В": 194,
    "Г": 195,
    "Д": 196,
    "Е": 197,
    "Ж": 198,
    "З": 199,
    "И": 200,
    "Й": 201,
    "К": 202,
    "Л": 203,
    "М": 204,
    "Н": 205,
    "О": 206,
    "П": 207,
    "Р": 208,
    "С": 209,
    "Т": 210,
    "У": 211,
    "Ф": 212,
    "Х": 213,
    "Ц": 214,
    "Ч": 215,
    "Ш": 216,
    "Щ": 217,
    "Ъ": 218,
    "Ы": 219,
    "Ь": 220,
    "Э": 221,
    "Ю": 222,
    "Я": 223,
    "а": 224,
    "б": 225,
    "в": 226,
    "г": 227,
    "д": 228,
    "е": 229,
    "ж": 230,
    "з": 231,
    "и": 232,
    "й": 233,
    "к": 234,
    "л": 235,
    "м": 236,
    "н": 237,
    "о": 238,
    "п": 239,
    "р": 240,
    "с": 241,
    "т": 242,
    "у": 243,
    "ф": 244,
    "х": 245,
    "ц": 246,
    "ч": 247,
    "ш": 248,
    "щ": 249,
    "ъ": 250,
    "ы": 251,
    "ь": 252,
    "э": 253,
    "ю": 254,
    "я": 255,
    " ": 32,
}

encoding = {
    '0000': '11110',
    '0001': '01001',
    '0010': '10100',
    '0011': '10101',
    '0100': '01010',
    '0101': '01011',
    '0110': '01110',
    '0111': '01111',
    '1000': '10010',
    '1001': '10011',
    '1010': '10110',
    '1011': '10111',
    '1100': '11010',
    '1101': '11011',
    '1110': '11100',
    '1111': '11101'
}

def str_to_raw(msg):
    res = []
    for i in msg:
        binary = bin(ch_dict[i])[2:].zfill(8)  # Convert to binary and pad with zeros
        for bit in binary:
            res.append(int(bit))
    return res

def raw_to_4b5b(raw_data):
    res = []
    for i in range(0, len(raw_data), 4):
        res.append(encoding[''.join(str(x) for x in raw_data[i:i+4])])
    return res
def bin4b5b_to_hex(bin_data):
    temp = ''.join(str(i) for i in bin_data)
    temp = hex(int(temp, 2))
    return temp
def bin_data_raw4b5b(bin_data):
    res = []
    for i in range(0, len(bin_data)):
        res.extend([int(x) for x in bin_data[i]])
    return res

def plot_setup(raw_data):
    x_max = len(raw_data)
    plt.figure(figsize=(15, 4))
    plt.title('Encoding of Message: ' + msg[:len(msg)-1] + '␣' ,
              fontsize=18, fontweight='bold')
    plt.xlim((0, x_max))
    plt.ylim((-0.2, 1.2))
    plt.yticks([0.5],
               [r'AMI'])
    for i in range(x_max):
        plt.plot([i+1, i+1], [-1, 1.2], color="lightgrey", linestyle="--")
    for i in range(2):
        plt.plot([0, x_max], [i, i], color="aliceblue", linestyle="--")
    for i in range(3):
        for j in range(x_max):
            plt.text(j + 0.5, i * 2 + 1.1, str(raw_data[j]), fontsize=5,
                     verticalalignment="bottom", horizontalalignment="center")
            
def ami(low, high, raw_bin):
    y = []
    switcher = 0
    middle = (high + low) / 2
    for i in range(len(raw_bin)):
        if raw_bin[i] == 0:
            y.extend([middle, middle, middle, middle])
        elif raw_bin[i] == 1:
            if switcher == 0:
                y.extend([high, high, high, high])
                switcher = 1
            else:
                y.extend([low, low, low, low])
                switcher = 0
    plt.plot(x_standard, y)

def count_digits(arr):
    counter = 0
    i = 0
    while i < len(arr):
        if(arr[i] == 0):
            if(i != len(arr) - 1 and arr[i+1] == 0):
                while i < len(arr) - 1 and arr[i + 1] == 0: i += 1
            else: counter += 1
        else: counter += 1
        i += 1
    return counter

def count_digits2(arr):
    count = 0
    i = 0
    while i < len(arr) - 2:
        if arr[i] == 0 and arr[i + 1] == 0 and arr[i+2] == 1:
            while i < len(arr) - 1 and arr[i + 1] == 0: i += 1
            count += 1
        if arr[i] == 0:
            while i < len(arr) - 1 and arr[i + 1] == 0: i += 1
        i += 1
    return count
def count_digits3(arr):
    counter = 0
    i = 0
    prev1 = 2
    prev2 = 2
    while i < len(arr):
        if arr[i] == 0 and prev1 == 0 and prev2 == 0:
                counter += 1
        prev2 = prev1
        prev1 = arr[i]
        i += 1
    return counter



    
if __name__ == "__main__":
    raw_data = str_to_raw(msg)
    bin_data = raw_to_4b5b(raw_data)
    for i in range(len(bin_data)):
        print(''.join(str(x) for x in raw_data[i:i+4])+" ->", end=" ")
        print(bin_data[i])
    raw_bin = bin_data_raw4b5b(bin_data)
    print(raw_bin)
    for i in range(len(raw_bin)):
        print(raw_bin[i], end="")
    print()
    print("message length: ", len(raw_bin))
    print(bin4b5b_to_hex(bin_data))
    for i_standard in range(len(raw_bin)):
        x_standard.append(i_standard)
        x_standard.append(i_standard + 0.5)
        x_standard.append(i_standard + 0.5)
        x_standard.append(i_standard + 1)
    plot_setup(raw_bin)
    ami(0, 1, raw_bin)
    test = [1,1,1,1,0,0,0,1,0,1,1,0,0]
    print("Number of transitions: ", count_digits(raw_bin))
    print("Number of transitions: ", count_digits2(raw_bin))
    print("Number of transitions: ", count_digits3(raw_bin))

