import numpy as np
import pandas as pd
import h2o
from h2o.automl import H2OAutoML
pd.options.display.width = 0
h2o.init()
h2o.connect()

def split_ingest(df):
    df_origin = pd.read_csv(df['csv'], low_memory=False)
    print(f"loaded DataFrame: \n{df_origin.head()}")

    train = df_origin.sample(frac=0.8,random_state=1)
    test = df_origin.drop(train.index)

    trainh2o = h2o.H2OFrame(train)
    testh2o = h2o.H2OFrame(test)

    x = trainh2o.columns
    print(x)
    y = df['label']
    x = x.remove(y)

    if df['type'] == "reg":
        trainh2o[y] = trainh2o[y].asnumeric()
        testh2o[y] = testh2o[y].asnumeric()
    elif df['type'] == "cla":
        trainh2o[y] = trainh2o[y].ascharacter()
        testh2o[y] = testh2o[y].ascharacter()
        trainh2o[y] = trainh2o[y].asfactor()
        testh2o[y] = testh2o[y].asfactor()

    return trainh2o, testh2o, x, y

def read_task_csv():
    df = pd.DataFrame({"csv": ["vgsales_alias.csv"],
                       "label": ["Global_Sales"],
                       "type": ["reg"],
                       "leader_model": ["vgsales_leader"]})

    return df

for idx, row in read_task_csv().iterrows():
    train, test, x, y = split_ingest(row)
    aml = H2OAutoML(max_models=20, seed=1, max_runtime_secs=86400)
    aml.train(x=x, y=y, training_frame=train)


    h2o.save_model(aml.leader, path=str(row['leader_model']))




