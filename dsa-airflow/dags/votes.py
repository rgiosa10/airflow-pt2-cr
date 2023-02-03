import os
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook

VOTES_FILE_NAME = 'votes.csv'

flavors_choices = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]

@task
def read_file():
    """
    read votes file from a CSV

    This function uses an Airflow FileSystem Connection called "data_fs" as the root folder
    to look for the airports file. Make sure this FileSystem connection exists
    """
    # get the data_fs filesystem root path
    data_fs = FSHook(conn_id='data_fs')     # get airflow connection for data_fs
    data_dir = data_fs.get_path()           # get its root path
    print(f"data_fs root path: {data_dir}")

    # create the full path to the airports file
    file_path = os.path.join(data_dir, VOTES_FILE_NAME)
    print(f"reading file: {file_path}")

    # read csv
    df = pd.read_csv(file_path, header=0)
    votes = df.votes.values.tolist()

    valid_votes = []
    for vote in votes:
        if vote in flavors_choices:
            valid_votes.append(vote)
    
    return valid_votes

@task
def tally_votes(list_of_votes: list):
    """
    This function takes a list as an argument, and prints the item that appear the most times in that list
    """
    vote_with_count_dict = {}
    list_of_vote_options = set(list_of_votes)
    for vote_option in list_of_vote_options:
        vote_with_count_dict[vote_option] = list_of_votes.count(vote_option)
    
    highest_voted = max(vote_with_count_dict, key=vote_with_count_dict.get)

    return highest_voted



@dag(
    schedule_interval="@once",
    start_date=datetime.utcnow(),
    catchup=False,
    default_view='graph',
    is_paused_upon_creation=True,
    tags=['dsa', 'dsa-example'],
)
def cake_flavor_vote():
    """Get flavor votes and find flavor with most votes"""

    # define the file sensor...
    # wait for the airports file in the "data_fs" filesystem connection
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        poke_interval=15,                   # check every 15 seconds
        timeout=(30 * 60),                  # timeout after 30 minutes
        mode='poke',                        # mode: poke, reschedule
        filepath=VOTES_FILE_NAME,        # file path to check (relative to fs_conn)
        fs_conn_id='data_fs',               # file system connection (root path)
    )

    # read the file
    read_file_task = read_file()
    
    # orchestrate tasks
    wait_for_file >> read_file_task


# create the dag
dag = cake_flavor_vote()