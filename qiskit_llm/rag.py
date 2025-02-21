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

class RAG():
    def __init__(self, **kwargs):
        """
        This function may take the following arguments:
        - device: cuda device to load model on, for one GPU the default is 0
        - cache_dir: directory in which to download models
        - dataset: dataset used to create RAG knowledge base (default is Qiskit Docs)
        - chunk_size: size of chunks to split documents into
        """

        os.environ["CUDA_VISIBLE_DEVICES"] = kwargs.get("device", "0")
        self.EMBEDDING_MODEL = "Alibaba-NLP/gte-base-en-v1.5"
        self.cache_dir = kwargs.get("cache_dir", "cache/")
        self.markdown_separators = ["\n#{1,6} ", "```\n", "\n\\*\\*\\*+\n", "\n---+\n", "\n\n", "\n", " ", ""]

        # Load dataset and chunk documents
        dataset_path = kwargs.get("dataset", "chralie04/qiskit_docs")
        dataset = datasets.load_dataset(dataset_path, split="train")
        self.knowledge_base = [Document(page_content=doc["text"], metadata={"source": doc["source"]}) for doc in tqdm(dataset)]
        docs_processed = self.split_documents(kwargs.get("chunk_size", 2048))

        embedding_model = HuggingFaceEmbeddings(
            model_name=self.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu", "trust_remote_code": True},
            encode_kwargs={"normalize_embeddings": True}
        )

        # Generate vector database and reranker
        self.KNOWLEDGE_VECTOR_DB = FAISS.from_documents(
            docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE
        )
        self.RERANKER = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0", n_gpu=1)

    # Function to chunk a knowledge base
    def split_documents(self, chunk_size: int):

        # Create a text_splitter model to chunk documents
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            AutoTokenizer.from_pretrained(self.EMBEDDING_MODEL, cache_dir=self.cache_dir, trust_remote_code=True),
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size/10),
            add_start_index=True,
            strip_whitespace=True,
            separators=self.markdown_separators
        )

        docs_processed = []
        for doc in self.knowledge_base:
            docs_processed += text_splitter.split_documents([doc])

        # Ensure returned documents are unique
        unique_texts = {}
        docs_processed_unique = []
        for doc in docs_processed:
            if doc.page_content not in unique_texts:
                unique_texts[doc.page_content] = True
                docs_processed_unique.append(doc)

        return docs_processed_unique

    # Function to augment a prompt using the RAG system
    def augment(self, prompt: str, num_docs: int = 30, num_docs_final: int = 5):

        # Carry out a similarity search on the prompt for num_docs documents, and then rerank to get the best num_docs_final
        relevant_docs = self.KNOWLEDGE_VECTOR_DB.similarity_search(query=prompt, k=num_docs)
        relevant_docs = [doc.page_content for doc in relevant_docs]
        relevant_docs = self.RERANKER.rerank(prompt, relevant_docs, k=num_docs_final)
        relevant_docs = [doc["content"] for doc in relevant_docs][:num_docs_final]

        prompt = "# Prompt:\n" + prompt + "\n# Context:\n"
        prompt += "".join([f"Document {str(i)}:::\n" + doc for i,doc in enumerate(relevant_docs)])

        return prompt
    
