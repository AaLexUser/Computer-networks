import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":
    x = np.arange(100, 10000, 100)
    y = np.ceil(x / 1480)
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_ylabel("Fragments, count")
    ax.set_xlabel("Size, bytes")
    ax.plot(x, y, marker="o", lw=2)
    ax.grid(True)
    ax.minorticks_on()
    fig.suptitle("ICMP")
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 300
    plt.savefig("../image/part1/fragPerSize.png")
    plt.show()

