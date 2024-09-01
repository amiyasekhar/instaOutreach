Project Overview
This project is designed to analyze and compare Instagram bios using various natural language processing techniques, including Cosine Similarity and Word Mover's Distance (WMD). The project consists of several scripts that interact with Instagram data, process bios, and determine the similarity between them based on pre-defined methods.
Contents
1. bios.py:
    * This script manages the Bios class, which encapsulates functionalities for bio storage, embedding creation, and similarity detection.
    * Features:
        * Bio storage and embedding using Sentence Transformers.
        * Cosine Similarity calculation with FAISS.
        * WMD calculation using Word2Vec and NLTK preprocessing.
2. combo.py:
    * Combines Cosine Similarity and WMD for a layered approach to bio comparison.
    * Process:
        * First Layer: Filters out dissimilar bios using Cosine Similarity.
        * Second Layer: Applies WMD to the filtered bios for deeper comparison.
3. cos_sim.py:
    * Focuses solely on Cosine Similarity to compare Instagram bios.
    * Process:
        * Creates bio embeddings.
        * Computes similarities using FAISS.
4. wmd.py:
    * Implements WMD for bio comparison.
    * Process:
        * Uses Word2Vec and NLTK for preprocessing and WMD calculation.
5. user.py:
    * Contains a User class for managing Instagram profiles, including fetching and storing follower/following information and bios.
    * Features:
        * Methods for setting and getting user data.
        * Interaction with Instagram APIs.
6. test.py:
    * A utility script for testing purposes.
7. instagram_page_source.txt:
    * Contains the HTML source code of an Instagram page used for analysis.
8. test.txt:
    * Contains bios extracted during testing.
9. Result Files:
    * wmd_results.txt: Results from WMD analysis.
    * cos_sim_results.txt: Results from Cosine Similarity analysis.
    * combo_sim_cos_wmd_results.txt: Results from the combined layered approach.
Installation and Setup
1. Clone the Repository: bashCopy code  git clone <repository-url>
2. cd <repository-directory>
3.   
4. Install Dependencies: Copy code  pip install -r requirements.txt
5.    The dependencies include:
    * sentence-transformers
    * faiss
    * gensim
    * nltk
6. Download NLTK Data: Copy code  python -m nltk.downloader stopwords punkt punkt_tab
7.   
8. Running the Scripts:
    * For Cosine Similarity:Copy code  python3 cos_sim.py
    *   
    * For WMD:Copy code  python3 wmd.py
    *   
    * For Combined Approach:Copy code  python3 combo.py
    *   
Explanation of Results
* Cosine Similarity Results (cos_sim_results.txt):
    * This file contains the results of comparing bios using Cosine Similarity, focusing on the vector space representation of the bios.
    * These results are fast to compute and provide a quick filter for obvious dissimilarities.
* WMD Results (wmd_results.txt):
    * This file contains the results of comparing bios using WMD, which considers the semantic meaning of words.
    * WMD is computationally expensive but provides a deep semantic comparison, ideal for nuanced bio similarities.
* Combined Approach Results (combo_sim_cos_wmd_results.txt):
    * This file contains the results from a two-layered approach where Cosine Similarity first filters out dissimilar bios, and WMD further refines the results.
Key Considerations
1. Threshold Adjustment:
    * The thresholds for Cosine Similarity and WMD can be adjusted based on the desired sensitivity of bio similarity detection.
2. Model Selection:
    * Different Sentence Transformers can be used depending on the specific use case. Experimenting with models like BERT or RoBERTa could yield different results.
3. Synonym Handling:
    * While the current setup handles semantic similarities, consider integrating additional synonym detection for more accurate comparisons.
4. Extensibility:
    * The scripts are modular and can be extended to include additional similarity measures like Jaccard or Manhattan distance if needed.
