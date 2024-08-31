import gensim.downloader as api
from gensim.models import Word2Vec
from gensim.similarities import WmdSimilarity

# Load the Word2Vec model
model = api.load("word2vec-google-news-300")

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

# Preprocess the bios (lowercase and split into words)
preprocessed_bios = [bio.lower().split() for bio in bios]

# Define the query bio
query_bio = "Blockchain expert | Crypto tips inside 🚀"

# Preprocess the query bio
preprocessed_query = query_bio.lower().split()

# Initialize the WMD similarity object with the corpus
instance = WmdSimilarity(preprocessed_bios, model, num_best=3)

# Find the most similar bios
similar_bios = instance[preprocessed_query]

with open("wmd_results.txt", "w") as file:
    file.write("Bios:\n")

    for bio in bios:
        file.write(f"{bio}\n")
    file.write("\n")
    file.write(f"Query Bio: {query_bio}")

    file.write("\n")
    for bio, score in similar_bios:
        file.write(f"Bio: {bio}, Score: {score}\n")
