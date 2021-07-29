# robo-advisor-1

## Prerequisites

    + Anaconda 3.7+
    + Python 3.7+
    + Pip

## Installation

Fork this remote repository [remote repository](https://github.com/PHeitmann9604/robo-advisor-1)  under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

'''sh
cd robo-advisor-1
'''

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

'''sh
conda create -n stocks-env python=3.8
conda activate stocks-env
'''

After activating the virtual environment, install package dependencies (see the "requirements.txt" file):

'''sh
pip install -r requirements.txt
'''

After installing the requirements, create a new file titled ".env"

'''sh
touch .env
'''

After creating the .env folder, enter your api key under the name ALPHAVANTAGE_API_KEY = "_____" (your individual API key should be in the quotes)

After activating the variable environment, installing all necessary packages, and entering your API key, the robo advisor is ready to run - initiate the advisor through the following command:

'''sh
python app/robo-advisor.py
'''

Follow the instructions and happy investing!