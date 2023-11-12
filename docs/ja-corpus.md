# コーパス

コーパス（Corpus）は、自然言語処理や言語学の研究において広く利用される重要なリソースです。

- [国立国語研究所 - 現代日本語書き言葉均衡コーパス](http://www.kotonoha.gr.jp/)
- [NAIST Text Corpus](https://sites.google.com/site/naisttextcorpus/)
- [青空文庫](https://www.aozora.gr.jp/)
- [日本語Wikipediaのダンプデータ](https://dumps.wikimedia.org/jawiki/)
- [NII言語資源共有データベース](https://cl.nii.ac.jp/)
- [日本政府のオープンデータ](https://www.data.go.jp/)
- [gooテキスト検索API](https://labs.goo.ne.jp/api/jp/search/)
- [Yahoo!ニュースのコーパス](https://developer.yahoo.co.jp/webapi/jlp/nlp/v1/parse.html)
- [NAIST Text Corpus](https://sites.google.com/site/naisttextcorpus/)
- [京都大学テキストコーパス](https://nlp.ist.i.kyoto-u.ac.jp/index.php?KNBC)
- [名古屋大学とNICTが共同開発した辞書](http://www.cl.ecei.tohoku.ac.jp/resources/sent_lex/)
- [現代日本語書き言葉均衡コーパス](https://pj.ninjal.ac.jp/corpus_center/bccwj/)
- [日本語評判分析用意データセット](https://www.rondhuit.com/download.html#ldcc)
- [法政大学言語メディア研究所 コーパス](https://nlp.flib.hosei.ac.jp/)
- [経済産業省報告書](http://www.kyowa-u.ac.jp/laboratory/pdf/ronso18_136.pdf)
- [地方会議コーパス](http://local-politics.jp/)
- [国会会議録検索システム　検索用API](https://kokkai.ndl.go.jp/api.html)
    - [会議単位簡易出力](https://kokkai.ndl.go.jp/api/meeting_list?)
    - [会議単位出力](https://kokkai.ndl.go.jp/api/meeting)
    - [発言単位出力](https://kokkai.ndl.go.jp/api/speech?)

## Preprocess
- [Sloth lib](http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt)
- [IBM Content Analytics](https://www.ibm.com/docs/ja/wca/3.5.0?topic=dictionaries-creating-xml-file-stop-words)

```py
def stopwords(self, doc):
    """
    Get stopwords from input document.
    """
    # Judged by class
    word_class = self.word_and_class(doc)        
    ok_class = [u"名詞", u"動詞"]
    stopwords = []
    for wc in word_class:
        if not wc[1] in ok_class:
            stopwords.append(wc[0])

    # Defined by SlpothLib
    slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    slothlib_file = urllib2.urlopen(slothlib_path)
    slothlib_stopwords = [line.decode("utf-8").strip() for line in slothlib_file]
    slothlib_stopwords = [ss for ss in slothlib_stopwords if not ss==u'']

    # Merge and drop duplication
    stopwords += slothlib_stopwords
    stopwords = list(set(stopwords))

    return stopwords

def main
    slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    slothlib_file = urllib2.urlopen(slothlib_path)
    slothlib_stopwords = [line.decode("utf-8").strip() for line in slothlib_file]
    slothlib_stopwords = [ss for ss in slothlib_stopwords if not ss==u'']

    text = '日本語の自然言語処理は本当にしんどい、と彼は十回言った。'
    sw = nltkjp.stopwords(text)

    words = nltkjp.word_tokenize(text)
    print '分かち書き：'
    for w in words:
        print w,
    print
    print

    print '分かち書き(ストップワードを除去)：'
    for w in words:
        if not w in sw:
        print w,
    print

```