from promptlab import PromptLab
from promptlab.model.ollama import Ollama, Ollama_Embedding
from promptlab.types import PromptTemplate, Dataset

def load_prompt_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split("user prompt", 1)
    if len(parts) < 2:
        return content.strip(), ""
    system_part = parts[0].replace("system prompt", "", 1).strip()
    user_part = parts[1].strip()
    
    return system_part, user_part

# system_prompt_v1, user_prompt_v1 = load_prompt_file("./prompts/prompt-v1.txt")
# system_prompt_v2, user_prompt_v2 = load_prompt_file("./prompts/prompt-v2.txt")

# Initialize PromptLab with SQLite storage
tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
pl = PromptLab(tracer_config)

# # Create a prompt template
# prompt_template = PromptTemplate(
#     name="phishing_url_detector",
#     description="A prompt for detecting phishing URLs.",
#     system_prompt=system_prompt_v1,
#     user_prompt=user_prompt_v1,
# )
# pt = pl.asset.create(prompt_template)

# # Create a dataset
# dataset = Dataset(
#     name="phishing_urls",
#     description="dataset for evaluating the phishing_url_detector prompt",
#     file_path="./data/phishing_urls.jsonl",
# )
# ds = pl.asset.create(dataset)

# # Update a prompt template
# prompt_template = PromptTemplate(
#     name="phishing_url_detector",
#     description="A prompt for detecting phishing URLs.",
#     system_prompt=system_prompt_v2,
#     user_prompt=user_prompt_v2,
# )
# pt = pl.asset.update(prompt_template)

prompt_template = pl.asset.get(
    asset_name="phishing_url_detector",
    version=1
)

dataset = pl.asset.get(
    asset_name="phishing_urls",
    version=0
)

# model instnace
model_config = {"type": "ollama", "model_deployment": "llama3.2"}
ollama = Ollama(model_config=model_config)

embedding_model_config = {
    "type": "ollama",
    "model_deployment": "nomic-embed-text:latest",
}
ollama_embedding = Ollama_Embedding(model_config=embedding_model_config)

# Run an experiment
experiment_config = {
    "inference_model": ollama,
    "embedding_model": ollama_embedding,
    "prompt_template": prompt_template,
    "dataset": dataset,
    "evaluation": [
        {
            "metric": "ExactMatch",
            "column_mapping": {"response": "$inference", "reference": "status"},
        }
    ],
}
pl.experiment.run(experiment_config)

