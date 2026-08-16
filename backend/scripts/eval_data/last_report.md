=== RAG 检索质量评测 ===
语料     : D:\Code\notebook\backend\scripts\eval_data\corpus
标注集   : 13 个问题
chunk_size: [500, 1000]（overlap=200）
k        : [1, 2, 4]

| chunk_size | k | 语料块数 | Hit@k | Recall@k | Precision@k | MRR@k | NDCG@k |
|---|---|---|---|---|---|---|---|
| 500 | 4 | 8 | 0.846 | 0.846 | 0.269 | 0.603 | 0.671 |
| 500 | 2 | 8 | 0.769 | 0.769 | 0.462 | 0.577 | 0.627 |
| 500 | 1 | 8 | 0.385 | 0.385 | 0.385 | 0.385 | 0.385 |
| 1000 | 4 | 4 | 1.000 | 1.000 | 0.269 | 0.622 | 0.719 |
| 1000 | 2 | 4 | 0.846 | 0.846 | 0.462 | 0.577 | 0.647 |
| 1000 | 1 | 4 | 0.308 | 0.308 | 0.308 | 0.308 | 0.308 |

逐题明细（chunk_size=500, k=4）：
  [MISS] Q 1 hit=0 recall=0.00  Neptune 支持单文件最大多大？
  [OK  ] Q 2 hit=1 recall=1.00  Neptune 的数据默认存几份副本？
  [MISS] Q 3 hit=0 recall=0.00  开启版本管理后，旧版本可以回滚多久？
  [OK  ] Q 4 hit=1 recall=1.00  Neptune 兼容什么协议方便迁移？
  [OK  ] Q 5 hit=1 recall=1.00  新用户每月免费赠送多少存储容量？
  [OK  ] Q 6 hit=1 recall=1.00  上传对象成功后的响应里包含哪些字段？
  [OK  ] Q 7 hit=1 recall=1.00  下载一个不存在的对象会返回什么状态码？
  [OK  ] Q 8 hit=1 recall=1.00  列举对象时 limit 的取值范围是多少？
  [OK  ] Q 9 hit=1 recall=1.00  token 已过期时接口会返回哪个错误码？
  [OK  ] Q10 hit=1 recall=1.00  每个 token 每分钟最多可以发起多少次请求？
  [OK  ] Q11 hit=1 recall=1.00  存储桶的命名有哪些要求？
  [OK  ] Q12 hit=1 recall=1.00  Neptune 分片上传的单个分片有多大？
  [OK  ] Q13 hit=1 recall=1.00  公开对象可以通过什么 URL 访问？

（已清理本轮 eval 数据）
