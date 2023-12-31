# BrainMRI-images-classification
## 注意（warning）
* このレポジトリは、個人向けのアプリです。十分に検証された内容ではありませんので、実際の業務や診療等では使用しないようにご留意下さい。
* This repository is web application for individual usage. App is not validated enough for practical use. So do not use this for actual diagnosis.
## 問題設定
* 都市部等の一部エリアに医師が集中し、地方は医師不足に陥っている。
* 日本における放射線画像診断装置の台数は先進国の中でも多く、人口100万人あたりの台数及び単位人口あたりの撮像回数もトップの水準を誇っている。
* 撮像機器で多くの医用画像を得ることが出来ても、放射線画像を読影し、所見のレポートを作成することは放射線科医でないと難しく、専門的な知識や経験を要する。
* 少子高齢化が進行し、労働人口が減少する中で、放射線科医の不足は深刻な問題になると推測される。

## 解決策の提案
* 上記の問題を解決するために、放射線科医の業務を効率化できるようなAIモデルを作成することが解決策になり得ると考えた。
* 放射線科医が行う画像診断業務には、読影とレポート作成の二つの業務がある。
    * 読影：MRI検査などによって得られる大量の医用画像データを１スライスずつ隅々まで丁寧に確認し、所見を抽出する。
    * レポート作成：読影によって得られた知見をレポートとしてまとめる。主治医は受領した読影レポートを参考にして、最終的な診断や治療方針を決定する。
* 本アプリケーションでは、上記の二つの業務の内、読影業務を効率化することが出来ると考えている。具体的には、放射線科医は、事前に腫瘍の有無を判別することで、注目すべき医用画像の見当をつけることが出来る。

## 概要
脳のMRI画像に腫瘍が写っているのか判別するサービスです。リクエストとしてMRI画像を送ると、腫瘍の有無の判別結果を返します。
## サービス構成
<img width="600" alt="スクリーンショット 2023-12-01 21 43 21" src="https://github.com/yuki1213ya/BrainMRI-images-classification/assets/136120500/1fd3bc79-0be0-4201-ad24-8ee6a256cd45">

## ディレクトリ構成
```
.
├── Dockerfile
├── __init__.py
├── docker-compose.yml
├── models
│   ├── efficientnet_v2_m-Fold-1.onnx　 　　　　MRI画像の分類モデル（Google Driveよりダウンロードする必要あり）
│   ├── Brain-MRI-Images-classfication.ipynb　モデルを作成したnotebook（APIにおいて必要は無し）
│   └── label.json　　　　　　　　　　　　　　　　　ラベル一覧
├── requirements.txt
├── run.sh
├── sample_images
│   ├── no_1.jpg　　　　　　　　　　　　　　 　　　　サンプル画像①（腫瘍なし）　　　　　　　　　
│   ├── no_2.jpg　　　　　　　　　　　　　　 　　　　サンプル画像②（腫瘍なし）　　　　　　　　　
│   ├── yes_1.jpg　　　　　　　　　　　　　　　　　　サンプル画像①（腫瘍あり）　　　
│   └── yes_2.jpg　　　　　　　　　　　　　　　　　　サンプル画像②（腫瘍あり）　　　
└── src
    ├── __init__.py
    ├── app
    │   ├── __init__.py
    │   ├── app.py　　　　　　　　　　　　　 　　　　アプリケーションの起動
    │   └── routers
    │       ├── __init__.py
    │       └── routers.py　　　　　　　　　　　　　エンドポイントの集約
    ├── configurations.py　　　　　　　　　 　　　　アプリケーションとモデルの設定
    ├── ml
    │   ├── __init__.py
    │   └── prediction.py　　　　　　　　　　　　　　分類モデル
    └── utils
        └── logging.conf　　　　　　　　　　 　　　　ロギングの設定
```
## 環境構築
1. レポジトリをクローンする
   ```
   git clone https://github.com/yuki1213ya/BrainMRI-images-classification.git
   ```  
2. Google driveからモデルをダウンロードし、`models/`に格納します。デフォルトでは、`efficientnet_v2_m-Fold-1.onnx`を使用していますが、`Dockerfile`の環境変数と`.gitignore`の設定を変更することで、別のモデルを使用する事ができます。（URL: https://drive.google.com/drive/folders/1aouJ5f4mXFhex5Lm-5bXR8RwYOklov6X ）
   * モデル精度の一覧（評価指標：AUC）

     | モデル名 | AUC |
     | ---- | ---- |
     | efficientnet_v2_m-Fold-0.onnx | 0.9984 |
     | efficientnet_v2_m-Fold-1.onnx | 0.9996 |
     | efficientnet_v2_m-Fold-2.onnx | 0.9993 |
     | efficientnet_v2_m-Fold-3.onnx | 0.9993 |
     | efficientnet_v2_m-Fold-4.onnx | 0.9996 |

3. Docker上でサーバーを起動する
   ```
   docker-compose up
   ```
4. 起動したAPIにクライアントからリクエストを送信
   ```
   # ヘルスチェック
   curl localhost:8000/health
   # 出力
   {
     "health":"ok"
   }

   
   # メタデータ
   curl localhost:8000/metadata
   # 出力
   {
      "input_type": "torch.tensor",
      "input_structure": "(1, 3, 480, 480)",
      "prediction_type": "float32",
      "prediction_structure": "(1,2)",
      "prediction_sample": [0.8, 0.2],
   }


   # ラベル一覧
   curl localhost:8000/label
   # 出力
   {
      "0"':'WITHOUT TUMOR',
     '1':'WITH TUMOR'
   }


   # テストデータで推論リクエスト
   curl localhost:8000/predict/test
   # 出力
   {"prediction":[2.2147816913786755e-09,1.0]}


   # 確率値での推論リクエスト
   curl -X POST -H "Content-Type: application/json" -d {"image_filepath":"sample_images/サンプル画像名.jpg"}' localhost:8000/predict
   # 出力
   {"prediction":[腫瘍なしの確率, 腫瘍ありの確率]}


   # ラベルの推論リクエスト
   curl -X POST -H "Content-Type: application/json" -d {"image_filepath":"sample_images/サンプル画像名.jpg"}' localhost:8000/predict/label
   # 出力①（腫瘍ありの場合）
   {"prediction":WITH TUMOR}
   # 出力②（腫瘍なしの場合）
   {"prediction":WITHOUT TUMOR}
   
   
   ```

## 反省点
* モデル作成において、軽量なモデルから試すべきだった点
    * 今回、特徴量抽出器として、`efficientnet-v2-m`を使用しましたが、学習済みモデルの選定に関して、他のモデルと比較検討せずに進めてしまいました。APIの構造上モデルのサイズを落とした方が、処理は早くなるので、より軽量な学習済みモデルを使うべきだったと反省しています。大きなモデルを使ったことにより、良い精度が出たことはポジティブな点ですが、ややオーバースペックすぎたかもしれません。
* 評価指標にAUCを用いるべきでは無かった点
    * 学習データのクラス比率は約1:3(陰性：陽性)であるため、不均衡データと言うことが出来ます。学習データが不均衡な場合、AUCは高く出る傾向にあるため、今回のデータセットに対して、適切では無かったと反省しています。次回、モデルを作成する際には、評価指標の違いや特徴を理解した上で、熟考したいと思います。

## 参考資料
* NTTデータ, 医師の診断を効率化する画像診断AIへの期待と狙い, 2021年8月27日, https://www.nttdata.com/jp/ja/data-insight/2021/0827/
