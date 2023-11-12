from bertopic import BERTopic
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
import umap
import matplotlib.pyplot as plt

def create_topic_model():
    umap_model = umap.UMAP(n_components=5, n_neighbors=15, min_dist=0.0)
    dbscan_model = DBSCAN(min_samples=10)

    topic_model = BERTopic(
        language="japanese",
        calculate_probabilities=False,
        verbose=True,
        nr_topics=20,
        umap_model=umap_model,
        hdbscan_model=dbscan_model
    )

    # Fix: Call fit on the topic_model
    topic_model.fit(data)  # Replace 'data' with your actual input data

    return topic_model

def visualize_topics(topic_model, top_n_topics=14, width=500):
    topics = topic_model.get_topics()
    topics = {k: v for k, v in topics.items() if k < top_n_topics}

    plt.figure(figsize=(width / 100, top_n_topics * 0.6))
    for topic, words in topics.items():
        plt.barh(str(topic), len(words))

    plt.xlabel("Word Count")
    plt.ylabel("Topic")
    plt.title("Top N Topics")
    plt.tight_layout()
    plt.savefig("topics.png")
    plt.show()

def web_ui():
    topic_model = create_topic_model()
    visualize_topics(topic_model)

if __name__ == "__main__":
    web_ui()
