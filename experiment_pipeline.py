import h2o
import pandas as pd
import numpy as np
from h2o.automl import H2OAutoML

h2o.init()

def split_ingest(df, ratio, na_prob, method):

    def impute(df, method):
        methods = {"reduce": df.dropna(),
                "ffill": df.ffill(axis=0),
                "mean": df.fillna(df.mean()),
                "mode": df.fillna(df.mode().iloc[0])}

        if method == "mean":
            mean = methods[method]
            return impute(mean, "reduce")
        else:
            return methods[method]

    df_origin = pd.read_csv(str("/content/drive/MyDrive/") + df['csv'], low_memory=False)
    print(f"loaded DataFrame: \n{df_origin.head()}")

    q_df = df_origin.drop(columns=df["label"])
    holes_df = q_df.mask(np.random.random(q_df.shape) < na_prob)
    holes_df[df["label"]] = df_origin[df["label"]]

    reduced_df = holes_df.sample(frac=ratio, random_state=0)

    imputed_df = impute(reduced_df, method)

    train = imputed_df.sample(frac=0.8)
    test = imputed_df.drop(train.index)

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
    df = pd.DataFrame({"csv": ["vgsales_alias.csv", "shootings.csv"],
                       "label": ["Global_Sales", "state"],
                       "type": ["reg", "cla"],
                       "leader_model": ["vgsales_leader", "shootings_leader"]})

    return df
    

def do_them_all(ratio, missing_rate, method):
    task_df = read_task_csv()

    for idx, row in task_df.iterrows():
        train, test, x, y = split_ingest(row, ratio, missing_rate, method)
        aml = H2OAutoML(max_models=20, seed=1, max_runtime_secs=86400)
        aml.train(x=x, y=y, training_frame=train)

        h2o.save_model(aml.leader, path=str("/content/drive/MyDrive/Shootings_Result/") + str(row['leader_model']) + str(missing_rate) + str(method))
        
        
        
import time
missing_rates = [0.01, 0.05, 0.1, 0.2]
methods = ["reduce", "ffill", "mean", "mode"]

c = 0
start_whole = time.time()
for i in range(1):
    for e in missing_rates:
        for m in methods:
            print(f"On the round {i}, missing rate {e}, and imputation method {m}")
            print(f" {c}/{30*len(missing_rates)*len(methods)} loops")
            time_round = time.time()
            print(f"Time elapsed so far: {time_round - start_whole}")
            do_them_all(0.2, e, m)
            end_time = time.time()
            print(f"Time took for this round: {end_time - time_round}")

