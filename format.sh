black oarepo_model_builder tests --target-version py310
autoflake --in-place --remove-all-unused-imports --recursive oarepo_model_builder tests
isort oarepo_model_builder tests  --profile black
