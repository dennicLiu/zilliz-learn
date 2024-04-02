# Zilliz-Learn
## 这是一个使用 Milvus 集群来存储和搜索聊天历史的项目，我们称之为Chat History Search。

### 功能
* 连接到 Milvus 集群
* 创建集合并插入聊天历史数据
* 为集合创建索引以加快搜索速度
* 在集合中搜索与给定文本相似的聊天历史
### 如何使用
* 克隆这个仓库到本地
* 安装依赖：运行命令 pip install -r requirements.txt
* 修改 config.py 中的配置信息
* 运行 main.py：运行命令 python main.py
### 依赖
* pymilvus：连接和操作 Milvus 集群
* requests：向文本嵌入服务发送请求来获取文本的嵌入向量
### 注意事项
* 确保你的 Milvus 集群是在线的，并且 URI 和 token 是正确的
* 确保你的文本嵌入服务是在线的，并且 URL 是正确的
* 这个项目是一个示例，可能需要根据你的实际需求进行修改和优化