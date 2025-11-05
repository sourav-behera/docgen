import os
import git
import logging

from indexer import run_indexer
from doc_generator import doc_generator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# TMP_DIR: str = os.path.join("..", "tmp")
TMP_DIR: str = "tmp"

def validate_repo_url(repo_url: str) -> bool:
    if repo_url.startswith("http://") or repo_url.startswith("https://") or repo_url.startswith("git@"):
        logger.info(f"Valid repository URL: {repo_url}")
        return True
    else:
        logger.error(f"Invalid repository URL: {repo_url}")
        return False

def get_repo_name(repo_url: str) -> str:
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    logger.info(f"Extracted repository name: {repo_name}")
    return repo_name

def clone_or_pull(repo_url: str):
    logger.info(f"Cloning or pulling repository from {repo_url}")
    repo_name = get_repo_name(repo_url)
    repo_path = os.path.join(TMP_DIR, repo_name)
    if validate_repo_url(repo_url) is True:
        logger.error("Aborting clone or pull due to invalid repository URL.")
        if not os.path.exists(TMP_DIR):
            logger.info(f"Clonning repository to {repo_path}")
            git.Repo.clone_from(repo_url, repo_path)
            logger.info(f"Repository cloned to {repo_path}")
        elif os.path.exists(repo_path):
            logger.info(f"Pulling latest changes in repository at {repo_path}")
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            logger.info(f"Repository at {repo_path} updated with latest changes")
        run_indexer()
        doc_generator(repo_path, os.path.join("tmp", "gameOfLife.gl", "src", "main.cpp"),"src") 
    else:
        logger.error("Aborting clone or pull due to invalid repository URL.")
        return