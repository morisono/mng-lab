from janome.tokenizer import Tokenizer
import yaml
import argparse
import gradio as gr
import networkx as nx
# import neologdn
# import unicodedata
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from collections import deque
import matplotlib.font_manager
from matplotlib.colors import ListedColormap
from collections import Counter
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
import spacy
import sentencepiece as spm

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def word_frequency(text):
    tokens = tokenize_sentence(text)
    word_counts = Counter(token.surface for token in tokens if token.part_of_speech.split(',')[0] == '名詞')

    for word, count in word_counts.items():
        print(f'{word}: {count}')

def generate_2d_map(text):
    # テキストを単語のリストにトークン化
    tokens = tokenize_sentence(text)
    words = [token.surface for token in tokens]

    # 単語をベクトル化
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([' '.join(words)])

    # TF-IDF変換
    transformer = TfidfTransformer()
    X_tfidf = transformer.fit_transform(X)

    # t-SNEによる2次元マップ生成
    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X_tfidf.toarray())

    # プロット
    plt.figure(figsize=(10, 8))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], marker='o')
    for i, word in enumerate(words):
        plt.annotate(word, xy=(X_tsne[i, 0], X_tsne[i, 1]), fontsize=8)
    plt.show()

def dependency_analysis(text):
    nlp = spacy.load("ja_ginza")

    doc = nlp(text)

    for sent in doc.sents:
        print(f'Sentence: {sent.text}')
        for token in sent:
            print(f'  {token.text}: {token.dep_} -> {token.head.text}')
        print('---')


def hierarchical_clustering(text):
    # テキストを単語のリストにトークン化
    tokens = tokenize_sentence(text)
    words = [token.surface for token in tokens]

    # 単語をベクトル化
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([' '.join(words)])

    # 階層的クラスタリング
    clustering = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    labels = clustering.fit_predict(X.toarray())

    # 結果表示
    for label, word in zip(labels, words):
        print(f'{word}: Cluster {label + 1}')

def cooccurrence_network(data, out_path):
    # font = {
    # 'family' : ['IPAexGothic', 'Meiryo', 'MS Mincho'],
        # 'style': normal,
        # 'variant': normal,
        # 'weight': normal,
        # 'stretch': normal,
    # }
    # matplotlib.rc('font', **font)
    G = nx.DiGraph()
    queue = deque([(key, values) for key, values in data.items()])

    while queue:
        key, values = queue.popleft()
        if values is not None:
            for value in values:
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        G.add_edge(key, sub_key)
                        queue.append((sub_key, sub_value))
                else:
                    G.add_edge(key, value)

    pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')

    plt.figure(figsize=(8, 6))

    # edge_alpha = np.amin([value*10,1])
    edge_opt = {
        'arrowstyle': '->',
        'arrowsize': 10,
        'width': 2,
        # 'alpha': edge_alpha
        'alpha': 0.5
    }

    node_sizes = [1.2 ** G.out_degree(n) * 300 for n in G.nodes]
    node_opt = {
        'node_color':'blue',
        'node_size': node_sizes,
        'alpha':0.2,
    }

    label_opt = {
        'font_size': 18
    }

    nx.draw_networkx_edges(G, pos, **edge_opt)
    nx.draw_networkx_nodes(G, pos, **node_opt)
    nx.draw_networkx_labels(G, pos, **label_opt)

    plt.axis('off')
    plt.savefig(out_path, format='svg')
    plt.close()

    return out_path

def tokenize_sentence(text):
    t = Tokenizer()
    tokens = list(t.tokenize(text))

    # テキストデータのパス
    # input_file = "path/to/your/text_data.txt"

    # # モデルの学習
    # spm.SentencePieceTrainer.train(input=f"--input={input_file} --model_prefix=mymodel --vocab_size=8000")

    # sp = spm.SentencePieceProcessor()
    # sp.load("mymodel.model")

    # text = "これはサンプルテキストです。"
    # tokens = sp.encode_as_pieces(text)

    print(tokens)

    return tokens

def hierarchical_structure(tokens):
    if not tokens:
        return None

    token = tokens[0]
    remaining_tokens = tokens[1:]

    token_data = {
        token.surface: hierarchical_structure(remaining_tokens)
    }

    return token_data

def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()

    for key, value in dict2.items():
        if key in dict1:
            if isinstance(dict1[key], list) and isinstance(value, list):
                merged_dict[key] = dict1[key] + value
            elif isinstance(dict1[key], dict) and isinstance(value, dict):
                merged_dict[key] = merge_dicts(dict1[key], value)
        else:
            merged_dict[key] = value

    return merged_dict

def process_text(text):
    sentences = text.split('\n') # TODO

    result = []

    for sentence in sentences:
        tokens = tokenize_sentence(sentence)
        sentence_structure = hierarchical_structure(tokens)
        if result:
            result[-1] = merge_dicts(result[-1], sentence_structure)
        else:
            result.append(sentence_structure)

        yaml_output = yaml.dump({'items': result}, allow_unicode=True)
    return yaml_output

def webui():
    def update(input_file, text, preview):
        out_path = 'out.txt'
        out_path_svg = 'graph.svg'

        if input_file:
            with open(input_file.name, 'r') as file:
                text = file.read() + text
        print(text, preview)
        out_content = process_text(text)
        with open(out_path, 'w') as file:
            file.write(out_content)

            if preview:
                out_path_svg = cooccurrence_network(yaml.safe_load(out_content), out_path_svg)
                return [
                    gr.File.update(out_path),
                    gr.Image.update(out_path_svg),
                    gr.Code.update(out_content)
                ]

            else:
                return [
                    gr.File.update(out_path),
                    gr.Image.update(''),
                    gr.Code.update('')
                ]

    inputs = [
        gr.File(),
        gr.TextArea(),
        gr.Checkbox()
    ]

    outputs = [
        gr.File(),
        gr.Image(),
        gr.Code(language='yaml', )
        # gr.TextArea(max_lines=20)
    ]

    examples = [
        [None, 'Hello, world. \nThis is example. \nHello, beautiful world.', True],
        ['data/demo1.txt', '', True],
        ['data/demo1.txt', 'Hello, world. \nThis is example. \nHello, beautiful world.', True],
    ]

    gr.Interface(update,
        title='Demo',
        description='Please input data to the light area.',
        inputs=inputs,
        outputs=outputs,
        examples=examples,
        # outputs=gr.TextArea(),
        live=False
    ).launch()

    # inputs[0:].change(update, inputs, outputs)

def main():
    parser = argparse.ArgumentParser(description='Process text and output YAML')
    parser.add_argument('-i', '--input_text', help='Input text to process')
    parser.add_argument('--webui', action='store_true', help='Launch webui')

    args = parser.parse_args()
    if args.input_text:
        with open(args.input_text, 'r') as file:

            if args.input_text.endswith('.yaml'):
                yaml_content = yaml.safe_load(file)
                sentence = "\n".join([str(item) for item in yaml_content['items']])
                result = process_text(sentence)
            else:
                result = process_text(file.read())

        print(result)

    elif args.webui:
        webui()

    else:
        print('error!')

if __name__ == "__main__":
    main()