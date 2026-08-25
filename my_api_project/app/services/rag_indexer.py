import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import chromadb
from chromadb.utils import embedding_functions

# 使用本地 embedding 模型（支持中文）
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# 持久化客户端
client = chromadb.PersistentClient(path="./chroma_db")

# 获取或创建 collection
collection = client.get_or_create_collection(
    name="battle_knowledge",
    embedding_function=embedding_fn
)

def index_documents(folder_path="./data"):
    """读取 data 目录下的所有 .txt 文件，分块存入向量库"""
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹 {folder_path} 不存在，请创建并放入知识文档")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        print(f"❌ {folder_path} 中没有 .txt 文件")
        return

    total_chunks = 0
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # 按段落切分（过滤空行和过短的段）
        chunks = [chunk.strip() for chunk in content.split('\n\n') if len(chunk.strip()) > 50]
        for i, chunk in enumerate(chunks):
            doc_id = f"{filename}_{i}"
            collection.add(
                documents=[chunk],
                ids=[doc_id],
                metadatas=[{"source": filename}]
            )
            total_chunks += 1
        print(f"✅ {filename}: 切分为 {len(chunks)} 块")
    print(f"🎉 总计索引 {total_chunks} 个文档块")

if __name__ == "__main__":
    index_documents()