from bertopic import BERTopic
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP
import gradio as gr

def create_topic_model():
    umap_model = UMAP(n_components=5, n_neighbors=15, min_dist=0.0)
    hdbscan_model = HDBSCAN(min_samples=10, gen_min_span_tree=True, prediction_data=True)

    topic_model = BERTopic(
        language="japanese",
        calculate_probabilities=False,
        verbose=True,
        nr_topics=20,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model
    )

    return topic_model

def visualize_topics(topic_model, top_n_topics=14, width=500):
    topic_model.visualize_barchart(top_n_topics=top_n_topics, width=width)

def web_ui():
    gr.Interface(visualize_topics,
                 inputs=[gr.inputs.Number(label="Top N Topics", default=14), gr.inputs.Number(label="Width", default=500)],
                 outputs=gr.outputs.Image(),
                 live=True).launch()

if __name__ == "__main__":
    topic_model = create_topic_model()
    web_ui()
