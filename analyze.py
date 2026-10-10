import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

if __name__ == "__main__":
    dlist =  os.listdir("datastorage")
    fig, ax = plt.subplots(1,1)
    for fname in dlist:
        with open("datastorage/"+fname, "rb") as file:
            datas, tstep = pickle.load(file)
        ax.plot(np.arange(len(datas))*tstep, np.sum(datas, axis=1), color="k")
    plt.show()
