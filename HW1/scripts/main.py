import matplotlib.pyplot as plt
import numpy as np

msg = "Алексей "
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

raw_data = []
x_standard = []

def plot_setup():
    x_max = len(raw_data)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 300
    plt.figure(figsize=(12, 8))
    plt.title('Encoding of Message: ' + msg[:len(msg)-1] + '␣',
              fontsize=18, fontweight='bold')
    plt.xlim((0, x_max))
    plt.ylim((-1, 6))
    plt.yticks([0.5, 2.5, 4.5],
               [r'$NoneReturnToZero$', r'$Manchester$', r'AMI'])
    for i in range(x_max):
        plt.plot([i+1, i+1], [-1, 16], color="lightgrey", linestyle="--")
    for i in range(6):
        plt.plot([0, 8], [i, i], color="aliceblue", linestyle="--")
    for i in range(3):
        for j in range(x_max):
            plt.text(j + 0.5, i * 2 + 1.1, str(raw_data[j]), fontsize=5,
                     verticalalignment="bottom", horizontalalignment="center")

def str_to_hex(msg):
    res = []
    for i in msg:
        res.append(hex(ch_dict[i]))
    return res

def str_to_bin(msg):
    res = []
    for i in msg:
        res.append(bin(ch_dict[i]))
    return res


def str_to_manchester(msg):
    res = []
    for i in msg:
        binary = bin(ch_dict[i])[2:].zfill(8)  # Convert to binary and pad with zeros
        manchester = ''.join('10' if bit == '1' else '01' for bit in binary)  # Manchester encode
        res.append(manchester)
    return res
def str_to_raw(msg):
    res = []
    for i in msg:
        binary = bin(ch_dict[i])[2:].zfill(8)  # Convert to binary and pad with zeros
        for bit in binary:
            res.append(int(bit))
    return res

def plot_manchester(manchester_msg):
    # Flatten the list of Manchester encoded strings
    manchester_signal = ''.join(manchester_msg)
    
    # Create a time array for the signal
    time = np.arange(len(manchester_signal))
    
    # Create a signal array where '1' is high and '0' is low
    signal = np.array([1 if bit == '1' else  0 for bit in manchester_signal])
    
    # Plot the signal
    plt.figure(figsize=(10,  2))
    plt.step(time, signal, where='post')
    plt.ylim(-0.5,  1.5)
    plt.yticks([0,  1])
    plt.xlim(0, len(manchester_signal))
    plt.title('Manchester Encoded Signal')
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.xticks(np.arange(0, len(manchester_signal), step=0.5))
    plt.grid(True, which='both', axis='x')
    plt.xticks(np.arange(0, len(manchester_signal), step=2) +  0.5)

def none_return_to_zero(low, high):
    y = []
    y_cycle = ([low, low, low, low], [high, high, high, high])
    for i in range(len(raw_data)):
        y.extend(y_cycle[raw_data[i]])
    plt.plot(x_standard, y)

def manchester(low, high):
    y = []
    for i in range(len(raw_data)):
        if raw_data[i] == 0:
            y.extend([low, low, high, high])
            plt.annotate("", xy=(i + 0.5, low + 0.51), xytext=(i + 0.5, low + 0.49),
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
        elif raw_data[i] == 1:
            y.extend([high, high, low, low])
            plt.annotate("", xy=(i + 0.5, low + 0.49), xytext=(i + 0.5, low + 0.51),
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.plot(x_standard, y)

def ami(low, high):
    y = []
    switcher = 0
    middle = (high + low) / 2
    for i in range(len(raw_data)):
        if raw_data[i] == 0:
            y.extend([middle, middle, middle, middle])
        elif raw_data[i] == 1:
            if switcher == 0:
                y.extend([high, high, high, high])
                switcher = 1
            else:
                y.extend([low, low, low, low])
                switcher = 0
    plt.plot(x_standard, y)
if __name__ == '__main__':
    raw_data = str_to_raw(msg)
    for i_standard in range(len(raw_data)):
        x_standard.append(i_standard)
        x_standard.append(i_standard + 0.5)
        x_standard.append(i_standard + 0.5)
        x_standard.append(i_standard + 1)
    plot_setup()
    none_return_to_zero(0, 1)
    manchester(2, 3)
    ami(4, 5)
    plt.savefig('encoding_1.png')
    plt.show()