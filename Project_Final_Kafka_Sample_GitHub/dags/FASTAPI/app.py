import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
import joblib
import pandas as pd
from io import BytesIO



description = """
This Netflix API allows you to make recommandations of movies for a given user.

## Get_Reco

Where you can: 
* `/load` the best matches for given user
"""

tags_metadata = [
    {
        "name": "Predictions",
        "description": "Use this endpoint for getting predictions"
    }
]

app = FastAPI(
    title="👨‍💼 API_Netflix_Reco",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)


model = joblib.load('../dags/FASTAPI/model/model.pkl')



@app.get("/")
async def index():

    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"

    return message



@app.get("/suggested_movies")
async def look_prediction(Cust_Id):
    """
    Simply returns last User ID predicted and associated suggested movies
    """
    df = pd.read_csv("../dags/FASTAPI/data/data_reco.csv", index_col=0)
    df['Estimate_Score'] = df['Movie_Id'].apply(lambda x: model.predict(int(Cust_Id), x).est)
    df = df.sort_values('Estimate_Score', ascending=False)
    best_movie = df.head(10)
    return best_movie.to_dict()



if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)