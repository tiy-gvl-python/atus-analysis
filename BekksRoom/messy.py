from BekksRoom.stats_functions import average_minutes, stdev_minutes
from BekksRoom.stats_functions import hypothesis_test_plot
import pandas as pd
import matplotlib as plt


def get_input(dataset):
    done = False
    std = 'n'
    avg = 'n'
    hypothesis = 'n'
    going_to_use_groupby = 'n'
    avg = input("want the average? y/n ")
    clean = input("Want your data cleaned?  We drop zeros and nan. y/n ")
    columns = []
    if avg == "y":
        print("Automatically including weight because you want the average")
        columns.append('weight')
    else:
        std = input("Want standard Deviation? y/n ")
        if std == 'y':
            print("Automatically including weight because you want the standard dev")
            columns.append('weight')
    if avg != 'y' or std != 'y':
        hypothesis = input("Want hypothesis testing? y/n ")
        if hypothesis == 'y':
            print("Automatically including weight because you want hypothesis test")
            columns.append('weight')
    if avg != 'y' and std != 'y' and hypothesis != 'y':
        going_to_use_groupby = input("Are you going to use groupby? y/n ")
        if going_to_use_groupby == 'y':
            print("Automatically including weight because you want to use groupby ")
            columns.append('weight')
    for item in dataset.columns.tolist():
        print(item)
    while not done:
        print("Enter you column as appears above, type DONE when done, or CLEAR if you messup")
        column = input("What columns do you want?")
        if column == 'DONE':
            done = True
            break
        if column == 'CLEAR':
            columns = []
        if column in dataset.columns.tolist():
            columns.append(column)
        else:
            print("Not in dataset")
        print(columns)
    return(avg, clean, columns, std, hypothesis, going_to_use_groupby)


def querys(datawork, query):
    return datawork[query]


def graph_data(dataset):
    wplot = input("What type of plot? bar or line (more to come)")
    if wplot == "bar":
        print(plt.style.available)
        plot_style = input("What style plot? Type it correctly!")
        plt.style.use(plot_style)
        print("Your data sir ", dataset)
        figuresize = input("Whats your figure size, just enter one number no floats")
        figuresize = int(figuresize)
        legends = input("Want a legend True/False")
        stacks = input("Want to stack it? True/False")
        xlabels = input("x label?")
        ylabels = input("y label?")
        grids = input("Want a grid True/False")
        ax = dataset.plot(kind="bar", figsize=(figuresize,figuresize), legend=eval(legends), stacked=eval(stacks))
        ax.set_ylabel(ylabels)
        ax.grid(eval(grids), 'both')
        ax.set_xlabel(xlabels)
        return ax
    if wplot == "line":
        print(plt.style.available)
        plot_style = input("What style plot? Type it correctly!")
        plt.style.use(plot_style)
        print("Your data sir ", dataset)
        figuresize = input("Whats your figure size, just enter one number no floats")
        figuresize = int(figuresize)
        legends = input("Want a legend True/False")
        xlabels = input("x label?")
        ylabels = input("y label?")
        grids = input("Want a grid True/False")
        ax = dataset.plot(kind="line", figsize=(figuresize,figuresize), legend=eval(legends))
        ax.set_ylabel(ylabels)
        ax.grid(eval(grids), 'both')
        ax.set_xlabel(xlabels)
        return ax


def datasets(dataset, query=None):
    avg, clean, columns, std, hypothesis, going_to_use_groupby = get_input(dataset)
    # print(avg, clean, columns)
    data = dataset[columns]
    if query is not None:
        data = querys(data, query)
    data.describe()
    if std == 'y':
        newdataframe = {}
        for item in data.columns.tolist():
            if item == "weight":
                pass
            else:
                newdataframe[item] = [stdev_minutes(data, item)]
        data = pd.DataFrame.from_dict(newdataframe, orient='columns', dtype=None)
    if avg == 'y':
        newdataframe = {}
        for item in data.columns.tolist():
            if item == "weight":
                pass
            else:
                newdataframe[item] = [average_minutes(data, item)]
        data = pd.DataFrame.from_dict(newdataframe, orient='columns', dtype=None)
    if clean == 'y':
        for item in data.columns.tolist():
            if item == "weight":
                pass
            else:
                data = data[data[item] > 0]
                data = data.dropna()
                # print(data)
    if going_to_use_groupby == 'y':
        while True:
            column_to_group = input("What column would you like to group by? ")
            if column_to_group in data:
                return data.groupby(column_to_group)
            else:
                print("Thats not in your columns")
    if hypothesis == 'y':
        group_var = input("What is your group variable?")
        test_var = input("What is your test variable?")
        data = hypothesis_test_plot(data, group_var, test_var)
    graphs = input("Want to graph your data? y/n")
    if graphs == 'y':
        plot = graph_data(data)
        return(data, plot)
    return data
