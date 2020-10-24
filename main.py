from simulator import simu

if __name__=="__main__":
    backlen = 250
    freq = 10
    stocknum = 10
    totalinput = 1000
    timelen = '2y'

    SIM = simu.SIM(backlen, freq, stocknum,totalinput, timelen)
    show = 1
    SIM.Test_sim('1934',show)
#30 days as freq
