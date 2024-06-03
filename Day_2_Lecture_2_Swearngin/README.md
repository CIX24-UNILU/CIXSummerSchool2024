# Install Python (3.10) 
brew install python@3.10

# Install Conda
brew install miniforge

# Create Conda environment
conda create -n cix-new python=3.10

# Activate the Conda environment
conda activate cix-new

# Set up the notebook kernel 
conda install ipykernel 
python -m ipykernel install --user --name cix-new

# install the packages 
pip install -r requirements.txt

# Install 7zip for downloading the data and extracting it. 
brew install p7zip

# Download the training data
cd downloads
python downloader.py

# Setup your hugging face account if you don't already have one. https://huggingface.co/

