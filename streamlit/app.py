import json
from typing import List, Tuple, Dict

import pandas as pd
import requests
import streamlit as st

from setup import BASEURL


import json
import requests
import streamlit as st

st.set_page_config(page_title="Recipe Adjuster", page_icon="🥣")

st.title("🥣 Recipe Ingredient Adjuster")
st.write("Paste your recipe as **ingredient: amount** pairs, pick the limited ingredient, enter the amount you have, and hit Adjust.")

with st.expander("Example input format", expanded=False):
    st.code("""flour: 250
sugar: 100
eggs: 100
milk: 150
vanilla: 1""")

# 1) Simple text area for ingredient_amount dict
raw = st.text_area(
    "Recipe (one per line, format: ingredient: amount)",
    height=160,
    placeholder="flour: 250\nsugar: 100\neggs: 100"
)

# Very small helper to parse "name: number" lines into a dict[str, float]
def parse_pairs(text: str):
    data = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            st.warning(f"Skipping line (missing colon): {line}")
            continue
        name, value = line.split(":", 1)
        name = name.strip()
        try:
            amount = float(value.strip())
        except ValueError:
            st.warning(f"Skipping line (not a number): {line}")
            continue
        if name:
            data[name] = amount
    return data

ingredient_amount = parse_pairs(raw)

options = list(ingredient_amount.keys()) if ingredient_amount else []
ingredient = st.selectbox(
    "Ingredient you have less of (the one to scale by):",
    options,
    index=None,  # default is empty selection
    placeholder="Select an ingredient..."
)

available_amount = st.number_input("How much of that ingredient do you have?", min_value=0.0, value=50.0, step=1.0)

# 3) Adjust button -> POST to FastAPI
if st.button("Adjust"):
    if not ingredient_amount:
        st.error("Please enter at least one line in the recipe box.")
    elif ingredient is None:
        st.error("Please select an ingredient.")
    else:
        payload = {
            "ingredient_amount": ingredient_amount,  # Dict[str, float]
            "ingredient": ingredient,                # str
            "available_amount": available_amount     # float
        }
        try:
            r = requests.post(f"{BASEURL.rstrip('/')}/adjust", json=payload, timeout=15)
            r.raise_for_status()
            data = r.json()

            st.success("Adjusted recipe calculated!")
            st.metric("Scale factor", data.get("scale_factor"))

            adjusted = data.get("adjusted_recipe", {})
            # Show neatly
            st.subheader("Adjusted Recipe")
            # Make a simple two-column display
            for k in adjusted:
                st.write(f"- **{k}**: {adjusted[k]}")

            # Optional downloads
            st.download_button(
                "Download JSON",
                data=json.dumps(data, indent=2),
                file_name="adjusted_recipe.json",
                mime="application/json"
            )
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
