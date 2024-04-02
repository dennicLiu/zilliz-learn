from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import requests
import config

def connect_to_cluster():
    """连接到集群"""
    try:
        connections.connect(alias="default", uri=config.CLUSTER_ENDPOINT, token=config.TOKEN)
    except Exception as e:
        print(f"Error connecting to the cluster: {e}")

def create_collection():
    """创建集合"""
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="role", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="content_vector", dtype=DataType.FLOAT_VECTOR, dim=1536),
    ]

    schema = CollectionSchema(
        fields, description="Schema of chat history", enable_dynamic_field=True
    )

    collection = Collection(
        name=config.COLLECTION_NAME, description="Chat history recently", schema=schema
    )
    return collection

def get_text_embedding(text):
    """获取文本的嵌入向量"""
    url = "http://192.168.31.125:8001/v1/embeddings"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"input": [text], "model": "chatglm3-6b"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["data"][0]["embedding"]
    else:
        return None

def insert_data_into_collection(collection, dialogs):
    """插入数据到集合"""
    for i, dialog in enumerate(dialogs):
        dialog["content_vector"] = get_text_embedding(dialog["content"])
    collection.insert(dialogs)

def create_index_for_collection(collection):
    """为集合创建索引"""
    index_params = {"index_type": "AUTOINDEX", "metric_type": "L2", "params": {}}
    collection.create_index(
        field_name="content_vector",
        index_params=index_params,
        index_name="content_vector_index",
    )

def search_in_collection(collection, new_text):
    """在集合中搜索"""
    new_vector = get_text_embedding(new_text)
    results = collection.search(
        data=[new_vector],
        anns_field="content_vector",
        param={"metric_type": "L2", "params": {"nprobe": 12}},
        expr="user_id==2",
        output_fields=["role", "content"],
        limit=1,
    )
    return results

def main():
    connect_to_cluster()
    collection = create_collection()
    insert_data_into_collection(collection, config.dialogs)
    create_index_for_collection(collection)
    collection.load()
    results = search_in_collection(collection, "查找vue 相关问题？")
    print(results)

if __name__ == "__main__":
    main()
