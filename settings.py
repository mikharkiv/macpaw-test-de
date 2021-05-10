import configparser
import argparse

parser = argparse.ArgumentParser(description='Processes files on AWS MacPaw bucket '
											'and writes it to DB')
parser.add_argument('--profile', help='Configuration profile to use', default='default', nargs=1)
parser.add_argument('--force', help='Process all files on bucket, even if they '
					'were already processed', action='store_true')
ARGS = parser.parse_args()

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
PROFILE = config[ARGS.profile]
