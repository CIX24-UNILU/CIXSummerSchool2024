Before running the notebooks, please complete the following steps. It is recommended to use a Python virtual environment, and to install Python 3.10 for running these notebooks. You can use Homebrew to install Python or pyenv, etc. The following instructions use minforge & conda, and Homebrew. If you use Windows, you can create your own virtual environment to set this up, and skip over the p7zip install. Follow the instructions for manual download in downloader.py

# Install Python (3.10) 
`brew install python@3.10`

# Install Conda
`brew install miniforge`

# Create Conda environment
`conda create -n cix-new python=3.10`

# Activate the Conda environment
`conda activate cix-new`

# Set up the notebook kernel 
1. `conda install ipykernel` 
2. `python -m ipykernel install --user --name cix-new`

# install the packages 
`pip install -r requirements.txt`

# Install 7zip for downloading the data and extracting it. 
`brew install p7zip`

# Download the training data
1. `cd downloads`
2. `python downloader.py`

# Setup your hugging face account if you don't already have one. https://huggingface.co/

# Set an OpenAI token
Open `tokens.json` and set the key "openai". 

# Questions? 
Reach out to me at <a href="mailto:mandamarie05@gmail.com">email</a>

