import time
import spidev
import datetime
import numpy as np
import matplotlib.pyplot as plt

meas_t = 200e-3
T = 1000
n_T = int(T/meas_t)

sp1 = spidev.SpiDev()
sp1.open(0,0)
sp1.max_speed_hz = 100000
sp1.mode = 0b00
sp2 = spidev.SpiDev()
sp2.open(1,0)
sp2.max_speed_hz = 100000


def bin_to_num(data):
    arb = data[0] >> 6
    val = (data[2] + (data[1]<<8) + ((data[0]^(arb << 6))<<16)) - (1<<22 if (arb & 1) else 0)
    return -val/10000.0*2

def valid_bytes(bytelist):
    return not(bytelist[0] == bytelist[1]== bytelist[2] == ((1<<8)-1))

def meas():
    bytes1 = sp1.readbytes(3)
    bytes2 = sp2.readbytes(3)
    if valid_bytes(bytes1) and valid_bytes(bytes2):
        val1 = bin_to_num(bytes1)/1.0018
        val2 = bin_to_num(bytes2)/1.0014
        return (val1, val2)
    else:
        print("NANmeas")
        return (np.nan, np.nan)

def measurements(n_meas, meas_t):
    datas = np.zeros((n_meas, 2))
    for i in range(n_meas): 
        time.sleep(meas_t)
        m = meas()
        datas[i,:] = m
        print(m)
    datas = np.array(datas)
    return datas
        

        


if __name__ == "__main__":
    print("Starting")
    datas = measurements(n_T, meas_t)
    adev = []
    ts = []
    i = 0
    datas = np.sum(datas, axis=1)
    datas = datas[~np.isnan(datas)]
    while  np.sum(den:=(np.abs(datas-np.average(datas)) > np.std(datas))) < 1/100*len(datas):
        print("Outliers detected")
        print(datas[den])
        datas = datas[~den]

    fig, ax = plt.subplots(1,1)
    ax.plot(meas_t*np.arange(len(datas)), datas)
    while (ld:=len(datas)) > 1:
        if ld % 2 == 1: datas = datas[:-1]
        i += 1
        datas = np.reshape(datas, (-1, 2))
        adev.append(np.sqrt(np.sum((datas[:,0] - datas[:,1])**2)/len(datas)))
        ts.append(2**(i-1)*meas_t)
        datas = np.nanmean(datas, axis=1)
    fig, ax = plt.subplots(1,1)
    ax.plot(ts, adev)
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.show()



