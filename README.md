プロジェクトの概要

pdf.py
指定したPDFファイルを解析して、テキスト・画像・テーブルの各要素を抽出して保存する

retriever.py
multi vector retrieverを構築して、エンベディングと、それに対応する元の要素（上記の要素）をそれぞれベクトルストア、ドキュメントストアに
追加する

rag.py
アプリ実行時に、RAGを実行して質問に対する回答を行う

main.py
PDFの解析→retrieverの構築→RAGの実行を行う

app.py
UIを表示する
