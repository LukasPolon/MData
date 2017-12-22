from sklearn import linear_model
from numpy import array

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn

from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression


class Regression(object):
    def __init__(self):
        self.data = None

    def get_data(self, data):
        self.data = data

    def linear_regression(self):
        new_data = self.data.drop('Close', axis=1)
        lm = LinearRegression()
        lm.fit(new_data, self.data.Close)
        e = pd.DataFrame(zip(new_data.columns, lm.coef_), columns=['features',
                                                            'estimatedCoefficients'])
        print(e)

    def linear_regression2(self):
        boston = load_boston()
        bos = pd.DataFrame(boston.data)
        bos.columns = boston.feature_names
        bos['PRICE'] = boston.target

        X = bos.drop('PRICE', axis=1)
        lm = LinearRegression()

        lm.fit(X, bos.PRICE)

        e = pd.DataFrame(zip(X.columns, lm.coef_), columns=['features',
                                                        'estimatedCoefficients'])
        pred = lm.predict(X)[0:5]
        print(pred)


if __name__ == '__main__':
    ob = Regression()
    ob.linear_regression()
