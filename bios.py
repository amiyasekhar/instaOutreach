from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize

class Bios:
    all_bios = []  # Class variable storing bios from all instances of the Bios class
    bio_embeddings = None
    index = None  # FAISS index will be initialized later

    # Load a pre-trained multilingual sentence transformer model
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Load the Word2Vec model for WMD
    w2v_model = api.load("word2vec-google-news-300")

    # Load the stopwords from NLTK
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('english'))

    def __init__(self, bio):
        '''
        Initialize a bio object and add the bio to the class variable all_bios.
        '''
        self.bio = bio
        if self.bio != "":
            Bios.all_bios.append(bio)
    
    @classmethod
    def create_embeddings(cls):
        '''
        Creating embeddings for ALL bios we have.
        '''
        # Create embeddings
        cls.bio_embeddings = cls.model.encode(cls.all_bios)

        # Normalize the embeddings (required for cosine similarity)
        cls.bio_embeddings = cls.bio_embeddings / np.linalg.norm(cls.bio_embeddings, axis=1, keepdims=True)

        # Initialize FAISS index for cosine similarity (inner product)
        dimension = cls.bio_embeddings.shape[1]
        cls.index = faiss.IndexFlatIP(dimension)

        # Add embeddings to the index
        cls.index.add(cls.bio_embeddings)

    @classmethod
    def find_similar_bios(cls, query_bio, k=2, wmd_threshold=1.5):
        """
        Function to find the most similar bios to a given query bio using a layered approach.
        
        Parameters:
        - query_bio (str): The bio to query.
        - k (int): The number of nearest neighbors to return.
        - wmd_threshold (float): Threshold for WMD filtering.

        Returns:
        - List of tuples containing the similar bios and their similarity scores.
        """

        # First Layer: Cosine Similarity
        query_embedding = cls.model.encode([query_bio])
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        distances, indices = cls.index.search(query_embedding, len(cls.all_bios))

        # Filter out bios with low cosine similarity
        filtered_bios = [(cls.all_bios[indices[0][i]], distances[0][i]) for i in range(len(cls.all_bios)) if distances[0][i] >= 0.2]

        # Second Layer: WMD
        preprocessed_query = [word for word in word_tokenize(query_bio.lower()) if word.isalnum() and word not in cls.stop_words]
        
        similar_bios = []
        for bio, cos_sim in filtered_bios:
            preprocessed_bio = [word for word in word_tokenize(bio.lower()) if word.isalnum() and word not in cls.stop_words]
            distance = cls.w2v_model.wmdistance(preprocessed_query, preprocessed_bio)
            if distance <= wmd_threshold:
                similar_bios.append((bio, distance))
        
        # Sort by WMD distance (lower is better)
        similar_bios = sorted(similar_bios, key=lambda x: x[1])
        
        return similar_bios[:k]

    
    def __str__(self):
        return self.bio

'''
# Example usage
bios = [
    "AI-driven entrepreneur 🚀 | DM for collabs",
    "Founder @TechWaveAI | Innovating the future",
    "Crypto wizard 🔮 | Trading tips & tricks"
]

# Creating instances
bio1 = Bios(bios[0])
bio2 = Bios(bios[1])
bio3 = Bios(bios[2])

# Creating embeddings for all bios
Bios.create_embeddings()

# Find similar bios
query_bio = "Blockchain expert | Crypto tips inside 🚀"
most_similar_bios = Bios.find_similar_bios(query_bio, k=2)

print("Most similar bios:")
for bio, score in most_similar_bios:
    print(f"Bio: {bio}, WMD Distance: {score}")
'''