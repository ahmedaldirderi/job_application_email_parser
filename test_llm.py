import os
import time
from spacy_llm.util import assemble
from gmail_app import GmailClient
from multiprocessing import Pool
from tqdm import tqdm

start_time = time.time()
nlp = assemble("job_config.cfg")
doc = nlp("Jack and Jill run up to the hill")
