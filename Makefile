.DEFAULT_GOAL := default

### LOCAL TEST ###

# api test run
# Swagger UI http://127.0.0.1:8000/docs
run_local_uvicorn:
		uvicorn adjust_ratio.api.fast:app --reload

# run both Streamlit and Uvicorn at the same time (!dont forget '&')
run_local_streamlit:
		uvicorn adjust_ratio.api.fast:app --reload &
		streamlit run streamlit/app.py
