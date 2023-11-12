import yaml
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import gradio as gr

# 入力テキスト
input_text = """
これは控えめに言って有益です
これは真面目なアドバイスなん
これは意外と知られていませんが
知らないだけで損してることは多い
これはわりと真面目なアドバイスなん
これは至って真面目なアドバイスなん
これらは結構ウソな信じている人が多い
これ言ったら炎上するかもしれないけど
"""

# クラスタリング関数
def cluster_text(input_text, method='KMeans', n_clusters=2):
    # テキストの前処理
    # ここで適切な形態素解析やトークナイゼーションを行うことができます
    # input_textを処理して、文を単語またはフレーズに分割します

    # 特徴ベクトルの抽出と次元削減
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(input_text)
    X_tsne = TSNE(n_components=2).fit_transform(X)

    # クラスタリング
    if method == 'KMeans':
        model = KMeans(n_clusters=n_clusters)
    else:
        # 他のクラスタリングアルゴリズムを使用できます
        pass

    labels = model.fit_predict(X)

    # 結果の描画（クラスタリング散布図）
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='rainbow')
    plt.savefig('cluster_plot.png')

    # 結果をYAMLで出力
    result = {'input_text': input_text, 'cluster_labels': labels.tolist()}
    with open('output.yaml', 'w') as yaml_file:
        yaml.dump(result, yaml_file)

# クラスタリング実行
cluster_text(input_text)

# Gradioでクラスタリング散布図を表示
def visualize_clusters(input_text, n_clusters):
    cluster_text(input_text, n_clusters=n_clusters)
    return 'cluster_plot.png'

iface = gr.Interface(fn=visualize_clusters, inputs=["text", "number"], outputs="image")
iface.launch()
