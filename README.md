# 最低限の顧客管理システム
> このプロジェクトは Docker × FastAPI × ポスグレDB のAPIの初期テンプレートになればいいなという構想で作成したものです。<br>
> リポジトリをForkしてカスタムしましょう！<br>
> ※100%AI生成なので業界標準のコーディングではない部分が存在するかもしれません。私はDockerとFastAPIの勉強中なので判断できません。

Issue、Pull request大歓迎です！

## 概要

このプロジェクトは、FastAPIを使用した顧客情報管理のためのRESTful APIシステムです。<br>
PostgreSQLデータベースを使用してデータを保存し、Dockerを利用して環境を簡単に構築できるようになっています。

## 機能

このAPIは以下の機能を提供します：

1. 顧客情報の取得（一覧・個別）
2. 新規顧客の登録
3. 既存顧客情報の更新
4. 顧客情報の削除

## システム構成

このシステムは以下の主要なコンポーネントで構成されています：

1. **FastAPI**: Pythonベースの高速なWeb APIフレームワーク
2. **PostgreSQL**: 関係データベース管理システム
3. **SQLAlchemy**: PythonのORMツール
4. **Docker**: コンテナ化プラットフォーム

## ファイル構成と役割

1. `Dockerfile`: Pythonアプリケーションのコンテナイメージを定義
2. `docker-compose.yml`: マルチコンテナDockerアプリケーションの定義と設定
3. `requirements.txt`: Pythonの依存パッケージリスト
4. `app/main.py`: FastAPIアプリケーションのメインエントリーポイント、APIエンドポイントの定義
5. `app/database.py`: データベース接続の設定
6. `app/models.py`: SQLAlchemyのORMモデル定義
7. `app/schemas.py`: Pydanticモデル（リクエスト/レスポンスのスキーマ）定義
8. `app/crud.py`: データベース操作関数（Create, Read, Update, Delete）

## API仕様

### 顧客一覧の取得
- エンドポイント: GET /customers/
- パラメータ: 
  - skip: スキップする顧客数（オプション、デフォルト: 0）
  - limit: 取得する顧客数の上限（オプション、デフォルト: 10）

### 個別顧客情報の取得
- エンドポイント: GET /customers/{customer_id}
- パラメータ:
  - customer_id: 取得する顧客のID

### 顧客情報の作成・更新・削除
- エンドポイント: POST /customers/
- リクエストボディ: CustomerCreateスキーマ
  - id: 顧客ID（新規作成時はNull）
  - name: 顧客名
  - phone_number: 電話番号
  - birth_date: 生年月日
  - delete_flag: 削除フラグ（削除時にTrue）

## データベース構造

顧客テーブル（customers）:
- id: 整数型、主キー
- name: 文字列型、インデックス付き
- phone_number: 文字列型、インデックス付き
- birth_date: 日付型

## セットアップ手順（Windows）

1. Docker Desktopをインストールします。

2. このプロジェクトのリポジトリをクローンまたはダウンロードします。

3. コマンドプロンプトを開き、プロジェクトのルートディレクトリに移動します：
   ```
   cd path\to\project
   ```

4. 以下のコマンドを実行してシステムを起動します：
   ```
   start.bat
   ```

5. システムが起動したら、ブラウザで `http://localhost:8000/docs` にアクセスし、Swagger UIでAPIドキュメントを確認できます。

## 使用方法

Swagger UIまたは任意のAPIクライアント（Postman等）を使用して、各エンドポイントにリクエストを送信できます。

例：
- 顧客一覧の取得: GET http://localhost:8000/customers/
- 個別顧客情報の取得: GET http://localhost:8000/customers/1
- 新規顧客の作成: POST http://localhost:8000/customers/
  ```json
  {
    "name": "山田太郎",
    "phone_number": "090-1234-5678",
    "birth_date": "1990-01-01"
  }
  ```

## Docker設定の解説

### Dockerfile

Dockerfileは、アプリケーションのコンテナイメージを作成するための指示書です。


```1:10:Dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


1. `FROM python:3.11`: Python 3.11の公式イメージを基にします。
2. `WORKDIR /app`: コンテナ内の作業ディレクトリを `/app` に設定します。
3. `COPY requirements.txt .`: ホストの `requirements.txt` をコンテナにコピーします。
4. `RUN pip install ...`: 必要なPythonパッケージをインストールします。
5. `COPY . /app`: プロジェクトの全ファイルをコンテナの `/app` ディレクトリにコピーします。
6. `CMD [...]`: コンテナ起動時に実行されるコマンドを指定します。

### docker-compose.yml

docker-compose.ymlは、複数のDockerコンテナを定義し、それらの関係を管理します。


```1:27:project/docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/customer_db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: customer_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

```


1. `services`: このプロジェクトで使用するサービス（コンテナ）を定義します。

2. `web` サービス:
   - `build: .`: カレントディレクトリのDockerfileを使用してイメージをビルドします。
   - `ports: - "8000:8000"`: ホストの8000番ポートをコンテナの8000番ポートにマッピングします。
   - `depends_on: - db`: データベースサービスが起動してから、このサービスを開始します。
   - `environment`: データベース接続情報を環境変数として設定します。
   - `command`: コンテナ起動時に実行されるコマンドを指定します。

3. `db` サービス:
   - `image: postgres:15`: PostgreSQL 15の公式イメージを使用します。
   - `environment`: PostgreSQLの設定（ユーザー名、パスワード、データベース名）を指定します。
   - `ports: - "5432:5432"`: ホストの5432番ポートをコンテナの5432番ポートにマッピングします。
   - `volumes`: データの永続化のために、ホストのボリュームをコンテナにマウントします。

4. `volumes`: 名前付きボリューム `postgres_data` を定義し、データベースデータを永続化します。

これらの設定により、アプリケーションとデータベースが別々のコンテナで動作し、ホストマシンから適切にアクセスできるようになります。<br>
ポートマッピングにより、ホストマシンのブラウザやAPIクライアントからアプリケーションにアクセスでき、データの永続化により、コンテナを停止してもデータが失われません。

## 注意事項

- このシステムはローカル開発環境用です。本番環境で使用する場合は、セキュリティ設定の見直しが必要です。
- データベースの永続化はDockerボリュームを使用しています。コンテナを削除してもデータは保持されます。

## トラブルシューティング

- ポートの競合が発生した場合は、`docker-compose.yml`ファイルでポート設定を変更してください。
- データベース接続エラーが発生した場合は、`DATABASE_URL`環境変数が正しく設定されているか確認してください。
