import pandas as pd
import numpy as np
from pydantic import BaseModel

from fastapi import FastAPI

# original recipe
# data = [
# ['flour', 97, 'g'],
# ['egg york', 125, 'g'],
# ['egg white', 157, 'g'],
# ['honey', 108,'g'],
# ['cream', 78,'g'],
# ['nuts', 14,'g']]
# df = pd.DataFrame(data, columns=['ingredient', 'amount', 'unit'])
#df_dict = df.set_index('ingredient')['amount'].to_dict()

# test input on FastAPI
# {
#   "df_dict": {
#     "flour": 97,
#     "egg york": 125,
#     "egg white": 157,
#     "honey": 108,
#     "cream": 78,
#     "nuts": 14
#   },
#   "ingredient": "egg white",
#   "available_amount": 80
# }


app = FastAPI()

# test to see if running
@app.get("/")
def root():
    return {'greeting': 'Hello, AI recipe generator! '}

adjusted_recipe = {}
class AdjustmentRequest(BaseModel):
    df_dict : dict
    ingredient: str
    available_amount: float

# 🔁 Send user's limited ingredient
@app.post("/adjust")
def calculate_dict(request: AdjustmentRequest) :
    ingredient_to_scale = request.ingredient
    new_amount = request.available_amount
    user_df_dict = request.df_dict

    original_amount = user_df_dict[ingredient_to_scale]
    scale_factor = new_amount / original_amount
    print(f"Scale factor: {scale_factor:.2f}")

    # Adjust all ingredient amounts using the scale factor
    global adjusted_recipe
    adjusted_recipe = {
        ingredient: round(amount * scale_factor, 2)
        for ingredient, amount in user_df_dict.items()
    }

    return {
        "adjusted_recipe": adjusted_recipe,
        "scale_factor": round(scale_factor, 2)
    }


# 👀 Get the updated ingredient list
@app.get("/adjusted-recipe")
def get_adjusted_recipe():
    if not adjusted_recipe:
        return {"message": "No adjustment has been made yet."}
    return {"adjusted_recipe": adjusted_recipe}
