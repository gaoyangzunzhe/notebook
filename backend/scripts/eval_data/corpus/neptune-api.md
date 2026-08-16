# Neptune REST API 参考

所有 API 请求的基准地址为 https://api.neptune.example.com/v1。请求与响应均使用 JSON 格式。

## 身份认证

在 HTTP 头中携带 Authorization: Bearer <token> 进行认证。token 在控制台创建，最长有效期 30 天。

## 上传对象

POST /objects

请求体为 multipart/form-data，包含两个字段：file 与 bucket。file 是要上传的文件内容，bucket 是目标存储桶名称。

上传成功后返回 201，响应体包含 object_id 和 version。object_id 是对象的唯一标识，长度为 24 位十六进制字符串。

## 下载对象

GET /objects/{object_id}

下载时需要携带参数 bucket 指明所属存储桶。响应返回文件二进制内容。如果对象不存在，返回 404；如果对象存在但未开启下载权限，返回 403。

## 列举对象

GET /objects

返回当前存储桶内的对象列表，分页参数为 limit 和 offset。limit 的取值范围是 1 到 1000，默认 100。列表按创建时间倒序排列。

## 删除对象

DELETE /objects/{object_id}

删除后对象不可恢复。如需保留历史版本，请先开启版本管理。

## 对象标签

可以为对象附加最多 10 个标签，每个标签为 key=value 形式。标签用于批量管理与筛选，不参与检索。

设置标签的接口为 PUT /objects/{object_id}/tags，请求体是 JSON 对象。修改标签不会改变对象的内容和版本号。

## 分享链接

GET /objects/{object_id}/share 可以生成一个带时效的分享链接。有效期可选 1 小时、1 天或 7 天，到期后链接自动失效。

## 错误码

常见的错误码如下：

400：请求参数不合法。

401：认证失败，token 缺失或已过期。

403：权限不足，无法执行该操作。

404：资源不存在。

429：请求过于频繁，已被限流。

500：服务内部错误。

限流规则是每个 token 每分钟最多 6000 次请求，超过后返回 429。
