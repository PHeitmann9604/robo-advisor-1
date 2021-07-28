# robo-advisor-1

# Fork this remote repository under your own control, then "clone" or download your remote copy onto your local computer.

# Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

'''
cd robo-advisor-1
'''

# Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

'''
conda create -n stocks-env python=3.8
conda activate stocks-env
'''

# After activating the virtual environment, install package dependencies (see the "requirements.txt" file):

'''
pip install -r requirements.txt
'''

# After installing the requirements, create a new file titled ".env"

'''
touch .env
'''

After creating the .env folder, enter your api key under the name ALPHAVANTAGE_API_KEY = "_____" (your individual API key should be in the quotes)

# after activating the variable environment, installing all necessary packages, and entering your API key, the robo advisor is ready to run - initiate the advisor through the following command:

'''
python app/robo-advisor.py
'''

Follow the instructions and happy investing!