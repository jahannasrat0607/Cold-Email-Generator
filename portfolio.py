import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Connect to a running ChromaDB server (no PersistentClient!)
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)

        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
