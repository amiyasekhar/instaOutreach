from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize

# Load the stopwords from NLTK
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Load the Word2Vec model for WMD
w2v_model = api.load("word2vec-google-news-300")

# Example bios
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

# Query bio
query_bio = "Blockchain expert | Crypto tips inside 🚀"

# First Layer: Cosine Similarity using FAISS
def first_layer_cosine_similarity_faiss(bios, query_bio, threshold=0.2):
    bio_embeddings = model.encode(bios)
    query_embedding = model.encode([query_bio])

    # Normalize embeddings to use cosine similarity
    bio_embeddings = bio_embeddings / np.linalg.norm(bio_embeddings, axis=1, keepdims=True)
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)

    # Initialize FAISS index
    dimension = bio_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(bio_embeddings)

    # Perform search
    D, I = index.search(query_embedding, len(bios))  # Search all bios

    # Filter based on the cosine similarity threshold
    filtered_bios = [(bios[I[0][i]], D[0][i]) for i in range(len(bios)) if D[0][i] >= threshold]

    return filtered_bios

# Second Layer: WMD
def second_layer_wmd(filtered_bios, query_bio):
    preprocessed_query = [word for word in word_tokenize(query_bio.lower()) if word.isalnum() and word not in stop_words]

    similar_bios = []
    for bio, _ in filtered_bios:
        preprocessed_bio = [word for word in word_tokenize(bio.lower()) if word.isalnum() and word not in stop_words]
        distance = w2v_model.wmdistance(preprocessed_query, preprocessed_bio)
        similar_bios.append((bio, distance))

    # Sort by WMD distance (lower is better)
    similar_bios = sorted(similar_bios, key=lambda x: x[1])

    return similar_bios

# Layered Approach
filtered_bios = first_layer_cosine_similarity_faiss(bios, query_bio, threshold=0.2)
similar_bios = second_layer_wmd(filtered_bios, query_bio)

# Output the results
with open("combo_sim_cos_wmd_results.txt", "w") as file:
    file.write("Bios:\n")

    for bio in bios:
        file.write(f"{bio}\n")
    file.write("\n")
    file.write(f"Query Bio: {query_bio}")

    file.write("\n")
    for bio, score in similar_bios:
        file.write(f"Bio: {bio}, Score: {score}\n")
