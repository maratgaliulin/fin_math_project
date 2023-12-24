import numpy as np

def cumsum_true_false(low, cumsum_tf):
    signal   = []
    
    for date, value in cumsum_tf.items():
        if value == True:
            signal.append(low[date])
        else:
            signal.append(np.nan)
            
    return signal