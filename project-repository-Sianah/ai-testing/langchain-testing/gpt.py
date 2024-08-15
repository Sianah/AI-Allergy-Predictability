import os
import sys

import constants
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] = constants.APIKEY

query = sys.argv[1]  # command line input
print(query)

loader = TextLoader('resume.txt')
index = VectorstoreIndexCreator().from_loaders([loader])
print(index.query(query))
