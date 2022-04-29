import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
parser = argparse.ArgumentParser(description="IDP Server Arguments",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e","--env", help="Select the environment to run the server in",
                    type=str,required=True,choices=['dev', 'prod'])
args = parser.parse_args()
config = vars(args)
if config['env'] == 'dev':
    env_path = Path(".") / ".env.dev"
    load_dotenv(dotenv_path=env_path)
elif config['env'] == "prod":
    env_path = Path(".") / ".env.prod"
    load_dotenv(dotenv_path=env_path)