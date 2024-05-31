# CIX24: XoT Tutorial

## Setting Up Your Environment

 Create a virtual environment (optional, but recommended). This step helps isolate the dependencies of your notebooks from the system-level Python environment.

* You will find a guide 👉 [here](https://docs.conda.io/en/latest/miniconda.html) and [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) on how to install Conda, as well as alternative methods for creating virtual environments on macOS, Windows and Linux:

### Creating a Conda Environment with Specified Packages:
1. To create a new Conda environment, open a new command prompt or terminal and use the following command:
    ```sh
    conda env create -f requirements.yml --name xot_tutorial
    ```
    Replace "xot_tutorial" with your desired environment name. This command will automatically install all the packages required for the tutorial in a new Conda environment. Once the installation is complete, you can proceed to the next step.

2. Activate the new environment:
    * On macOS/Linux:
    ```sh
    conda activate xot_tutorial
    ```

    * On Windows:
    ```sh
    activate xot_tutorial
    ```
<!-- 3. Install Requirements:

    First you need to install pipreqs library by running the following command:
    ```sh
    pip install pipreqs
    ```
    Now you can run the following command to install the required packages:

    ```sh
    pip install -r requirements.txt
    ```
    Once the installation is complete, all the packages specified in the requirements.txt file should be installed in your environment. -->


## Prepare an API Key

In this tutorial, we will be using the OpenAI API to interact with the GPT-4 model. You may use the OpenAI API or any other API that you have access to. To use the OpenAI API, you will need an API key.

First, create an [OpenAI account](https://platform.openai.com/signup) or [sign in](https://platform.openai.com/login). Next, navigate to the [API key page](https://platform.openai.com/account/api-keys) and "Create new secret key", optionally naming the key. Make sure to save this somewhere safe and do not share it with anyone.

If your organization has a subscription to the Azure OpenAI API, you can use that API key as well.

## Create an Environment File to Save Your API Key Safely in the Tutorial Directory

Create a new file named `.env` in the root directory of the tutorial. Add the following line to the file, replacing the placeholder with your actual API key:

```sh
MY_OPENAI_API_BASE="Usually 'https://api.openai.com/v1/' if you use OpenAI API"
MY_OPENAI_API_KEY="INSERT YOUR API KEY HERE"
```

Or if you use Azure OpenAI API, you can add the following line to the file, replacing the placeholder with your actual API key:

```sh
MY_AZURE_ENDPOINT="INSERT YOUR API BASE HERE"
MY_AZURE_API_KEY="INSERT YOUR API KEY"
MY_AZURE_DEPLOYMENT_NAME="INSERT YOUR DEPLOYMENT NAME"
MY_AZURE_API_VERSION="INSERT YOUR API VERSION"
```

You can run the first part of `XoT_Tutorial.ipynb`, "Prepare your OpenAI GPT Model" to test your API key.

## Running the Notebooks

We recommend using Visual Studio Code (vscode) to run the notebooks. You can install the Python and Jupyter extension pack in vscode and open the notebooks in the editor. You can then run the notebooks cell by cell.

* You will find a guide 👉 [here](https://code.visualstudio.com/docs/setup/setup-overview#_cross-platform) on how to install Visual Studio Code on your computer. You may need to follow the guide for your operating system.
* You will find a guide 👉 [here](https://code.visualstudio.com/docs/python/jupyter-support) on how to install the Python and Jupyter extension pack in vscode.
