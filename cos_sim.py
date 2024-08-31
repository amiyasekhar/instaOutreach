from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Example bios including emojis
bios = [
    "AI-driven entrepreneur 🚀 | DM for collabs",
    "Founder @TechWaveAI | Innovating the future",
    "Crypto wizard 🔮 | Trading tips & tricks",
    "E-commerce strategist | Scaling online businesses",
    "Building the future of tech @InnovateAI",
    "AI & Blockchain enthusiast | Let’s connect!",
    "Marketing guru | Specializing in SEO & growth",
    "Founder @CryptoBoost | Blockchain is the future",
    "AI researcher | Exploring the edge of technology",
    "E-commerce expert | Growing brands globally",
    "Crypto investor | Always looking for the next big thing",
    "Digital marketing specialist | Helping brands grow",
    "Tech entrepreneur | AI & ML at the core",
    "Blockchain believer | Trading insights daily",
    "SEO expert | Boosting online visibility",
    "Founder @AIWave | Transforming industries",
    "Crypto & AI aficionado | DM for collabs",
    "Building smarter tech @NextGenAI",
    "E-commerce wizard | Scaling businesses worldwide",
    "Blockchain expert | Crypto tips inside 🚀",
    "AI innovator | Shaping the digital future",
    "Digital marketing pro | Expert in e-commerce",
    "Crypto trader | Blockchain enthusiast 💰",
    "Tech founder | AI & ML leading the way",
    "E-commerce growth strategist | Building brands",
    "Blockchain fanatic | Trading secrets revealed",
    "SEO master | Helping businesses rank higher",
    "AI startup founder | Innovating the future",
    "Crypto expert | Blockchain believer 🚀",
    "Digital marketing ninja | Scaling online stores",
    "Founder @AIRevolution | Redefining tech",
    "E-commerce specialist | Global growth strategist",
    "Blockchain and crypto enthusiast | Daily updates",
    "AI-driven entrepreneur | Building smarter tech",
    "SEO and e-commerce expert | Boosting brands",
    "Founder @CryptoInsight | Blockchain innovator",
    "Digital marketing maven | E-commerce growth",
    "AI and ML enthusiast | Shaping tomorrow",
    "Crypto investor | Blockchain trends 🚀",
    "E-commerce expert | Scaling global brands",
    "AI startup founder | Innovating with tech",
    "SEO specialist | Helping brands get noticed",
    "Blockchain believer | Crypto insights inside",
    "Tech visionary | AI & Blockchain at the core",
    "E-commerce growth hacker | Scaling worldwide",
    "Crypto trader | Blockchain enthusiast 💰🚀",
    "ceo @gyasmma dm to learn more",
    "ecommerce. crypto. AI",
    "Founder of a tech startup focusing on AI and machine learning",
    "Digital marketing expert specializing in e-commerce and SEO",
    "Blockchain enthusiast and cryptocurrency trader 💰🚀"
]

# Load a multilingual pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Create embeddings
bio_embeddings = model.encode(bios)

# Normalize the embeddings (required for cosine similarity)
bio_embeddings = bio_embeddings / np.linalg.norm(bio_embeddings, axis=1, keepdims=True)

# Ensure bio_embeddings has the correct shape
dimension = bio_embeddings.shape[1]

# Initialize FAISS index for cosine similarity (inner product)
index = faiss.IndexFlatIP(dimension)

# Add embeddings to the index
index.add(bio_embeddings)

def find_similar_bios(query_bio, k=2):
    """
    Function to find the most similar bios to a given query bio.
    
    Parameters:
    - query_bio (str): The bio to query.
    - k (int): The number of nearest neighbors to return.

    Returns:
    - List of tuples containing the similar bios and their similarity scores.
    """
    # Define a query bio and embed it
    query_embedding = model.encode([query_bio])

    # Normalize the query embedding (required for cosine similarity)
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)

    # Search for the most similar bios
    distances, indices = index.search(query_embedding, k)

    similar_bios = [(bios[indices[0][i]], distances[0][i]) for i in range(k)]
    
    return similar_bios

# Example usage
query_bio = "Blockchain expert | Crypto tips inside 🚀"
most_similar_bios = find_similar_bios(query_bio, k=3)

# print("Most similar bios:")
with open("cos_sim_results.txt", "w") as file:
    file.write("Bios:\n")

    for bio in bios:
        file.write(f"{bio}\n")
    file.write("\n")
    file.write(f"Query Bio: {query_bio}")

    file.write("\n")
    for bio, score in most_similar_bios:
        file.write(f"Bio: {bio}, Score: {score}\n")
