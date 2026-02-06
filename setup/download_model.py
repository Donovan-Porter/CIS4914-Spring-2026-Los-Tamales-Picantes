from huggingface_hub import snapshot_download
import os

# Define the desired local directory
download_location = os.path.join(os.getcwd(), "model")

# Download the repository snapshot to the local directory
snapshot_download(repo_id="LiquidAI/LFM2-350M", local_dir=download_location)