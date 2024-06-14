import logging
import os
import sys
from datetime import datetime
from typing import List, Set, Tuple

import chromadb
from dotenv import load_dotenv
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.base.embeddings.base import similarity
from llama_index.core.objects import ObjectIndex
from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from tools.github_search_tool import call_github_api

# takes in documents and adds them to a vector store
documents = SimpleDirectoryReader("./data").load_data()
db = chromadb.PersistentClient(path="./chroma_db")


# apply settings to LLM
llm = OpenAI(temperature=0.2, model="gpt-4", streaming=True)

# load api api_key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def create_index(documents, db):
    # create collection
    chroma_collection = db.get_or_create_collection("quickstart")

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    return index


github_search = FunctionTool.from_defaults(
    fn=call_github_api, name="github_search_tool"
)

# Create index for work resume and streams tokens
result_index = create_index(documents, db)
work_resume_engine = result_index.as_query_engine(streaming=True)
streaming_response = work_resume_engine.query(
    "Read the entirety of my resume and tell users everything in a polite manner"
)


work_resume_tool = QueryEngineTool.from_defaults(
    work_resume_engine,
    name="work_resume_tool",
    description="This tool allows you to pull information from my Work Resume",
)

all_tools = [work_resume_tool] + [github_search]


def create_agent(sys_prompt: str, all_tools: List):
    obj_index = ObjectIndex.from_objects(
        all_tools,
        index_cls=VectorStoreIndex,
    )

    agent = OpenAIAgent.from_tools(
        tool_retriever=obj_index.as_retriever(),
        verbose=True,
        system_prompt=sys_prompt,
    )

    return agent


# run the agent
def run():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    openai_agent = create_agent(
        sys_prompt="Reply in a nice manner.",
        all_tools=all_tools,
    )
    response = openai_agent.chat(
        "What projects are listed on Jon's github and give me a summary report of all of them."
    )
    print(response)
