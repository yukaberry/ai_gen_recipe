import pandas as pd
import numpy as np

from pydantic import BaseModel, Field, model_validator
from typing import Dict

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

app = FastAPI()

# test to see if running
@app.get("/")
def root():
    return {'greeting': 'Hello, AI recipe generator! '}

# adjusted_recipe = {}

class AdjustmentRequest(BaseModel):

    """
    ingredient_amount : Dictionary, ngredient names (e.g., 'flour') to quantities in grams (int)

    """
    ingredient_amount : Dict[str, float]
    ingredient: str
    available_amount: float


    @model_validator(mode='after')
    def check_ingredient_exists(cls, values):

        """
        values : object
        """
        ingredient_amount = values.ingredient_amount
        ingredient = values.ingredient
        if ingredient not in ingredient_amount:
            raise ValueError(f"Ingredient '{ingredient}' not found in df_dict.")
        return values


# send user's limited ingredient
@app.post("/adjust")
def calculate_dict(request: AdjustmentRequest) :

    """
    What It Does:

    **User submits:

    - Full recipe (ingredients + amounts)

    - One ingredient they do not have enough of

    **API:

    - Calculates a scale factor based on the available amount

    - Adjusts all other ingredients proportionally

    - Returns the updated recipe
    """

    ingredient_to_scale = request.ingredient
    new_amount = request.available_amount
    # user_ingredient_amount= request.ingredient_amount
    # original_amount = user_ingredient_amount[ingredient_to_scale]
    original_amount = request.ingredient_amount[ingredient_to_scale]


    scale_factor = new_amount / original_amount

    # Adjust all ingredient amounts using the scale factor
    adjusted_recipe = {
        ingredient: round(amount * scale_factor, 2)
        for ingredient, amount in request.ingredient_amount.items()
    }

    return {
        "adjusted_recipe": adjusted_recipe,
        "scale_factor": round(scale_factor, 2)
    }    # print(f"Scale factor: {scale_factor:.2f}")

    # Adjust all ingredient amounts using the scale factor
    adjusted_recipe = {
        ingredient: round(amount * scale_factor, 2)
        for ingredient, amount in request.ingredient_amount.items()
    }

    return {
        "adjusted_recipe": adjusted_recipe,
        "scale_factor": round(scale_factor, 2)
    }


# 👀 Get the updated ingredient list
@app.get("/adjusted-recipe")
def get_adjusted_recipe(recipe):
    if not recipe:
        return {"message": "No adjustment has been made yet."}
    return {"adjusted_recipe": recipe}
