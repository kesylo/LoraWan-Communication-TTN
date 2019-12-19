import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')


def animate(i):
    data_lora1 = pd.read_csv('lora1.csv')
    data_lora2 = pd.read_csv('lora2.csv')
    x1 = data_lora1['x_values']
    x2 = data_lora2['x_values']
    y1 = data_lora1['ligth']
    y2 = data_lora2['ligth']

    plt.cla()

    plt.plot(x1, y1, label='lumière_lora1 (lux)')
    plt.plot(x2, y2, label='lumière_lora2 (lux)')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
