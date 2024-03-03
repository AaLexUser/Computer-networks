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

def str_to_raw(msg):
    res = []
    for i in msg:
        binary = bin(ch_dict[i])[2:].zfill(8)  # Convert to binary and pad with zeros
        for bit in binary:
            res.append(int(bit))
    return res

def scramble57(raw_data):
    x = np.array(raw_data, dtype=int)
    x_scrambled = np.zeros(len(x), dtype=int)
    for i in range(5):
        x_scrambled[i] = x[i]
    for i in range(5, 7):
        x_scrambled[i] = x[i] ^ x_scrambled[i-5]
    for i in range(7, len(x)):
        x_scrambled[i] = x[i] ^ x_scrambled[i-5] ^ x_scrambled[i-7]
    return x_scrambled
def scramble35(raw_data):
    x = np.array(raw_data, dtype=int)
    x_scrambled = np.zeros(len(x), dtype=int)
    for i in range(3):
        x_scrambled[i] = x[i]
    for i in range(3, 5):
        x_scrambled[i] = x[i] ^ x_scrambled[i-3]
    for i in range(5, len(x)):
        x_scrambled[i] = x[i] ^ x_scrambled[i-3] ^ x_scrambled[i-5]
    return x_scrambled

def max_zeros(x):
    max_zeros = 0
    zeros = 0
    for i in range(len(x)):
        if x[i] == 0:
            zeros += 1
        else:
            if zeros > max_zeros:
                max_zeros = zeros
            zeros = 0
    return max_zeros

def scramble_search(raw_data):
    min_zeros_num = len(raw_data)
    min_zeros_scrambled = []
    min_n = 0
    min_i = 0
    for n in range(1, len(raw_data)-1):
        print("N: ", n)
        for i in range(1, len(raw_data) - n):
            x = np.array(raw_data, dtype=int)
            x_scrambled = np.zeros(len(x), dtype=int)
            for j in range(0, i):
                x_scrambled[j] = x[j]
            for j in range(i, i+n):
                x_scrambled[j] = x[j] ^ x_scrambled[j-i]
            for j in range(i+n, len(x)):
                x_scrambled[j] = x[j] ^ x_scrambled[j-i] ^ x_scrambled[j-i-n]
            if max_zeros(x_scrambled) < min_zeros_num:
                min_zeros_num = max_zeros(x_scrambled)
                min_zeros_scrambled = x_scrambled
                min_n = n
                min_i = i
            print(i, "{", i, i+n, "}", max_zeros(x_scrambled))
    print("Min zeros: ", min_zeros_num)
    print("N: ", min_n)
    print("I: ", min_i)
    return min_zeros_scrambled

def scramble1516(raw_data):
    x = np.array(raw_data, dtype=int)
    x_scrambled = np.zeros(len(x), dtype=int)
    for i in range(15):
        x_scrambled[i] = x[i]
    for i in range(15, 16):
        x_scrambled[i] = x[i] ^ x_scrambled[i-15]
    for i in range(16, len(x)):
        x_scrambled[i] = x[i] ^ x_scrambled[i-15] ^ x_scrambled[i-16]
    return x_scrambled
    
def file_write(x_scrambled, raw_data, i, n):
    with open("scrambled.txt", "w") as file:
        for j in range(0, i):
            file.write(f'$$B_'+"{"+f'{j+1}'+"}" +f' = A_'+"{"+f'{j+1}'+"}"+f'= {x_scrambled[j]}$$\n')
        for j in range(i, i+n):
            file.write(f'$$B_'+"{"+f'{j+1}'+"}"+f' = A_'+"{"+f'{j+1}'+"}"+f' \oplus B_'+"{"+f'{j-i+1}'+"}"+f' = {raw_data[j]} \oplus {x_scrambled[j-i]} = {x_scrambled[j]}$$\n')
        for j in range(i+n, len(x_scrambled)):
            file.write(f'$$B_'+"{"+f'{j+1}'+"}"+f' = A_'+"{"+f'{j+1}'+"}"+f' \oplus B_'+"{"+f'{j+1-i}'+"}"+f' \oplus B_'+"{"+f'{j+1-i-n}'+"}"+f' = {raw_data[j]} \oplus {x_scrambled[j-i]} \oplus {x_scrambled[j-i-n]} = {x_scrambled[j]}$$\n')

def bin_to_hex(bin_data):
    temp = ''.join(str(i) for i in bin_data)
    temp = hex(int(temp, 2))
    return temp

def plot_setup(raw_data):
    x_max = len(raw_data)
    plt.figure(figsize=(30, 4))
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 300
    plt.title('Encoding of Message: ' + msg[:len(msg)-1] ,
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
    prev1 = 2
    prev2 = 2
    prev3 = 2
    while i < len(arr):
        if(arr[i] == 1):
            counter += 1
            if(prev1 == 0 and prev2 != 0 ):
                counter += 1
        prev3 = prev2
        prev2 = prev1
        prev1 = arr[i]
        i += 1
    if(prev1 == 0 and prev2 != 0):
        counter += 1
    return counter

def count_digits2(arr):
    count = 0
    i = 0
    prev1 = 2
    prev2 = 2
    prev3 = 2
    while i < len(arr):
        if(arr[i]== 1 and prev1 == 0 and prev2 == 0 and prev3 != 0):
            count += 1
        prev3 = prev2
        prev2 = prev1
        prev1 = arr[i]
        i += 1
    
    if(prev1 == 0 and prev2 == 0 and prev3 != 0):
        count += 1
    return count

def count_digits3(arr):
    counter = 0
    i = 0
    prev1 = 2
    prev2 = 2
    prev3 = 2
    prev4 = 2
    while i < len(arr):
        if arr[i] == 1 and prev1 == 0 and prev2 == 0 and prev3 == 0 and prev4 != 0:
                counter += 1
        prev4 = prev3
        prev3 = prev2
        prev2 = prev1
        prev1 = arr[i]
        i += 1

    if prev1 == 0 and prev2 == 0 and prev3 == 0 and prev4 != 0:
        counter += 1
    return counter

def count_digits4(arr):
    counter = 0
    i = 0
    prev1 = 2
    prev2 = 2
    prev3 = 2
    while i < len(arr):
        if arr[i] == 0 and prev1 == 0 and prev2 == 0 and prev3 == 0:
                counter += 1
        prev3 = prev2
        prev2 = prev1
        prev1 = arr[i]
        i += 1
    return counter


if __name__ == "__main__":
    raw_data = str_to_raw(msg)
    print(raw_data)
    print(scramble_search(raw_data))
    bin_data_res = scramble1516(raw_data)
    print(bin_data_res)
    file_write(scramble1516(raw_data),raw_data, 15, 1)
    print("Hex res: " + bin_to_hex(scramble1516(bin_data_res)))
    print("Message length: ", len(bin_data_res))
    print("Message lenght in bytes: ", len(bin_data_res) / 8)

    for i_standard in range(len(bin_data_res)):
        x_standard.append(i_standard)
        x_standard.append(i_standard + 0.5)
        x_standard.append(i_standard + 0.5)
        x_standard.append(i_standard + 1)
    plot_setup(bin_data_res)
    ami(0, 1, bin_data_res)
    plt.savefig('encoding_3.png')
    
    print("Digits 1: ", count_digits(bin_data_res))
    print("Digits 2: ", count_digits2(bin_data_res))
    print("Digits 3: ", count_digits3(bin_data_res))
    print("Digits 4: ", count_digits4(bin_data_res))





