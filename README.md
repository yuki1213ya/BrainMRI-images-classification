# BrainMRI-images-classification
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
│   ├── efficientnet_v2_m-Fold-1.onnx　 MRI画像の分類モデル（Google Driveよりダウンロードする必要あり）
│   └── label.json　　　　　　　　　　　　　ラベル一覧
├── requirements.txt
├── run.sh
├── sample_images
│   ├── no_1.jpg　　　　　　　　　　　　　　 サンプル画像①（腫瘍なし）　　　　　　　　　
│   ├── no_2.jpg　　　　　　　　　　　　　　 サンプル画像②（腫瘍なし）　　　　　　　　　
│   ├── yes_1.jpg　　　　　　　　　　　　　　サンプル画像①（腫瘍あり）　　　
│   └── yes_2.jpg　　　　　　　　　　　　　　サンプル画像②（腫瘍あり）　　　
└── src
    ├── __init__.py
    ├── app
    │   ├── __init__.py
    │   ├── app.py　　　　　　　　　　　　　 アプリケーションの起動
    │   └── routers
    │       ├── __init__.py
    │       └── routers.py　　　　　　　　　エンドポイントの集約
    ├── configurations.py　　　　　　　　　 アプリケーションとモデルの設定
    ├── ml
    │   ├── __init__.py
    │   └── prediction.py　　　　　　　　　　分類モデル
    └── utils
        └── logging.conf　　　　　　　　　　 ロギングの設定
```
## 環境構築
1. レポジトリをクローンする
   ```
   git clone https://github.com/yuki1213ya/BrainMRI-images-classification.git
   ```  
2. Google driveからモデルをダウンロードし、`models/`に格納します。デフォルトでは、`efficientnet_v2_m-Fold-1.onnx`を使用していますが、`Dockerfile`の環境変数と`.gitignore`の設定を変更することで、別のモデルを使用する事ができます。（URL: https://drive.google.com/drive/folders/1aouJ5f4mXFhex5Lm-5bXR8RwYOklov6X）
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
