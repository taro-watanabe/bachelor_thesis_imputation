import numpy as np
import pandas as np
import pandas as pd
import scipy as sc
from scipy.stats import norm

def htest(mu, sigmasq, x, rate, method):

    sigma = sigmasq**0.5
    normalized_x = (x-mu)/sigma
    print(x)
    print(normalized_x)

    dist = norm()

    if dist.cdf(normalized_x) < 0.5:
        p = dist.cdf(normalized_x)
        note = 1
    else:
        p = 1 - dist.cdf(normalized_x)
        note = 0

    print(p)

    result = pd.DataFrame({'p-value': [''],
                           'Lower': [''],
                           '1%': [''],
                           '5%': [''],
                           '10%': [''],
                          'rate': [''],
                           'method': ['']})

    result['p-value'][0] = p

    if note:
        result['Lower'][0] = 'Yes'

    else:
        result['Lower'][0] = '-'

    if p < 0.01:
        result['1%'][0] = 'Significant'
        result['5%'][0] = 'Significant'
        result['10%'][0] = 'Significant'


    elif p < 0.05:
        result['1%'][0] = '-'
        result['5%'][0] = 'Significant'
        result['10%'][0] = 'Significant'

    elif p < 0.1:
        result['1%'][0] = '-'
        result['5%'][0] = '-'
        result['10%'][0] = 'Significant'

    else:
        result['1%'][0] = '-'
        result['5%'][0] = '-'
        result['10%'][0] = '-'

    result['rate'] = rate
    result['method'] = method
    print(result)
    return result




list_mu = [2.76, 2.58, 4.75, 3.03, 2.99, 3.00, 5.51, 4.16, 2.86, 4.21, 5.56, 3.88, 4.62, 4.46, 5.12, 5.18]
list_sigma = [2.66, 1.70, 2.61, 1.97, 5.56, 3.29, 1.50, 3.93, 12.03, 1.3, 2.94, 11.57, 46.10, 4.03, 5.74, 44.79]

list_rate = ['1%', '1%', '1%', '1%', '5%', '5%', '5%', '5%', '10%', '10%', '10%', '10%', '20%', '20%', '20%', '20%']
list_method = ['Remove', 'Forward Fill', "Mode", "Mean"]

ini = pd.DataFrame({'p-value': [''],
                    'Lower': [''],
                    '1%': [''],
                    '5%': [''],
                    '10%': [''],
                    'rate': [''],
                    'method': ['']})

for i in range(len(list_mu)):
    #0.2532763480168034

    res = htest(list_mu[i], list_sigma[i], 0.0004, list_rate[i], list_method[(i)%4])

    ini = pd.concat([ini, res])

ini = ini.reset_index(drop=True)
print(ini)
ini.to_latex('vgsales_htest')



