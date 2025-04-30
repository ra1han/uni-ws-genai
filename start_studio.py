from promptlab import PromptLab


# Initialize PromptLab with SQLite storage
tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
pl = PromptLab(tracer_config)

# Start the PromptLab Studio to view results
pl.studio.start(8000)
