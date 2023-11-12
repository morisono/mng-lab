import urllib
import untangle
import urllib.parse

def freq_graph():
    # 形態素解析
    to_mecab()
    #ストップワードよみこみ
    stop_word=slothLib.sloth()
    # Counterオブジェクトに単語をセット
    word_counter = Counter()
    for line in make_lines():
        for morpheme in line:
            if morpheme['pos'] == '動詞' or morpheme['pos'] == '名詞' or morpheme['pos'] == '形容詞':
                if len(morpheme['surface'])>3:
                    if not morpheme['surface'] in stop_word:
                    #リストに入れないと、１文字づつカウントしてしまう
                        word_counter.update([morpheme['surface']])
    # 頻度上位30語の取得
    size = 30
    #ｓｉｚｅの数だけ、上位の単語を表示する
    list_word = word_counter.most_common(size)
    print(list_word)

    # 単語（x軸用）と出現数（y軸用）のリストに分解
    list_zipped = list(zip(*list_word))
    words = list_zipped[0]
    counts = list_zipped[1]

    # グラフで使うフォント情報(デフォルトのままでは日本語が表示できない)
    fp = FontProperties(
        fname='/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf'
    )

    # 棒グラフのデータ指定
    plt.bar(
        range(0, size),     # x軸の値（0,1,2...9）
        counts,             # それに対応するy軸の値
        align='center'      # x軸における棒グラフの表示位置
    )

    # x軸のラベルの指定
    plt.xticks(
        range(0, size),     # x軸の値（0,1,2...
        words,              # それに対応するラベル
        fontproperties=fp   # 使うフォント情報
    )

    # x軸の値の範囲の調整
    plt.xlim(
        xmin=-1, xmax=size  # -1〜10（左右に1の余裕を持たせて見栄え良く）
    )

    # グラフのタイトル、ラベル指定
    plt.title(
        '37. 頻度上位30語',    # タイトル
        fontproperties=fp   # 使うフォント情報
    )
    plt.xlabel(
        '出現頻度が高い30語',# x軸ラベル
        fontproperties=fp   # 使うフォント情報
    )
    plt.ylabel(
        '出現頻度',         # y軸ラベル
        fontproperties=fp   # 使うフォント情報
    )

    # グリッドを表示
    plt.grid(axis='y')

    # 表示
    plt.show()

def sloth():
    import urllib3
    from bs4 import BeautifulSoup

    slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    http = urllib3.PoolManager()
    #↑urlib3系のおまじない
    slothlib_file =http.request('GET',slothlib_path)
    soup=BeautifulSoup(slothlib_file.data,'lxml')
    soup=str(soup).split()#soupは文字列じゃないので注意
    #SlothLibに存在しないストップワードを自分で追加↓
    mydict=['いる','内閣総理大臣','おり','ない','あり','ある','いく','なっ','する','あっ']
    soup.extend(mydict)
    return soup


if __name__ == '__main__':
    start='1'#発言の通し番号
    while start!=None:
        keyword = '安倍晋三'
        startdate='2017-01-01'
        enddate= '2018-01-01'
        meeting='予算委員会'
        #urllib.parse.quoteが日本語をコーディングしてくれる
        url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'+urllib.parse.quote('startRecord='+ start
        + '&maximumRecords=100&speaker='+ keyword
        + '&nameOfMeeting='+ meeting
        + '&from=' + startdate
        + '&until='+ enddate)
        #Get信号のリクエストの検索結果（XML）
        obj = untangle.parse(url)

        for record in obj.data.records.record:
            speechrecord = record.recordData.speechRecord
            print(speechrecord.date.cdata,
                speechrecord.speech.cdata)

            file=open('abe_2017.txt','a')
            file.write(speechrecord.speech.cdata)
            file.close()
            #一度に１００件しか帰ってこないので、開始位置を変更して繰り返しGET関数を送信
        start=obj.data.nextRecordPosition.cdata
```