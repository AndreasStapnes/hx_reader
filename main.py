import time
import spidev
import datetime
import numpy as np
import pickle

sleep_t = 1000e-3
meas_t = 100e-3

w_crit = 3
subcrit_slumber_t = 2


sp1 = spidev.SpiDev()
sp1.open(0,0)
sp1.max_speed_hz = 100000
sp1.mode = 0b00
sp2 = spidev.SpiDev()
sp2.open(1,0)
sp2.max_speed_hz = 100000
    #sp2.mode = 0b11

def bin_to_num(data):
    arb = data[0] >> 6
    val = (data[2] + (data[1]<<8) + ((data[0]^(arb << 6))<<16)) - (1<<22 if (arb & 1) else 0)
    return -val/10000.0*2

def valid_bytes(bytelist):
    #print(bytelist)
    return not(bytelist[0] == bytelist[1]== bytelist[2] == ((1<<8)-1))

def meas():
    bytes1 = sp1.readbytes(4)[:3]
    bytes2 = sp2.readbytes(4)[:3]
    if valid_bytes(bytes1) and valid_bytes(bytes2):
        val1 = (bin_to_num(bytes1)/1.0018 + 0.207)*0.9578
        val2 = (bin_to_num(bytes2)/1.0014 + 0.041)*0.9647
        return (val1, val2)
    else:
        print("NANmeas")
        return (np.nan, np.nan)

def measurement_run():
    global prog
    datas = []
    subcrit_i = 0
    while True: 
        time.sleep(meas_t)
        m = meas()
        print(m)
        datas.append(m)
        prog.set_description(f"{np.sum(m):.2f}  ")
        #print(m)
        #print("*", end="")
        if (m[0] + m[1]) < w_crit:
            subcrit_i += 1;
            if subcrit_i*meas_t > subcrit_slumber_t:
                break
        else: subcrit_i = 0
    datas = np.array(datas)
    prog.close()
    dt = datetime.datetime.now()
    fname = f"datastorage/{str(dt.year)[-2:]}{str(dt.month).rjust(2,'0')}{str(dt.day).rjust(2,'0')}-{str(dt.hour).rjust(2,'0')}h{str(dt.minute).rjust(2,'0')}m{str(dt.second).rjust(2,'0')}s.bin"
    with open(fname, "wb") as file:
        pickle.dump([datas, meas_t], file)    
        print("Storing datas!")
    print(f"Vol={np.sum(datas)/1000*9.8*meas_t:.2f}kNs")
    prog = tqdm.tqdm()
    return datas

        

        
import tqdm
import matplotlib.pyplot as plt
i = 0
if __name__ == "__main__":
    prog = tqdm.tqdm()
    while True:
        m = meas()
        #print("subcrit - ", m)
        prog.update()
        msum = m[0] + m[1]
        if not np.isnan(msum) and msum  > w_crit:
            #prog.close()
            #print("Starting measrun!")
            d = measurement_run()
            #prog = tqdm.tqdm()
        time.sleep(sleep_t)


