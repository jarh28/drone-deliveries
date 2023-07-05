# Welcome to: DroneDeliveries
Hello! In this project I built a REST API for managing medication shipping by drones. So, I hope you enjoy reading this code or at least it can be useful for you. :D

## Setting up the environment
First, you need to install `python` and `pip` in your computer. Follow these links to offical websites for [python installation](https://www.python.org/downloads/) and [pip installation](https://pip.pypa.io/en/stable/installation/). Once installations had been done just run the following command in a terminal:

    pip install -r requirements.txt

Notice that you should open the terminal at the project root directory. Last but not least, I use the version 3.9 of python so I strongly recommend you to use the same. 

If you prefer to use `Anaconda`, it's fine. You can download from [here](https://docs.anaconda.com/free/anaconda/install/index.html). Once `Anaconda` is installed, create a new clean environment and install all of the dependencies.

    conda create -n <environment-name> python=3.9 pip

Once created, just run the same `pip` command to install `requirements.txt`.

## Starting the server
Open a terminal at the project root directory and type the following command:

    uvicorn app:app --reload

## Running the tests
Open a terminal at the project root directory and type the following command:

    python -m unittest discover -p 'test_*.py'


## Generate the Database
I used a SQLite database so you do not need to install a database server. If for some reason you need to generate again the database you just need to run the script `generate_db.py` with `python`.

    python generate_db.py
