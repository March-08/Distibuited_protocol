# libraries and data
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
 
# # Make a data frame
# df=pd.DataFrame({'x': range(1,11), 'y1': np.random.randn(10), 'y2': np.random.randn(10)+range(1,11), 'y3': np.random.randn(10)+range(11,21), 'y4': np.random.randn(10)+range(6,16), 'y5': np.random.randn(10)+range(4,14)+(0,0,0,0,0,0,0,-3,-8,-6), 'y6': np.random.randn(10)+range(2,12), 'y7': np.random.randn(10)+range(5,15), 'y8': np.random.randn(10)+range(4,14), 'y9': np.random.randn(10)+range(4,14), 'y10': np.random.randn(10)+range(2,12) })
#
# # style
# plt.style.use('seaborn-darkgrid')
#
# # create a color palette
# palette = plt.get_cmap('Set1')
#
# # multiple line plot
# num=0
# for column in df.drop('x', axis=1):
#     num=num+1
#     plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
#
# # Add legend
# plt.legend(loc=2, ncol=2)
#
# # Add titles
# plt.title("A (bad) Spaghetti plot", loc='left', fontsize=12, fontweight=0, color='orange')
# plt.xlabel("Time")
# plt.ylabel("Score")
# plt.show()











#10 lanci su 10,20...nodi con stessa prob, vediamo i tempi
def plot_time():
    nodes = [10, 20, 30, 40, 50, 100, 110, 130, 140, 150, 200, 240, 250]
    total_time = []
    avg_time = []
    min_time = []
    max_time = []
    times_all_correctly_informed = []
    avg_rounds_number = []


    for i in nodes:
        f = open("../reports/10_throws_0.7_p/stats_10_throws_" + str(i) + "_nodes_0.7_p.txt", "r+")
        line = f.readline()
        while (line):
            line = line.strip().split(":")
            if line[0] == "avg_time":
                avg_time.append(line[1])
            if line[0] == "total_time":
                total_time.append(float(line[1]))
            if line[0] == "min_time ":
                min_time.append(line[1])
            if line[0] == "max_time":
                max_time.append(line[1])
            if line[0] == "times_all_correctly_informed":
                times_all_correctly_informed.append(line[1])
            if line[0] == "avg_rounds_number":
                avg_rounds_number.append(line[1])



            line = f.readline()

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(15,7))
    bg_color = (1,1,0.9)
    ax.set_facecolor(bg_color)
    #ax.plot(spr_x, out.best_fit, 'r-', label='total fit')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.plot(nodes, avg_time, color='g',label="avg time")
    plt.plot(nodes, total_time, color='orange',label="total time")
    plt.plot(nodes, min_time, color='red',label="min time")
    plt.plot(nodes, max_time, color='blue',label="max time")
    plt.xlabel('Number of nodes')
    plt.ylabel('Time ')
    plt.title('Breathe before speaking')
    plt.style.use('dark_background')
    plt.yticks(np.arange(min(total_time), max(total_time), 10))
    plt.grid(True)
    plt.grid(linestyle='-', linewidth='0.2', color='black')

    plt.legend(loc="upper left")
    plt.show()



#10 lanci con 60 nodi cambiando le probabilita
def plot_time_on_p():
    total_time=[]
    avg_time=[]
    avg_source_degree=[]


    prob=["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"]
    for i in prob:
        f = open("../reports/10_throws_"+i+"_p/stats_10_throws_" + "60" + "_nodes_"+i+"_p.txt", "r+")
        line = f.readline()
        while (line):
            line = line.strip().split(":")

            if line[0] == "total_time":
                total_time.append(float(line[1]))
            if line[0] == "avg_time":
                avg_time.append(float(line[1]))
            if line[0] == "avg_source_degree":
                avg_source_degree.append(float(line[1]))

            line = f.readline()


    print(len(total_time))
    y_pos = np.arange(len(prob))
    plt.bar(y_pos, total_time, align='center', alpha=0.5,)
    plt.xticks(y_pos, prob)
    plt.ylabel('seconds')
    plt.xlabel('Probability')
    plt.title('Breathe before speaking')
    plt.style.use('dark_background')
    plt.show()

    print(len(total_time))
    y_pos = np.arange(len(avg_source_degree))
    plt.bar(y_pos, total_time, align='center', alpha=0.5, )
    plt.xticks(y_pos, avg_source_degree)
    plt.ylabel('seconds')
    plt.xlabel('source degree')
    plt.title('Breathe before speaking')
    plt.style.use('dark_background')
    plt.show()

def plt_100():
    numberEdges  = []
    correctly_informed= []
    sourceDegree = []

    f = open("../reports/100_throws_0.7_p/each_throw_100_throws_" + "120" + "_nodes_" + "0.7" + "_p.txt", "r+")
    line = f.readline()
    while (line):
        line = line.strip().split(":")
        if line[0] == "numberEdges ":
            numberEdges.append(float(line[1]))
        if line[0] == "correctly informed " :
            correctly_informed.append(float(line[1]))
        if line[0] == "sourceDegree ":
            sourceDegree.append(float(line[1]))

        line = f.readline()


    y_pos = np.arange(len(numberEdges))
    plt.bar(y_pos, correctly_informed, align='center', alpha=1, )
    plt.xticks(y_pos, numberEdges)
    plt.ylabel('seconds')
    plt.xlabel('source degree')
    plt.title('Breathe before speaking')
    plt.show()

plot_time()
plot_time_on_p()
#plt_100()
