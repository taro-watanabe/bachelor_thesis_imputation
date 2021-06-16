import numpy as np
import pandas as pd
import os
import h2o
from h2o import load_model as lm

h2o.init()

def load_model(name, path='Video_Game_Results'):
    model = h2o.load_model(str(path) + str(name))
    df = model.summary().as_data_frame()
    df.to_latex(f'{str(path) + str(name)}')

    return model


def save_accuracy(path):
    df = pd.DataFrame({'MSE': []})
    try:
        os.mkdir(f'{path + "meta"}')
    except:
        pass

    for filename in os.listdir(path):
        print(filename)

        try:
            model = h2o.load_model(str(path) + str(filename))
            #print(model)
            df.append(dict(MSE=model.mse(xval=True)), ignore_index=True)

            temp_df = pd.DataFrame({'MSE': [model.mse(xval=True)]})
            #print(df)

            df = df.append(temp_df)

            scores = model.scoring_history()
            #print(model)

            if model.summary():
                summary = model.summary().as_data_frame()

            else:
                summary = pd.DataFrame({'Placeholder': ["Stackensenble has no summary"]})


            if scores is None:
                scores = pd.DataFrame()
                pass
            if not scores.empty:
                pass
                scores.to_latex(f'{str(path) + "meta/" + str(filename) + "_" + "scores"}')
            else:
                pass
            summary.to_latex(f'{str(path) + "meta/" + str(filename) + "_" + "summary"}')

        except:
            pass
    df.index = np.arange(len(df))
    df = df[:30]
    df.to_latex(f'{str(path) + "meta/" + str(filename) + "_" + "MSEjoined"}')


