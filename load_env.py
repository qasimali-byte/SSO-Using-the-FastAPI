import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
parser = argparse.ArgumentParser(description="IDP Server Arguments",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e","--env", help="Select the environment to run the server in",
                    type=str,required=False,choices=['dev', 'prod'])
# args = parser.parse_args()
# config = vars(args)
config = {'env': 'heroku'}

if config['env'] == 'dev':
    env_path = Path(".") / "envs/.env.dev"
    load_dotenv(dotenv_path=env_path)
elif config['env'] == "prod":
    env_path = Path(".") / "envs/.env.prod"
    load_dotenv(dotenv_path=env_path)
elif config['env'] == "heroku":
    env_path = Path(".") / "envs/.env.h"
    load_dotenv(dotenv_path=env_path)
else:
    env_path = Path(".") / "envs/.env.dev"
    load_dotenv(dotenv_path=env_path)

# pg_restore -d d32v36qske75hi latest_dump_13_7_2022.dump -h ec2-3-219-229-143.compute-1.amazonaws.com --username rzgkwrpyrytfqy  -w 5e54fb5402d0bee5b63b6914ed99fad2ec10c1a6901f3a92bc239b5bda4f5c20
# pg_restore -d postgres://rzgkwrpyrytfqy:5e54fb5402d0bee5b63b6914ed99fad2ec10c1a6901f3a92bc239b5bda4f5c20@ec2-3-219-229-143.compute-1.amazonaws.com:5432/d32v36qske75hi latest_dump_13_7_2022.dump