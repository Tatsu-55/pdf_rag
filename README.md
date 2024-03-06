プロジェクトの概要

pdf.py <br>
指定したPDFファイルを解析して、テキスト・画像・テーブルの各要素を抽出して保存する
<br>
retriever.py<br>
multi vector retrieverを構築して、エンベディングと、それに対応する元の要素（上記の要素）をそれぞれベクトルストア、ドキュメントストアに
追加する
<br>
rag.py<br>
アプリ実行時に、RAGを実行して質問に対する回答を行う
<br>
main.py<br>
PDFの解析→retrieverの構築→RAGの実行を行う
<br>
app.py<br>
UIを表示する
