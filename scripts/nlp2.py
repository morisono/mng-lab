import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster import hierarchy
import numpy as np

def process_tree(input_text, output_yaml, output_svg, structure_level, output_dendrogram='out.den.svg'):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(input_text)

    kmeans = KMeans(n_clusters=structure_level)
    kmeans.fit(X)

    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    labels = [terms[i] for i in order_centroids[:, 0]]

    structured_data = {'data': labels}
    with open(output_yaml, 'w') as outfile:
        yaml.dump(structured_data, outfile)

    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(X.toarray())

    fig, ax = plt.subplots()
    scatter = ax.scatter(reduced_data[:, 0], reduced_data[:, 1], c=kmeans.labels_, cmap='viridis')

    plt.savefig(output_svg, format='svg')

    Z = hierarchy.linkage(X.toarray(), 'ward')
    plt.figure()
    plt.title('Hierarchical Clustering Dendrogram')
    dendrogram(Z)
    plt.savefig(output_dendrogram, format='svg')


def process_scatterplot(input_text, output_yaml, output_svg, structure_level):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(input_text)

    kmeans = KMeans(n_clusters=structure_level)
    kmeans.fit(X)

    structured_data = {'data': kmeans.labels_.tolist()}
    with open(output_yaml, 'w') as outfile:
        yaml.dump(structured_data, outfile)

    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(X.toarray())

    fig, ax = plt.subplots()
    scatter = ax.scatter(reduced_data[:, 0], reduced_data[:, 1], c=kmeans.labels_, cmap='viridis')

    plt.savefig(output_svg, format='svg')

def webui():
    iface = gr.Interface(fn=visualize_clusters, inputs=["text", "number"], outputs="image")

    iface.launch()

if __name__ == '__main__':
    params = {
    'input_text': """
        これは控えめに言って有益です
        これは真面目なアドバイスなん
        これは意外と知られていませんが
        知らないだけで損してることは多い
        これはわりと真面目なアドバイスなん
        これは至って真面目なアドバイスなん
        これらは結構ウソな信じている人が多い
        これ言ったら炎上するかもしれないけど""".split('\n'),
    'output_yaml': 'out.yaml',
    'output_svg': 'out.svg',
    'structure_level': 1
    }

    # process_tree(**params)
    process_scatterplot(**params)