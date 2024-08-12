import pandas as pd
from tqdm import tqdm
from typing import Optional, List, Tuple
import datasets
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from ragatouille import RAGPretrainedModel

EMBEDDING_MODEL = "Alibaba-NLP/gte-base-en-v1.5"
cache_dir = "chralie04/"

MARKDOWN_SEPARATORS = [
  "\n#{1,6} ",
  "```\n",
  "\n\\*\\*\\*+\n",
  "\n---+\n",
  "\n\n",
  "\n",
  " ",
  "",
]

ds = datasets.load_dataset("chralie04/qiskit_docs", split="train")

KNOWLEDGE_BASE = [
  Document(page_content=doc["text"], metadata={"source": doc["source"]}) for doc in tqdm(ds)
]

# Chunking

def split_documents(
  chunk_size: int,
  knowledge_base: List[Document],
  tokenizer_name: Optional[str] = EMBEDDING_MODEL,
  ) -> List[Document]:

  text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    AutoTokenizer.from_pretrained(tokenizer_name, cache_dir=cache_dir, trust_remote_code=True),
    chunk_size=chunk_size,
    chunk_overlap=int(chunk_size / 10),
    add_start_index=True,
    strip_whitespace=True,
    separators=MARKDOWN_SEPARATORS
  )

  docs_processed = []
  for doc in knowledge_base:
    docs_processed += text_splitter.split_documents([doc])

  unique_texts = {}
  docs_processed_unique = []
  for doc in docs_processed:
    if doc.page_content not in unique_texts:
      unique_texts[doc.page_content] = True
      docs_processed_unique.append(doc)
  return docs_processed_unique

docs_processed = split_documents(
  2048,
  KNOWLEDGE_BASE,
  tokenizer_name=EMBEDDING_MODEL
)

# Vector DB

embedding_model = HuggingFaceEmbeddings(
  model_name=EMBEDDING_MODEL,
  model_kwargs={"device": "cuda", "trust_remote_code": True},
  encode_kwargs={"normalize_embeddings": True}
)

KNOWLEDGE_VECTOR_DATABASE = FAISS.from_documents(
  docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE
)

# LLM Reader model

RERANKER = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0", n_gpu=3)

def answer_with_rag(
  question: str,
  knowledge_index: FAISS,
  reranker: Optional[RAGPretrainedModel] = None,
  num_retrieved_docs: int = 30,
  num_docs_final: int = 5
  ) -> Tuple[str, List[Document]]:
  
  relevant_docs = knowledge_index.similarity_search(query=question, k=num_retrieved_docs)
  relevant_docs = [doc.page_content for doc in relevant_docs]

  if reranker:
    relevant_docs = reranker.rerank(question, relevant_docs, k=num_docs_final)
    relevant_docs = [doc["content"] for doc in relevant_docs]

  relevant_docs = relevant_docs[:num_docs_final]

  prompt = "# Prompt:\n" + question + "\n# Context:\n"
  prompt += "".join([f"Document {str(i)}:::\n" + doc for i, doc in enumerate(relevant_docs)])

  print(prompt)

question = """
from qiskit import QuantumCircuit

\"\"\" Write a function that creates a quantum circuit that prepares a Bell state using two qubits.
Returns:
  QuantumCircuit: The quantum circuit that prepares the Bell state
\"\"\"

"""

answer_with_rag(question, KNOWLEDGE_VECTOR_DATABASE, reranker=RERANKER)
