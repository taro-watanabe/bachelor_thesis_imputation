import numpy as np
import pandas as pd
import h2o
from h2o.automl import H2OAutoML
pd.options.display.width = 0
h2o.init()
h2o.connect()


df_origin = pd.read_csv("heart.csv")
print(df_origin)

def split_ingest(csv, label):
    if type(csv) != str:
        raise Exception("csv title  must be a string!!")

    if type(label) != str:
        raise Exception("label column name must be a string!!")

    df_origin = pd.read_csv(csv)
    print(f"loaded DataFrame: \n{df_origin.head()}")

    train = df_origin.sample(frac=0.8,random_state=1)
    test = df_origin.drop(train.index)

    trainh2o = h2o.H2OFrame(train)
    testh2o = h2o.H2OFrame(test)

    x = trainh2o.columns
    y = label
    x = x.remove(y)

    trainh2o[y] = trainh2o[y].asfactor()
    testh2o[y] = testh2o[y].asfactor()

    return trainh2o, testh2o, x, y

print(split_ingest("healthcare-dataset-stroke-data.csv", "stroke"))


train, test, x, y = split_ingest("healthcare-dataset-stroke-data.csv", "stroke")
aml = H2OAutoML(max_models=20, seed=1)
aml.train(x=x, y=y, training_frame=train)

lb = aml.leaderboard
print(lb)
print(aml.leader)


