import csv
import numpy
import matplotlib.pyplot
import typing
import scipy.stats


# Define function for loading data
def load_csv(file: str, nc: int) -> dict:
    d = {}
    with open(file, "r") as f:
        the_file = csv.reader(f, delimiter=',')
        for idx, line in enumerate(the_file):
            if idx is 0:
                headings = line
            else:
                temp = {}
                for i in range(0, nc):
                    if "Id" in headings[i]:
                        try:
                            temp[headings[i]] = int(line[i])
                        except ValueError:
                            try:
                                temp[headings[i]] = int(float(line[i]))
                            except ValueError:
                                temp[headings[i]] = -1

                    elif headings[i] in ["Ranking", "Score"]:
                        temp[headings[i]] = float(line[i])
                    else:
                        temp[headings[i]] = line[i]
                d[temp["Id"]] = temp
    return d


def plot_slope(x: numpy.ndarray,
               xs: typing.List[typing.Union[int, float]],
               ys: typing.List[typing.Union[int, float]],
               format_string: str):
    slope = scipy.stats.pearsonr(numpy.array(xs), -numpy.array(ys))
    b = -numpy.mean(ys) - slope[0]*numpy.mean(xs)
    y = slope[0]*x + b
    matplotlib.pyplot.plot(x, y, format_string)