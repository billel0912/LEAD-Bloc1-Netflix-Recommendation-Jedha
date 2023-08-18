import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from surprise.model_selection import GridSearchCV
import joblib


df = pd.read_csv('data/data_cleaned_sample.csv')

reader = Reader()

data = Dataset.load_from_df(df[['Cust_Id', 'Movie_Id', 'Rating']][:], reader)

param_grid = {
    "n_epochs": [5, 10],
    "lr_all": [0.002, 0.005],
    "reg_all": [0.4, 0.6],
    "n_factors": [50, 100]
    }


gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=5)
gs.fit(data)


# best RMSE score
print("The best score of RMSE :", gs.best_score["rmse"])

# best MAE score
print("The best score of MAE : ", gs.best_score["mae"])

# combination of parameters that gave the best RMSE score
print("The best params of RMSE :", gs.best_params["rmse"])

# combination of parameters that gave the best RMSE score
print("The best params of MAE :", gs.best_params["mae"])


# Train the model with the best parameters
best_params_rmse = gs.best_params["rmse"]

model = SVD(**best_params_rmse)
trainset = data.build_full_trainset()
model.fit(trainset)

# Save the model as a file
model_file = "model/model_sample.pkl"
joblib.dump(model, model_file, compress=True)
