import argparse
import logging
from git_operations import clone_or_pull

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cli_main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description="Documentation Generation Tool")
    parser.add_argument('--repo', type=str, required=True, help='Path to the repository')

    args = parser.parse_args()
    if args.repo:
        logger.info(f"Processing repository: {args.repo}")
        clone_or_pull(args.repo)
    else:
        parser.print_help()
        logger.error("No repository URL provided.")