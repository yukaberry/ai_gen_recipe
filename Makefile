.DEFAULT_GOAL := default

run_uvicorn:
		uvicorn adjust_ratio.api.fast:app --reload
