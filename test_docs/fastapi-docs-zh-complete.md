

---

# Source: docs/_llm-test.md


# LLM 测试文件 { #llm-test-file }

本文用于测试用于翻译文档的 <abbr title="Large Language Model - 大型语言模型">LLM</abbr> 是否理解 `scripts/translate.py` 中的 `general_prompt` 以及 `docs/{language code}/llm-prompt.md` 中的语言特定提示。语言特定提示会追加到 `general_prompt` 之后。

这里添加的测试会被所有语言特定提示的设计者看到。

用法如下：

* 准备语言特定提示——`docs/{language code}/llm-prompt.md`。
* 将本文重新翻译为你的目标语言（例如使用 `translate.py` 的 `translate-page` 命令）。这会在 `docs/{language code}/docs/_llm-test.md` 下创建翻译。
* 检查翻译是否正确。
* 如有需要，改进你的语言特定提示、通用提示，或英文文档。
* 然后手动修正翻译中剩余的问题，确保这是一个优秀的译文。
* 重新翻译，在已有的优秀译文基础上进行。理想情况是 LLM 不再对译文做任何更改。这意味着通用提示和你的语言特定提示已经尽可能完善（有时它仍会做一些看似随机的改动，原因是[LLM 不是确定性算法](https://doublespeak.chat/#/handbook#deterministic-output)）。

测试如下：

## 代码片段 { #code-snippets }

//// tab | 测试

这是一个代码片段：`foo`。这是另一个代码片段：`bar`。还有一个：`baz quux`。

////

//// tab | 信息

代码片段的内容应保持不变。

参见 `scripts/translate.py` 中通用提示的 `### Content of code snippets` 部分。

////

## 引号 { #quotes }

//// tab | 测试

昨天，我的朋友写道："如果你把 incorrectly 拼对了，你就把它拼错了"。我回答："没错，但 'incorrectly' 错的不是 '"incorrectly"'"。

/// note | 注意

LLM 很可能会把这段翻错。我们只关心在重新翻译时它是否能保持修正后的译文。

///

////

//// tab | 信息

提示词设计者可以选择是否将中性引号转换为排版引号。也可以保持不变。

例如参见 `docs/de/llm-prompt.md` 中的 `### Quotes` 部分。

////

## 代码片段中的引号 { #quotes-in-code-snippets }

//// tab | 测试

`pip install "foo[bar]"`

代码片段中的字符串字面量示例：`"this"`，`'that'`。

一个较难的字符串字面量示例：`f"I like {'oranges' if orange else "apples"}"`

硬核：`Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | 信息

... 但是，代码片段内的引号必须保持不变。

////

## 代码块 { #code-blocks }

//// tab | 测试

一个 Bash 代码示例...

```bash
# 向宇宙打印问候
echo "Hello universe"
```

...以及一个控制台代码示例...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...以及另一个控制台代码示例...

```console
// 创建目录 "Code"
$ mkdir code
// 切换到该目录
$ cd code
```

...以及一个 Python 代码示例...

```Python
wont_work()  # 这不会起作用 😱
works(foo="bar")  # 这可行 🎉
```

...就这些。

////

//// tab | 信息

代码块中的代码不应被修改，注释除外。

参见 `scripts/translate.py` 中通用提示的 `### Content of code blocks` 部分。

////

## 选项卡与彩色提示框 { #tabs-and-colored-boxes }

//// tab | 测试

/// note | 注意
一些文本
///

/// note | 技术细节
一些文本
///

/// tip | 提示
一些文本
///

/// warning | 警告
一些文本
///

/// danger | 危险
一些文本
///

////

//// tab | 信息

选项卡以及 `Info`/`Note`/`Warning`/等提示块，应在竖线（`|`）后添加其标题的翻译。

参见 `scripts/translate.py` 中通用提示的 `### Special blocks` 与 `### Tab blocks` 部分。

////

## Web 与内部链接 { #web-and-internal-links }

//// tab | 测试

链接文本应被翻译，链接地址应保持不变：

* [链接到上面的标题](#code-snippets)
* [内部链接](index.md#installation)
* [外部链接](https://sqlmodel.tiangolo.com/)
* [样式链接](https://fastapi.tiangolo.com/css/styles.css)
* [脚本链接](https://fastapi.tiangolo.com/js/logic.js)
* [图片链接](https://fastapi.tiangolo.com/img/foo.jpg)

链接文本应被翻译，且链接地址应指向对应的译文页面：

* [FastAPI 链接](https://fastapi.tiangolo.com/zh/)

////

//// tab | 信息

链接的文本应被翻译，但地址保持不变。唯一的例外是指向 FastAPI 文档页面的绝对链接，此时应指向对应语言的译文。

参见 `scripts/translate.py` 中通用提示的 `### Links` 部分。

////

## HTML "abbr" 元素 { #html-abbr-elements }

//// tab | 测试

这里有一些包裹在 HTML "abbr" 元素中的内容（有些是虚构的）：

### abbr 提供了完整短语 { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - 尽管去做">GTD</abbr>
* <abbr title="less than - 小于"><code>lt</code></abbr>
* <abbr title="XML Web Token - XML Web 令牌">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - 并行服务器网关接口">PSGI</abbr>

### abbr 提供了完整短语与解释 { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mozilla 开发者网络: 为开发者编写的文档，由 Firefox 团队撰写">MDN</abbr>
* <abbr title="Input/Output - 输入/输出: 磁盘读写，网络通信。">I/O</abbr>.

////

//// tab | 信息

"abbr" 元素的 "title" 属性需要按照特定规则进行翻译。

译文可以自行添加 "abbr" 元素以解释英语单词，LLM 不应删除这些元素。

参见 `scripts/translate.py` 中通用提示的 `### HTML abbr elements` 部分。

////

## HTML "dfn" 元素 { #html-dfn-elements }

* <dfn title="配置为以某种方式连接并协同工作的一组机器。">集群</dfn>
* <dfn title="一种使用具有多个隐藏层的人工神经网络的机器学习方法，从输入层到输出层构建了完整的内部结构">深度学习</dfn>

## 标题 { #headings }

//// tab | 测试

### 开发 Web 应用——教程 { #develop-a-webapp-a-tutorial }

你好。

### 类型提示与注解 { #type-hints-and-annotations }

再次你好。

### 超类与子类 { #super-and-subclasses }

再次你好。

////

//// tab | 信息

关于标题的唯一硬性规则是：LLM 必须保持花括号内的哈希部分不变，以确保链接不会失效。

参见 `scripts/translate.py` 中通用提示的 `### Headings` 部分。

语言特定的说明可参见例如 `docs/de/llm-prompt.md` 中的 `### Headings` 部分。

////

## 文档中使用的术语 { #terms-used-in-the-docs }

//// tab | 测试

* 你
* 你的

* 例如
* 等

* 作为 `int` 的 `foo`
* 作为 `str` 的 `bar`
* 作为 `list` 的 `baz`

* 教程 - 用户指南
* 高级用户指南
* SQLModel 文档
* API 文档
* 自动文档

* 数据科学
* 深度学习
* 机器学习
* 依赖注入
* HTTP Basic 认证
* HTTP Digest
* ISO 格式
* JSON Schema 标准
* JSON schema
* schema 定义
* 密码流
* 移动端

* 已弃用
* 设计的
* 无效
* 动态地
* 标准
* 默认
* 区分大小写
* 不区分大小写

* 为应用提供服务
* 为页面提供服务

* 应用
* 应用程序

* 请求
* 响应
* 错误响应

* 路径操作
* 路径操作装饰器
* 路径操作函数

* 请求体
* 请求体
* 响应体
* JSON 请求体
* 表单体
* 文件体
* 函数体

* 参数
* 请求体参数
* 路径参数
* 查询参数
* Cookie 参数
* Header 参数
* 表单参数
* 函数参数

* 事件
* 启动事件
* 服务器启动
* 关闭事件
* lifespan 事件

* 处理器
* 事件处理器
* 异常处理器
* 处理

* 模型
* Pydantic 模型
* 数据模型
* 数据库模型
* 表单模型
* 模型对象

* 类
* 基类
* 父类
* 子类
* 子类
* 兄弟类
* 类方法

* Header
* Headers
* 授权 Header
* `Authorization` header
* 转发 Header

* 依赖注入系统
* 依赖项
* 可依赖项
* 依赖方

* I/O 密集型
* CPU 密集型
* 并发
* 并行
* 多进程

* 环境变量
* 环境变量
* `PATH`
* `PATH` 变量

* 认证
* 认证提供方
* 授权
* 授权表单
* 授权提供方
* 用户进行认证
* 系统对用户进行认证

* CLI
* 命令行界面

* 服务器
* 客户端

* 云服务提供商
* 云服务

* 开发
* 开发阶段

* dict
* 字典
* 枚举
* 枚举
* 枚举成员

* 编码器
* 解码器
* 编码
* 解码

* 异常
* 抛出

* 表达式
* 语句

* 前端
* 后端

* GitHub 讨论
* GitHub issue

* 性能
* 性能优化

* 返回类型
* 返回值

* 安全
* 安全方案

* 任务
* 后台任务
* 任务函数

* 模板
* 模板引擎

* 类型注解
* 类型提示

* 服务器 worker
* Uvicorn worker
* Gunicorn Worker
* worker 进程
* worker 类
* 工作负载

* 部署
* 部署

* SDK
* 软件开发工具包

* `APIRouter`
* `requirements.txt`
* Bearer Token
* 破坏性变更
* bug
* 按钮
* 可调用对象
* 代码
* 提交
* 上下文管理器
* 协程
* 数据库会话
* 磁盘
* 域名
* 引擎
* 虚假 X
* HTTP GET 方法
* 项
* 库
* 生命周期
* 锁
* 中间件
* 移动应用
* 模块
* 挂载
* 网络
* 源
* 覆盖
* 载荷
* 处理器
* 属性
* 代理
* Pull Request
* 查询
* RAM
* 远程机器
* 状态码
* 字符串
* 标签
* Web 框架
* 通配符
* 返回
* 校验

////

//// tab | 信息

这是一份不完整且非规范性的（主要是）技术术语清单，取自文档中常见的词汇。它可能有助于提示词设计者判断哪些术语需要对 LLM 提供额外指引。例如当它总是把一个好的译法改回次优译法，或在你的语言中对某个术语的词形变化有困难时。

参见例如 `docs/de/llm-prompt.md` 中的 `### List of English terms and their preferred German translations` 部分。

////



---

# Source: docs/about/index.md


# 关于 { #about }

关于 FastAPI、其设计、灵感等。🤓



---

# Source: docs/advanced/additional-responses.md


# OpenAPI 中的附加响应 { #additional-responses-in-openapi }

/// warning | 警告

这是一个相对高级的话题。

如果你刚开始使用 **FastAPI**，可能暂时用不到。

///

你可以声明附加响应，包括额外的状态码、媒体类型、描述等。

这些附加响应会被包含在 OpenAPI 模式中，因此它们也会出现在 API 文档中。

但是对于这些附加响应，你必须确保直接返回一个 `Response`（例如 `JSONResponse`），并携带你的状态码和内容。

## 带有 `model` 的附加响应 { #additional-response-with-model }

你可以向你的*路径操作装饰器*传入参数 `responses`。

它接收一个 `dict`：键是每个响应的状态码（例如 `200`），值是包含该响应信息的另一个 `dict`。

这些响应的每个 `dict` 都可以有一个键 `model`，包含一个 Pydantic 模型，就像 `response_model` 一样。

**FastAPI** 会获取该模型，生成它的 JSON Schema，并将其放在 OpenAPI 中的正确位置。

例如，要声明另一个状态码为 `404` 且具有 Pydantic 模型 `Message` 的响应，你可以这样写：

{* ../../docs_src/additional_responses/tutorial001_py310.py hl[18,22] *}

/// note | 注意

记住你需要直接返回 `JSONResponse`。

///

/// note | 注意

`model` 键不是 OpenAPI 的一部分。

**FastAPI** 会从这里获取 Pydantic 模型，生成 JSON Schema，并把它放到正确的位置。

正确的位置是：

* 在键 `content` 中，它的值是另一个 JSON 对象（`dict`），该对象包含：
    * 一个媒体类型作为键，例如 `application/json`，它的值是另一个 JSON 对象，该对象包含：
        * 一个键 `schema`，它的值是来自该模型的 JSON Schema，这里就是正确的位置。
            * **FastAPI** 会在这里添加一个引用，指向你 OpenAPI 中另一个位置的全局 JSON Schemas，而不是直接内联。这样，其他应用和客户端可以直接使用这些 JSON Schemas，提供更好的代码生成工具等。

///

为该*路径操作*在 OpenAPI 中生成的响应将是：

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

这些模式在 OpenAPI 模式中被引用到另一个位置：

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## 主响应的其他媒体类型 { #additional-media-types-for-the-main-response }

你可以使用同一个 `responses` 参数为同一个主响应添加不同的媒体类型。

例如，你可以添加一个额外的媒体类型 `image/png`，声明你的*路径操作*可以返回 JSON 对象（媒体类型为 `application/json`）或 PNG 图片：

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | 注意

请注意，你必须直接使用 `FileResponse` 返回图片。

///

/// note | 注意

除非你在 `responses` 参数中明确指定不同的媒体类型，否则 FastAPI 会假设响应与主响应类具有相同的媒体类型（默认是 `application/json`）。

但是如果你指定了一个媒体类型为 `None` 的自定义响应类，FastAPI 会对任何具有关联模型的附加响应使用 `application/json`。

///

## 组合信息 { #combining-information }

你也可以把来自多个位置的响应信息组合在一起，包括 `response_model`、`status_code` 和 `responses` 参数。

你可以声明一个 `response_model`，使用默认状态码 `200`（或根据需要使用自定义状态码），然后在 `responses` 中直接在 OpenAPI 模式里为同一个响应声明附加信息。

**FastAPI** 会保留来自 `responses` 的附加信息，并把它与你的模型生成的 JSON Schema 合并。

例如，你可以声明一个状态码为 `404` 的响应，它使用一个 Pydantic 模型并带有自定义的 `description`。

以及一个状态码为 `200` 的响应，它使用你的 `response_model`，但包含自定义的 `example`：

{* ../../docs_src/additional_responses/tutorial003_py310.py hl[20:31] *}

所有这些都会被合并并包含到你的 OpenAPI 中，并显示在 API 文档里：

<img src="/img/tutorial/additional-responses/image01.png">

## 组合预定义响应和自定义响应 { #combine-predefined-responses-and-custom-ones }

你可能希望有一些适用于许多*路径操作*的预定义响应，但同时又想把它们与每个*路径操作*所需的自定义响应组合在一起。

在这些情况下，你可以使用 Python 的“解包”`dict` 的技巧 `**dict_to_unpack`：

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

这里，`new_dict` 将包含来自 `old_dict` 的所有键值对，再加上新的键值对：

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

你可以使用该技巧在*路径操作*中重用一些预定义响应，并把它们与额外的自定义响应组合在一起。

例如：

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## 关于 OpenAPI 响应的更多信息 { #more-information-about-openapi-responses }

要查看响应中究竟可以包含什么，你可以查看 OpenAPI 规范中的以下部分：

* [OpenAPI Responses 对象](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object)，它包含 `Response Object`。
* [OpenAPI Response 对象](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object)，你可以把这里的任何内容直接包含到 `responses` 参数中的每个响应里。包括 `description`、`headers`、`content`（在这里声明不同的媒体类型和 JSON Schemas），以及 `links`。



---

# Source: docs/advanced/additional-status-codes.md


# 额外的状态码 { #additional-status-codes }

**FastAPI** 默认使用 `JSONResponse` 返回一个响应，将你的 *路径操作* 中的返回内容放到该 `JSONResponse` 中。

**FastAPI** 会自动使用默认的状态码或者使用你在 *路径操作* 中设置的状态码。

## 额外的状态码 { #additional-status-codes_1 }

如果你想要返回主要状态码之外的状态码，你可以通过直接返回一个 `Response` 来实现，比如 `JSONResponse`，然后直接设置额外的状态码。

例如，假设你想有一个 *路径操作* 能够更新条目，并且更新成功时返回 200 「成功」 的 HTTP 状态码。

但是你也希望它能够接受新的条目。并且当这些条目不存在时，会自动创建并返回 201 「创建」的 HTTP 状态码。

要实现它，导入 `JSONResponse`，然后在其中直接返回你的内容，并将 `status_code` 设置为你要的值。

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | 警告

当你直接返回一个像上面例子中的 `Response` 对象时，它会直接返回。

它不会用模型等进行序列化。

确保其中有你想要的数据，且返回的值为合法的 JSON（如果你使用 `JSONResponse` 的话）。

///

/// note | 技术细节

你也可以使用 `from starlette.responses import JSONResponse`。　

出于方便，**FastAPI** 为开发者提供同 `starlette.responses` 一样的 `fastapi.responses`。但是大多数可用的响应都是直接来自 Starlette。`status` 也是一样。

///

## OpenAPI 和 API 文档 { #openapi-and-api-docs }

如果你直接返回额外的状态码和响应，它们不会包含在 OpenAPI 方案（API 文档）中，因为 FastAPI 没办法预先知道你要返回什么。

但是你可以使用：[额外的响应](additional-responses.md)，在代码中记录这些内容。



---

# Source: docs/advanced/advanced-dependencies.md


# 高级依赖项 { #advanced-dependencies }


## 参数化的依赖项 { #parameterized-dependencies }

目前我们看到的依赖项都是固定的函数或类。

但有时你可能希望为依赖项设置参数，而不必声明许多不同的函数或类。

假设我们要有一个依赖项，用来检查查询参数 `q` 是否包含某个固定内容。

但我们希望能够把这个固定内容参数化。

## “可调用”的实例 { #a-callable-instance }

在 Python 中，可以让某个类的实例变成“可调用对象”（callable）。

这里指的是类的实例（类本身已经是可调用的），而不是类本身。

为此，声明一个 `__call__` 方法：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[12] *}

在这种情况下，**FastAPI** 会使用这个 `__call__` 来检查附加参数和子依赖，并且稍后会调用它，把返回值传递给你的*路径操作函数*中的参数。

## 参数化实例 { #parameterize-the-instance }

现在，我们可以用 `__init__` 声明实例的参数，用来“参数化”这个依赖项：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[9] *}

在本例中，**FastAPI** 不会接触或关心 `__init__`，我们会在自己的代码中直接使用它。

## 创建实例 { #create-an-instance }

我们可以这样创建该类的实例：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[18] *}

这样就把依赖项“参数化”了，现在它内部带有属性 `checker.fixed_content` 的值 `"bar"`。

## 把实例作为依赖项 { #use-the-instance-as-a-dependency }

然后，我们可以在 `Depends(checker)` 中使用这个 `checker`，而不是 `Depends(FixedContentQueryChecker)`，因为依赖项是实例 `checker`，不是类本身。

解析依赖项时，**FastAPI** 会像这样调用 `checker`：

```Python
checker(q="somequery")
```

...并将其返回值作为依赖项的值，传给我们的*路径操作函数*中的参数 `fixed_content_included`：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[22] *}

/// tip | 提示

这些看起来可能有些牵强，目前它的用处也许还不太明显。

这些示例刻意保持简单，但展示了整体的工作方式。

在安全相关的章节里，有一些工具函数就是以相同的方式实现的。

如果你理解了这里的内容，你就已经知道那些安全工具在底层是如何工作的。

///

## 带 `yield` 的依赖项、`HTTPException`、`except` 与后台任务 { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | 警告

你很可能不需要了解这些技术细节。

这些细节主要在你的 FastAPI 应用版本低于 0.121.0 且你正遇到带 `yield` 的依赖项问题时才有用。

///

带 `yield` 的依赖项随着时间演进以覆盖不同用例并修复一些问题，下面是变更摘要。

### 带 `yield` 的依赖项与 `scope` { #dependencies-with-yield-and-scope }

在 0.121.0 版本中，FastAPI 为带 `yield` 的依赖项新增了 `Depends(scope="function")` 的支持。

使用 `Depends(scope="function")` 时，`yield` 之后的退出代码会在*路径操作函数*结束后、响应发送给客户端之前立即执行。

而当使用默认的 `Depends(scope="request")` 时，`yield` 之后的退出代码会在响应发送之后执行。

你可以在文档 [带 `yield` 的依赖项 - 提前退出与 `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) 中了解更多。

### 带 `yield` 的依赖项与 `StreamingResponse`（技术细节） { #dependencies-with-yield-and-streamingresponse-technical-details }

在 FastAPI 0.118.0 之前，如果你使用带 `yield` 的依赖项，它会在*路径操作函数*返回后、发送响应之前运行 `yield` 之后的退出代码。

这样做的目的是避免在等待响应通过网络传输期间不必要地占用资源。

这也意味着，如果你返回的是 `StreamingResponse`，那么该带 `yield` 的依赖项的退出代码会在开始发送响应前就已经执行完毕。

例如，如果你在带 `yield` 的依赖项中持有一个数据库会话，那么 `StreamingResponse` 在流式发送数据时将无法使用该会话，因为会话已经在 `yield` 之后的退出代码里被关闭了。

在 0.118.0 中，这一行为被回退为：让 `yield` 之后的退出代码在响应发送之后再执行。

/// note | 注意

如你在下文所见，这与 0.106.0 之前的行为非常相似，但对若干边界情况做了改进和修复。

///

#### 需要提前执行退出代码的用例 { #use-cases-with-early-exit-code }

在某些特定条件下，旧的行为（在发送响应之前执行带 `yield` 依赖项的退出代码）会更有利。

例如，设想你在带 `yield` 的依赖项中仅用数据库会话来校验用户，而在*路径操作函数*中并不会再次使用该会话；同时，响应需要很长时间才能发送完，比如一个缓慢发送数据的 `StreamingResponse`，且它出于某种原因并不使用数据库。

这种情况下，会一直持有数据库会话直到响应发送完毕；但如果并不再使用它，就没有必要一直占用。

代码可能如下：

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

退出代码（自动关闭 `Session`）位于：

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...会在响应把慢速数据发送完之后才运行：

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

但由于 `generate_stream()` 并不使用数据库会话，因此在发送响应期间保持会话打开并非必要。

如果你使用的是 SQLModel（或 SQLAlchemy）并碰到这种特定用例，你可以在不再需要时显式关闭会话：

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

这样会话会释放数据库连接，让其他请求可以使用。

如果你还有其他需要在 `yield` 依赖项中提前退出的用例，请创建一个 [GitHub 讨论问题](https://github.com/fastapi/fastapi/discussions/new?category=questions)，说明你的具体用例以及为何提前关闭会对你有帮助。

如果确有有力的用例需要提前关闭，我会考虑新增一种选择性启用提前关闭的方式。

### 带 `yield` 的依赖项与 `except`（技术细节） { #dependencies-with-yield-and-except-technical-details }

在 FastAPI 0.110.0 之前，如果你在带 `yield` 的依赖项中用 `except` 捕获了一个异常，并且没有再次抛出它，那么该异常会被自动抛出/转发给任意异常处理器或内部服务器错误处理器。

在 0.110.0 中对此作出了变更，以修复将异常转发为未处理（内部服务器错误）时造成的内存消耗问题，并使其与常规 Python 代码的行为保持一致。

### 后台任务与带 `yield` 的依赖项（技术细节） { #background-tasks-and-dependencies-with-yield-technical-details }

在 FastAPI 0.106.0 之前，`yield` 之后抛出异常是不可行的，因为带 `yield` 的依赖项中的退出代码会在响应发送之后才执行，此时[异常处理器](../tutorial/handling-errors.md#install-custom-exception-handlers)已经运行完毕。

之所以这样设计，主要是为了允许在后台任务中继续使用依赖项通过 `yield`“产出”的对象，因为退出代码会在后台任务完成之后才执行。

在 FastAPI 0.106.0 中，这一行为被修改，目的是避免在等待响应通过网络传输时一直占用资源。

/// tip | 提示

另外，后台任务通常是一段独立的逻辑，应该单独处理，并使用它自己的资源（例如它自己的数据库连接）。

因此，这样做你的代码通常会更清晰。

///

如果你过去依赖于旧行为，现在应在后台任务内部自行创建所需资源，并且只在内部使用不依赖于带 `yield` 依赖项资源的数据。

例如，不要复用相同的数据库会话，而是在后台任务内部创建一个新的会话，并用这个新会话从数据库获取对象。然后，不是把数据库对象本身作为参数传给后台任务函数，而是传递该对象的 ID，并在后台任务函数内部再次获取该对象。



---

# Source: docs/advanced/advanced-python-types.md


# 高级 Python 类型 { #advanced-python-types }

这里有一些在使用 Python 类型时可能有用的额外想法。

## 使用 `Union` 或 `Optional` { #using-union-or-optional }

如果你的代码因为某些原因不能使用 `|`，例如它不是在类型注解里，而是在 `response_model=` 之类的参数中，那么你可以使用 `typing` 中的 `Union` 来代替竖线（`|`）。

例如，你可以声明某个值可以是 `str` 或 `None`：

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` 也提供了一个声明“可能为 `None`”的快捷方式：`Optional`。

从我非常主观的角度给个小建议：

- 🚨 避免使用 `Optional[SomeType]`
- 改用 ✨`Union[SomeType, None]`✨。

两者是等价的，底层其实也是一样的。但我更推荐使用 `Union` 而不是 `Optional`，因为单词“optional”（可选）看起来会暗示该值是可选的，而它真正的含义是“它可以是 `None`”，即使它并不是可选的，仍然是必填的。

我认为 `Union[SomeType, None]` 更能明确表达其含义。

这只是关于词语和命名的问题，但这些词语会影响你和你的队友如何看待代码。

举个例子，看这段函数：

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

参数 `name` 被定义为 `Optional[str]`，但它并不是“可选”的，你不能不传这个参数就调用函数：

```Python
say_hi()  # 哎呀，这会报错！😱
```

参数 `name` 仍然是必填的（不是“可选”），因为它没有默认值。不过，`name` 接受 `None` 作为取值：

```Python
say_hi(name=None)  # 这样可以，None 是有效的 🎉
```

好消息是，在大多数情况下，你可以直接使用 `|` 来定义类型联合：

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

因此，通常你不必为像 `Optional` 和 `Union` 这样的名字而操心。😎



---

# Source: docs/advanced/async-tests.md


# 异步测试 { #async-tests }

您已经了解了如何使用 `TestClient` 测试 **FastAPI** 应用程序。但是到目前为止，您只了解了如何编写同步测试，而没有使用 `async` 异步函数。

在测试中能够使用异步函数可能会很有用，比如当您需要异步查询数据库的时候。想象一下，您想要测试向 FastAPI 应用程序发送请求，然后验证您的后端是否成功在数据库中写入了正确的数据，与此同时您使用了异步的数据库的库。

让我们看看如何才能实现这一点。

## pytest.mark.anyio { #pytest-mark-anyio }

如果我们想在测试中调用异步函数，那么我们的测试函数必须是异步的。 AnyIO 为此提供了一个简洁的插件，它允许我们指定一些测试函数要异步调用。

## HTTPX { #httpx }

即使您的 **FastAPI** 应用程序使用普通的 `def` 函数而不是 `async def` ，它本质上仍是一个 `async` 异步应用程序。

`TestClient` 在内部通过一些“魔法”操作，使得您可以在普通的 `def` 测试函数中调用异步的 FastAPI 应用程序，并使用标准的 pytest。但当我们在异步函数中使用它时，这种“魔法”就不再生效了。由于测试以异步方式运行，我们无法在测试函数中继续使用 `TestClient`。

`TestClient` 是基于 [HTTPX](https://www.python-httpx.org) 的。幸运的是，我们可以直接使用它来测试 API。

## 示例 { #example }

举个简单的例子，让我们来看一个与[更大的应用](../tutorial/bigger-applications.md)和[测试](../tutorial/testing.md)中描述的类似文件结构：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

文件 `main.py` 将包含:

{* ../../docs_src/async_tests/app_a_py310/main.py *}

文件 `test_main.py` 将包含针对 `main.py` 的测试，现在它可能看起来如下：

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## 运行测试 { #run-it }

您可以通过以下方式照常运行测试：

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 详细说明 { #in-detail }

这个标记 `@pytest.mark.anyio` 会告诉 pytest 该测试函数应该被异步调用：

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip | 提示

请注意，测试函数现在用的是 `async def`，而不是像以前使用 `TestClient` 时那样只是 `def` 。

///

我们现在可以使用应用程序创建一个 `AsyncClient` ，并使用 `await` 向其发送异步请求。

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

这相当于：

```Python
response = client.get('/')
```

...我们曾经通过它向 `TestClient` 发出请求。

/// tip | 提示

请注意，我们正在将 async/await 与新的 `AsyncClient` 一起使用——请求是异步的。

///

/// warning | 警告

如果您的应用程序依赖于生命周期事件， `AsyncClient` 将不会触发这些事件。为了确保它们被触发，请使用 [florimondmanca/asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage) 中的 `LifespanManager` 。

///

## 其他异步函数调用 { #other-asynchronous-function-calls }

由于测试函数现在是异步的，因此除了在测试中向 FastAPI 应用程序发送请求之外，您现在还可以调用（和使用 `await` 等待）其他 `async` 异步函数，就和您在代码中的其他任何地方调用它们的方法一样。

/// tip | 提示

如果您在测试程序中集成异步函数调用的时候遇到一个 `RuntimeError: Task attached to a different loop` 的报错（例如，使用 [MongoDB 的 MotorClient](https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop) 时），请记住，只能在异步函数中实例化需要事件循环的对象，例如在 `@app.on_event("startup")` 回调中初始化。

///



---

# Source: docs/advanced/behind-a-proxy.md


# 使用代理 { #behind-a-proxy }

在很多情况下，你会在 FastAPI 应用前面使用像 Traefik 或 Nginx 这样的**代理**。

这些代理可以处理 HTTPS 证书等事项。

## 代理转发的请求头 { #proxy-forwarded-headers }

在你的应用前面的**代理**通常会在把请求转发给你的**服务器**之前，临时设置一些请求头，让服务器知道该请求是由代理**转发**的，并告知原始（公网）URL，包括域名、是否使用 HTTPS 等。

**服务器**程序（例如通过 **FastAPI CLI** 运行的 **Uvicorn**）能够解析这些请求头，然后把这些信息传递给你的应用。

但出于安全考虑，由于服务器并不知道自己处在受信任的代理之后，它默认不会解析这些请求头。

/// note | 技术细节

这些代理相关的请求头包括：

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

### 启用代理转发的请求头 { #enable-proxy-forwarded-headers }

你可以用 *CLI 选项* `--forwarded-allow-ips` 启动 FastAPI CLI，并传入应该被信任、允许读取这些转发请求头的 IP 地址列表。

如果设置为 `--forwarded-allow-ips="*"`，就会信任所有来源 IP。

如果你的**服务器**位于受信任的**代理**之后，并且只有代理会与它通信，这将使其接受该**代理**的任何 IP。

<div class="termy">

```console
$ fastapi run --forwarded-allow-ips="*"

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 使用 HTTPS 的重定向 { #redirects-with-https }

例如，假设你定义了一个*路径操作* `/items/`：

{* ../../docs_src/behind_a_proxy/tutorial001_01_py310.py hl[6] *}

如果客户端尝试访问 `/items`，默认会被重定向到 `/items/`。

但在设置 *CLI 选项* `--forwarded-allow-ips` 之前，它可能会重定向到 `http://localhost:8000/items/`。

而你的应用可能托管在 `https://mysuperapp.com`，重定向应当是 `https://mysuperapp.com/items/`。

通过设置 `--proxy-headers`，FastAPI 现在就可以重定向到正确的位置。😎

```
https://mysuperapp.com/items/
```

/// tip | 提示

如果你想了解更多关于 HTTPS 的内容，查看指南：[关于 HTTPS](../deployment/https.md)。

///

### 代理转发请求头如何工作 { #how-proxy-forwarded-headers-work }

下面是一个可视化图示，展示了**代理**如何在客户端与**应用服务器**之间添加转发请求头：

```mermaid
sequenceDiagram
    participant Client
    participant Proxy as Proxy/Load Balancer
    participant Server as FastAPI Server

    Client->>Proxy: HTTPS Request<br/>Host: mysuperapp.com<br/>Path: /items

    Note over Proxy: Proxy adds forwarded headers

    Proxy->>Server: HTTP Request<br/>X-Forwarded-For: [client IP]<br/>X-Forwarded-Proto: https<br/>X-Forwarded-Host: mysuperapp.com<br/>Path: /items

    Note over Server: Server interprets headers<br/>(if --forwarded-allow-ips is set)

    Server->>Proxy: HTTP Response<br/>with correct HTTPS URLs

    Proxy->>Client: HTTPS Response
```

**代理**会拦截原始客户端请求，并在将请求传递给**应用服务器**之前，添加特殊的*转发*请求头（`X-Forwarded-*`）。

这些请求头保留了原始请求中否则会丢失的信息：

- X-Forwarded-For：原始客户端的 IP 地址
- X-Forwarded-Proto：原始协议（`https`）
- X-Forwarded-Host：原始主机（`mysuperapp.com`）

当 **FastAPI CLI** 配置了 `--forwarded-allow-ips` 后，它会信任并使用这些请求头，例如用于在重定向中生成正确的 URL。

## 移除路径前缀的代理 { #proxy-with-a-stripped-path-prefix }

你可能会有一个代理，为你的应用添加一个路径前缀。

在这些情况下，你可以使用 `root_path` 来配置你的应用。

`root_path` 是 ASGI 规范（FastAPI 基于该规范，通过 Starlette 构建）提供的机制。

`root_path` 用于处理这些特定情况。

在挂载子应用时，它也会在内部使用。

“移除路径前缀的代理”在这里的意思是：你可以在代码中声明一个路径 `/app`，然后在顶层添加一层（代理），把你的 **FastAPI** 应用放在类似 `/api/v1` 的路径下。

在这种情况下，原始路径 `/app` 实际上会在 `/api/v1/app` 提供服务。

即使你的所有代码都假设只有 `/app`。

{* ../../docs_src/behind_a_proxy/tutorial001_py310.py hl[6] *}

代理会在将请求传递给应用服务器（可能是通过 FastAPI CLI 运行的 Uvicorn）之前，实时**“移除”**这个**路径前缀**，让你的应用认为它是在 `/app` 被服务，这样你就不需要更新所有代码去包含 `/api/v1` 前缀。

到这里，一切都会像往常一样工作。

但是，当你打开集成的文档界面（前端）时，它会期望在 `/openapi.json` 获取 OpenAPI 模式，而不是在 `/api/v1/openapi.json`。

因此，（在浏览器中运行的）前端会尝试访问 `/openapi.json`，但无法获取 OpenAPI 模式。

因为我们的应用使用了路径前缀为 `/api/v1` 的代理，前端需要从 `/api/v1/openapi.json` 获取 OpenAPI 模式。

```mermaid
graph LR

browser("Browser")
proxy["Proxy on http://0.0.0.0:9999/api/v1/app"]
server["Server on http://127.0.0.1:8000/app"]

browser --> proxy
proxy --> server
```

/// tip | 提示

IP `0.0.0.0` 通常表示程序监听该机器/服务器上的所有可用 IP。

///

文档界面还需要 OpenAPI 模式声明该 API 的 `server` 位于 `/api/v1`（代理后面）。例如：

```JSON hl_lines="4-8"
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        }
    ],
    "paths": {
            // More stuff here
    }
}
```

在此示例中，“Proxy” 可以是 **Traefik** 之类的。服务器可以是用 **Uvicorn** 的 **FastAPI CLI** 运行你的 FastAPI 应用。

### 提供 `root_path` { #providing-the-root-path }

为此，你可以像下面这样使用命令行选项 `--root-path`：

<div class="termy">

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果你使用 Hypercorn，它也有 `--root-path` 选项。

/// note | 技术细节

ASGI 规范为这种用例定义了 `root_path`。

命令行选项 `--root-path` 会提供该 `root_path`。

///

### 查看当前的 `root_path` { #checking-the-current-root-path }

你可以获取应用在每个请求中使用的当前 `root_path`，它是 `scope` 字典的一部分（ASGI 规范的一部分）。

这里我们把它包含在响应消息中仅用于演示。

{* ../../docs_src/behind_a_proxy/tutorial001_py310.py hl[8] *}

然后，如果你这样启动 Uvicorn：

<div class="termy">

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

响应类似于：

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

### 在 FastAPI 应用中设置 `root_path` { #setting-the-root-path-in-the-fastapi-app }

或者，如果你无法提供类似 `--root-path` 的命令行选项，你可以在创建 FastAPI 应用时设置参数 `root_path`：

{* ../../docs_src/behind_a_proxy/tutorial002_py310.py hl[3] *}

把 `root_path` 传给 `FastAPI` 等同于把命令行选项 `--root-path` 传给 Uvicorn 或 Hypercorn。

### 关于 `root_path` { #about-root-path }

请注意，服务器（Uvicorn）不会用这个 `root_path` 做别的事情，只会把它传给应用。

但是，如果你用浏览器打开 [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app)，你会看到正常的响应：

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

因此，它不会期望被访问于 `http://127.0.0.1:8000/api/v1/app`。

Uvicorn 会期望代理以 `http://127.0.0.1:8000/app` 访问 Uvicorn，而在顶部额外添加 `/api/v1` 前缀是代理的职责。

## 关于移除路径前缀的代理 { #about-proxies-with-a-stripped-path-prefix }

请记住，移除路径前缀只是配置代理的一种方式。

在很多情况下，默认是代理不会移除路径前缀。

在这种情况下（没有移除路径前缀），代理会监听类似 `https://myawesomeapp.com`，当浏览器访问 `https://myawesomeapp.com/api/v1/app` 且你的服务器（例如 Uvicorn）监听 `http://127.0.0.1:8000` 时，代理（未移除路径前缀）会以相同路径访问 Uvicorn：`http://127.0.0.1:8000/api/v1/app`。

## 使用 Traefik 进行本地测试 { #testing-locally-with-traefik }

你可以很容易地使用 [Traefik](https://docs.traefik.io/) 在本地运行一个移除路径前缀的实验。

[下载 Traefik](https://github.com/containous/traefik/releases)，它是一个单独的二进制文件，你可以解压压缩包并直接在终端中运行。

然后创建一个 `traefik.toml` 文件，内容如下：

```TOML hl_lines="3"
[entryPoints]
  [entryPoints.http]
    address = ":9999"

[providers]
  [providers.file]
    filename = "routes.toml"
```

这告诉 Traefik 监听端口 9999，并使用另一个文件 `routes.toml`。

/// tip | 提示

我们使用 9999 端口而不是标准 HTTP 端口 80，这样你就不需要用管理员（`sudo`）权限运行。

///

现在创建另一个文件 `routes.toml`：

```TOML hl_lines="5  12  20"
[http]
  [http.middlewares]

    [http.middlewares.api-stripprefix.stripPrefix]
      prefixes = ["/api/v1"]

  [http.routers]

    [http.routers.app-http]
      entryPoints = ["http"]
      service = "app"
      rule = "PathPrefix(`/api/v1`)"
      middlewares = ["api-stripprefix"]

  [http.services]

    [http.services.app]
      [http.services.app.loadBalancer]
        [[http.services.app.loadBalancer.servers]]
          url = "http://127.0.0.1:8000"
```

这个文件配置 Traefik 使用路径前缀 `/api/v1`。

随后 Traefik 会把请求转发到运行在 `http://127.0.0.1:8000` 的 Uvicorn。

现在启动 Traefik：

<div class="termy">

```console
$ ./traefik --configFile=traefik.toml

INFO[0000] Configuration loaded from file: /home/user/awesomeapi/traefik.toml
```

</div>

然后使用 `--root-path` 选项启动你的应用：

<div class="termy">

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 查看响应 { #check-the-responses }

现在，如果你访问 Uvicorn 端口对应的 URL：[http://127.0.0.1:8000/app](http://127.0.0.1:8000/app)，你会看到正常响应：

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

/// tip | 提示

注意，尽管你是通过 `http://127.0.0.1:8000/app` 访问，它仍显示 `root_path` 为 `/api/v1`，该值来自 `--root-path` 选项。

///

现在打开包含路径前缀、使用 Traefik 端口的 URL：[http://127.0.0.1:9999/api/v1/app](http://127.0.0.1:9999/api/v1/app)。

我们得到相同的响应：

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

但这次 URL 中带有代理提供的前缀路径：`/api/v1`。

当然，这里的想法是每个人都通过代理访问应用，因此带有路径前缀 `/api/v1` 的版本才是“正确”的。

而不带路径前缀的版本（`http://127.0.0.1:8000/app`）由 Uvicorn 直接提供，仅供_代理_（Traefik）访问。

这说明了代理（Traefik）如何使用路径前缀，以及服务器（Uvicorn）如何使用 `--root-path` 选项提供的 `root_path`。

### 查看文档界面 { #check-the-docs-ui }

有趣的部分来了。✨

访问应用的“官方”方式应该是通过我们定义的带有路径前缀的代理。因此，正如预期的那样，如果你尝试不带路径前缀、直接由 Uvicorn 提供的文档界面，它将无法工作，因为它期望通过代理访问。

你可以在 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看：

<img src="/img/tutorial/behind-a-proxy/image01.png">

但如果我们在“官方”URL（代理端口为 `9999`）的 `/api/v1/docs` 访问文档界面，它就能正常工作！🎉

你可以在 [http://127.0.0.1:9999/api/v1/docs](http://127.0.0.1:9999/api/v1/docs) 查看：

<img src="/img/tutorial/behind-a-proxy/image02.png">

完全符合我们的预期。✔️

这是因为 FastAPI 使用该 `root_path` 在 OpenAPI 中创建默认的 `server`，其 URL 来自 `root_path`。

## 附加的服务器 { #additional-servers }

/// warning | 警告

这是一个更高级的用例，可以跳过。

///

默认情况下，**FastAPI** 会在 OpenAPI 模式中使用 `root_path` 的 URL 创建一个 `server`。

但你也可以提供其他备选的 `servers`，例如你希望让“同一个”文档界面同时与预发布环境和生产环境交互。

如果你传入了自定义的 `servers` 列表，并且存在 `root_path`（因为你的 API 位于代理后面），**FastAPI** 会在列表开头插入一个使用该 `root_path` 的“server”。

例如：

{* ../../docs_src/behind_a_proxy/tutorial003_py310.py hl[4:7] *}

会生成如下的 OpenAPI 模式：

```JSON hl_lines="5-7"
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        },
        {
            "url": "https://stag.example.com",
            "description": "Staging environment"
        },
        {
            "url": "https://prod.example.com",
            "description": "Production environment"
        }
    ],
    "paths": {
            // More stuff here
    }
}
```

/// tip | 提示

注意这个自动生成的服务器，`url` 的值为 `/api/v1`，取自 `root_path`。

///

在文档界面 [http://127.0.0.1:9999/api/v1/docs](http://127.0.0.1:9999/api/v1/docs) 中，它看起来是这样的：

<img src="/img/tutorial/behind-a-proxy/image03.png">

/// tip | 提示

文档界面会与你所选择的服务器交互。

///

/// note | 技术细节

OpenAPI 规范中的 `servers` 属性是可选的。

如果你没有指定 `servers` 参数，并且 `root_path` 等于 `/`，则默认情况下，生成的 OpenAPI 模式中会完全省略 `servers` 属性，这等价于只有一个 `url` 值为 `/` 的服务器。

///

### 从 `root_path` 禁用自动服务器 { #disable-automatic-server-from-root-path }

如果你不希望 **FastAPI** 包含一个使用 `root_path` 的自动服务器，可以使用参数 `root_path_in_servers=False`：

{* ../../docs_src/behind_a_proxy/tutorial004_py310.py hl[9] *}

这样它就不会被包含到 OpenAPI 模式中。

## 挂载子应用 { #mounting-a-sub-application }

如果你需要在使用带有 `root_path` 的代理时挂载一个子应用（参见 [子应用 - 挂载](sub-applications.md)），你可以像预期的那样正常操作。

FastAPI 会在内部智能地使用 `root_path`，因此它可以直接正常工作。✨



---

# Source: docs/advanced/custom-response.md


# 自定义响应 - HTML、流、文件等 { #custom-response-html-stream-file-others }

默认情况下，**FastAPI** 会返回 JSON 响应。

你可以像在 [直接返回响应](response-directly.md) 中那样，直接返回 `Response` 来重载它。

但如果你直接返回一个 `Response`（或其任意子类，比如 `JSONResponse`），返回的数据不会自动转换（即使你声明了 `response_model`），也不会自动生成文档（例如，在生成的 OpenAPI 中，HTTP 头 `Content-Type` 里的特定「媒体类型」不会被包含）。

你还可以在 *路径操作装饰器* 中通过 `response_class` 参数声明要使用的 `Response`（例如任意 `Response` 子类）。

你从 *路径操作函数* 中返回的内容将被放在该 `Response` 中。

/// note | 注意

如果你使用不带有媒体类型的响应类，FastAPI 会认为你的响应没有任何内容，所以不会在生成的 OpenAPI 文档中记录响应格式。

///

## JSON 响应 { #json-responses }

默认情况下 FastAPI 返回 JSON 响应。

如果你声明了一个[响应模型](../tutorial/response-model.md)，FastAPI 会使用 Pydantic 将数据序列化为 JSON。

如果你没有声明响应模型，FastAPI 会使用 [JSON 兼容编码器](../tutorial/encoder.md) 中解释的 `jsonable_encoder`，并把结果放进一个 `JSONResponse`。

如果你在 `response_class` 中声明了一个 JSON 媒体类型（`application/json`）的类（比如 `JSONResponse`），你返回的数据会使用你在 *路径操作装饰器* 中声明的任意 Pydantic `response_model` 自动转换（和过滤）。但数据不会由 Pydantic 序列化为 JSON 字节；而是先用 `jsonable_encoder` 转换后传给 `JSONResponse`，由它使用 Python 标准 JSON 库序列化为字节。

### JSON 性能 { #json-performance }

简而言之，如果你想要获得最大性能，请使用[响应模型](../tutorial/response-model.md)，并且不要在 *路径操作装饰器* 中声明 `response_class`。

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML 响应 { #html-response }

使用 `HTMLResponse` 来从 **FastAPI** 中直接返回一个 HTML 响应。

* 导入 `HTMLResponse`。
* 将 `HTMLResponse` 作为你的 *路径操作* 的 `response_class` 参数传入。

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// note | 注意

参数 `response_class` 也会用来定义响应的「媒体类型」。

在这个例子中，HTTP 头的 `Content-Type` 会被设置成 `text/html`。

并且在 OpenAPI 文档中也会这样记录。

///

### 返回一个 `Response` { #return-a-response }

正如你在 [直接返回响应](response-directly.md) 中了解到的，你也可以通过直接返回响应在 *路径操作* 中直接重载响应。

和上面一样的例子，返回一个 `HTMLResponse` 看起来可能是这样：

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | 警告

*路径操作函数* 直接返回的 `Response` 不会被 OpenAPI 的文档记录（比如，`Content-Type` 不会被文档记录），并且在自动化交互文档中也是不可见的。

///

/// note | 注意

当然，实际的 `Content-Type` 头、状态码等等，将来自于你返回的 `Response` 对象。

///

### 在 OpenAPI 中文档化并重载 `Response` { #document-in-openapi-and-override-response }

如果你想要在函数内重载响应，但是同时在 OpenAPI 中文档化「媒体类型」，你可以使用 `response_class` 参数并返回一个 `Response` 对象。

接着 `response_class` 参数只会被用来文档化 OpenAPI 的 *路径操作*，你的 `Response` 用来返回响应。

#### 直接返回 `HTMLResponse` { #return-an-htmlresponse-directly }

比如像这样：

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

在这个例子中，函数 `generate_html_response()` 已经生成并返回 `Response` 对象而不是在 `str` 中返回 HTML。

通过返回函数 `generate_html_response()` 的调用结果，你已经返回一个重载 **FastAPI** 默认行为的 `Response` 对象。

但如果你在 `response_class` 中也传入了 `HTMLResponse`，**FastAPI** 会知道如何在 OpenAPI 和交互式文档中使用 `text/html` 将其文档化为 HTML：

<img src="/img/tutorial/custom-response/image01.png">

## 可用响应 { #available-responses }

这里有一些可用的响应。

要记得你可以使用 `Response` 来返回任何其他东西，甚至创建一个自定义的子类。

/// note | 技术细节

你也可以使用 `from starlette.responses import HTMLResponse`。

**FastAPI** 提供了同 `fastapi.responses` 相同的 `starlette.responses` 只是为了方便开发者。但大多数可用的响应都直接来自 Starlette。

///

### `Response` { #response }

其他全部的响应都继承自主类 `Response`。

你可以直接返回它。

`Response` 类接受如下参数：

* `content` - 一个 `str` 或者 `bytes`。
* `status_code` - 一个 `int` 类型的 HTTP 状态码。
* `headers` - 一个由字符串组成的 `dict`。
* `media_type` - 一个给出媒体类型的 `str`，比如 `"text/html"`。

FastAPI（实际上是 Starlette）将自动包含 Content-Length 的头。它还将包含一个基于 `media_type` 的 Content-Type 头，并为文本类型附加一个字符集。

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

如上文所述，接受文本或字节并返回 HTML 响应。

### `PlainTextResponse` { #plaintextresponse }

接受文本或字节并返回纯文本响应。

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

接受数据并返回一个 `application/json` 编码的响应。

如上文所述，这是 **FastAPI** 中使用的默认响应。

/// note | 技术细节

但如果你声明了响应模型或返回类型，将直接使用它来把数据序列化为 JSON，并直接返回一个具备正确 JSON 媒体类型的响应，而不会使用 `JSONResponse` 类。

这是获得最佳性能的理想方式。

///

### `RedirectResponse` { #redirectresponse }

返回 HTTP 重定向。默认情况下使用 307 状态码（临时重定向）。

你可以直接返回一个 `RedirectResponse`：

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

或者你可以把它用于 `response_class` 参数：

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

如果你这么做，那么你可以在 *路径操作* 函数中直接返回 URL。

在这种情况下，将使用 `RedirectResponse` 的默认 `status_code`，即 `307`。

---

你也可以将 `status_code` 参数和 `response_class` 参数结合使用：

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

采用异步生成器或普通生成器/迭代器（带有 `yield` 的函数），然后流式传输响应主体。

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | 技术细节

一个 `async` 任务只有在到达 `await` 时才能被取消。如果没有 `await`，生成器（带有 `yield` 的函数）无法被正确取消，即使已请求取消也可能继续运行。

由于这个小示例不需要任何 `await` 语句，我们添加 `await anyio.sleep(0)`，给事件循环一个处理取消的机会。

对于大型或无限流，这一点更为重要。

///

/// tip | 提示

与其直接返回 `StreamingResponse`，更推荐遵循 [流式数据](./stream-data.md) 的写法，它更方便并在幕后为你处理取消。

如果你在流式传输 JSON Lines，请参阅教程：[流式传输 JSON Lines](../tutorial/stream-json-lines.md)。

///

### `FileResponse` { #fileresponse }

异步传输文件作为响应。

与其他响应类型相比，接受不同的参数集进行实例化：

* `path` - 要流式传输的文件的文件路径。
* `headers` - 任何自定义响应头，传入字典类型。
* `media_type` - 给出媒体类型的字符串。如果未设置，则文件名或路径将用于推断媒体类型。
* `filename` - 如果给出，它将包含在响应的 `Content-Disposition` 中。

文件响应将包含适当的 `Content-Length`、`Last-Modified` 和 `ETag` 响应头。

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

你也可以使用 `response_class` 参数：

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

在这种情况下，你可以在 *路径操作* 函数中直接返回文件路径。

## 自定义响应类 { #custom-response-class }

你可以创建你自己的自定义响应类，继承自 `Response` 并使用它。

例如，假设你想用一些设置来使用 [`orjson`](https://github.com/ijl/orjson)。

假设你想让它返回带缩进、格式化的 JSON，因此你想使用 orjson 选项 `orjson.OPT_INDENT_2`。

你可以创建一个 `CustomORJSONResponse`。你需要做的主要事情是实现一个 `Response.render(content)` 方法，并返回 `bytes`：

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

现在，不再是返回：

```json
{"message": "Hello World"}
```

...这个响应将返回：

```json
{
  "message": "Hello World"
}
```

当然，你很可能会找到比格式化 JSON 更好的方式来利用这一点。😉

### `orjson` 或响应模型 { #orjson-or-response-model }

如果你追求的是性能，使用[响应模型](../tutorial/response-model.md) 往往比返回 `orjson` 响应更好。

使用响应模型时，FastAPI 会使用 Pydantic 直接把数据序列化为 JSON，不需要诸如通过 `jsonable_encoder` 转换这样的中间步骤（其他情况下会发生）。

并且在底层，Pydantic 使用与 `orjson` 相同的 Rust 机制来序列化 JSON，所以使用响应模型你已经可以获得最佳性能。

## 默认响应类 { #default-response-class }

在创建 **FastAPI** 类实例或 `APIRouter` 时，你可以指定默认要使用的响应类。

用于定义它的参数是 `default_response_class`。

在下面的示例中，**FastAPI** 会在所有 *路径操作* 中默认使用 `HTMLResponse`，而不是 JSON。

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | 提示

你仍然可以像之前一样在 *路径操作* 中重载 `response_class`。

///

## 额外文档 { #additional-documentation }

你还可以使用 `responses` 在 OpenAPI 中声明媒体类型和许多其他详细信息：[OpenAPI 中的额外响应](additional-responses.md)。



---

# Source: docs/advanced/dataclasses.md


# 使用数据类 { #using-dataclasses }


FastAPI 基于 **Pydantic** 构建，我已经向你展示过如何使用 Pydantic 模型声明请求与响应。

但 FastAPI 也支持以相同方式使用 [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)：

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

这仍然得益于 **Pydantic**，因为它对 [`dataclasses` 的内置支持](https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel)。

因此，即便上面的代码没有显式使用 Pydantic，FastAPI 也会使用 Pydantic 将那些标准数据类转换为 Pydantic 风格的 dataclasses。

并且，它仍然支持以下功能：

* 数据验证
* 数据序列化
* 数据文档等

这与使用 Pydantic 模型时的工作方式相同。而且底层实际上也是借助 Pydantic 实现的。

/// note | 注意

请注意，数据类不能完成 Pydantic 模型能做的所有事情。

因此，你可能仍然需要使用 Pydantic 模型。

但如果你已有一堆数据类，这个技巧可以让它们很好地为使用 FastAPI 的 Web API 所用。🤓

///

## 在 `response_model` 中使用数据类 { #dataclasses-in-response-model }

你也可以在 `response_model` 参数中使用 `dataclasses`：

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

该数据类会被自动转换为 Pydantic 的数据类。

这样，它的模式会显示在 API 文档界面中：

<img src="/img/tutorial/dataclasses/image01.png">

## 在嵌套数据结构中使用数据类 { #dataclasses-in-nested-data-structures }

你也可以把 `dataclasses` 与其它类型注解组合在一起，创建嵌套数据结构。

在某些情况下，你可能仍然需要使用 Pydantic 的 `dataclasses` 版本。例如，如果自动生成的 API 文档出现错误。

在这种情况下，你可以直接把标准的 `dataclasses` 替换为 `pydantic.dataclasses`，它是一个可直接替换的实现：

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. 我们仍然从标准库的 `dataclasses` 导入 `field`。
2. `pydantic.dataclasses` 是 `dataclasses` 的可直接替换版本。
3. `Author` 数据类包含一个由 `Item` 数据类组成的列表。
4. `Author` 数据类被用作 `response_model` 参数。
5. 你可以将其它标准类型注解与数据类一起用作请求体。

   在本例中，它是一个 `Item` 数据类列表。
6. 这里我们返回一个字典，里面的 `items` 是一个数据类列表。

   FastAPI 仍然能够将数据<dfn title="把数据转换为可以传输的格式">序列化</dfn>为 JSON。
7. 这里的 `response_model` 使用了 “`Author` 数据类列表” 的类型注解。

   同样，你可以将 `dataclasses` 与标准类型注解组合使用。
8. 注意，这个 *路径操作函数* 使用的是常规的 `def` 而不是 `async def`。

   一如既往，在 FastAPI 中你可以按需组合 `def` 和 `async def`。

   如果需要回顾何时用哪一个，请查看关于 [`async` 和 `await`](../async.md#in-a-hurry) 的文档中的 _“急不可待？”_ 一节。
9. 这个 *路径操作函数* 返回的不是数据类（当然也可以返回数据类），而是包含内部数据的字典列表。

   FastAPI 会使用（包含数据类的）`response_model` 参数来转换响应。

你可以将 `dataclasses` 与其它类型注解以多种不同方式组合，来构建复杂的数据结构。

更多细节请参考上面代码中的内联注释提示。

## 深入学习 { #learn-more }

你还可以把 `dataclasses` 与其它 Pydantic 模型组合、从它们继承、把它们包含到你自己的模型中等。

想了解更多，请查看 [Pydantic 关于 dataclasses 的文档](https://docs.pydantic.dev/latest/concepts/dataclasses/)。

## 版本 { #version }

自 FastAPI 版本 `0.67.0` 起可用。🔖



---

# Source: docs/advanced/events.md


# 生命周期事件 { #lifespan-events }


你可以定义在应用**启动**前执行的逻辑（代码）。这意味着在应用**开始接收请求**之前，这些代码只会被执行**一次**。

同样地，你可以定义在应用**关闭**时应执行的逻辑。在这种情况下，这段代码将在**处理可能的多次请求后**执行**一次**。

因为这段代码在应用开始接收请求**之前**执行，也会在处理可能的若干请求**之后**执行，它覆盖了整个应用程序的**生命周期**（“生命周期”这个词很重要😉）。

这对于设置你需要在整个应用中使用的**资源**非常有用，这些资源在请求之间**共享**，你可能需要在之后进行**释放**。例如，数据库连接池，或加载一个共享的机器学习模型。

## 用例 { #use-case }

让我们从一个示例**用例**开始，看看如何用它来解决问题。

假设你有几个**机器学习的模型**，你想要用它们来处理请求。🤖

相同的模型在请求之间是共享的，因此并非每个请求或每个用户各自拥有一个模型。

假设加载模型可能**需要相当长的时间**，因为它必须从**磁盘**读取大量数据。因此你不希望每个请求都加载它。

你可以在模块/文件的顶部加载它，但这也意味着即使你只是在运行一个简单的自动化测试，它也会**加载模型**，这样测试将**变慢**，因为它必须在能够独立运行代码的其他部分之前等待模型加载完成。

这就是我们要解决的问题——在处理请求前加载模型，但只是在应用开始接收请求前，而不是在代码被加载时。

## Lifespan { #lifespan }

你可以使用 `FastAPI` 应用的 `lifespan` 参数和一个“上下文管理器”（稍后我将为你展示）来定义**启动**和**关闭**的逻辑。

让我们从一个例子开始，然后详细介绍。

我们使用 `yield` 创建了一个异步函数 `lifespan()` 像这样：

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

在这里，我们在 `yield` 之前将（虚拟的）模型函数放入机器学习模型的字典中，以此模拟加载模型的耗时**启动**操作。这段代码将在应用程序**开始处理请求之前**执行，即**启动**期间。

然后，在 `yield` 之后，我们卸载模型。这段代码将会在应用程序**完成处理请求后**执行，即在**关闭**之前。这可以释放诸如内存或 GPU 之类的资源。

/// tip | 提示

**关闭**事件会在你**停止**应用时发生。

可能你需要启动一个新版本，或者你只是厌倦了运行它。 🤷

///

### 生命周期函数 { #lifespan-function }

首先要注意的是，我们定义了一个带有 `yield` 的异步函数。这与带有 `yield` 的依赖项非常相似。

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

这个函数在 `yield` 之前的部分，会在应用启动前执行。

剩下的部分在 `yield` 之后，会在应用完成后执行。

### 异步上下文管理器 { #async-context-manager }

如你所见，这个函数有一个装饰器 `@asynccontextmanager`。

它将函数转化为所谓的“**异步上下文管理器**”。

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

在 Python 中，**上下文管理器**是一个你可以在 `with` 语句中使用的东西，例如，`open()` 可以作为上下文管理器使用。

```Python
with open("file.txt") as file:
    file.read()
```

Python 的最近几个版本也有了一个**异步上下文管理器**，你可以通过 `async with` 来使用：

```Python
async with lifespan(app):
    await do_stuff()
```

你可以像上面一样创建一个上下文管理器或者异步上下文管理器，它的作用是在进入 `with` 块时，执行 `yield` 之前的代码，并且在离开 `with` 块时，执行 `yield` 后面的代码。

但在我们上面的例子里，我们并不是直接使用，而是传递给 FastAPI 来供其使用。

`FastAPI` 的 `lifespan` 参数接受一个**异步上下文管理器**，所以我们可以把我们新定义的异步上下文管理器 `lifespan` 传给它。

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## 替代事件（弃用） { #alternative-events-deprecated }

/// warning | 警告

配置**启动**和**关闭**的推荐方法是使用 `FastAPI` 应用的 `lifespan` 参数，如前所示。如果你提供了一个 `lifespan` 参数，启动（`startup`）和关闭（`shutdown`）事件处理器将不再生效。要么使用 `lifespan`，要么配置所有事件，两者不能共用。

你可以跳过这一部分。

///

有一种替代方法可以定义在**启动**和**关闭**期间执行的逻辑。

你可以定义在应用启动前或应用关闭时需要执行的事件处理器（函数）。

事件函数既可以声明为异步函数（`async def`），也可以声明为普通函数（`def`）。

### `startup` 事件 { #startup-event }

使用事件 `"startup"` 声明一个在应用启动前运行的函数：

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

本例中，`startup` 事件处理器函数为项目“数据库”（只是一个 `dict`）提供了一些初始值。

**FastAPI** 支持多个事件处理器函数。

只有所有 `startup` 事件处理器运行完毕，**FastAPI** 应用才开始接收请求。

### `shutdown` 事件 { #shutdown-event }

使用事件 `"shutdown"` 声明一个在应用关闭时运行的函数：

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

此处，`shutdown` 事件处理器函数会向文件 `log.txt` 写入一行文本 `"Application shutdown"`。

/// note | 注意

在 `open()` 函数中，`mode="a"` 指的是“追加”。因此这行文本会添加在文件已有内容之后，不会覆盖之前的内容。

///

/// tip | 提示

注意，本例使用 Python 标准的 `open()` 函数与文件交互。

这个函数执行 I/O（输入/输出）操作，需要“等待”内容写进磁盘。

但 `open()` 不使用 `async` 和 `await`。

因此，声明事件处理函数要使用 `def`，而不是 `async def`。

///

### `startup` 和 `shutdown` 一起使用 { #startup-and-shutdown-together }

启动和关闭的逻辑很可能是连接在一起的，你可能希望启动某个东西然后结束它，获取一个资源然后释放它等等。

在不共享逻辑或变量的不同函数中处理这些逻辑比较困难，因为你需要在全局变量中存储值或使用类似的方式。

因此，推荐使用上面所述的 `lifespan`。

## 技术细节 { #technical-details }

只是为好奇者提供的技术细节。🤓

在底层，这部分是 ASGI 技术规范中的 [Lifespan 协议](https://asgi.readthedocs.io/en/latest/specs/lifespan.html)的一部分，定义了称为 `startup` 和 `shutdown` 的事件。

/// note | 注意

你可以在 [Starlette 的 Lifespan 文档](https://www.starlette.dev/lifespan/) 中阅读更多关于 `lifespan` 处理器的内容。

包括如何处理生命周期状态，以便在代码的其他部分使用。

///

## 子应用 { #sub-applications }

🚨 请注意，这些生命周期事件（startup 和 shutdown）只会在主应用上执行，不会在[子应用 - 挂载](sub-applications.md)上执行。



---

# Source: docs/advanced/generate-clients.md


# 生成 SDK { #generating-sdks }

因为 **FastAPI** 基于 **OpenAPI** 规范，它的 API 可以用许多工具都能理解的标准格式来描述。

这让你可以轻松生成最新的**文档**、多语言的客户端库（<abbr title="Software Development Kits - 软件开发工具包">**SDKs**</abbr>），以及与代码保持同步的**测试**或**自动化工作流**。

本指南将带你为 FastAPI 后端生成一个 **TypeScript SDK**。

## 开源 SDK 生成器 { #open-source-sdk-generators }

一个功能多样的选择是 [OpenAPI Generator](https://openapi-generator.tech/)，它支持**多种编程语言**，可以根据你的 OpenAPI 规范生成 SDK。

对于 **TypeScript 客户端**，[Hey API](https://heyapi.dev/) 是为 TypeScript 生态打造的专用方案，提供优化的使用体验。

你还可以在 [OpenAPI.Tools](https://openapi.tools/#sdk) 上发现更多 SDK 生成器。

/// tip | 提示

FastAPI 会自动生成 **OpenAPI 3.1** 规范，因此你使用的任何工具都必须支持该版本。

///

## 创建一个 TypeScript SDK { #create-a-typescript-sdk }

先从一个简单的 FastAPI 应用开始：

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

请注意，这些*路径操作*使用 `Item` 和 `ResponseMessage` 模型来定义它们的请求载荷和响应载荷。

### API 文档 { #api-docs }

访问 `/docs` 时，你会看到有用于请求发送和响应接收数据的**模式**：

<img src="/img/tutorial/generate-clients/image01.png">

之所以能看到这些模式，是因为它们在应用中用模型声明了。

这些信息会包含在应用的 **OpenAPI 模式** 中，并显示在 API 文档里。

OpenAPI 中包含的这些模型信息就是用于**生成客户端代码**的基础。

### Hey API { #hey-api }

当我们有了带模型的 FastAPI 应用后，可以使用 Hey API 来生成 TypeScript 客户端。最快的方式是通过 npx。

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

这会在 `./src/client` 生成一个 TypeScript SDK。

你可以在其官网了解如何[安装 `@hey-api/openapi-ts`](https://heyapi.dev/openapi-ts/get-started)，以及阅读[生成结果](https://heyapi.dev/openapi-ts/output)的说明。

### 使用 SDK { #using-the-sdk }

现在你可以导入并使用客户端代码了。它可能是这样，并且你会发现方法有自动补全：

<img src="/img/tutorial/generate-clients/image02.png">

要发送的载荷也会有自动补全：

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | 提示

请注意 `name` 和 `price` 的自动补全，它们是在 FastAPI 应用中的 `Item` 模型里定义的。

///

你发送的数据会有**内联错误**：

<img src="/img/tutorial/generate-clients/image04.png">

响应对象同样有自动补全：

<img src="/img/tutorial/generate-clients/image05.png">

## 带有标签的 FastAPI 应用 { #fastapi-app-with-tags }

很多情况下，你的 FastAPI 应用会更大，你可能会用标签来划分不同组的*路径操作*。

例如，你可以有一个 **items** 相关的部分和另一个 **users** 相关的部分，它们可以用标签来分隔：

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### 生成带标签的 TypeScript 客户端 { #generate-a-typescript-client-with-tags }

如果你为使用了标签的 FastAPI 应用生成客户端，通常也会根据标签来拆分客户端代码。

这样你就可以在客户端代码中把内容正确地组织和分组：

<img src="/img/tutorial/generate-clients/image06.png">

在这个例子中，你会有：

* `ItemsService`
* `UsersService`

### 客户端方法名 { #client-method-names }

现在，像 `createItemItemsPost` 这样的生成方法名看起来不太简洁：

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...这是因为客户端生成器会使用每个*路径操作*的 OpenAPI 内部**操作 ID（operation ID）**。

OpenAPI 要求每个操作 ID 在所有*路径操作*中都是唯一的，因此 FastAPI 会使用**函数名**、**路径**和**HTTP 方法/操作**来生成操作 ID，因为这样可以确保操作 ID 是唯一的。

接下来我会告诉你如何改进。🤓

## 自定义操作 ID 与更好的方法名 { #custom-operation-ids-and-better-method-names }

你可以**修改**这些操作 ID 的**生成**方式，使之更简单，从而在客户端中得到**更简洁的方法名**。

在这种情况下，你需要用其他方式确保每个操作 ID 依然是**唯一**的。

例如，你可以确保每个*路径操作*都有一个标签，然后基于**标签**和*路径操作***名称**（函数名）来生成操作 ID。

### 自定义唯一 ID 生成函数 { #custom-generate-unique-id-function }

FastAPI 为每个*路径操作*使用一个**唯一 ID**，它既用于**操作 ID**，也用于请求或响应里任何需要的自定义模型名称。

你可以自定义这个函数。它接收一个 `APIRoute` 并返回一个字符串。

例如，这里使用第一个标签（你很可能只有一个标签）和*路径操作*名称（函数名）。

然后你可以把这个自定义函数通过 `generate_unique_id_function` 参数传给 **FastAPI**：

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### 使用自定义操作 ID 生成 TypeScript 客户端 { #generate-a-typescript-client-with-custom-operation-ids }

现在再次生成客户端，你会看到方法名已经改进：

<img src="/img/tutorial/generate-clients/image07.png">

如你所见，方法名现在由标签和函数名组成，不再包含 URL 路径和 HTTP 操作的信息。

### 为客户端生成器预处理 OpenAPI 规范 { #preprocess-the-openapi-specification-for-the-client-generator }

生成的代码中仍有一些**重复信息**。

我们已经知道这个方法与 **items** 有关，因为它位于 `ItemsService`（来自标签），但方法名里仍然带有标签名前缀。😕

通常我们仍然希望在 OpenAPI 中保留它，以确保操作 ID 的**唯一性**。

但对于生成的客户端，我们可以在生成之前**修改** OpenAPI 的操作 ID，只是为了让方法名更美观、更**简洁**。

我们可以把 OpenAPI JSON 下载到 `openapi.json` 文件中，然后用如下脚本**移除这个标签前缀**：

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

这样，操作 ID 会从 `items-get_items` 之类的名字重命名为 `get_items`，从而让客户端生成器生成更简洁的方法名。

### 使用预处理后的 OpenAPI 生成 TypeScript 客户端 { #generate-a-typescript-client-with-the-preprocessed-openapi }

因为最终结果现在保存在 `openapi.json` 中，你需要更新输入位置：

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

生成新客户端后，你将拥有**简洁的方法名**，并具备**自动补全**、**内联错误**等功能：

<img src="/img/tutorial/generate-clients/image08.png">

## 优点 { #benefits }

使用自动生成的客户端时，你会获得以下内容的**自动补全**：

* 方法。
* 请求体中的数据、查询参数等。
* 响应数据。

你还会为所有内容获得**内联错误**。

每当你更新后端代码并**重新生成**前端时，新的*路径操作*会作为方法可用，旧的方法会被移除，其他任何更改都会反映到生成的代码中。🤓

这也意味着如果有任何变更，它会自动**反映**到客户端代码中。而当你**构建**客户端时，如果所用数据存在任何**不匹配**，它会直接报错。

因此，你可以在开发周期的早期就**发现许多错误**，而不必等到错误在生产环境中暴露给最终用户后再去调试问题所在。✨



---

# Source: docs/advanced/index.md


# 高级用户指南 { #advanced-user-guide }

## 附加功能 { #additional-features }

主要的[教程 - 用户指南](../tutorial/index.md)足以带你了解 **FastAPI** 的所有主要特性。

在接下来的章节中，你将看到其他选项、配置和附加功能。

/// tip | 提示

接下来的章节**不一定是“高级”的**。

对于你的用例，解决方案很可能就在其中之一。

///

## 先阅读教程 { #read-the-tutorial-first }

仅凭主要[教程 - 用户指南](../tutorial/index.md)中的知识，你已经可以使用 **FastAPI** 的大多数功能。

接下来的章节默认你已经读过它，并理解其中的核心概念。



---

# Source: docs/advanced/json-base64-bytes.md


# 在 JSON 中使用 Base64 表示字节 { #json-with-bytes-as-base64 }

如果你的应用需要接收和发送 JSON 数据，但其中需要包含二进制数据，可以将其编码为 base64。

## Base64 与文件 { #base64-vs-files }

请先考虑是否可以使用 [请求文件](../tutorial/request-files.md) 来上传二进制数据，并使用 [自定义响应 - FileResponse](./custom-response.md#fileresponse) 来发送二进制数据，而不是把它编码进 JSON。

JSON 只能包含 UTF-8 编码的字符串，因此无法直接包含原始字节。

Base64 可以把二进制数据编码为字符串，但为此会使用比原始二进制更多的字符，因此通常比直接使用文件的效率更低。

仅当你确实需要在 JSON 中包含二进制数据且无法使用文件时，才使用 base64。

## Pydantic `bytes` { #pydantic-bytes }

你可以声明带有 `bytes` 字段的 Pydantic 模型，然后在模型配置中使用 `val_json_bytes` 指定用 base64 来*验证*输入的 JSON 数据；作为验证的一部分，它会将该 base64 字符串解码为字节。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

查看 `/docs` 时，你会看到字段 `data` 期望接收 base64 编码的字节：

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

你可以发送如下请求：

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | 提示

`aGVsbG8=` 是 `hello` 的 base64 编码。

///

随后 Pydantic 会解码该 base64 字符串，并在模型的 `data` 字段中提供原始字节。

你将会收到类似的响应：

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## 用于输出数据的 Pydantic `bytes` { #pydantic-bytes-for-output-data }

对于输出数据，你也可以在模型配置中为 `bytes` 字段使用 `ser_json_bytes`，Pydantic 会在生成 JSON 响应时将字节以 base64 进行*序列化*。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## 用于输入和输出数据的 Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

当然，你也可以使用同一个配置了 base64 的模型，在接收和发送 JSON 数据时，同时处理输入（使用 `val_json_bytes` 进行*验证*）和输出（使用 `ser_json_bytes` 进行*序列化*）。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}



---

# Source: docs/advanced/middleware.md


# 高级中间件 { #advanced-middleware }

用户指南介绍了如何为应用添加[自定义中间件](../tutorial/middleware.md)。

以及如何[使用 `CORSMiddleware` 处理 CORS](../tutorial/cors.md)。

本章学习如何使用其它中间件。

## 添加 ASGI 中间件 { #adding-asgi-middlewares }

因为 **FastAPI** 基于 Starlette，且执行 <abbr title="Asynchronous Server Gateway Interface - 异步服务器网关接口">ASGI</abbr> 规范，所以可以使用任意 ASGI 中间件。

中间件不必是专为 FastAPI 或 Starlette 定制的，只要遵循 ASGI 规范即可。

总之，ASGI 中间件是类，并把 ASGI 应用作为第一个参数。

因此，有些第三方 ASGI 中间件的文档推荐以如下方式使用中间件：

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

但 FastAPI（实际上是 Starlette）提供了一种更简单的方式，能让内部中间件在处理服务器错误的同时，还能让自定义异常处理器正常运作。

为此，要使用 `app.add_middleware()` （与 CORS 中的示例一样）。

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` 的第一个参数是中间件的类，其它参数则是要传递给中间件的参数。

## 集成中间件 { #integrated-middlewares }

**FastAPI** 为常见用例提供了一些中间件，下面介绍怎么使用这些中间件。

/// note | 技术细节

以下几个示例中也可以使用 `from starlette.middleware.something import SomethingMiddleware`。

**FastAPI** 在 `fastapi.middleware` 中提供的中间件只是为了方便开发者使用，但绝大多数可用的中间件都直接继承自 Starlette。

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

强制所有传入请求必须是 `https` 或 `wss`。

任何传向 `http` 或 `ws` 的请求都会被重定向至安全方案。

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

强制所有传入请求都必须正确设置 `Host` 请求头，以防 HTTP 主机头攻击。

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

支持以下参数：

* `allowed_hosts` - 允许的域名（主机名）列表。`*.example.com` 等通配符域名可以匹配子域名。若要允许任意主机名，可使用 `allowed_hosts=["*"]` 或省略此中间件。
* `www_redirect` - 若设置为 `True`，对允许主机的非 www 版本的请求将被重定向到其 www 版本。默认为 `True`。

如果传入的请求没有通过验证，则发送 `400` 响应。

## `GZipMiddleware` { #gzipmiddleware }

处理 `Accept-Encoding` 请求头中包含 `"gzip"` 请求的 GZip 响应。

中间件会处理标准响应与流响应。

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

支持以下参数：

* `minimum_size` - 小于该最小字节数的响应不使用 GZip。默认值是 `500`。
* `compresslevel` - GZip 压缩使用的级别，为 1 到 9 的整数。默认为 `9`。值越低压缩越快但文件更大，值越高压缩越慢但文件更小。

## 其它中间件 { #other-middlewares }

除了上述中间件外，FastAPI 还支持其它 ASGI 中间件。

例如：

* [Uvicorn 的 `ProxyHeadersMiddleware`](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)
* [MessagePack](https://github.com/florimondmanca/msgpack-asgi)

其它可用中间件详见 [Starlette 官档 - 中间件](https://www.starlette.dev/middleware/) 及 [ASGI Awesome 列表](https://github.com/florimondmanca/awesome-asgi)。



---

# Source: docs/advanced/openapi-callbacks.md


# OpenAPI 回调 { #openapi-callbacks }

你可以创建一个包含*路径操作*的 API，该*路径操作*可以触发对其他人创建的*外部 API*的请求（很可能就是那个会*使用*你的 API 的同一个开发者）。

当你的 API 应用调用*外部 API*时，这个过程被称为“回调”。因为外部开发者编写的软件会先向你的 API 发送请求，然后你的 API 再*回调*，向*外部 API*发送请求（很可能也是该开发者创建的）。

在这种情况下，你可能希望记录该外部 API *应该*是什么样子。它应该有哪些*路径操作*，应该接收什么请求体，应该返回什么响应等。

## 使用回调的应用 { #an-app-with-callbacks }

让我们通过一个例子来看这一切。

假设你开发一个可以创建发票的应用。

这些发票会有 `id`、`title`（可选）、`customer` 和 `total`。

你的 API 用户（外部开发者）会通过 POST 请求在你的 API 中创建一张发票。

然后你的 API 会（假设）：

* 将发票发送给外部开发者的某个客户。
* 收款。
* 向 API 用户（外部开发者）发回通知。
    * 这会通过（从*你的 API*）向该外部开发者提供的某个*外部 API*发送 POST 请求来完成（这就是“回调”）。

## 常规 **FastAPI** 应用 { #the-normal-fastapi-app }

我们先看看在添加回调之前，常规 API 应用会是什么样子。

它会有一个接收 `Invoice` 请求体的*路径操作*，以及一个包含回调 URL 的查询参数 `callback_url`。

这部分很常规，大部分代码你应该已经很熟悉了：

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[7:11,34:51] *}

/// tip | 提示

`callback_url` 查询参数使用 Pydantic 的 [Url](https://docs.pydantic.dev/latest/api/networks/) 类型。

///

唯一的新内容是*路径操作装饰器*中的参数 `callbacks=invoices_callback_router.routes`。接下来我们会看看它是什么。

## 为回调编写文档 { #documenting-the-callback }

实际的回调代码会高度依赖你自己的 API 应用。

而且很可能在不同应用之间差异很大。

它可能只有一两行代码，例如：

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

但回调最重要的部分可能是确保你的 API 用户（外部开发者）正确实现*外部 API*，与*你的 API*将在回调请求体中发送的数据等相匹配。

因此，接下来我们要做的是添加代码，用来记录该*外部 API*应该是什么样子，才能接收来自*你的 API*的回调。

这份文档会显示在你的 API 的 `/docs` 下的 Swagger UI 中，并且会让外部开发者知道如何构建*外部 API*。

本例不实现回调本身（那可能只是一行代码），只实现文档部分。

/// tip | 提示

实际的回调只是一个 HTTP 请求。

自己实现回调时，你可以使用类似 [HTTPX](https://www.python-httpx.org) 或 [Requests](https://requests.readthedocs.io/) 的工具。

///

## 编写回调文档代码 { #write-the-callback-documentation-code }

这段代码不会在你的应用中执行，我们只需要用它来*记录*该*外部 API*应该是什么样子。

不过，你已经知道如何使用 **FastAPI** 轻松为 API 创建自动文档了。

因此，我们会使用相同的知识来记录该*外部 API*应该是什么样子...通过创建外部 API 应该实现的*路径操作*（也就是你的 API 将调用的那些）。

/// tip | 提示

在编写用于记录回调的代码时，可以想象你就是那个*外部开发者*。而且你现在正在实现的是*外部 API*，不是*你的 API*。

临时采用这个（*外部开发者*的）视角，可以帮助你更清楚地判断该把参数、请求体的 Pydantic 模型、响应等放在该*外部 API*的什么位置。

///

### 创建回调 `APIRouter` { #create-a-callback-apirouter }

首先创建一个新的 `APIRouter`，它将包含一个或多个回调。

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[1,23] *}

### 创建回调*路径操作* { #create-the-callback-path-operation }

要创建回调*路径操作*，请使用你在上面创建的同一个 `APIRouter`。

它看起来应该就像普通的 FastAPI *路径操作*：

* 它可能应该声明要接收的请求体，例如 `body: InvoiceEvent`。
* 它也可以声明要返回的响应，例如 `response_model=InvoiceEventReceived`。

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[14:16,19:20,26:30] *}

它与普通*路径操作*有 2 个主要区别：

* 它不需要任何实际代码，因为你的应用永远不会调用这段代码。它只用于记录*外部 API*。因此，函数可以只有 `pass`。
* *路径*可以包含 [OpenAPI 3 表达式](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression)（见下文），其中可以使用带参数的变量，以及发送到*你的 API*的原始请求的部分内容。

### 回调路径表达式 { #the-callback-path-expression }

回调*路径*可以有一个 [OpenAPI 3 表达式](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression)，其中可以包含发送到*你的 API*的原始请求的部分内容。

在这个例子中，它是这个 `str`：

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

所以，如果你的 API 用户（外部开发者）向*你的 API*发送请求到：

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

并带有如下 JSON 请求体：

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

那么*你的 API*会处理该发票，并在稍后的某个时间点，向 `callback_url`（*外部 API*）发送回调请求：

```
https://www.external.org/events/invoices/2expen51ve
```

并带有类似如下内容的 JSON 请求体：

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

它会预期该*外部 API*返回类似如下 JSON 请求体的响应：

```JSON
{
    "ok": true
}
```

/// tip | 提示

请注意，使用的回调 URL 包含在 `callback_url` 中作为查询参数接收到的 URL（`https://www.external.org/events`），也包含 JSON 请求体内部的发票 `id`（`2expen51ve`）。

///

### 添加回调路由 { #add-the-callback-router }

此时，你已经在上面创建的回调路由中拥有了所需的*回调路径操作*（即*外部开发者*应该在*外部 API*中实现的那些）。

现在，在*你的 API 的路径操作装饰器*中使用参数 `callbacks`，传入该回调路由的 `.routes` 属性：

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[33] *}

/// tip | 提示

请注意，你不是把路由本身（`invoices_callback_router`）传给 `callbacks=`，而是传它的 `.routes`，也就是 `invoices_callback_router.routes`。FastAPI 会使用这些路由来生成回调的 OpenAPI 文档。

///

### 查看文档 { #check-the-docs }

现在你可以启动应用并访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到文档中为你的*路径操作*包含了一个 "Callbacks" 部分，展示了*外部 API*应该是什么样子：

<img src="/img/tutorial/openapi-callbacks/image01.png">



---

# Source: docs/advanced/openapi-webhooks.md


# OpenAPI 网络钩子 { #openapi-webhooks }

有些情况下，您可能想告诉您的 API **用户**，您的应用程序可以携带一些数据调用*他们的*应用程序（给它们发送请求），通常是为了**通知**某种**事件**。

这意味着，与通常由您的用户向您的 API 发送请求的流程相反，是**您的 API**（或您的应用）可以**向他们的系统**（他们的 API、他们的应用）**发送请求**。

这通常被称为**网络钩子**（Webhook）。

## 使用网络钩子的步骤 { #webhooks-steps }

通常的过程是**您**在代码中**定义**要发送的消息，即**请求的主体**。

您还需要以某种方式定义您的应用程序将在**何时**发送这些请求或事件。

**用户**会以某种方式（例如在某个网页仪表板上）定义您的应用程序发送这些请求应该使用的 **URL**。

所有关于注册网络钩子的 URL 的**逻辑**以及发送这些请求的实际代码都由您决定。您可以在**自己的代码**中以任何想要的方式来编写它。

## 使用 `FastAPI` 和 OpenAPI 文档化网络钩子 { #documenting-webhooks-with-fastapi-and-openapi }

使用 **FastAPI**，您可以利用 OpenAPI 来自定义这些网络钩子的名称、您的应用可以发送的 HTTP 操作类型（例如 `POST`、`PUT` 等）以及您的应用将发送的**请求体**。

这能让您的用户更轻松地**实现他们的 API** 来接收您的**网络钩子**请求，他们甚至可能能够自动生成一些自己的 API 代码。

/// note | 注意

网络钩子在 OpenAPI 3.1.0 及以上版本中可用，FastAPI `0.99.0` 及以上版本支持。

///

## 带有网络钩子的应用程序 { #an-app-with-webhooks }

当您创建一个 **FastAPI** 应用程序时，有一个 `webhooks` 属性可以用来定义网络钩子，方式与您定义*路径操作*的时候相同，例如使用 `@app.webhooks.post()` 。

{* ../../docs_src/openapi_webhooks/tutorial001_py310.py hl[9:12,15:20] *}

您定义的网络钩子将被包含在 `OpenAPI` 的架构中，并出现在自动生成的**文档 UI** 中。

/// note | 注意

`app.webhooks` 对象实际上只是一个 `APIRouter` ，与您在使用多个文件来构建应用程序时所使用的类型相同。

///

请注意，使用网络钩子时，您实际上并没有声明一个*路径*（比如 `/items/` ），您传递的文本只是这个网络钩子的**标识符**（事件的名称）。例如在 `@app.webhooks.post("new-subscription")` 中，网络钩子的名称是 `new-subscription` 。

这是因为我们预计**您的用户**会以其他方式（例如通过网页仪表板）来定义他们希望接收网络钩子的请求的实际 **URL 路径**。

### 查看文档 { #check-the-docs }

现在您可以启动您的应用程序并访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

您会看到您的文档不仅有正常的*路径操作*显示，现在还多了一些**网络钩子**：

<img src="/img/tutorial/openapi-webhooks/image01.png">



---

# Source: docs/advanced/path-operation-advanced-configuration.md


# 路径操作的高级配置 { #path-operation-advanced-configuration }

## OpenAPI 的 operationId { #openapi-operationid }

/// warning

如果你并非 OpenAPI 的“专家”，你可能不需要这部分内容。

///

你可以在 *路径操作* 中通过参数 `operation_id` 设置要使用的 OpenAPI `operationId`。

务必确保每个操作的 `operation_id` 都是唯一的。

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### 使用 *路径操作函数* 的函数名作为 operationId { #using-the-path-operation-function-name-as-the-operationid }

如果你想用 API 的函数名作为 `operationId`，你可以向 `FastAPI` 传入自定义的 `generate_unique_id_function`。

该函数会接收每个 `APIRoute`，并返回用于该路径操作的 `operationId`。

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2,5:6,9] *}

/// warning

如果你这样做，务必确保你的每个 *路径操作函数* 的名字唯一。

即使它们在不同的模块中（Python 文件）。

///

## 从 OpenAPI 中排除 { #exclude-from-openapi }

使用参数 `include_in_schema` 并将其设置为 `False`，来从生成的 OpenAPI 方案中排除一个 *路径操作*（这样一来，就从自动化文档系统中排除掉了）：

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## 来自 docstring 的高级描述 { #advanced-description-from-docstring }

你可以限制 *路径操作函数* 的 `docstring` 中用于 OpenAPI 的行数。

添加一个 `\f`（一个“换页”的转义字符）可以使 **FastAPI** 在那一位置截断用于 OpenAPI 的输出。

剩余部分不会出现在文档中，但是其他工具（比如 Sphinx）可以使用剩余部分。

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## 附加响应 { #additional-responses }

你可能已经见过如何为一个 *路径操作* 声明 `response_model` 和 `status_code`。

这定义了该 *路径操作* 主响应的元数据。

你也可以为它声明带有各自模型、状态码等的附加响应。

文档中有一个完整章节，你可以阅读这里的[OpenAPI 中的附加响应](additional-responses.md)。

## OpenAPI Extra { #openapi-extra }

当你在应用中声明一个 *路径操作* 时，**FastAPI** 会自动生成与该 *路径操作* 相关的元数据，以包含到 OpenAPI 方案中。

/// note | 技术细节

在 OpenAPI 规范中，这被称为 [Operation 对象](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object)。

///

它包含关于该 *路径操作* 的所有信息，并用于生成自动文档。

它包括 `tags`、`parameters`、`requestBody`、`responses` 等。

这个特定于 *路径操作* 的 OpenAPI 方案通常由 **FastAPI** 自动生成，但你也可以扩展它。

/// tip

这是一个较低层级的扩展点。

如果你只需要声明附加响应，更方便的方式是使用[OpenAPI 中的附加响应](additional-responses.md)。

///

你可以使用参数 `openapi_extra` 扩展某个 *路径操作* 的 OpenAPI 方案。

### OpenAPI 扩展 { #openapi-extensions }

例如，这个 `openapi_extra` 可用于声明 [OpenAPI 扩展](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions)：

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

当你打开自动 API 文档时，你的扩展会显示在该 *路径操作* 的底部。

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

如果你查看最终生成的 OpenAPI（在你的 API 的 `/openapi.json`），你也会看到你的扩展作为该 *路径操作* 的一部分：

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### 自定义 OpenAPI 路径操作方案 { #custom-openapi-path-operation-schema }

`openapi_extra` 中的字典会与该 *路径操作* 自动生成的 OpenAPI 方案进行深度合并。

因此，你可以在自动生成的方案上添加额外数据。

例如，你可以决定用自己的代码读取并验证请求，而不使用 FastAPI 与 Pydantic 的自动功能，但你仍然希望在 OpenAPI 方案中定义该请求。

你可以用 `openapi_extra` 来做到：

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

在这个示例中，我们没有声明任何 Pydantic 模型。事实上，请求体甚至没有被 <dfn title="从某种纯文本格式（如字节）转换为 Python 对象">解析</dfn> 为 JSON，而是直接以 `bytes` 读取，并由函数 `magic_data_reader()` 以某种方式负责解析。

尽管如此，我们仍然可以声明请求体的预期方案。

### 自定义 OpenAPI 内容类型 { #custom-openapi-content-type }

使用同样的技巧，你可以用一个 Pydantic 模型来定义 JSON Schema，然后把它包含到该 *路径操作* 的自定义 OpenAPI 方案部分中。

即使请求中的数据类型不是 JSON，你也可以这样做。

例如，在这个应用中我们不使用 FastAPI 集成的从 Pydantic 模型提取 JSON Schema 的功能，也不使用对 JSON 的自动校验。实际上，我们将请求的内容类型声明为 YAML，而不是 JSON：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

尽管我们没有使用默认的集成功能，我们仍然使用 Pydantic 模型手动生成我们想以 YAML 接收的数据的 JSON Schema。

然后我们直接使用请求并将请求体提取为 `bytes`。这意味着 FastAPI 甚至不会尝试将请求负载解析为 JSON。

接着在我们的代码中，我们直接解析该 YAML 内容，然后再次使用同一个 Pydantic 模型来验证该 YAML 内容：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip

这里我们复用了同一个 Pydantic 模型。

但同样地，我们也可以用其他方式对其进行验证。

///



---

# Source: docs/advanced/response-change-status-code.md


# 响应 - 更改状态码 { #response-change-status-code }

你可能之前已经了解到，你可以设置默认的[响应状态码](../tutorial/response-status-code.md)。

但在某些情况下，你需要返回一个不同于默认值的状态码。

## 使用场景 { #use-case }

例如，假设你想默认返回一个HTTP状态码为“OK”`200`。

但如果数据不存在，你想创建它，并返回一个HTTP状态码为“CREATED”`201`。

但你仍然希望能够使用`response_model`过滤和转换你返回的数据。

对于这些情况，你可以使用一个`Response`参数。

## 使用 `Response` 参数 { #use-a-response-parameter }

你可以在你的*路径操作函数*中声明一个`Response`类型的参数（就像你可以为cookies和头部做的那样）。

然后你可以在这个*临时*响应对象中设置`status_code`。

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

然后你可以像平常一样返回任何你需要的对象（一个`dict`、一个数据库模型等）。

如果你声明了一个`response_model`，它仍然会被用来过滤和转换你返回的对象。

**FastAPI**将使用这个*临时*响应来提取状态码（也包括cookies和头部），并将它们放入包含你返回的值的最终响应中，该响应由任何`response_model`过滤。

你也可以在依赖项中声明`Response`参数，并在其中设置状态码。但请注意，最后设置的状态码将会生效。



---

# Source: docs/advanced/response-cookies.md


# 响应 Cookies { #response-cookies }

## 使用 `Response` 参数 { #use-a-response-parameter }

你可以在*路径操作函数*中声明一个类型为 `Response` 的参数。

然后你可以在这个*临时*响应对象中设置 Cookie。

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

然后你可以像平常一样返回所需的任何对象（`dict`、数据库模型等）。

如果你声明了 `response_model`，它仍会用于过滤和转换你返回的对象。

**FastAPI** 会使用这个*临时*响应来提取 Cookie（还有 header 和状态码），并将它们放入最终响应中；最终响应包含你返回的值，并经过任何 `response_model` 过滤。

你也可以在依赖项中声明 `Response` 参数，并在其中设置 Cookie（和 header）。

## 直接返回 `Response` { #return-a-response-directly }

在代码中直接返回 `Response` 时，你也可以创建 Cookie。

为此，你可以按照[直接返回 Response](response-directly.md)中的说明创建一个响应。

然后在其中设置 Cookie，并返回它：

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | 提示

请记住，如果你直接返回响应，而不是使用 `Response` 参数，FastAPI 会直接返回它。

因此，你必须确保你的数据类型正确。例如，如果你返回的是 `JSONResponse`，数据就需要兼容 JSON。

并且还要确保你没有发送本应由 `response_model` 过滤的数据。

///

### 更多信息 { #more-info }

/// note | 技术细节

你也可以使用 `from starlette.responses import Response` 或者 `from starlette.responses import JSONResponse`。

**FastAPI** 为了方便开发者，提供了与 `starlette.responses` 相同的 `fastapi.responses`。但大多数可用的响应都直接来自 Starlette。

由于 `Response` 经常用于设置 header 和 Cookie，**FastAPI** 也在 `fastapi.Response` 中提供了它。

///

要查看所有可用参数和选项，请查看 [Starlette 文档](https://www.starlette.dev/responses/#set-cookie)。



---

# Source: docs/advanced/response-directly.md


# 直接返回响应 { #return-a-response-directly }

当你创建一个 **FastAPI** *路径操作* 时，你可以正常返回以下任意一种数据：`dict`，`list`，Pydantic 模型，数据库模型等等。

如果你声明了 [响应模型](../tutorial/response-model.md)，FastAPI 会使用它通过 Pydantic 将数据序列化为 JSON。

如果你没有声明响应模型，**FastAPI** 会使用在 [JSON 兼容编码器](../tutorial/encoder.md) 中阐述的 `jsonable_encoder`。
然后，**FastAPI** 会将其放入一个 `JSONResponse` 中。

你也可以直接创建一个 `JSONResponse` 并返回它。

/// tip | 提示

通常使用 [响应模型](../tutorial/response-model.md) 会比直接返回 `JSONResponse` 拥有更好的性能，因为它会在 Rust 中使用 Pydantic 序列化数据。

///

## 返回 `Response` { #return-a-response }

你可以返回一个 `Response` 或其任意子类。

/// note | 注意

`JSONResponse` 本身是一个 `Response` 的子类。

///

当你返回一个 `Response` 时，**FastAPI** 会直接传递它。

**FastAPI** 不会用 Pydantic 模型做任何数据转换，不会将响应内容转换成任何类型，等等。

这种特性给你极大的可扩展性。你可以返回任何数据类型，重写任何数据声明或者校验，等等。

这也带来了很大的责任。你必须确保你返回的数据是正确的、格式正确、可被序列化，等等。

## 在 `Response` 中使用 `jsonable_encoder` { #using-the-jsonable-encoder-in-a-response }

由于 **FastAPI** 并未对你返回的 `Response` 做任何改变，你必须确保你已经准备好响应内容。

例如，如果不首先将 Pydantic 模型转换为 `dict`，并将所有数据类型（如 `datetime`、`UUID` 等）转换为兼容 JSON 的类型，则不能将其放入 `JSONResponse` 中。

对于这些情况，在将数据传递给响应之前，你可以使用 `jsonable_encoder` 来转换你的数据：

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | 技术细节

你也可以使用 `from starlette.responses import JSONResponse`。

出于方便，**FastAPI** 会提供与 `starlette.responses` 相同的 `fastapi.responses` 给开发者。但是大多数可用的响应都直接来自 Starlette。

///

## 返回自定义 `Response` { #returning-a-custom-response }

上面的例子展示了需要的所有部分，但还不够实用，因为你本可以只是直接返回 `item`，而 **FastAPI** 默认帮你把这个 `item` 放到 `JSONResponse` 中，又默认将其转换成了 `dict` 等等。

现在，让我们看看你如何才能返回一个自定义的响应。

假设你想要返回一个 [XML](https://en.wikipedia.org/wiki/XML) 响应。

你可以把你的 XML 内容放到一个字符串中，放到一个 `Response` 中，然后返回：

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## 响应模型如何工作 { #how-a-response-model-works }

当你在路径操作中声明一个 [响应模型 - 返回类型](../tutorial/response-model.md) 时，**FastAPI** 会使用它通过 Pydantic 将数据序列化为 JSON。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

由于这些工作会在 Rust 侧完成，性能将比在常规 Python 中配合 `JSONResponse` 类完成要好得多。

当使用 `response_model` 或返回类型时，FastAPI 不会使用 `jsonable_encoder` 来转换数据（那样会更慢），也不会使用 `JSONResponse` 类。

相反，它会采用使用该响应模型（或返回类型）由 Pydantic 生成的 JSON 字节，并直接返回一个具有正确 JSON 媒体类型（`application/json`）的 `Response`。

## 说明 { #notes }

当你直接返回 `Response` 时，它的数据既没有校验，又不会进行转换（序列化），也不会自动生成文档。

但是你仍可以参考 [OpenAPI 中的额外响应](additional-responses.md) 给响应编写文档。

在后续的章节中你可以了解到如何使用/声明这些自定义的 `Response` 的同时还保留自动化的数据转换和文档等。



---

# Source: docs/advanced/response-headers.md


# 响应头 { #response-headers }


## 使用 `Response` 参数 { #use-a-response-parameter }

你可以在你的*路径操作函数*中声明一个 `Response` 类型的参数（就像你可以为 cookies 做的那样）。

然后你可以在这个*临时*响应对象中设置头部。

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

然后你可以像平常一样返回任何你需要的对象（例如一个 `dict` 或者一个数据库模型）。

如果你声明了一个 `response_model`，它仍然会被用来过滤和转换你返回的对象。

**FastAPI** 将使用这个*临时*响应来提取头部（也包括 cookies 和状态码），并将它们放入包含你返回的值的最终响应中，该响应由任何 `response_model` 过滤。

你也可以在依赖项中声明 `Response` 参数，并在其中设置头部（和 cookies）。

## 直接返回 `Response` { #return-a-response-directly }

你也可以在直接返回 `Response` 时添加头部。

按照[直接返回响应](response-directly.md)中所述创建响应，并将头部作为附加参数传递：

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | 技术细节

你也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。

**FastAPI** 提供了与 `fastapi.responses` 相同的 `starlette.responses`，只是为了方便你（开发者）。但是，大多数可用的响应都直接来自 Starlette。

由于 `Response` 经常用于设置头部和 cookies，**FastAPI** 还在 `fastapi.Response` 中提供了它。

///

## 自定义头部 { #custom-headers }

请注意，可以通过[使用 `X-` 前缀](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)添加自定义专有头部。

但是，如果你有自定义头部，并希望浏览器中的客户端能够看到它们，你需要将它们添加到你的 CORS 配置中（在 [CORS（跨源资源共享）](../tutorial/cors.md) 中阅读更多），使用在 [Starlette 的 CORS 文档](https://www.starlette.dev/middleware/#corsmiddleware)中记录的 `expose_headers` 参数。



---

# Source: docs/advanced/security/http-basic-auth.md


# HTTP 基础授权 { #http-basic-auth }

最简单的用例是使用 HTTP 基础授权（HTTP Basic Auth）。

在 HTTP 基础授权中，应用需要请求头包含用户名与密码。

如果没有接收到 HTTP 基础授权，就返回 HTTP 401 `"Unauthorized"` 错误。

并返回响应头 `WWW-Authenticate`，其值为 `Basic`，以及可选的 `realm` 参数。

HTTP 基础授权让浏览器显示内置的用户名与密码提示。

输入用户名与密码后，浏览器会把它们自动发送至请求头。

## 简单的 HTTP 基础授权 { #simple-http-basic-auth }

* 导入 `HTTPBasic` 与 `HTTPBasicCredentials`
* 使用 `HTTPBasic` 创建**安全方案**
* 在*路径操作*的依赖项中使用 `security`
* 返回类型为 `HTTPBasicCredentials` 的对象：
    * 包含发送的 `username` 与 `password`

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

第一次打开 URL（或在 API 文档中点击 **Execute** 按钮）时，浏览器要求输入用户名与密码：

<img src="/img/tutorial/security/image12.png">

## 检查用户名 { #check-the-username }

以下是更完整的示例。

使用依赖项检查用户名与密码是否正确。

为此要使用 Python 标准模块 [`secrets`](https://docs.python.org/3/library/secrets.html) 检查用户名与密码。

`secrets.compare_digest()` 需要仅包含 ASCII 字符（英语字符）的 `bytes` 或 `str`，这意味着它不适用于像`á`一样的字符，如 `Sebastián`。

为了解决这个问题，我们首先将 `username` 和 `password` 转换为使用 UTF-8 编码的 `bytes` 。

然后我们可以使用 `secrets.compare_digest()` 来确保 `credentials.username` 是 `"stanleyjobson"`，且 `credentials.password` 是`"swordfish"`。

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

这类似于：

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

但使用 `secrets.compare_digest()`，可以防御**时差攻击**，更加安全。

### 时差攻击 { #timing-attacks }

什么是**时差攻击**？

假设攻击者试图猜出用户名与密码。

他们发送用户名为 `johndoe`，密码为 `love123` 的请求。

然后，Python 代码执行如下操作：

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

但就在 Python 比较完 `johndoe` 的第一个字母 `j` 与 `stanleyjobson` 的 `s` 时，Python 就已经知道这两个字符串不相同了，它会这么想，**没必要浪费更多时间执行剩余字母的对比计算了**。应用立刻就会返回**错误的用户或密码**。

但接下来，攻击者继续尝试 `stanleyjobsox` 和 密码 `love123`。

应用代码会执行类似下面的操作：

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

此时，Python 要对比 `stanleyjobsox` 与 `stanleyjobson` 中的 `stanleyjobso`，才能知道这两个字符串不一样。因此会多花费几微秒来返回**错误的用户或密码**。

#### 反应时间对攻击者的帮助 { #the-time-to-answer-helps-the-attackers }

通过服务器花费了更多微秒才发送**错误的用户或密码**响应，攻击者会知道猜对了一些内容，起码开头字母是正确的。

然后，他们就可以放弃 `johndoe`，再用类似 `stanleyjobsox` 的内容进行尝试。

#### **专业**攻击 { #a-professional-attack }

当然，攻击者不用手动操作，而是编写每秒能执行成千上万次测试的攻击程序，每次都会找到更多正确字符。

但是，在您的应用的**帮助**下，攻击者利用时间差，就能在几分钟或几小时内，以这种方式猜出正确的用户名和密码。

#### 使用 `secrets.compare_digest()` 修补 { #fix-it-with-secrets-compare-digest }

在此，代码中使用了 `secrets.compare_digest()`。

简单的说，它使用相同的时间对比 `stanleyjobsox` 和 `stanleyjobson`，还有 `johndoe` 和 `stanleyjobson`。对比密码时也一样。

在代码中使用 `secrets.compare_digest()` ，就可以安全地防御这整类安全攻击。

### 返回错误 { #return-the-error }

检测到凭证不正确后，返回 `HTTPException` 及状态码 401（与无凭证时返回的内容一样），并添加响应头 `WWW-Authenticate`，让浏览器再次显示登录提示：

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}



---

# Source: docs/advanced/security/index.md


# 高级安全 { #advanced-security }

## 附加特性 { #additional-features }

除 [教程 - 用户指南: 安全性](../../tutorial/security/index.md) 中涵盖的功能之外，还有一些额外的功能来处理安全性。

/// tip | 提示

接下来的章节**并不一定是 "高级的"**。

而且对于你的使用场景来说，解决方案很可能就在其中。

///

## 先阅读教程 { #read-the-tutorial-first }

接下来的部分假设你已经阅读了主要的 [教程 - 用户指南: 安全性](../../tutorial/security/index.md)。

它们都基于相同的概念，但支持一些额外的功能。



---

# Source: docs/advanced/security/oauth2-scopes.md


# OAuth2 作用域 { #oauth2-scopes }

你可以在 **FastAPI** 中直接使用 OAuth2 作用域（Scopes），它们已无缝集成。

这样你就可以按照 OAuth2 标准，构建更精细的权限系统，并将其集成进你的 OpenAPI 应用（以及 API 文档）中。

带作用域的 OAuth2 是很多大型身份验证提供商使用的机制，例如 Facebook、Google、GitHub、Microsoft、X (Twitter) 等。它们用它来为用户和应用授予特定权限。

每次你“使用” Facebook、Google、GitHub、Microsoft、X (Twitter) “登录”时，该应用就在使用带作用域的 OAuth2。

本节将介绍如何在你的 **FastAPI** 应用中，使用相同的带作用域的 OAuth2 管理认证与授权。

/// warning | 警告

本节内容相对进阶，如果你刚开始，可以先跳过。

你并不一定需要 OAuth2 作用域，你也可以用你自己的方式处理认证与授权。

但带作用域的 OAuth2 能很好地集成进你的 API（通过 OpenAPI）和 API 文档。

不过，无论如何，你都可以在代码中按需强制这些作用域，或任何其它安全/授权需求。

很多情况下，带作用域的 OAuth2 可能有点“大材小用”。

但如果你确实需要它，或者只是好奇，请继续阅读。

///

## OAuth2 作用域与 OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 规范将“作用域”定义为由空格分隔的字符串列表。

这些字符串的内容可以是任意格式，但不应包含空格。

这些作用域表示“权限”。

在 OpenAPI（例如 API 文档）中，你可以定义“安全方案”（security schemes）。

当这些安全方案使用 OAuth2 时，你还可以声明并使用作用域。

每个“作用域”只是一个（不带空格的）字符串。

它们通常用于声明特定的安全权限，例如：

* 常见示例：`users:read` 或 `users:write`
* Facebook / Instagram 使用 `instagram_basic`
* Google 使用 `https://www.googleapis.com/auth/drive`

/// note | 注意

在 OAuth2 中，“作用域”只是一个声明所需特定权限的字符串。

是否包含像 `:` 这样的字符，或者是不是一个 URL，并不重要。

这些细节取决于具体实现。

对 OAuth2 而言，它们都只是字符串。

///

## 全局纵览 { #global-view }

首先，让我们快速看看与**用户指南**中 [OAuth2 实现密码（含哈希）、Bearer + JWT 令牌](../../tutorial/security/oauth2-jwt.md) 示例相比有哪些变化。现在开始使用 OAuth2 作用域：

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

下面我们逐步回顾这些更改。

## OAuth2 安全方案 { #oauth2-security-scheme }

第一个变化是：我们在声明 OAuth2 安全方案时，添加了两个可用的作用域 `me` 和 `items`。

参数 `scopes` 接收一个 `dict`，以作用域为键、描述为值：

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

因为我们现在声明了这些作用域，所以当你登录/授权时，它们会显示在 API 文档里。

你可以选择要授予访问权限的作用域：`me` 和 `items`。

这与使用 Facebook、Google、GitHub 等登录时授予权限的机制相同：

<img src="/img/tutorial/security/image11.png">

## 带作用域的 JWT 令牌 { #jwt-token-with-scopes }

现在，修改令牌的*路径操作*以返回请求的作用域。

我们仍然使用 `OAuth2PasswordRequestForm`。它包含 `scopes` 属性，其值是 `list` of `str`，包含请求中接收到的每个作用域。

我们把这些作用域作为 JWT 令牌的一部分返回。

/// danger | 危险

为简单起见，此处我们只是把接收到的作用域直接添加到了令牌中。

但在你的应用里，为了安全起见，你应该只添加该用户实际能够拥有的作用域，或你预先定义的作用域。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## 在*路径操作*与依赖项中声明作用域 { #declare-scopes-in-path-operations-and-dependencies }

现在我们声明，路径操作 `/users/me/items/` 需要作用域 `items`。

为此，从 `fastapi` 导入并使用 `Security`。

你可以用 `Security` 来声明依赖（就像 `Depends` 一样），但 `Security` 还接收一个 `scopes` 参数，其值是作用域（字符串）列表。

在这里，我们把依赖函数 `get_current_active_user` 传给 `Security`（就像用 `Depends` 一样）。

同时还传入一个作用域 `list`，此处仅包含一个作用域：`items`（也可以包含更多）。

依赖函数 `get_current_active_user` 也可以声明子依赖，不仅可以用 `Depends`，也可以用 `Security`。它声明了自己的子依赖函数（`get_current_user`），并添加了更多的作用域需求。

在这个例子里，它需要作用域 `me`（也可以需要多个作用域）。

/// note | 注意

不必在不同位置添加不同的作用域。

这里这样做，是为了演示 **FastAPI** 如何处理在不同层级声明的作用域。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// note | 技术细节

`Security` 实际上是 `Depends` 的子类，它只多了一个我们稍后会看到的参数。

但当你使用 `Security` 而不是 `Depends` 时，**FastAPI** 会知道它可以声明安全作用域，在内部使用它们，并用 OpenAPI 文档化 API。

另外，从 `fastapi` 导入的 `Query`、`Path`、`Depends`、`Security` 等，实际上都是返回特殊类的函数。

///

## 使用 `SecurityScopes` { #use-securityscopes }

现在更新依赖项 `get_current_user`。

上面那些依赖会用到它。

这里我们使用之前创建的同一个 OAuth2 方案，并把它声明为依赖：`oauth2_scheme`。

因为这个依赖函数本身没有任何作用域需求，所以我们可以用 `Depends(oauth2_scheme)`，当不需要指定安全作用域时，不必使用 `Security`。

我们还声明了一个从 `fastapi.security` 导入的特殊参数 `SecurityScopes` 类型。

这个 `SecurityScopes` 类类似于 `Request`（`Request` 用来直接获取请求对象）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## 使用 `scopes` { #use-the-scopes }

参数 `security_scopes` 的类型是 `SecurityScopes`。

它会有一个 `scopes` 属性，包含一个列表，里面是它自身以及所有把它作为子依赖的依赖项所需要的所有作用域。也就是说，所有“依赖者”……这可能有点绕，下面会再次解释。

`security_scopes` 对象（类型为 `SecurityScopes`）还提供了一个 `scope_str` 属性，它是一个用空格分隔这些作用域的单个字符串（我们将会用到它）。

我们创建一个 `HTTPException`，后面可以在多个位置复用（`raise`）它。

在这个异常中，我们包含所需的作用域（如果有的话），以空格分隔的字符串（使用 `scope_str`）。我们把这个包含作用域的字符串放在 `WWW-Authenticate` 响应头中（这是规范要求的一部分）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## 校验 `username` 与数据形状 { #verify-the-username-and-data-shape }

我们校验是否获取到了 `username`，并提取作用域。

然后使用 Pydantic 模型验证这些数据（捕获 `ValidationError` 异常），如果读取 JWT 令牌或用 Pydantic 验证数据时出错，就抛出我们之前创建的 `HTTPException`。

为此，我们给 Pydantic 模型 `TokenData` 添加了一个新属性 `scopes`。

通过用 Pydantic 验证数据，我们可以确保确实得到了例如一个由作用域组成的 `list` of `str`，以及一个 `str` 类型的 `username`。

而不是，例如得到一个 `dict` 或其它什么，这可能会在后续某个时刻破坏应用，形成安全风险。

我们还验证是否存在该用户名的用户，如果没有，就抛出前面创建的同一个异常。

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## 校验 `scopes` { #verify-the-scopes }

现在我们要验证，这个依赖以及所有依赖者（包括*路径操作*）所需的所有作用域，是否都包含在接收到的令牌里的作用域中，否则就抛出 `HTTPException`。

为此，我们使用 `security_scopes.scopes`，它包含一个由这些作用域组成的 `list[str]`。

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## 依赖树与作用域 { #dependency-tree-and-scopes }

再次回顾这个依赖树与作用域。

由于 `get_current_active_user` 依赖把 `get_current_user` 作为子依赖，因此在 `get_current_active_user` 中声明的作用域 `"me"` 会被包含在传给 `get_current_user` 的 `security_scopes.scopes` 所需作用域列表中。

*路径操作*本身也声明了一个作用域 `"items"`，它也会包含在传给 `get_current_user` 的 `security_scopes.scopes` 列表中。

依赖与作用域的层级结构如下：

* *路径操作* `read_own_items` 包含：
    * 带有依赖的必需作用域 `["items"]`：
    * `get_current_active_user`：
        *  依赖函数 `get_current_active_user` 包含：
            * 带有依赖的必需作用域 `["me"]`：
            * `get_current_user`：
                * 依赖函数 `get_current_user` 包含：
                    * 自身不需要任何作用域。
                    * 一个使用 `oauth2_scheme` 的依赖。
                    * 一个类型为 `SecurityScopes` 的 `security_scopes` 参数：
                        * 该 `security_scopes` 参数有一个 `scopes` 属性，它是一个包含上面所有已声明作用域的 `list`，因此：
                            * 对于*路径操作* `read_own_items`，`security_scopes.scopes` 将包含 `["me", "items"]`。
                            * 对于*路径操作* `read_users_me`，`security_scopes.scopes` 将包含 `["me"]`，因为它在依赖 `get_current_active_user` 中被声明。
                            * 对于*路径操作* `read_system_status`，`security_scopes.scopes` 将包含 `[]`（空列表），因为它既没有声明任何带 `scopes` 的 `Security`，其依赖 `get_current_user` 也没有声明任何 `scopes`。

/// tip | 提示

这里重要且“神奇”的地方是，`get_current_user` 在检查每个*路径操作*时会得到不同的 `scopes` 列表。

这一切都取决于为该特定*路径操作*在其自身以及依赖树中的每个依赖里声明的 `scopes`。

///

## 关于 `SecurityScopes` 的更多细节 { #more-details-about-securityscopes }

你可以在任意位置、多个位置使用 `SecurityScopes`，不一定非得在“根”依赖里。

它总会包含当前 `Security` 依赖中以及所有依赖者在“该特定”*路径操作*和“该特定”依赖树里声明的安全作用域。

因为 `SecurityScopes` 会包含依赖者声明的所有作用域，你可以在一个核心依赖函数里用它验证令牌是否具有所需作用域，然后在不同的*路径操作*里声明不同的作用域需求。

它们会针对每个*路径操作*分别检查。

## 查看文档 { #check-it }

打开 API 文档，你可以进行身份验证，并指定要授权的作用域。

<img src="/img/tutorial/security/image11.png">

如果你不选择任何作用域，你依然会“通过认证”，但当你访问 `/users/me/` 或 `/users/me/items/` 时，会收到一个错误，提示你没有足够的权限。你仍然可以访问 `/status/`。

如果你选择了作用域 `me`，但没有选择作用域 `items`，你可以访问 `/users/me/`，但不能访问 `/users/me/items/`。

当第三方应用使用用户提供的令牌访问这些*路径操作*时，也会发生同样的情况，取决于用户授予该应用了多少权限。

## 关于第三方集成 { #about-third-party-integrations }

在这个示例中我们使用的是 OAuth2 的“password”流。

当我们登录自己的应用（很可能还有我们自己的前端）时，这是合适的。

因为我们可以信任它来接收 `username` 和 `password`，毕竟我们掌控它。

但如果你在构建一个 OAuth2 应用，让其它应用来连接（也就是说，你在构建等同于 Facebook、Google、GitHub 等的身份验证提供商），你应该使用其它的流。

最常见的是隐式流（implicit flow）。

最安全的是代码流（authorization code flow），但实现更复杂，需要更多步骤。也因为更复杂，很多提供商最终会建议使用隐式流。

/// note | 注意

每个身份验证提供商常常会用不同的方式给它们的流命名，以融入自己的品牌。

但归根结底，它们实现的都是同一个 OAuth2 标准。

///

**FastAPI** 在 `fastapi.security.oauth2` 中为所有这些 OAuth2 身份验证流提供了工具。

## 装饰器 `dependencies` 中的 `Security` { #security-in-decorator-dependencies }

就像你可以在装饰器的 `dependencies` 参数中定义 `Depends` 的 `list`（详见[路径操作装饰器依赖项](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md)），你也可以在那儿配合 `Security` 使用 `scopes`。



---

# Source: docs/advanced/settings.md


# 设置和环境变量 { #settings-and-environment-variables }

在许多情况下，你的应用可能需要一些外部设置或配置，例如密钥、数据库凭据、电子邮件服务的凭据等。

这些设置中的大多数是可变的（可能会改变），例如数据库 URL。并且很多可能是敏感的，比如密钥。

因此，通常会将它们提供为由应用程序读取的环境变量。

/// tip | 提示

要理解环境变量，你可以阅读[环境变量](../environment-variables.md)。

///

## 类型和验证 { #types-and-validation }

这些环境变量只能处理文本字符串，因为它们在 Python 之外，并且必须与其他程序及系统的其余部分兼容（甚至与不同的操作系统，如 Linux、Windows、macOS）。

这意味着，在 Python 中从环境变量读取的任何值都是 `str` 类型，任何到不同类型的转换或任何验证都必须在代码中完成。

## Pydantic 的 `Settings` { #pydantic-settings }

幸运的是，Pydantic 提供了一个很好的工具来处理来自环境变量的这些设置：[Pydantic：Settings 管理](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)。

### 安装 `pydantic-settings` { #install-pydantic-settings }

首先，确保你创建并激活了[虚拟环境](../virtual-environments.md)，然后安装 `pydantic-settings` 包：

<div class="termy">

```console
$ pip install pydantic-settings
---> 100%
```

</div>

当你用以下方式安装 `all` 扩展时，它也会被一并安装：

<div class="termy">

```console
$ pip install "fastapi[all]"
---> 100%
```

</div>

### 创建 `Settings` 对象 { #create-the-settings-object }

从 Pydantic 导入 `BaseSettings` 并创建一个子类，这与创建 Pydantic 模型非常相似。

与 Pydantic 模型一样，用类型注解声明类属性，也可以指定默认值。

你可以使用与 Pydantic 模型相同的验证功能和工具，例如不同的数据类型，以及使用 `Field()` 进行附加验证。

{* ../../docs_src/settings/tutorial001_py310.py hl[2,5:8,11] *}

/// tip | 提示

如果你想要一个可以快速复制粘贴的示例，请不要使用这个示例，使用下面最后一个示例。

///

当你创建该 `Settings` 类的实例（此处是 `settings` 对象）时，Pydantic 会以不区分大小写的方式读取环境变量，因此，大写变量 `APP_NAME` 仍会用于属性 `app_name`。

接着它会转换并验证数据。因此，当你使用该 `settings` 对象时，你将获得你声明的类型的数据（例如 `items_per_user` 将是 `int`）。

### 使用 `settings` { #use-the-settings }

然后你可以在应用中使用新的 `settings` 对象：

{* ../../docs_src/settings/tutorial001_py310.py hl[18:20] *}

### 运行服务器 { #run-the-server }

接下来，运行服务器，并把配置作为环境变量传入，例如你可以设置 `ADMIN_EMAIL` 和 `APP_NAME`：

<div class="termy">

```console
$ ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" fastapi run main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

/// tip | 提示

要为单个命令设置多个环境变量，只需用空格分隔它们，并把它们都放在命令前面。

///

然后，`admin_email` 设置将为 `"deadpool@example.com"`。

`app_name` 将为 `"ChimichangApp"`。

而 `items_per_user` 会保持默认值 `50`。

## 在另一个模块中放置设置 { #settings-in-another-module }

你可以把这些设置放在另一个模块文件中，就像你在[更大的应用 - 多个文件](../tutorial/bigger-applications.md)中看到的那样。

例如，可以有一个 `config.py` 文件：

{* ../../docs_src/settings/app01_py310/config.py *}

然后在 `main.py` 文件中使用它：

{* ../../docs_src/settings/app01_py310/main.py hl[3,11:13] *}

/// tip | 提示

你还需要一个 `__init__.py` 文件，就像你在[更大的应用 - 多个文件](../tutorial/bigger-applications.md)中看到的那样。

///

## 在依赖项中提供设置 { #settings-in-a-dependency }

在某些情况下，从依赖项中提供设置可能更有用，而不是在所有地方都使用一个全局的 `settings` 对象。

这在测试期间尤其有用，因为可以很容易地用你自己的自定义设置覆盖依赖项。

### 配置文件 { #the-config-file }

延续上一个示例，你的 `config.py` 文件可能如下所示：

{* ../../docs_src/settings/app02_an_py310/config.py hl[10] *}

注意，现在我们不再创建默认实例 `settings = Settings()`。

### 主应用文件 { #the-main-app-file }

现在我们创建一个依赖项，返回一个新的 `config.Settings()`。

{* ../../docs_src/settings/app02_an_py310/main.py hl[6,12:13] *}

/// tip | 提示

我们稍后会讨论 `@lru_cache`。

目前你可以把 `get_settings()` 当作普通函数。

///

然后我们可以在路径操作函数中将其作为依赖项引入，并在需要的任何地方使用它。

{* ../../docs_src/settings/app02_an_py310/main.py hl[17,19:21] *}

### 设置与测试 { #settings-and-testing }

接着，在测试期间，通过为 `get_settings` 创建依赖项覆盖，就可以很容易地提供一个不同的设置对象：

{* ../../docs_src/settings/app02_an_py310/test_main.py hl[9:10,13,21] *}

在依赖项覆盖中，我们在创建新的 `Settings` 对象时为 `admin_email` 设置了一个新值，然后返回该新对象。

然后我们可以测试它是否被使用。

## 读取 `.env` 文件 { #reading-a-env-file }

如果你有许多设置可能经常变化，或在不同环境中不同，那么把它们放进一个文件中，然后像环境变量一样从中读取，可能非常有用。

这种做法非常常见：这些环境变量通常放在名为 `.env` 的文件中，该文件被称为 “dotenv”。

/// tip | 提示

以点（`.`）开头的文件在类 Unix 系统（如 Linux 和 macOS）中是隐藏文件。

但 dotenv 文件并不一定必须是这个确切的文件名。

///

Pydantic 支持使用一个外部库来从这类文件中读取。你可以在 [Pydantic Settings：Dotenv（.env）支持](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support) 中阅读更多信息。

/// tip | 提示

要使其工作，你需要执行 `pip install python-dotenv`。

///

### `.env` 文件 { #the-env-file }

你可以有一个 `.env` 文件，内容如下：

```bash
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
```

### 从 `.env` 中读取设置 { #read-settings-from-env }

然后更新 `config.py`：

{* ../../docs_src/settings/app03_an_py310/config.py hl[9] *}

/// tip | 提示

`model_config` 属性仅用于 Pydantic 配置。你可以在 [Pydantic：概念：配置](https://docs.pydantic.dev/latest/concepts/config/) 中阅读更多信息。

///

这里我们在你的 Pydantic `Settings` 类中定义配置项 `env_file`，并将其设置为我们想要使用的 dotenv 文件名。

### 使用 `lru_cache` 仅创建一次 `Settings` { #creating-the-settings-only-once-with-lru-cache }

从磁盘读取文件通常是一个代价较高（缓慢）的操作，所以你可能希望只在第一次读取，然后复用同一个设置对象，而不是为每个请求都重新读取。

但是，每次我们执行：

```Python
Settings()
```

都会创建一个新的 `Settings` 对象，并且在创建时会再次读取 `.env` 文件。

如果依赖项函数是这样的：

```Python
def get_settings():
    return Settings()
```

我们就会为每个请求创建该对象，并为每个请求读取 `.env` 文件。 ⚠️

但由于我们在顶部使用了 `@lru_cache` 装饰器，`Settings` 对象只会在第一次调用时创建一次。 ✔️

{* ../../docs_src/settings/app03_an_py310/main.py hl[1,11] *}

接着，对于后续请求中依赖项里对 `get_settings()` 的任何调用，它不会再次执行 `get_settings()` 的内部代码并创建新的 `Settings` 对象，而是会一遍又一遍地返回第一次调用时返回的那个相同对象。

#### `lru_cache` 技术细节 { #lru-cache-technical-details }

`@lru_cache` 会修改它所装饰的函数，使其返回第一次返回的相同值，而不是每次都重新计算并执行函数代码。

因此，下面的函数会针对每个参数组合执行一次。然后，当以完全相同的参数组合调用该函数时，将重复使用该参数组合先前返回的值。

例如，如果你有一个函数：

```Python
@lru_cache
def say_hi(name: str, salutation: str = "Ms."):
    return f"Hello {salutation} {name}"
```

你的程序可能会像这样执行：

```mermaid
sequenceDiagram

participant code as Code
participant function as say_hi()
participant execute as Execute function

    rect rgba(0, 255, 0, .1)
        code ->> function: say_hi(name="Camila")
        function ->> execute: 执行函数代码
        execute ->> code: 返回结果
    end

    rect rgba(0, 255, 255, .1)
        code ->> function: say_hi(name="Camila")
        function ->> code: 返回存储的结果
    end

    rect rgba(0, 255, 0, .1)
        code ->> function: say_hi(name="Rick")
        function ->> execute: 执行函数代码
        execute ->> code: 返回结果
    end

    rect rgba(0, 255, 0, .1)
        code ->> function: say_hi(name="Rick", salutation="Mr.")
        function ->> execute: 执行函数代码
        execute ->> code: 返回结果
    end

    rect rgba(0, 255, 255, .1)
        code ->> function: say_hi(name="Rick")
        function ->> code: 返回存储的结果
    end

    rect rgba(0, 255, 255, .1)
        code ->> function: say_hi(name="Camila")
        function ->> code: 返回存储的结果
    end
```

在我们的依赖项 `get_settings()` 的情况下，该函数甚至不接受任何参数，因此它始终返回相同的值。

这样，它的行为几乎就像是一个全局变量。但由于它使用了依赖项函数，我们可以在测试时很容易地覆盖它。

`@lru_cache` 是 `functools` 的一部分，它属于 Python 标准库。你可以在 [Python 文档中关于 `@lru_cache` 的章节](https://docs.python.org/3/library/functools.html#functools.lru_cache)阅读更多信息。

## 小结 { #recap }

你可以使用 Pydantic Settings 来处理应用的设置或配置，享受 Pydantic 模型的全部能力。

* 通过使用依赖项，你可以简化测试。
* 你可以与它一起使用 `.env` 文件。
* 使用 `@lru_cache` 可以避免为每个请求反复读取 dotenv 文件，同时允许你在测试时进行覆盖。



---

# Source: docs/advanced/stream-data.md


# 流式数据 { #stream-data }

如果你要流式传输可以结构化为 JSON 的数据，你应该[流式传输 JSON Lines](../tutorial/stream-json-lines.md)。

但如果你想**流式传输纯二进制数据**或字符串，可以按下面的方法操作。

/// note | 注意

自 FastAPI 0.134.0 起新增。

///

## 使用场景 { #use-cases }

如果你想流式传输纯字符串，例如直接来自某个 **AI LLM** 服务的输出，可以使用它。

你也可以用它来流式传输**大型二进制文件**，在读取的同时按块发送，无需一次性把所有内容读入内存。

你还可以用这种方式流式传输**视频**或**音频**，甚至可以在处理的同时生成并发送。

## 使用 `yield` 的 `StreamingResponse` { #a-streamingresponse-with-yield }

如果你在*路径操作函数*中声明 `response_class=StreamingResponse`，你就可以使用 `yield` 依次发送每个数据块。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI 会将每个数据块原样交给 `StreamingResponse`，不会尝试将其转换为 JSON 或做类似处理。

### 非 async 的*路径操作函数* { #non-async-path-operation-functions }

你也可以使用常规的 `def` 函数（不带 `async`），并以相同方式使用 `yield`。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### 无需注解 { #no-annotation }

你其实不需要为流式二进制数据声明返回类型注解。

由于 FastAPI 不会使用 Pydantic 将数据转换为 JSON，也不会以任何方式序列化，在这种情况下，类型注解只供你的编辑器和工具使用，FastAPI 不会使用它。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

这也意味着，使用 `StreamingResponse` 时，你拥有按需精确生成与编码字节数据的**自由**，同时也承担相应的**责任**，它与类型注解无关。🤓

### 流式传输字节 { #stream-bytes }

主要的用例之一是流式传输 `bytes` 而不是字符串，这当然可以做到。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## 自定义 `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

在上面的示例中，虽然按字节流式传输了数据，但响应没有 `Content-Type` 头，因此客户端不知道接收到的数据类型。

你可以创建 `StreamingResponse` 的自定义子类，将 `Content-Type` 头设置为你要流式传输的数据类型。

例如，你可以创建一个 `PNGStreamingResponse`，通过 `media_type` 属性把 `Content-Type` 头设置为 `image/png`：

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

然后你可以在*路径操作函数*中通过 `response_class=PNGStreamingResponse` 使用这个新类：

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### 模拟文件 { #simulate-a-file }

在这个示例中，我们用 `io.BytesIO` 模拟了一个文件，它是只驻留在内存中的类文件对象，但提供相同的接口。

例如，我们可以像对文件那样迭代它来消费其内容。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | 技术细节

另外两个变量 `image_base64` 和 `binary_image` 表示一张图像，先用 Base64 编码，再转换为 bytes，最后传给 `io.BytesIO`。

只是为了让它们能和示例放在同一个文件里，便于你直接复制运行。🥚

///

通过使用 `with` 代码块，我们确保在生成器函数（带有 `yield` 的函数）完成后关闭这个类文件对象。也就是在发送完响应之后。

在这个特定示例中这并不那么重要，因为它是一个内存中的假文件（使用 `io.BytesIO`），但对于真实文件，确保在完成相关工作后关闭文件是很重要的。

### 文件与异步 { #files-and-async }

大多数情况下，类文件对象默认与 async 和 await 不兼容。

例如，它们没有 `await file.read()`，也不支持 `async for chunk in file`。

而且很多情况下，读取它们是一个阻塞操作（可能会阻塞事件循环），因为数据来自磁盘或网络。

/// note | 注意

上面的示例其实是个例外，因为 `io.BytesIO` 对象已经在内存中，所以读取它不会阻塞。

但在许多情况下，读取文件或类文件对象会发生阻塞。

///

为避免阻塞事件循环，你可以简单地把*路径操作函数*声明为常规的 `def`（而不是 `async def`），这样 FastAPI 会在一个线程池工作线程上运行它，从而避免阻塞主事件循环。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | 提示

如果你需要在异步函数里调用阻塞代码，或在阻塞函数里调用异步函数，可以使用 [Asyncer](https://asyncer.tiangolo.com)，它是 FastAPI 的姐妹库。

///

### `yield from` { #yield-from }

当你在迭代某个对象（例如类文件对象），并为每个条目执行 `yield` 时，你也可以使用 `yield from` 直接产出每个条目，从而省去 `for` 循环。

这并不是 FastAPI 特有的功能，只是 Python 的语法，但这是一个值得知道的小技巧。😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}



---

# Source: docs/advanced/strict-content-type.md


# 严格的 Content-Type 检查 { #strict-content-type-checking }

默认情况下，FastAPI 对 JSON 请求体使用严格的 `Content-Type` 头检查。这意味着，JSON 请求必须包含有效的 `Content-Type` 头（例如 `application/json`），其请求体才会被按 JSON 解析。

## CSRF 风险 { #csrf-risk }

此默认行为在一个非常特定的场景下，可防御一类跨站请求伪造（CSRF）攻击。

这类攻击利用了浏览器的一个事实：当请求满足以下条件时，浏览器允许脚本在不进行任何 CORS 预检的情况下直接发送请求：

- 没有 `Content-Type` 头（例如使用 `fetch()` 携带 `Blob` 作为 body）
- 且不发送任何认证凭据。

这种攻击主要在以下情况下相关：

- 应用在本地（如 `localhost`）或内网中运行
- 且应用没有任何认证，假定来自同一网络的请求都可信。

## 攻击示例 { #example-attack }

假设你构建了一个本地运行的 AI 代理。

它提供了一个 API，地址为

```
http://localhost:8000/v1/agents/multivac
```

另有一个前端，地址为

```
http://localhost:8000
```

/// tip | 提示

注意它们的主机相同。

///

之后，你可以通过前端让该 AI 代理替你执行操作。

由于它在本地运行、而非暴露在开放的互联网，你决定不配置任何认证，只信任对本地网络的访问。

于是，你的某位用户安装并在本地运行了它。

然后他（她）可能会打开一个恶意网站，例如

```
https://evilhackers.example.com
```

该恶意网站使用 `fetch()` 携带 `Blob` 作为 body，向本地 API 发送请求，地址为

```
http://localhost:8000/v1/agents/multivac
```

尽管恶意网站与本地应用的主机不同，浏览器仍不会触发 CORS 预检请求，原因是：

- 请求不涉及任何认证，无需发送凭据。
- 浏览器认为它并未发送 JSON（因为缺少 `Content-Type` 头）。

于是，该恶意网站就可能让本地 AI 代理替用户向前老板发送愤怒消息……甚至更糟。😅

## 开放的互联网 { #open-internet }

如果你的应用部署在开放的互联网，你不会“信任网络”，也不会允许任何人不经认证就发送特权请求。

攻击者完全可以直接运行脚本向你的 API 发送请求，无需借助浏览器交互，因此你很可能已经对任何特权端点做好了安全防护。

在这种情况下，以上攻击/风险不适用于你。

该风险/攻击主要发生在应用运行于本地网络、且“仅依赖网络隔离作为保护”的场景。

## 允许无 Content-Type 的请求 { #allowing-requests-without-content-type }

如果你需要兼容不发送 `Content-Type` 头的客户端，可以通过设置 `strict_content_type=False` 来关闭严格检查：

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

启用该设置后，缺少 `Content-Type` 头的请求其请求体也会按 JSON 解析，这与旧版本 FastAPI 的行为一致。

/// note | 注意

此行为和配置在 FastAPI 0.132.0 中新增。

///



---

# Source: docs/advanced/sub-applications.md


# 子应用 - 挂载 { #sub-applications-mounts }

如果需要两个独立的 FastAPI 应用，拥有各自独立的 OpenAPI 与文档，则需设置一个主应用，并**挂载**一个（或多个）子应用。

## 挂载 **FastAPI** 应用 { #mounting-a-fastapi-application }

**挂载**是指在特定路径中添加完全**独立**的应用，然后在该路径下使用*路径操作*声明的子应用处理所有事务。

### 顶层应用 { #top-level-application }

首先，创建主（顶层）**FastAPI** 应用及其*路径操作*：

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### 子应用 { #sub-application }

接下来，创建子应用及其*路径操作*。

子应用只是另一个标准 FastAPI 应用，但这个应用是被**挂载**的应用：

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### 挂载子应用 { #mount-the-sub-application }

在顶层应用 `app` 中，挂载子应用 `subapi`。

本例的子应用挂载在 `/subapi` 路径下：

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### 查看自动 API 文档 { #check-the-automatic-api-docs }

现在，运行 `fastapi` 命令：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后在 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 打开文档。

下图显示的是主应用 API 文档，只包括其自有的*路径操作*。

<img src="/img/tutorial/sub-applications/image01.png">

然后查看子应用文档 [http://127.0.0.1:8000/subapi/docs](http://127.0.0.1:8000/subapi/docs)。

下图显示的是子应用的 API 文档，也是只包括其自有的*路径操作*，所有这些路径操作都在 `/subapi` 子路径前缀下。

<img src="/img/tutorial/sub-applications/image02.png">

两个用户界面都可以正常运行，因为浏览器能够与每个指定的应用或子应用会话。

### 技术细节：`root_path` { #technical-details-root-path }

以上述方式挂载子应用时，FastAPI 使用 ASGI 规范中的 `root_path` 机制处理挂载子应用路径之间的通信。

这样，子应用就可以为自动文档使用路径前缀。

并且子应用还可以再挂载子应用，一切都会正常运行，FastAPI 可以自动处理所有 `root_path`。

关于 `root_path` 及如何显式使用 `root_path` 的内容，详见[使用代理](behind-a-proxy.md)一章。



---

# Source: docs/advanced/templates.md


# 模板 { #templates }

**FastAPI** 支持多种模板引擎。

Flask 等工具使用的 Jinja2 是最用的模板引擎。

在 Starlette 的支持下，**FastAPI** 应用可以直接使用工具轻易地配置 Jinja2。

## 安装依赖项 { #install-dependencies }

确保你创建一个[虚拟环境](../virtual-environments.md)，激活它，并安装 `jinja2`：

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates` { #using-jinja2templates }

* 导入 `Jinja2Templates`
* 创建可复用的 `templates` 对象
* 在返回模板的*路径操作*中声明 `Request` 参数
* 使用 `templates` 渲染并返回 `TemplateResponse`，传递模板的名称、request 对象以及一个包含多个键值对（用于 Jinja2 模板）的 "context" 字典。

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | 注意

在 FastAPI 0.108.0，Starlette 0.29.0 之前，`name` 是第一个参数。
并且，在此之前，`request` 对象是作为 context 的一部分以键值对的形式传递的。

///

/// tip | 提示

通过声明 `response_class=HTMLResponse`，API 文档就能识别响应的对象是 HTML。

///

/// note | 技术细节

您还可以使用 `from starlette.templating import Jinja2Templates`。

**FastAPI** 的 `fastapi.templating` 只是为开发者提供的快捷方式。实际上，绝大多数可用响应都直接继承自 Starlette。`Request` 与 `StaticFiles` 也一样。

///

## 编写模板 { #writing-templates }

编写模板 `templates/item.html`，代码如下：

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### 模板上下文值 { #template-context-values }

在包含如下语句的html中:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...这将显示你从 "context" 字典传递的 `id`:

```Python
{"id": id}
```

例如。当 ID 为 `42` 时, 会渲染成:

```html
Item ID: 42
```

### 模板 `url_for` 参数 { #template-url-for-arguments }

你还可以在模板内使用 `url_for()`，其参数与*路径操作函数*的参数相同。

所以，该部分:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...将生成一个与处理*路径操作函数* `read_item(id=id)`的 URL 相同的链接

例如。当 ID 为 `42` 时, 会渲染成:

```html
<a href="/items/42">
```

## 模板与静态文件 { #templates-and-static-files }

你还可以在模板内部将 `url_for()` 用于静态文件，例如你挂载的 `name="static"` 的 `StaticFiles`。

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

本例中，它将链接到 `static/styles.css` 中的 CSS 文件：

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

因为使用了 `StaticFiles`，**FastAPI** 应用会自动提供位于 URL `/static/styles.css` 的 CSS 文件。

## 更多说明 { #more-details }

包括如何测试模板在内的更多详情，请查看 [Starlette 的模板文档](https://www.starlette.dev/templates/)。



---

# Source: docs/advanced/testing-dependencies.md


# 使用覆盖测试依赖项 { #testing-dependencies-with-overrides }

## 测试时覆盖依赖项 { #overriding-dependencies-during-testing }

有些场景下，您可能需要在测试时覆盖依赖项。

即不希望运行原有依赖项（及其子依赖项）。

反之，要在测试期间（或只是为某些特定测试）提供只用于测试的依赖项，并使用此依赖项的值替换原有依赖项的值。

### 用例：外部服务 { #use-cases-external-service }

常见实例是调用外部第三方身份验证应用。

向第三方应用发送令牌，然后返回经验证的用户。

但第三方服务商处理每次请求都可能会收费，并且耗时通常也比调用写死的模拟测试用户更长。

一般只要测试一次外部验证应用就够了，不必每次测试都去调用。

此时，最好覆盖调用外部验证应用的依赖项，使用返回模拟测试用户的自定义依赖项就可以了。

### 使用 `app.dependency_overrides` 属性 { #use-the-app-dependency-overrides-attribute }

对于这些用例，**FastAPI** 应用支持 `app.dependency_overrides` 属性，该属性就是**字典**。

要在测试时覆盖原有依赖项，这个字典的键应当是原依赖项（函数），值是覆盖依赖项（另一个函数）。

这样一来，**FastAPI** 就会调用覆盖依赖项，不再调用原依赖项。

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | 提示

**FastAPI** 应用中的任何位置都可以实现覆盖依赖项。

原依赖项可用于*路径操作函数*、*路径操作装饰器*（不需要返回值时）、`.include_router()` 调用等。

FastAPI 可以覆盖这些位置的依赖项。

///

然后，使用 `app.dependency_overrides` 把覆盖依赖项重置为空**字典**：

```Python
app.dependency_overrides = {}
```

/// tip | 提示

如果只在某些测试时覆盖依赖项，您可以在测试开始时（在测试函数内）设置覆盖依赖项，并在结束时（在测试函数结尾）重置覆盖依赖项。

///



---

# Source: docs/advanced/testing-events.md


# 测试事件：lifespan 和 startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

当你需要在测试中运行 `lifespan` 时，可以将 `TestClient` 与 `with` 语句一起使用：

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}

你可以在[官方 Starlette 文档站点的“在测试中运行 lifespan”](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)阅读更多细节。

对于已弃用的 `startup` 和 `shutdown` 事件，可以按如下方式使用 `TestClient`：

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}



---

# Source: docs/advanced/testing-websockets.md


# 测试 WebSockets { #testing-websockets }

你可以使用同一个 `TestClient` 来测试 WebSockets。

为此，在 `with` 语句中使用 `TestClient` 连接到 WebSocket：

{* ../../docs_src/app_testing/tutorial002_py310.py hl[27:31] *}

/// note | 注意

更多细节请查看 Starlette 的文档：[测试 WebSockets](https://www.starlette.dev/testclient/#testing-websocket-sessions)。

///



---

# Source: docs/advanced/using-request-directly.md


# 直接使用 Request { #using-the-request-directly }

至此，我们已经使用多种类型声明了请求的各种组件。

并从以下对象中提取数据：

* 路径参数
* 请求头
* Cookies
* 等

**FastAPI** 使用这种方式验证数据、转换数据，并自动生成 API 文档。

但有时，我们也需要直接访问 `Request` 对象。

## `Request` 对象的细节 { #details-about-the-request-object }

实际上，**FastAPI** 的底层是 **Starlette**，**FastAPI** 只不过是在 **Starlette** 顶层提供了一些工具，所以能直接使用 Starlette 的 [`Request`](https://www.starlette.dev/requests/) 对象。

但直接从 `Request` 对象提取数据时（例如，读取请求体），这些数据不会被 **FastAPI** 验证、转换或文档化（使用 OpenAPI，为自动的 API 用户界面）。

不过，仍可以验证、转换与注释（使用 Pydantic 模型的请求体等）其它正常声明的参数。

但在某些特定情况下，还是需要提取 `Request` 对象。

## 直接使用 `Request` 对象 { #use-the-request-object-directly }

假设要在*路径操作函数*中获取客户端 IP 地址和主机。

此时，需要直接访问请求。

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

把*路径操作函数*的参数类型声明为 `Request`，**FastAPI** 就能把 `Request` 传递到参数里。

/// tip | 提示

注意，本例除了声明请求参数之外，还声明了路径参数。

因此，能够提取、验证路径参数、并转换为指定类型，还可以用 OpenAPI 注释。

同样，您也可以正常声明其它参数，而且还可以提取 `Request`。

///

## `Request` 文档 { #request-documentation }

你可以在[Starlette 官方文档站点的 `Request` 对象](https://www.starlette.dev/requests/)中阅读更多细节。

/// note | 技术细节

您也可以使用 `from starlette.requests import Request`。

**FastAPI** 直接提供它只是为了方便开发者，但它直接来自 Starlette。

///



---

# Source: docs/advanced/websockets.md


# WebSockets { #websockets }

您可以在 **FastAPI** 中使用 [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)。

## 安装 `websockets` { #install-websockets }

请确保您创建一个[虚拟环境](../virtual-environments.md)、激活它，并安装 `websockets`（一个让使用“WebSocket”协议更容易的 Python 库）：

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets 客户端 { #websockets-client }

### 在生产环境中 { #in-production }

在您的生产系统中，您可能使用现代框架（如 React、Vue.js 或 Angular）创建了一个前端。

要使用 WebSockets 与后端进行通信，您可能会使用前端的工具。

或者，您可能有一个原生移动应用程序，直接使用原生代码与 WebSocket 后端通信。

或者，您可能有其他与 WebSocket 终端通信的方式。

---

但是，在本示例中，我们将使用一个非常简单的 HTML 文档，其中包含一些 JavaScript，全部放在一个长字符串中。

当然，这并不是最优的做法，您不应该在生产环境中使用它。

在生产环境中，您应该选择上述任一选项。

但这是一种专注于 WebSockets 的服务器端并提供一个工作示例的最简单方式：

{* ../../docs_src/websockets_/tutorial001_py310.py hl[2,6:38,41:43] *}

## 创建 `websocket` { #create-a-websocket }

在您的 **FastAPI** 应用程序中，创建一个 `websocket`：

{* ../../docs_src/websockets_/tutorial001_py310.py hl[1,46:47] *}

/// note | 技术细节

您也可以使用 `from starlette.websockets import WebSocket`。

**FastAPI** 直接提供了相同的 `WebSocket`，只是为了方便开发人员。但它直接来自 Starlette。

///

## 等待消息并发送消息 { #await-for-messages-and-send-messages }

在您的 WebSocket 路由中，您可以使用 `await` 等待消息并发送消息。

{* ../../docs_src/websockets_/tutorial001_py310.py hl[48:52] *}

您可以接收和发送二进制、文本和 JSON 数据。

## 尝试一下 { #try-it }

将代码放在 `main.py`，然后运行你的应用程序：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

在浏览器中打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)。

您将看到一个简单的页面，如下所示：

<img src="/img/tutorial/websockets/image01.png">

您可以在输入框中输入消息并发送：

<img src="/img/tutorial/websockets/image02.png">

您的 **FastAPI** 应用程序将通过 WebSockets 回复：

<img src="/img/tutorial/websockets/image03.png">

您可以发送（和接收）多条消息：

<img src="/img/tutorial/websockets/image04.png">

所有这些消息都将使用同一个 WebSocket 连接。

## 使用 `Depends` 和其他依赖项 { #using-depends-and-others }

在 WebSocket 端点中，您可以从 `fastapi` 导入并使用以下内容：

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

它们的工作方式与其他 FastAPI 端点/*路径操作* 相同：

{* ../../docs_src/websockets_/tutorial002_an_py310.py hl[68:69,82] *}

/// note | 注意

由于这是一个 WebSocket，抛出 `HTTPException` 并不是很合理，而是抛出 `WebSocketException`。

您可以使用[规范中定义的有效关闭代码](https://tools.ietf.org/html/rfc6455#section-7.4.1)。

///

### 尝试带有依赖项的 WebSockets { #try-the-websockets-with-dependencies }

运行你的应用程序：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

在浏览器中打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)。

在页面中，您可以设置：

* "Item ID"，用于路径。
* "Token"，作为查询参数。

/// tip | 提示

注意，查询参数 `token` 将由依赖项处理。

///

通过这样，您可以连接 WebSocket，然后发送和接收消息：

<img src="/img/tutorial/websockets/image05.png">

## 处理断开连接和多个客户端 { #handling-disconnections-and-multiple-clients }

当 WebSocket 连接关闭时，`await websocket.receive_text()` 将引发 `WebSocketDisconnect` 异常，您可以捕获并处理该异常，就像本示例中的示例一样。

{* ../../docs_src/websockets_/tutorial003_py310.py hl[79:81] *}

尝试以下操作：

* 使用多个浏览器选项卡打开应用程序。
* 从这些选项卡中发送消息。
* 然后关闭其中一个选项卡。

这将引发 `WebSocketDisconnect` 异常，并且所有其他客户端都会收到类似以下的消息：

```
Client #1596980209979 left the chat
```

/// tip | 提示

上面的应用程序是一个最小和简单的示例，用于演示如何处理和向多个 WebSocket 连接广播消息。

但请记住，由于所有内容都在内存中以单个列表的形式处理，因此它只能在进程运行时工作，并且只能使用单个进程。

如果您需要与 FastAPI 集成更简单但更健壮的方案，支持 Redis、PostgreSQL 或其他，请查看 [encode/broadcaster](https://github.com/encode/broadcaster)。

///

## 更多信息 { #more-info }

要了解更多选项，请查看 Starlette 的文档：

* [`WebSocket` 类](https://www.starlette.dev/websockets/)。
* [基于类的 WebSocket 处理](https://www.starlette.dev/endpoints/#websocketendpoint)。



---

# Source: docs/advanced/wsgi.md


# 包含 WSGI - Flask，Django，其它 { #including-wsgi-flask-django-others }


您可以挂载 WSGI 应用，正如您在 [子应用 - 挂载](sub-applications.md)、[在代理之后](behind-a-proxy.md) 中所看到的那样。

为此, 您可以使用 `WSGIMiddleware` 来包装你的 WSGI 应用，如：Flask，Django，等等。

## 使用 `WSGIMiddleware` { #using-wsgimiddleware }

/// note | 注意

需要安装 `a2wsgi`，例如使用 `pip install a2wsgi`。

///

您需要从 `a2wsgi` 导入 `WSGIMiddleware`。

然后使用该中间件包装 WSGI 应用（例如 Flask）。

之后将其挂载到某一个路径下。

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | 注意

之前推荐使用 `fastapi.middleware.wsgi` 中的 `WSGIMiddleware`，但它现在已被弃用。

建议改用 `a2wsgi` 包，使用方式保持不变。

只要确保已安装 `a2wsgi` 包，并且从 `a2wsgi` 正确导入 `WSGIMiddleware` 即可。

///

## 检查 { #check-it }

现在，所有定义在 `/v1/` 路径下的请求将会被 Flask 应用处理。

其余的请求则会被 **FastAPI** 处理。

如果你运行它并访问 [http://localhost:8000/v1/](http://localhost:8000/v1/)，你将会看到由 Flask 返回的响应：

```txt
Hello, World from Flask!
```

如果你访问 [http://localhost:8000/v2](http://localhost:8000/v2)，你将会看到由 FastAPI 返回的响应：

```JSON
{
    "message": "Hello World"
}
```



---

# Source: docs/alternatives.md


# 替代方案、灵感与对比 { #alternatives-inspiration-and-comparisons }

是什么启发了 **FastAPI**，它与替代方案的比较，以及它从中学到的东西。

## 介绍 { #intro }

没有前人的工作，就不会有 **FastAPI**。

在它诞生之前，已经有许多工具为其提供了灵感。

我曾经多年避免创建一个新框架。起初，我尝试用许多不同的框架、插件和工具来解决 **FastAPI** 所覆盖的全部功能。

但在某个时刻，除了创造一个能提供所有这些功能的东西之外，别无选择；它要吸收以往工具的最佳理念，并以尽可能好的方式组合起来，利用之前都不存在的语言特性（Python 3.6+ 类型提示）。

## 先前的工具 { #previous-tools }

### [Django](https://www.djangoproject.com/) { #django }

它是最流行且被广泛信任的 Python 框架。被用于构建 Instagram 等系统。

它与关系型数据库（如 MySQL、PostgreSQL）耦合相对紧密，因此若要以 NoSQL 数据库（如 Couchbase、MongoDB、Cassandra 等）作为主要存储引擎并不容易。

它最初用于在后端生成 HTML，而不是创建由现代前端（如 React、Vue.js、Angular）或与之通信的其他系统（如 <abbr title="Internet of Things - 物联网">IoT</abbr> 设备）使用的 API。

### [Django REST Framework](https://www.django-rest-framework.org/) { #django-rest-framework }

Django REST framework 作为一个灵活工具箱而创建，用于在底层使用 Django 构建 Web API，从而增强其 API 能力。

它被包括 Mozilla、Red Hat、Eventbrite 在内的许多公司使用。

它是最早的**自动 API 文档**的范例之一，这正是启发“寻找” **FastAPI** 的最初想法之一。

/// note | 注意

Django REST Framework 由 Tom Christie 创建。他也是 Starlette 和 Uvicorn 的作者，**FastAPI** 就是基于它们构建的。

///

/// tip | 启发 **FastAPI**：

提供自动化的 API 文档 Web 界面。

///

### [Flask](https://flask.palletsprojects.com) { #flask }

Flask 是一个“微框架”，它不包含数据库集成，也没有像 Django 那样的许多默认内建功能。

这种简单与灵活使得可以将 NoSQL 数据库作为主要的数据存储系统。

由于非常简单，它相对直观易学，尽管文档在某些部分略显偏技术。

它也常用于不一定需要数据库、用户管理，或任何 Django 预构建功能的应用；当然，许多这类功能可以通过插件添加。

这种组件解耦、可按需扩展的“微框架”特性，是我想保留的关键点。

鉴于 Flask 的简洁，它似乎非常适合构建 API。接下来要找的，就是 Flask 版的 “Django REST Framework”。

/// tip | 启发 **FastAPI**：

成为微框架。让按需组合所需的工具与组件变得容易。

提供简单易用的路由系统。

///

### [Requests](https://requests.readthedocs.io) { #requests }

**FastAPI** 实际上不是 **Requests** 的替代品。它们的作用范围完全不同。

在 FastAPI 应用程序内部使用 Requests 其实非常常见。

尽管如此，FastAPI 依然从 Requests 中获得了不少灵感。

**Requests** 是一个用于与 API 交互（作为客户端）的库，而 **FastAPI** 是一个用于构建 API（作为服务端）的库。

它们处在某种意义上的“对立端”，彼此互补。

Requests 设计非常简单直观，易于使用，且有合理的默认值。同时它也非常强大、可定制。

这就是为什么，正如其官网所说：

> Requests 是有史以来下载量最高的 Python 包之一

它的用法非常简单。例如，进行一次 `GET` 请求，你会这样写：

```Python
response = requests.get("http://example.com/some/url")
```

对应地，FastAPI 的 API *路径操作*可能看起来是这样的：

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

可以看到 `requests.get(...)` 与 `@app.get(...)` 的相似之处。

/// tip | 启发 **FastAPI**：

* 提供简单直观的 API。
* 直接、自然地使用 HTTP 方法名（操作）。
* 具备合理默认值，同时支持强大定制能力。

///

### [Swagger](https://swagger.io/) / [OpenAPI](https://github.com/OAI/OpenAPI-Specification/) { #swagger-openapi }

我想从 Django REST Framework 得到的主要特性之一是自动 API 文档。

随后我发现有一个用于用 JSON（或 YAML，JSON 的扩展）来描述 API 的标准，称为 Swagger。

并且已经有了用于 Swagger API 的 Web 用户界面。因此，只要能为 API 生成 Swagger 文档，就能自动使用这个 Web 界面。

后来，Swagger 交由 Linux 基金会管理，并更名为 OpenAPI。

因此，在谈到 2.0 版本时人们常说 “Swagger”，而 3+ 版本则称为 “OpenAPI”。

/// tip | 启发 **FastAPI**：

采用并使用开放的 API 规范标准，而非自定义模式。

并集成基于标准的用户界面工具：

* [Swagger UI](https://github.com/swagger-api/swagger-ui)
* [ReDoc](https://github.com/Rebilly/ReDoc)

选择这两者是因为它们相当流行且稳定；但稍作搜索，你就能找到数十种 OpenAPI 的替代用户界面（都可以与 **FastAPI** 搭配使用）。

///

### Flask REST 框架 { #flask-rest-frameworks }

有若干基于 Flask 的 REST 框架，但在投入时间精力深入调研后，我发现许多已停止维护或被弃用，并存在多处未解决问题，不太适合采用。

### [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) { #marshmallow }

API 系统所需的主要特性之一是数据“<dfn title="也称为：编组、转换">序列化</dfn>”，即将代码（Python）中的数据转换为可通过网络发送的形式。例如，将包含数据库数据的对象转换为 JSON 对象、将 `datetime` 对象转换为字符串等。

API 的另一个重要特性是数据校验，确保数据在给定约束下是有效的。例如，某个字段必须是 `int` 而不是任意字符串。这对传入数据尤其有用。

没有数据校验系统的话，你就得在代码里手写所有检查。

这些正是 Marshmallow 要提供的功能。它是个很棒的库，我之前大量使用过。

但它诞生于 Python 类型提示出现之前。因此，定义每个<dfn title="数据应如何构造的定义">模式</dfn>都需要使用 Marshmallow 提供的特定工具和类。

/// tip | 启发 **FastAPI**：

使用代码定义“模式”，自动提供数据类型与校验。

///

### [Webargs](https://webargs.readthedocs.io/en/latest/) { #webargs }

API 的另一个重要需求是从传入请求中<dfn title="读取并转换为 Python 数据">解析</dfn>数据。

Webargs 是一个在多个框架（包括 Flask）之上提供该功能的工具。

它在底层使用 Marshmallow 进行数据校验，并且由相同的开发者创建。

在拥有 **FastAPI** 之前，我也大量使用过它，这是个很棒的工具。

/// note | 注意

Webargs 由与 Marshmallow 相同的开发者创建。

///

/// tip | 启发 **FastAPI**：

对传入请求数据进行自动校验。

///

### [APISpec](https://apispec.readthedocs.io/en/stable/) { #apispec }

Marshmallow 与 Webargs 通过插件提供了校验、解析与序列化。

但文档仍然缺失，于是出现了 APISpec。

它为许多框架提供插件（Starlette 也有插件）。

它的工作方式是：你在处理路由的每个函数的文档字符串里，用 YAML 格式编写模式定义。

然后它会生成 OpenAPI 模式。

这正是它在 Flask、Starlette、Responder 等框架里的工作方式。

但这样我们又回到了在 Python 字符串中维护一套“微语法”（一大段 YAML）的问题上。

编辑器很难为此提供帮助；而且如果我们修改了参数或 Marshmallow 模式，却忘了同步更新那个 YAML 文档字符串，生成的模式就会过时。

/// note | 注意

APISpec 由与 Marshmallow 相同的开发者创建。

///

/// tip | 启发 **FastAPI**：

支持开放的 API 标准 OpenAPI。

///

### [Flask-apispec](https://flask-apispec.readthedocs.io/en/latest/) { #flask-apispec }

这是一个 Flask 插件，将 Webargs、Marshmallow 与 APISpec 结合在一起。

它利用 Webargs 与 Marshmallow 的信息，通过 APISpec 自动生成 OpenAPI 模式。

这是个很棒却被低估的工具；它理应比许多 Flask 插件更流行。或许是因为它的文档过于简洁与抽象。

这解决了在 Python 文档字符串里书写 YAML（另一套语法）的问题。

在构建 **FastAPI** 之前，Flask + Flask-apispec + Marshmallow + Webargs 的组合是我最喜欢的后端技术栈。

使用它促成了若干 Flask 全栈脚手架的诞生。以下是我（以及若干外部团队）至今使用的主要技术栈：

* [https://github.com/tiangolo/full-stack](https://github.com/tiangolo/full-stack)
* [https://github.com/tiangolo/full-stack-flask-couchbase](https://github.com/tiangolo/full-stack-flask-couchbase)
* [https://github.com/tiangolo/full-stack-flask-couchdb](https://github.com/tiangolo/full-stack-flask-couchdb)

这些全栈脚手架也成为了[**FastAPI** 项目脚手架](project-generation.md)的基础。

/// note | 注意

Flask-apispec 由与 Marshmallow 相同的开发者创建。

///

/// tip | 启发 **FastAPI**：

从定义序列化与校验的同一份代码自动生成 OpenAPI 模式。

///

### [NestJS](https://nestjs.com/)（以及 [Angular](https://angular.io/)） { #nestjs-and-angular }

这甚至不是 Python。NestJS 是一个 JavaScript（TypeScript）的 NodeJS 框架，受 Angular 启发。

它实现了与 Flask-apispec 有些类似的效果。

它集成了受 Angular 2 启发的依赖注入系统。与我所知的其他依赖注入系统一样，需要预先注册“可注入项”，因此会增加冗长与重复。

由于参数用 TypeScript 类型描述（类似 Python 类型提示），编辑器支持相当好。

但由于 TypeScript 的类型在编译为 JavaScript 后不会保留，无法只依赖这些类型同时定义校验、序列化与文档。受此以及一些设计决策影响，为了获得校验、序列化与自动 schema 生成，需要在许多位置添加装饰器，因此代码会相当冗长。

它对嵌套模型的支持并不好。如果请求的 JSON 体是包含嵌套 JSON 对象的 JSON 对象，则无法被正确文档化和校验。

/// tip | 启发 **FastAPI**：

使用 Python 类型以获得出色的编辑器支持。

拥有强大的依赖注入系统，并设法尽量减少代码重复。

///

### [Sanic](https://sanic.readthedocs.io/en/latest/) { #sanic }

它是最早的一批基于 `asyncio` 的极速 Python 框架之一，且做得与 Flask 很相似。

/// note | 技术细节

它使用了 [`uvloop`](https://github.com/MagicStack/uvloop) 来替代 Python 默认的 `asyncio` 循环。这正是它如此之快的原因。

它显然启发了 Uvicorn 和 Starlette；在公开的基准测试中，它们目前比 Sanic 更快。

///

/// tip | 启发 **FastAPI**：

找到实现疯狂性能的路径。

这就是 **FastAPI** 基于 Starlette 的原因，因为它是目前可用的最快框架（由第三方基准测试验证）。

///

### [Falcon](https://falconframework.org/) { #falcon }

Falcon 是另一个高性能 Python 框架，它被设计为精简且可作为 Hug 等其他框架的基础。

它设计为接收两个参数的函数：一个“请求”和一个“响应”。然后从请求中“读取”，向响应中“写入”。由于这种设计，无法用标准的 Python 类型提示将请求参数和请求体声明为函数形参。

因此，数据校验、序列化与文档要么需要手写完成，无法自动化；要么需要在 Falcon 之上实现一个框架，例如 Hug。其他受 Falcon 设计启发、采用“一个 request 对象 + 一个 response 对象作为参数”的框架也有同样的区别。

/// tip | 启发 **FastAPI**：

寻找获得卓越性能的方法。

与 Hug（Hug 基于 Falcon）一起，启发 **FastAPI** 在函数中声明一个 `response` 参数。尽管在 FastAPI 中它是可选的，主要用于设置 headers、cookies 和可选的状态码。

///

### [Molten](https://moltenframework.com/) { #molten }

我在构建 **FastAPI** 的早期阶段发现了 Molten。它有不少相似的想法：

* 基于 Python 类型提示。
* 从这些类型获得校验与文档。
* 依赖注入系统。

它没有使用像 Pydantic 这样的第三方数据校验、序列化与文档库，而是有自己的实现。因此这些数据类型定义不太容易在其他地方复用。

它需要稍微冗长一些的配置。并且由于基于 WSGI（而非 ASGI），它并未设计为充分利用 Uvicorn、Starlette、Sanic 等工具所提供的高性能。

其依赖注入系统需要预先注册依赖，且依赖根据声明的类型来解析。因此无法为同一类型声明多于一个“组件”。

路由在一个地方集中声明，使用在其他地方声明的函数（而不是使用可以直接放在处理端点函数之上的装饰器）。这更接近 Django 的做法，而不是 Flask（和 Starlette）。它在代码中割裂了相对紧耦合的内容。

/// tip | 启发 **FastAPI**：

通过模型属性的“默认值”为数据类型定义额外校验。这提升了编辑器支持，而这在当时的 Pydantic 中尚不可用。

这实际上促成了对 Pydantic 的部分更新，以支持这种校验声明风格（这些功能现已在 Pydantic 中可用）。

///

### [Hug](https://github.com/hugapi/hug) { #hug }

Hug 是最早使用 Python 类型提示来声明 API 参数类型的框架之一。这一绝妙想法也启发了其他工具。

它在声明中使用自定义类型而不是标准的 Python 类型，但这依然是巨大的进步。

它也是最早生成一个自定义 JSON 模式来声明整个 API 的框架之一。

它并不基于 OpenAPI 与 JSON Schema 这类标准。因此与其他工具（如 Swagger UI）的集成并非一帆风顺。但它仍是非常有创新性的想法。

它有一个有趣且少见的特性：使用同一框架，可以同时创建 API 与 CLI。

由于基于同步 Python Web 框架的上一代标准（WSGI），它无法处理 WebSocket 等，尽管它的性能仍然很高。

/// note | 注意

Hug 由 Timothy Crosley 创建，他也是 [`isort`](https://github.com/timothycrosley/isort) 的作者，这是一个能自动排序 Python 文件中导入的优秀工具。

///

/// tip | 启发 **FastAPI** 的想法：

Hug 启发了 APIStar 的部分设计，也是我当时最看好的工具之一，与 APIStar 并列。

Hug 促使 **FastAPI** 使用 Python 类型提示来声明参数，并自动生成定义整个 API 的模式。

Hug 启发 **FastAPI** 在函数中声明 `response` 参数，用于设置 headers 与 cookies。

///

### [APIStar](https://github.com/encode/apistar) (<= 0.5) { #apistar-0-5 }

就在决定动手构建 **FastAPI** 之前，我找到了 **APIStar** 服务器。它几乎具备我想要的一切，设计也很出色。

在我见过的框架中，它是最早使用 Python 类型提示来声明参数和请求的实现之一（早于 NestJS 与 Molten）。我与 Hug 几乎同时发现了它。但 APIStar 使用了 OpenAPI 标准。

它基于相同的类型提示，在多处自动进行数据校验、序列化并生成 OpenAPI 模式。

请求体模式定义并未使用与 Pydantic 相同的 Python 类型提示，它更接近 Marshmallow，因此编辑器支持不如 Pydantic 好，但即便如此，APIStar 仍是当时可用的最佳选择。

它在当时拥有最好的性能基准（仅被 Starlette 超越）。

起初它没有自动 API 文档 Web 界面，但我知道我可以把 Swagger UI 加进去。

它有一个依赖注入系统。与上文提到的其他工具一样，需要预先注册组件。但这依然是很棒的特性。

我从未在完整项目中使用过它，因为它没有安全集成，因此我无法用它替代基于 Flask-apispec 的全栈脚手架所具备的全部功能。我曾把“提交一个增加该功能的 PR”放在了待办里。

但随后，项目的重心发生了变化。

它不再是一个 API Web 框架，因为作者需要专注于 Starlette。

现在 APIStar 是一组用于校验 OpenAPI 规范的工具，而不是 Web 框架。

/// note | 注意

APIStar 由 Tom Christie 创建。他还创建了：

* Django REST Framework
* Starlette（**FastAPI** 基于其之上）
* Uvicorn（被 Starlette 与 **FastAPI** 使用）

///

/// tip | 启发 **FastAPI**：

诞生。

用同一套 Python 类型同时声明多件事（数据校验、序列化与文档），并且还能提供出色的编辑器支持——我认为这是个极其巧妙的想法。

在长时间寻找与测试多种替代之后，APIStar 是当时最好的选择。

随后 APIStar 不再作为服务器存在，而 Starlette 出现，成为实现该体系的更佳基础。这成为构建 **FastAPI** 的最终灵感来源。

我把 **FastAPI** 视为 APIStar 的“精神续作”，并在此基础上，结合前述工具的经验，改进并增强了功能、类型系统及其他各方面。

///

## **FastAPI** 所使用的组件 { #used-by-fastapi }

### [Pydantic](https://docs.pydantic.dev/) { #pydantic }

Pydantic 是一个基于 Python 类型提示来定义数据校验、序列化与文档（使用 JSON Schema）的库。

这使得它极其直观。

它可与 Marshmallow 类比。尽管在基准测试中它比 Marshmallow 更快。并且由于同样基于 Python 类型提示，编辑器支持优秀。

/// tip | **FastAPI** 用它来：

处理所有数据校验、数据序列化与自动模型文档（基于 JSON Schema）。

随后 **FastAPI** 会把这些 JSON Schema 数据纳入 OpenAPI（以及完成其他所有工作）。

///

### [Starlette](https://www.starlette.dev/) { #starlette }

Starlette 是一个轻量级的 <dfn title="构建异步 Python Web 应用的新标准">ASGI</dfn> 框架/工具集，非常适合构建高性能的 asyncio 服务。

它非常简单直观。被设计为易于扩展，且具有模块化组件。

它具备：

* 性能极其出色。
* 支持 WebSocket。
* 进程内后台任务。
* 启动与停止事件。
* 基于 HTTPX 的测试客户端。
* CORS、GZip、静态文件、流式响应。
* 会话与 Cookie 支持。
* 100% 测试覆盖率。
* 100% 类型注解的代码库。
* 极少的强依赖。

Starlette 目前是测试中最快的 Python 框架。仅次于 Uvicorn，它不是框架，而是服务器。

Starlette 提供了 Web 微框架的全部基础能力。

但它不提供自动的数据校验、序列化或文档。

这正是 **FastAPI** 在其之上增加的主要内容之一，全部基于 Python 类型提示（通过 Pydantic）。此外还有依赖注入系统、安全工具、OpenAPI 模式生成等。

/// note | 技术细节

ASGI 是由 Django 核心团队成员推动的新“标准”。它尚不是正式的“Python 标准”（PEP），尽管正朝此方向推进。

尽管如此，已有多种工具将其作为“标准”使用。这极大提升了互操作性：你可以把 Uvicorn 换成其他 ASGI 服务器（如 Daphne 或 Hypercorn），或添加 ASGI 兼容的工具，如 `python-socketio`。

///

/// tip | **FastAPI** 用它来：

处理所有核心 Web 部分，并在其之上扩展功能。

`FastAPI` 类本身直接继承自 `Starlette`。

因此，凡是你能用 Starlette 完成的事，也能直接用 **FastAPI** 完成；可以把它看作“加速版”的 Starlette。

///

### [Uvicorn](https://www.uvicorn.dev/) { #uvicorn }

Uvicorn 是一个基于 uvloop 与 httptools 构建的极速 ASGI 服务器。

它不是 Web 框架，而是服务器。例如它不提供按路径路由的工具——这是 Starlette（或 **FastAPI**）这类框架在其之上提供的功能。

它是 Starlette 与 **FastAPI** 推荐的服务器。

/// tip | **FastAPI** 推荐将其作为：

运行 **FastAPI** 应用的主要 Web 服务器。

你也可以使用 `--workers` 命令行选项以获得异步的多进程服务器。

更多细节见[部署](deployment/index.md)一节。

///

## 基准与速度 { #benchmarks-and-speed }

要理解、比较并查看 Uvicorn、Starlette 与 FastAPI 之间的差异，请查看[基准](benchmarks.md)一节。



---

# Source: docs/async.md


# 并发 async / await { #concurrency-and-async-await }

有关路径操作函数的 `async def` 语法以及异步代码、并发和并行的一些背景知识。

## 赶时间吗？ { #in-a-hurry }

<abbr title="too long; didn't read - 太长；没看"><strong>TL;DR:</strong></abbr>

如果你正在使用第三方库，它们会告诉你使用 `await` 关键字来调用它们，就像这样：

```Python
results = await some_library()
```

然后，通过 `async def` 声明你的 *路径操作函数*：

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | 注意

你只能在被 `async def` 创建的函数内使用 `await`。

///

---

如果你正在使用一个第三方库和某些组件（比如：数据库、API、文件系统等）进行通信，而该第三方库不支持使用 `await`（目前大多数数据库库都是这样），这种情况你可以像平常那样使用 `def` 声明一个路径操作函数，就像这样：

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

如果你的应用程序（以某种方式）不需要与其他任何东西通信而等待其响应，请使用 `async def`，即使函数内部不需要使用 `await`。

---

如果你不清楚，使用 `def` 就好。

---

**注意**：你可以根据需要在路径操作函数中混合使用 `def` 和 `async def`，并使用最适合你的方式去定义每个函数。FastAPI 将为它们做正确的事情。

无论如何，在上述任何情况下，FastAPI 仍将异步工作，速度也非常快。

但是，通过遵循上述步骤，它将能够进行一些性能优化。

## 技术细节 { #technical-details }

Python 的现代版本支持通过一种叫**“协程”**——使用 `async` 和 `await` 语法的东西来写**“异步代码”**。

让我们在下面的部分中逐一介绍：

* **异步代码**
* **`async` 和 `await`**
* **协程**

## 异步代码 { #asynchronous-code }

异步代码仅仅意味着编程语言 💬 有办法告诉计算机/程序 🤖 在代码中的某个点，它 🤖 将不得不等待在某些地方完成一些事情。让我们假设一些事情被称为 "慢文件"📝。

所以，在等待"慢文件"📝完成的这段时间，计算机可以做一些其他工作。

然后计算机/程序 🤖 每次有机会都会回来，因为它又在等待，或者它 🤖 完成了当前所有的工作。而且它 🤖 将查看它等待的所有任务中是否有已经完成的，做它必须做的任何事情。

接下来，它 🤖 取第一个完成的任务（比如是我们的"慢文件"📝）并继续与之相关的一切。

这个"等待其他事情"通常指的是一些相对较慢（与处理器和 RAM 存储器的速度相比）的 <abbr title="Input and Output - 输入和输出">I/O</abbr> 操作，比如说等待：

* 通过网络发送来自客户端的数据
* 客户端通过网络接收由你的程序发送的数据
* 磁盘中文件的内容被系统读取并提供给你的程序
* 你的程序提供给系统的内容被写入磁盘
* 一个 API 的远程调用
* 一个数据库操作，直到完成
* 一个数据库查询，直到返回结果
* 等等。

这个执行的时间大多是在等待 <abbr title="Input and Output - 输入和输出">I/O</abbr> 操作，因此它们被叫做 "I/O 密集型" 操作。

它被称为"异步"的原因是因为计算机/程序不必与慢任务"同步"，去等待任务完成的确切时刻，而在此期间不做任何事情直到能够获取任务结果才继续工作。

相反，作为一个"异步"系统，一旦完成，任务就可以排队等待一段时间（几微秒），等待计算机程序完成它要做的任何事情，然后回来获取结果并继续处理它们。

对于"同步"（与"异步"相反），他们通常也使用"顺序"一词，因为计算机程序在切换到另一个任务之前是按顺序执行所有步骤，即使这些步骤涉及到等待。

### 并发与汉堡 { #concurrency-and-burgers }

上述**异步**代码的思想有时也被称为**“并发”**，它不同于**“并行”**。

**并发**和**并行**都与“不同的事情或多或少同时发生”有关。

但是*并发*和*并行*之间的细节是完全不同的。

要了解差异，请想象以下关于汉堡的故事：

### 并发汉堡 { #concurrent-burgers }

你和你的恋人一起去快餐店，你排队在后面，收银员从你前面的人接单。😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

然后轮到你了，你为你的恋人和你选了两个非常豪华的汉堡。🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

收银员对厨房里的厨师说了一些话，让他们知道他们必须为你准备汉堡（尽管他们目前正在为之前的顾客准备汉堡）。

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

你付钱了。 💸

收银员给你轮到的号码。

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

当你在等待的时候，你和你的恋人一起去挑选一张桌子，然后你们坐下来聊了很长时间（因为汉堡很豪华，需要一些时间来准备）。

当你和你的恋人坐在桌子旁，等待汉堡的时候，你可以用这段时间来欣赏你的恋人是多么的棒、可爱和聪明✨😍✨。

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

在等待中和你的恋人交谈时，你会不时地查看柜台上显示的号码，看看是否已经轮到你了。

然后在某个时刻，终于轮到你了。你去柜台拿汉堡然后回到桌子上。

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

你们享用了汉堡，整个过程都很开心。✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// note | 注意

漂亮的插画来自 [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot)。🎨

///

---

在那个故事里，假设你是计算机程序 🤖。

当你在排队时，你只是闲着😴，等待轮到你，不做任何非常“有成效”的事情。但排队很快，因为收银员只接订单（不准备订单），所以这一切都还好。

然后，当轮到你时，需要你做一些实际性的“有成效”的工作，比如查看菜单，决定你想要什么，让你的恋人选择，支付，检查你是否提供了正确的账单或卡，检查你的收费是否正确，检查订单是否有正确的项目，等等。

此时，即使你仍然没有汉堡，你和收银员的工作也“暂停”了⏸，因为你必须等待一段时间 🕙 让你的汉堡做好。

但是，当你离开柜台并坐在桌子旁，手里拿着你的号码时，你可以将焦点切换到 🔀 你的恋人上，并在这上面“工作”⏯ 🤓。你可以做一些非常“有成效”的事情，比如和你的恋人调情😍。

之后，收银员 💁 把号码显示在显示屏上，并说到“汉堡做好了”，而当显示的号码变成你的号码时，你不会立刻疯狂地跳起来。因为你知道没有人会偷你的汉堡，因为你有你的号码，而其他人又有他们自己的号码。

所以你要等待你的恋人完成故事（完成当前的工作 ⏯ / 正在处理的任务 🤓)，轻轻微笑，说你要去拿汉堡 ⏸。

然后你去柜台 🔀，回到现在已经完成 ⏯ 的初始任务，拿起汉堡，说声谢谢，然后把它们送到桌上。这就完成了与柜台交互的那个步骤/任务 ⏹。这反过来又产生了一项新任务，即“吃汉堡”🔀 ⏯，而上一个“拿汉堡”的任务已经结束了 ⏹。

### 并行汉堡 { #parallel-burgers }

现在让我们假设不是“并发汉堡”，而是“并行汉堡”。

你和你的恋人一起去吃并行快餐。

你站在队伍中，同时是厨师的几个收银员（比方说 8 个）从前面的人那里接单。

你之前的每个人都在等待他们的汉堡准备好后才离开柜台，因为 8 名收银员都会在下一份订单前马上准备好汉堡。

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

然后，终于轮到你了，你为你的恋人和你订购了两个非常精美的汉堡。

你付钱了 💸。

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

收银员去厨房。

你站在柜台前 🕙 等待着，这样就不会有人在你之前抢走你的汉堡，因为没有轮流的号码。

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

当你和你的恋人忙于不让任何人出现在你面前，并且在它们到来的时候拿走你的汉堡时，你无法关注到你的恋人。😞

这是“同步”的工作，你被迫与收银员/厨师 👨‍🍳“同步”。你必须 🕙 等待，并在收银员/厨师 👨‍🍳 完成汉堡并将它们交给你的确切时刻出现在那儿，否则其他人可能会拿走它们。

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

你经过长时间的等待 🕙，收银员/厨师 👨‍🍳 终于带着汉堡回到了柜台。

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

你拿着汉堡，和你的恋人一起上桌。

你们仅仅是吃了它们，就结束了。⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

没有太多的交谈或调情，因为大部分时间 🕙 都在柜台前等待。😞

/// note | 注意

漂亮的插画来自 [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot)。🎨

///

---

在这个并行汉堡的场景中，你是一个计算机程序 🤖 且有两个处理器（你和你的恋人），都在等待 🕙，并将他们的注意力 ⏯ 投入到长时间“在柜台前等待”🕙 上。

这家快餐店有 8 个处理器（收银员/厨师）。而并发汉堡店可能只有 2 个（一个收银员和一个厨师）。

但最终的体验仍然不是最好的。😞

---

这将是与汉堡的类似故事。🍔

一种更“贴近生活”的例子，想象一家银行。

直到最近，大多数银行都有多个出纳员 👨‍💼👨‍💼👨‍💼👨‍💼 还有一条长长排队队伍 🕙🕙🕙🕙🕙🕙🕙🕙。

所有收银员都是一个接一个地在客户面前做完所有的工作 👨‍💼⏯。

你必须在队伍里 🕙 排很久，否则就会错过你的顺序。

你可不会想带你的恋人 😍 和你一起去银行办事 🏦。

### 汉堡结论 { #burger-conclusion }

在“你与恋人一起吃汉堡”的这个场景中，因为有很多人在等待 🕙，使用并发系统更有意义 ⏸🔀⏯。

大多数 Web 应用都是这样的。

你的服务器正在等待 🕙 很多很多用户通过他们不太好的网络发送来的请求。

然后再次等待 🕙 响应回来。

这个“等待”🕙 是以微秒为单位测量的，但总的来说，最后还是等待很久。

这就是为什么为 Web API 使用异步 ⏸🔀⏯ 很有意义。

这种异步机制正是 NodeJS 受到欢迎的原因（尽管 NodeJS 不是并行的），也是 Go 作为编程语言的优势所在。

这与 **FastAPI** 的性能水平相同。

你可以同时拥有并行性和异步性，你可以获得比大多数经过测试的 NodeJS 框架更高的性能，并且与 Go 不相上下，Go 是一种更接近于 C 的编译语言（[全部归功于 Starlette](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1)）。

### 并发比并行好吗？ { #is-concurrency-better-than-parallelism }

不！这不是故事的本意。

并发不同于并行。而是在需要大量等待的特定场景下效果更好。因此，在 Web 应用程序开发中，它通常比并行要好得多，但这并不意味着全部。

因此，为了平衡这一点，想象一下下面的短篇故事：

> 你必须打扫一个又大又脏的房子。

*是的，这就是完整的故事。*

---

在任何地方，都不需要等待 🕙，只需要在房子的多个地方做着很多工作。

你可以像汉堡的例子那样轮流执行，先是客厅，然后是厨房，但因为你不需要等待 🕙，对于任何事情都是清洁，清洁，还是清洁，轮流不会影响任何事情。

无论是否轮流执行（并发），都需要相同的时间来完成，而你也会完成相同的工作量。

但在这种情况下，如果你能带上 8 名前收银员/厨师，现在是清洁工一起清扫，他们中的每一个人（加上你）都能占据房子的一个区域来清扫，你就可以在额外的帮助下并行地更快地完成所有工作。

在这个场景中，每个清洁工（包括你）都将是一个处理器，完成这个工作的一部分。

由于大多数执行时间是由实际工作（而不是等待）占用的，并且计算机中的工作是由 <abbr title="Central Processing Unit - 中央处理器">CPU</abbr> 完成的，所以他们称这些问题为“CPU 密集型”。

---

CPU 密集型操作的常见示例是需要复杂的数学处理。

例如：

* **音频**或**图像**处理；
* **计算机视觉**：一幅图像由数百万像素组成，每个像素有 3 种颜色值，处理通常需要同时对这些像素进行计算；
* **机器学习**：它通常需要大量的“矩阵”和“向量”乘法。想象一个包含数字的巨大电子表格，并同时将所有数字相乘；
* **深度学习**：这是机器学习的一个子领域，同样适用。只是没有一个数字的电子表格可以相乘，而是一个庞大的数字集合，在很多情况下，你需要使用一个特殊的处理器来构建和/或使用这些模型。

### 并发 + 并行: Web + 机器学习 { #concurrency-parallelism-web-machine-learning }

使用 **FastAPI**，你可以利用 Web 开发中常见的并发机制的优势（NodeJS 的主要吸引力）。

并且，你也可以利用并行和多进程（让多个进程并行运行）的优点来处理与机器学习系统中类似的 **CPU 密集型** 工作。

这一点，再加上 Python 是**数据科学**、机器学习（尤其是深度学习）的主要语言这一简单事实，使得 **FastAPI** 与数据科学/机器学习 Web API 和应用程序（以及其他许多应用程序）非常匹配。

了解如何在生产环境中实现这种并行性，可查看此文 [部署](deployment/index.md)。

## `async` 和 `await` { #async-and-await }

现代版本的 Python 有一种非常直观的方式来定义异步代码。这使它看起来就像正常的“顺序”代码，并在适当的时候为你“等待”。

当有一个操作需要等待才能给出结果，且支持这个新的 Python 特性时，你可以编写如下代码：

```Python
burgers = await get_burgers(2)
```

这里的关键是 `await`。它告诉 Python 它必须等待 ⏸ `get_burgers(2)` 完成它的工作 🕙，然后将结果存储在 `burgers` 中。这样，Python 就会知道此时它可以去做其他事情 🔀 ⏯（比如接收另一个请求）。

要使 `await` 工作，它必须位于支持这种异步机制的函数内。因此，只需使用 `async def` 声明它：

```Python hl_lines="1"
async def get_burgers(number: int):
    # 执行一些异步操作来制作汉堡
    return burgers
```

...而不是 `def`:

```Python hl_lines="2"
# 这不是异步的
def get_sequential_burgers(number: int):
    # 执行一些顺序操作来制作汉堡
    return burgers
```

使用 `async def`，Python 就知道在该函数中，它将遇上 `await`，并且它可以“暂停”⏸ 执行该函数，直至执行其他操作 🔀 后回来。

当你想调用一个 `async def` 函数时，你必须“等待”它。因此，这不会起作用：

```Python
# 这样不行，因为 get_burgers 是用 async def 定义的
burgers = get_burgers(2)
```

---

因此，如果你使用的库告诉你可以使用 `await` 调用它，则需要使用 `async def` 创建路径操作函数，如：

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### 更多技术细节 { #more-technical-details }

你可能已经注意到，`await` 只能在 `async def` 定义的函数内部使用。

但与此同时，必须“等待”通过 `async def` 定义的函数。因此，带 `async def` 的函数也只能在 `async def` 定义的函数内部调用。

那么，这关于先有鸡还是先有蛋的问题，如何调用第一个 `async` 函数？

如果你使用 **FastAPI**，你不必担心这一点，因为“第一个”函数将是你的路径操作函数，FastAPI 将知道如何做正确的事情。

但如果你想在没有 FastAPI 的情况下使用 `async` / `await`，则可以这样做。

### 编写自己的异步代码 { #write-your-own-async-code }

Starlette（和 **FastAPI**）是基于 [AnyIO](https://anyio.readthedocs.io/en/stable/) 实现的，这使得它们可以兼容 Python 的标准库 [asyncio](https://docs.python.org/3/library/asyncio-task.html) 和 [Trio](https://trio.readthedocs.io/en/stable/)。

特别是，你可以直接使用 [AnyIO](https://anyio.readthedocs.io/en/stable/) 来处理高级的并发用例，这些用例需要在自己的代码中使用更高级的模式。

即使你没有使用 FastAPI，你也可以使用 [AnyIO](https://anyio.readthedocs.io/en/stable/) 编写自己的异步程序，使其拥有较高的兼容性并获得一些好处（例如，结构化并发）。

我基于 AnyIO 新建了一个库，作为一个轻量级的封装层，用来优化类型注解，同时提供了更好的**自动补全**、**内联错误提示**等功能。这个库还附带了一个友好的入门指南和教程，能帮助你**理解**并编写**自己的异步代码**：[Asyncer](https://asyncer.tiangolo.com/)。如果你有**结合使用异步代码和常规**（阻塞/同步）代码的需求，这个库会特别有用。

### 其他形式的异步代码 { #other-forms-of-asynchronous-code }

这种使用 `async` 和 `await` 的风格在语言中相对较新。

但它使处理异步代码变得容易很多。

这种相同的语法（或几乎相同）最近也包含在现代版本的 JavaScript 中（在浏览器和 NodeJS 中）。

但在此之前，处理异步代码非常复杂和困难。

在以前版本的 Python，你可以使用多线程或者 [Gevent](https://www.gevent.org/)。但代码的理解、调试和思考都要复杂许多。

在以前版本的 NodeJS / 浏览器 JavaScript 中，你会使用“回调”，因此也可能导致“回调地狱”。

## 协程 { #coroutines }

**协程**只是 `async def` 函数返回的一个非常奇特的东西的称呼。Python 知道它有点像一个函数，它可以启动，也会在某个时刻结束，而且它可能会在内部暂停 ⏸，只要内部有一个 `await`。

通过使用 `async` 和 `await` 的异步代码的所有功能大多数被概括为“协程”。它可以与 Go 的主要关键特性 “Goroutines” 相媲美。

## 结论 { #conclusion }

让我们再来回顾下上文所说的：

> Python 的现代版本可以通过使用 `async` 和 `await` 语法创建**协程**，并用于支持**异步代码**。

现在应该能明白其含义了。✨

所有这些使得 FastAPI（通过 Starlette）如此强大，也是它拥有如此令人印象深刻的性能的原因。

## 非常技术性的细节 { #very-technical-details }

/// warning | 警告

你可以跳过这里。

这些都是 FastAPI 如何在内部工作的技术细节。

如果你有相当多的技术知识（协程、线程、阻塞等），并且对 FastAPI 如何处理 `async def` 与常规 `def` 感到好奇，请继续。

///

### 路径操作函数 { #path-operation-functions }

当你使用 `def` 而不是 `async def` 来声明一个*路径操作函数*时，它运行在外部的线程池中并等待其结果，而不是直接调用（因为它会阻塞服务器）。

如果你使用过另一个不以上述方式工作的异步框架，并且你习惯于用普通的 `def` 定义普通的仅计算路径操作函数，以获得微小的性能增益（大约 100 纳秒），请注意，在 FastAPI 中，效果将完全相反。在这些情况下，最好使用 `async def`，除非路径操作函数内使用执行阻塞 <abbr title="Input/Output - 输入/输出：磁盘读写，网络通信。">I/O</abbr> 的代码。

在这两种情况下，**FastAPI** [仍然会更快](index.md#performance)（或至少与之前的框架相当）。

### 依赖 { #dependencies }

这同样适用于[依赖](tutorial/dependencies/index.md)。如果一个依赖是标准的 `def` 函数而不是 `async def`，它将被运行在外部线程池中。

### 子依赖 { #sub-dependencies }

你可以拥有多个相互依赖的依赖以及[子依赖](tutorial/dependencies/sub-dependencies.md)（作为函数的参数），它们中的一些可能是通过 `async def` 声明，也可能是通过 `def` 声明。它们仍然可以正常工作，这些通过 `def` 声明的函数将会在外部线程中调用（来自线程池），而不是“被等待”。

### 其他工具函数 { #other-utility-functions }

你可直接调用通过 `def` 或 `async def` 创建的任何其他工具函数，FastAPI 不会影响你调用它们的方式。

这与 FastAPI 为你调用*路径操作函数*和依赖项的逻辑相反。

如果你的工具函数是通过 `def` 声明的，它将被直接调用（在代码中编写的地方），而不会在线程池中；如果这个函数通过 `async def` 声明，当在代码中调用时，你就应该使用 `await` 等待函数的结果。

---

再次提醒，这些是非常技术性的细节，如果你来搜索它可能对你有用。

否则，你最好应该遵守的指导原则<a href="#in-a-hurry">赶时间吗？</a>。



---

# Source: docs/benchmarks.md


# 基准测试 { #benchmarks }

第三方机构 TechEmpower 的基准测试表明在 Uvicorn 下运行的 **FastAPI** 应用程序是 [可用的最快的 Python 框架之一](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)，仅次于 Starlette 和 Uvicorn 本身（由 FastAPI 内部使用）。

但是在查看基准得分和对比时，请注意以下几点。

## 基准测试和速度 { #benchmarks-and-speed }

当你查看基准测试时，几个不同类型的工具被等效地做比较是很常见的情况。

具体来说，是将 Uvicorn，Starlette 和 FastAPI 一起比较（在许多其它工具中）。

该工具解决的问题最简单，它将获得更好的性能。而且大多数基准测试并未测试该工具提供的其他功能。

层次结构如下：

* **Uvicorn**：ASGI服务器
    * **Starlette**：（使用 Uvicorn）网络微框架
        * **FastAPI**：（使用 Starlette） 具有多个附加功能的API微框架，用于构建API，进行数据验证等。

* **Uvicorn**:
    * 具有最佳性能，因为除了服务器本身外，它没有太多额外的代码。
    * 你不会直接在 Uvicorn 中编写应用程序。这意味着你的代码至少必须包含 Starlette（或 **FastAPI**）提供的代码。如果你这样做了（即直接在 Uvicorn 中编写应用程序），最终的应用程序会和使用了框架并且最小化了应用代码和 bug 的情况具有相同的性能损耗。
    * 如果你要对比 Uvicorn，请将其与 Daphne，Hypercorn，uWSGI 等应用服务器进行比较。
* **Starlette**:
    * 性能仅次于 Uvicorn。实际上，Starlette 使用 Uvicorn 运行。因此，由于必须执行更多的代码，它只会比 Uvicorn 更慢。
    * 但它为你提供了构建简单的网络程序的工具，并具有基于路径的路由等功能。
    * 如果想对比与 Starlette 对标的开发框架，请将其与 Sanic，Flask，Django 等网络框架（或微框架）进行比较。
* **FastAPI**:
    * 与 Starlette 使用 Uvicorn 一样，由于 **FastAPI** 使用 Starlette，因此 FastAPI 不能比 Starlette 更快。
    * FastAPI 在 Starlette 基础上提供了更多功能。例如在开发 API 时，所需的数据验证和序列化功能。FastAPI 可以帮助你自动生成 API文档，（文档在应用程序启动时自动生成，所以不会增加应用程序运行时的开销）。
    * 如果你不使用 FastAPI 而直接使用 Starlette（或诸如 Sanic，Flask，Responder 等其它工具），你则要自己实现所有的数据验证和序列化。那么最终你的应用程序会和使用 FastAPI 构建的程序有相同的开销。一般这种数据验证和序列化的操作在你应用程序的代码中会占很大比重。
    * 因此，通过使用 FastAPI 意味着你可以节省开发时间，减少编码错误，用更少的编码实现其功能，并且相比不使用 FastAPI 你很大可能会获得相同或更好的性能（因为那样你必须在代码中实现所有相同的功能）。
    * 如果你想对比 FastAPI，请与能够提供数据验证、序列化和文档的网络应用程序框架（或工具集）进行对比，例如具有集成自动数据验证、序列化和自动化文档的 Flask-apispec，NestJS，Molten 等。



---

# Source: docs/deployment/cloud.md


# 在云服务商上部署 FastAPI { #deploy-fastapi-on-cloud-providers }

你几乎可以使用**任何云服务商**来部署你的 FastAPI 应用。

在大多数情况下，主流云服务商都有部署 FastAPI 的指南。

## FastAPI Cloud { #fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 由 **FastAPI** 背后的同一作者与团队打造。

它简化了**构建**、**部署**和**访问** API 的流程，几乎不费力。

它把使用 FastAPI 构建应用时相同的**开发者体验**带到了将应用**部署**到云上的过程。🎉

FastAPI Cloud 是 *FastAPI and friends* 开源项目的主要赞助方和资金提供者。✨

## 云服务商 - 赞助商 { #cloud-providers-sponsors }

还有一些云服务商也会 ✨ [**赞助 FastAPI**](https://github.com/sponsors/tiangolo) ✨。🙇

你也可以考虑按照他们的指南尝试他们的服务：

* [Render](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi)
* [Railway](https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi)



---

# Source: docs/deployment/concepts.md


# 部署概念 { #deployments-concepts }

在部署 **FastAPI** 应用程序，或者实际上，任何类型的 Web API 时，有几个你可能会关心的概念，通过掌握这些概念你可以找到**最合适的**方法来**部署你的应用程序**。

一些重要的概念是：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 启动前的先前步骤

我们接下来了解它们将如何影响**部署**。

最终目标是能够以**安全**的方式**为你的 API 客户端**提供服务，同时**避免中断**，并且尽可能高效地利用**计算资源**（例如远程服务器/虚拟机）。 🚀

我将在这里告诉你更多关于这些**概念**的信息，希望能给你提供**直觉**来决定如何在非常不同的环境中部署你的 API，甚至是在尚不存在的**未来**环境里。

通过考虑这些概念，你将能够**评估和设计**部署**你自己的 API** 的最佳方式。

在接下来的章节中，我将为你提供更多部署 FastAPI 应用程序的**具体方案**。

但现在，让我们仔细看一下这些重要的**概念性想法**。这些概念也适用于任何其他类型的 Web API。 💡

## 安全性 - HTTPS { #security-https }

在[上一章有关 HTTPS](https.md) 中，我们了解了 HTTPS 如何为你的 API 提供加密。

我们还看到，HTTPS 通常由应用程序服务器的**外部**组件（**TLS 终止代理**）提供。

并且必须有某个东西负责**更新 HTTPS 证书**，它可以是相同的组件，也可以是不同的组件。

### HTTPS 示例工具 { #example-tools-for-https }

你可以用作 TLS 终止代理的一些工具包括：

* Traefik
    * 自动处理证书更新 ✨
* Caddy
    * 自动处理证书更新 ✨
* Nginx
    * 使用 Certbot 等外部组件进行证书更新
* HAProxy
    * 使用 Certbot 等外部组件进行证书更新
* 带有 Ingress Controller（如 Nginx）的 Kubernetes
    * 使用诸如 cert-manager 之类的外部组件来进行证书更新
* 由云服务商内部处理，作为其服务的一部分（请阅读下文👇）

另一种选择是你可以使用**云服务**来完成更多工作，包括设置 HTTPS。它可能有一些限制或向你收取更多费用等。但在这种情况下，你不必自己设置 TLS 终止代理。

我将在接下来的章节中向你展示一些具体示例。

---

接下来要考虑的概念都是关于运行实际 API 的程序（例如 Uvicorn）。

## 程序和进程 { #program-and-process }

我们将讨论很多关于正在运行的“**进程**”的内容，因此弄清楚它的含义以及与“**程序**”这个词有什么区别是很有用的。

### 什么是程序 { #what-is-a-program }

**程序**这个词通常用来描述很多东西：

* 你编写的 **代码**，**Python 文件**。
* 操作系统可以**执行**的**文件**，例如：`python`、`python.exe` 或 `uvicorn`。
* 在操作系统上**运行**、使用 CPU 并将内容存储在内存上的特定程序。这也被称为**进程**。

### 什么是进程 { #what-is-a-process }

**进程**这个词通常以更具体的方式使用，仅指在操作系统中运行的东西（如上面的最后一点）：

* 在操作系统上**运行**的特定程序。
    * 这不是指文件，也不是指代码，它**具体**指的是操作系统正在**执行**和管理的东西。
* 任何程序，任何代码，**只有在执行时才能做事**。因此，是当有**进程正在运行**时。
* 该进程可以由你或操作系统**终止**（或“杀死”）。那时，它停止运行/被执行，并且它**不再能做事情**。
* 你计算机上运行的每个应用程序背后都有一些进程，每个正在运行的程序，每个窗口等。并且通常在计算机打开时**同时**运行许多进程。
* **同一程序**可以有**多个进程**同时运行。

如果你检查操作系统中的“任务管理器”或“系统监视器”（或类似工具），你将能够看到许多正在运行的进程。

例如，你可能会看到有多个进程运行同一个浏览器程序（Firefox、Chrome、Edge 等）。它们通常每个 tab 运行一个进程，再加上一些其他额外的进程。

<img class="shadow" src="/img/deployment/concepts/image01.png">

---

现在我们知道了术语 **进程** 和 **程序** 之间的区别，让我们继续讨论部署。

## 启动时运行 { #running-on-startup }

在大多数情况下，当你创建 Web API 时，你希望它**始终运行**、不间断，以便你的客户端始终可以访问它。当然，除非你有特定原因希望它仅在某些情况下运行，但大多数时候你希望它不断运行并且**可用**。

### 在远程服务器中 { #in-a-remote-server }

当你设置远程服务器（云服务器、虚拟机等）时，你可以做的最简单的事情就是使用 `fastapi run`（它使用 Uvicorn）或类似方式，手动运行，就像本地开发时一样。

它将会**在开发过程中**发挥作用并且很有用。

但是，如果你与服务器的连接丢失，**正在运行的进程**可能会终止。

如果服务器重新启动（例如更新后或从云提供商迁移后），你可能**不会注意到它**。因此，你甚至不知道必须手动重新启动该进程。所以，你的 API 将一直处于挂掉的状态。 😱

### 启动时自动运行 { #run-automatically-on-startup }

一般来说，你可能希望服务器程序（例如 Uvicorn）在服务器启动时自动启动，并且不需要任何**人为干预**，让进程始终与你的 API 一起运行（例如 Uvicorn 运行你的 FastAPI 应用程序）。

### 单独的程序 { #separate-program }

为了实现这一点，你通常会有一个**单独的程序**来确保你的应用程序在启动时运行。在许多情况下，它还可以确保其他组件或应用程序也运行，例如数据库。

### 启动时运行的示例工具 { #example-tools-to-run-at-startup }

可以完成这项工作的工具的一些示例是：

* Docker
* Kubernetes
* Docker Compose
* Docker in Swarm Mode
* Systemd
* Supervisor
* 作为其服务的一部分由云提供商内部处理
* 其他的...

我将在接下来的章节中为你提供更具体的示例。

## 重新启动 { #restarts }

与确保应用程序在启动时运行类似，你可能还想确保它在失败后**重新启动**。

### 我们会犯错误 { #we-make-mistakes }

作为人类，我们总是会犯**错误**。软件几乎*总是*在不同的地方隐藏着 **bug**。 🐛

作为开发人员，当我们发现这些 bug 并实现新功能（也可能添加新 bug 😅）时，我们会不断改进代码。

### 自动处理小错误 { #small-errors-automatically-handled }

使用 FastAPI 构建 Web API 时，如果我们的代码中存在错误，FastAPI 通常会将其限制在触发错误的单个请求中。 🛡

对于该请求，客户端将收到 **500 内部服务器错误**，但应用程序将继续处理下一个请求，而不是完全崩溃。

### 更大的错误 - 崩溃 { #bigger-errors-crashes }

尽管如此，在某些情况下，我们编写的一些代码可能会**导致整个应用程序崩溃**，从而导致 Uvicorn 和 Python 崩溃。 💥

尽管如此，你可能不希望应用程序因为某个地方出现错误而保持死机状态，你可能希望它**继续运行**，至少对于未损坏的*路径操作*。

### 崩溃后重新启动 { #restart-after-crash }

但在那些严重错误导致正在运行的**进程**崩溃的情况下，你需要一个外部组件来负责**重新启动**进程，至少尝试几次...

/// tip | 提示

...尽管如果整个应用程序只是**立即崩溃**，那么永远重新启动它可能没有意义。但在这些情况下，你可能会在开发过程中注意到它，或者至少在部署后立即注意到它。

因此，让我们关注主要情况，在**未来**的某些特定情况下，它可能会完全崩溃，但重新启动它仍然有意义。

///

你可能希望让这个负责重新启动你的应用程序的东西作为一个**外部组件**，因为到那时，使用 Uvicorn 和 Python 的同一应用程序已经崩溃了，因此同一应用程序的相同代码中没有任何东西可以对此做什么。

### 自动重新启动的示例工具 { #example-tools-to-restart-automatically }

在大多数情况下，用于**启动时运行程序**的同一工具也用于处理自动**重新启动**。

例如，可以通过以下方式处理：

* Docker
* Kubernetes
* Docker Compose
* Docker in Swarm Mode
* Systemd
* Supervisor
* 作为其服务的一部分由云提供商内部处理
* 其他的...

## 复制 - 进程和内存 { #replication-processes-and-memory }

对于 FastAPI 应用程序，使用像运行 Uvicorn 的 `fastapi` 命令这样的服务器程序，在**一个进程**中运行一次就可以同时为多个客户端提供服务。

但在许多情况下，你会希望同时运行多个工作进程。

### 多进程 - Workers { #multiple-processes-workers }

如果你的客户端数量多于单个进程可以处理的数量（例如，如果虚拟机不是太大），并且服务器的 CPU 中有**多个核心**，那么你可以让**多个进程**同时运行同一个应用程序，并在它们之间分发所有请求。

当你运行同一 API 程序的**多个进程**时，它们通常称为 **workers**。

### 工作进程和端口 { #worker-processes-and-ports }

还记得文档[关于 HTTPS](https.md) 中说的，在服务器中只有一个进程可以侦听端口和 IP 地址的一种组合吗？

现在仍然是对的。

因此，为了能够同时拥有**多个进程**，必须有一个**单个进程侦听端口**，然后以某种方式将通信传输到每个工作进程。

### 每个进程的内存 { #memory-per-process }

现在，当程序将内容加载到内存中时，例如，将机器学习模型加载到变量中，或者将大文件的内容加载到变量中，所有这些都会**消耗服务器的一些内存 (RAM)**。

多个进程通常**不共享任何内存**。这意味着每个正在运行的进程都有自己的东西、变量和内存。如果你的代码消耗了大量内存，**每个进程**将消耗等量的内存。

### 服务器内存 { #server-memory }

例如，如果你的代码加载**大小为 1 GB** 的机器学习模型，则当你使用 API 运行一个进程时，它将至少消耗 1 GB RAM。如果你启动 **4 个进程**（4 个工作进程），每个进程将消耗 1 GB RAM。因此，你的 API 总共将消耗 **4 GB RAM**。

如果你的远程服务器或虚拟机只有 3 GB RAM，尝试加载超过 4 GB RAM 将导致问题。 🚨

### 多进程 - 一个例子 { #multiple-processes-an-example }

在此示例中，有一个 **Manager Process** 启动并控制两个 **Worker Processes**。

该管理器进程可能是监听 IP 中的**端口**的进程。它将所有通信传输到工作进程。

这些工作进程将是运行你的应用程序的进程，它们将执行主要计算以接收**请求**并返回**响应**，并且它们将加载你放入 RAM 中的变量中的任何内容。

<img src="/img/deployment/concepts/process-ram.drawio.svg">

当然，除了你的应用程序之外，同一台机器可能还运行**其他进程**。

一个有趣的细节是，随着时间的推移，每个进程使用的 **CPU 百分比**可能会发生很大变化，但**内存 (RAM)** 通常会或多或少保持**稳定**。

如果你有一个每次执行相当数量的计算的 API，并且你有很多客户端，那么 **CPU 利用率** 可能*也会保持稳定*（而不是不断快速上升和下降）。

### 复制工具和策略示例 { #examples-of-replication-tools-and-strategies }

可以通过多种方法来实现这一目标，我将在接下来的章节中向你详细介绍具体策略，例如在谈论 Docker 和容器时。

要考虑的主要限制是必须有一个**单个**组件来处理**公共 IP** 中的**端口**。然后它必须有一种方法将通信**传输**到复制的**进程/worker**。

以下是一些可能的组合和策略：

* 带有 `--workers` 的 **Uvicorn**
    * 一个 Uvicorn **进程管理器**将监听 **IP** 和**端口**，并且它将启动**多个 Uvicorn 工作进程**。
* **Kubernetes** 和其他分布式**容器系统**
    * **Kubernetes** 层中的某些东西将侦听 **IP** 和**端口**。复制将通过拥有**多个容器**来完成，每个容器运行**一个 Uvicorn 进程**。
* **云服务** 为你处理此问题
    * 云服务可能**为你处理复制**。它可能会让你定义**要运行的进程**，或要使用的**容器镜像**，在任何情况下，它很可能是**单个 Uvicorn 进程**，并且云服务将负责复制它。

/// tip | 提示

如果这些关于**容器**、Docker 或 Kubernetes 的内容还没有多大意义，请不要担心。

我将在以后的章节中向你详细介绍容器镜像、Docker、Kubernetes 等：[容器中的 FastAPI - Docker](docker.md)。

///

## 启动之前的步骤 { #previous-steps-before-starting }

在很多情况下，你希望在**启动**应用程序之前执行一些步骤。

例如，你可能想要运行**数据库迁移**。

但在大多数情况下，你只想执行这些步骤**一次**。

因此，在启动应用程序之前，你将需要一个**单个进程**来执行这些**前面的步骤**。

而且你必须确保它是运行前面步骤的单个进程，*即使*之后你为应用程序本身启动**多个进程**（多个 worker）。如果这些步骤由**多个进程**运行，它们会通过**并行**运行来**重复**工作，并且如果这些步骤像数据库迁移一样需要小心处理，它们可能会导致彼此之间发生冲突。

当然，也有一些情况，多次运行前面的步骤也没有问题，这样的话就好办多了。

/// tip | 提示

另外，请记住，根据你的设置，在某些情况下，你在启动应用程序之前**可能甚至不需要任何先前的步骤**。

在这种情况下，你就不必担心这些。 🤷

///

### 前面步骤策略的示例 { #examples-of-previous-steps-strategies }

这将在**很大程度上取决于你部署系统的方式**，并且可能与你启动程序、处理重启等的方式有关。

以下是一些可能的想法：

* Kubernetes 中的“Init Container”在应用程序容器之前运行
* 一个 bash 脚本，运行前面的步骤，然后启动你的应用程序
    * 你仍然需要一种方法来启动/重新启动*那个* bash 脚本、检测错误等。

/// tip | 提示

我将在以后的章节中为你提供使用容器执行此操作的更具体示例：[容器中的 FastAPI - Docker](docker.md)。

///

## 资源利用率 { #resource-utilization }

你的服务器是一个**资源**，你可以通过你的程序消耗或**利用** CPU 上的计算时间以及可用的 RAM 内存。

你想要消耗/利用多少系统资源？你可能很容易认为“不多”，但实际上，你可能希望在不崩溃的情况下**尽可能多地消耗**。

如果你支付了 3 台服务器的费用，但只使用了它们的一点点 RAM 和 CPU，那么你可能**浪费金钱** 💸，并且可能**浪费服务器电力** 🌎，等等。

在这种情况下，最好只拥有 2 台服务器并使用更高比例的资源（CPU、内存、磁盘、网络带宽等）。

另一方面，如果你有 2 台服务器，并且正在使用**它们 100% 的 CPU 和 RAM**，则在某些时候，一个进程会要求更多内存，并且服务器将不得不使用磁盘作为“内存”（这可能会慢数千倍），甚至**崩溃**。或者一个进程可能需要执行一些计算，并且必须等到 CPU 再次空闲。

在这种情况下，最好购买**一台额外的服务器**并在其上运行一些进程，以便它们都有**足够的 RAM 和 CPU 时间**。

由于某种原因，你的 API 的使用量也有可能出现**激增**。也许它像病毒一样传播开来，或者也许其他一些服务或机器人开始使用它。在这些情况下，你可能需要额外的资源来保证安全。

你可以将一个**任意数字**设置为目标，例如，资源利用率**在 50% 到 90%** 之间。重点是，这些可能是你想要衡量和用来调整部署的主要内容。

你可以使用 `htop` 等简单工具来查看服务器中使用的 CPU 和 RAM 或每个进程使用的数量。或者你可以使用更复杂的监控工具，这些工具可能分布在服务器等上。

## 回顾 { #recap }

你在这里阅读了一些在决定如何部署应用程序时可能需要牢记的主要概念：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 启动前的先前步骤

了解这些想法以及如何应用它们应该会给你足够的直觉，以便在配置和调整部署时做出任何决定。 🤓

在接下来的部分中，我将为你提供更具体的示例，说明你可以遵循的可能策略。 🚀



---

# Source: docs/deployment/docker.md


# 容器中的 FastAPI - Docker { #fastapi-in-containers-docker }


部署 FastAPI 应用时，常见做法是构建一个**Linux 容器镜像**。通常使用 [**Docker**](https://www.docker.com/) 实现。然后你可以用几种方式之一部署该镜像。

使用 Linux 容器有多种优势，包括**安全性**、**可复制性**、**简单性**等。

/// tip | 提示

赶时间并且已经了解这些？直接跳到下面的 [`Dockerfile` 👇](#build-a-docker-image-for-fastapi)。

///

<details>
<summary>Dockerfile 预览 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# 如果在 Nginx 或 Traefik 等代理后运行，请添加 --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## 什么是容器 { #what-is-a-container }

容器（主要是 Linux 容器）是一种非常**轻量**的方式，用来打包应用及其所有依赖和必要文件，并让它们与同一系统中的其他容器（其他应用或组件）相互隔离。

Linux 容器复用宿主机（物理机、虚拟机、云服务器等）的同一个 Linux 内核。这意味着它们非常轻量（相较于模拟整个操作系统的完整虚拟机）。

因此，容器消耗的**资源很少**，大致相当于直接运行进程（而虚拟机会多很多）。

容器还拥有各自**隔离**的运行进程（通常只有一个）、文件系统和网络，简化了部署、安全、开发等。

## 什么是容器镜像 { #what-is-a-container-image }

**容器**是从**容器镜像**运行的。

容器镜像是容器中所有文件、环境变量以及应该运行的默认命令/程序的一个**静态**版本。这里的**静态**指容器**镜像**本身并不在运行，仅仅是被打包的文件和元数据。

与存放静态内容的“**容器镜像**”相对，“**容器**”通常指一个正在运行的实例，即正在被**执行**的东西。

当**容器**启动并运行（从**容器镜像**启动）后，它可以创建或修改文件、环境变量等。这些更改只存在于该容器中，不会持久化到底层的容器镜像中（不会写回磁盘）。

容器镜像可类比为**程序**文件及其内容，例如 `python` 和某个文件 `main.py`。

而**容器**本身（相对**容器镜像**）就是该镜像的实际运行实例，可类比为**进程**。事实上，容器只有在有**进程在运行**时才处于运行状态（通常只有一个进程）。当容器中没有任何进程在运行时，容器就会停止。

## 容器镜像 { #container-images }

Docker 一直是创建和管理**容器镜像**与**容器**的主要工具之一。

还有一个公共的 [Docker Hub](https://hub.docker.com/)，其中为许多工具、环境、数据库和应用提供了预制的**官方容器镜像**。

例如，有官方的 [Python 镜像](https://hub.docker.com/_/python)。

还有许多用于不同目的（如数据库）的镜像，例如：

* [PostgreSQL](https://hub.docker.com/_/postgres)
* [MySQL](https://hub.docker.com/_/mysql)
* [MongoDB](https://hub.docker.com/_/mongo)
* [Redis](https://hub.docker.com/_/redis) 等。

通过使用预制的容器镜像，可以很容易地**组合**并使用不同工具。例如，试用一个新的数据库。在大多数情况下，你可以直接使用**官方镜像**，只需通过环境变量配置即可。

这样，在很多场景中你可以学习容器和 Docker，并将这些知识复用到许多不同的工具和组件中。

因此，你可以运行包含不同内容的**多个容器**，比如一个数据库、一个 Python 应用、一个带 React 前端的 Web 服务器，并通过它们的内部网络连接在一起。

所有容器管理系统（如 Docker 或 Kubernetes）都内置了这些网络功能。

## 容器与进程 { #containers-and-processes }

**容器镜像**通常在其元数据中包含在**容器**启动时应运行的默认程序或命令以及要传递给该程序的参数。这与命令行中做的事情非常相似。

当**容器**启动时，它将运行该命令/程序（尽管你可以覆盖它，让其运行不同的命令/程序）。

只要**主进程**（命令或程序）在运行，容器就在运行。

容器通常只有**一个进程**，但也可以由主进程启动子进程，这样同一个容器中就会有**多个进程**。

但不可能在没有**至少一个运行中的进程**的情况下让容器保持运行。如果主进程停止，容器也会停止。

## 为 FastAPI 构建 Docker 镜像 { #build-a-docker-image-for-fastapi }

好啦，现在动手构建点东西！🚀

我将演示如何基于**官方 Python** 镜像，**从零开始**为 FastAPI 构建一个**Docker 镜像**。

这在**大多数情况**下都适用，例如：

* 使用 **Kubernetes** 或类似工具
* 运行在 **Raspberry Pi**
* 使用某个为你运行容器镜像的云服务，等等

### 包依赖 { #package-requirements }

通常你会把应用的**包依赖**放在某个文件里。

这主要取决于你用来**安装**这些依赖的工具。

最常见的方式是使用 `requirements.txt` 文件，每行一个包名及其版本范围。

当然，你也可以参考你在[关于 FastAPI 版本](versions.md)中读到的思路来设置版本范围。

例如，你的 `requirements.txt` 可能是：

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

通常你会用 `pip` 安装这些依赖，例如：

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// note | 注意

还有其他格式和工具可以定义并安装包依赖。

///

### 编写 **FastAPI** 代码 { #create-the-fastapi-code }

* 创建 `app` 目录并进入
* 创建空文件 `__init__.py`
* 创建 `main.py`，内容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

现在在同一个项目目录下创建 `Dockerfile` 文件：

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. 从官方 Python 基础镜像开始。

2. 将当前工作目录设置为 `/code`。

    我们会把 `requirements.txt` 文件和 `app` 目录放在这里。

3. 将依赖文件复制到 `/code` 目录。

    首先**只**复制依赖文件，不要复制其他代码。

    因为这个文件**不常变化**，Docker 会检测并在此步骤使用**缓存**，从而也为下一步启用缓存。

4. 安装依赖文件中的包依赖。

    `--no-cache-dir` 选项告诉 `pip` 不要在本地保存下载的包，只有当以后还要再次用 `pip` 安装相同包时才需要，但在容器场景下不是这样。

    /// note | 注意

    `--no-cache-dir` 只和 `pip` 有关，与 Docker 或容器无关。

    ///

    `--upgrade` 选项告诉 `pip` 如果包已安装则进行升级。

    由于上一步复制文件可能被 **Docker 缓存**检测到，因此这一步在可用时也会**使用 Docker 缓存**。

    在开发过程中反复构建镜像时，此步骤使用缓存可以为你**节省大量时间**，而不必**每次**都**下载并安装**所有依赖。

5. 将 `./app` 目录复制到 `/code` 目录。

    这里包含了所有**最常变化**的代码，因此 Docker **缓存**很难用于这一步或**其后的步骤**。

    所以，把它放在 `Dockerfile` 的**靠后位置**，有助于优化容器镜像的构建时间。

6. 设置使用 `fastapi run` 的**命令**（底层使用 Uvicorn）。

    `CMD` 接受一个字符串列表，每个字符串相当于你在命令行中用空格分隔输入的内容。

    该命令会从**当前工作目录**运行，也就是你用 `WORKDIR /code` 设置的 `/code` 目录。

/// tip | 提示

点击代码中的每个编号气泡查看每行的作用。👆

///

/// warning | 警告

务必**始终**使用 `CMD` 指令的**exec 形式**，如下所述。

///

#### 使用 `CMD` - Exec 形式 { #use-cmd-exec-form }

[`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) 指令有两种写法：

✅ **Exec** 形式：

```Dockerfile
# ✅ 推荐
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** 形式：

```Dockerfile
# ⛔️ 不要这样
CMD fastapi run app/main.py --port 80
```

务必使用**exec** 形式，以确保 FastAPI 可以优雅停机并触发[生命周期事件](../advanced/events.md)。

你可以在 [Docker 文档（Shell 与 Exec 形式）](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form)中了解更多。

在使用 `docker compose` 时这一点尤为明显。更多技术细节参见该 FAQ：[为什么我的服务需要 10 秒才能重新创建或停止？](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop)

#### 目录结构 { #directory-structure }

此时你的目录结构应类似：

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### 在 TLS 终止代理后面 { #behind-a-tls-termination-proxy }

如果你在 Nginx 或 Traefik 等 TLS 终止代理（负载均衡器）后面运行容器，请添加 `--proxy-headers` 选项，这会通过 FastAPI CLI 告诉 Uvicorn 信任该代理发送的标头，表明应用运行在 HTTPS 后等。

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker 缓存 { #docker-cache }

这个 `Dockerfile` 里有个重要技巧：我们先**只复制依赖文件**，而不是其他代码。原因如下：

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker 等工具是**增量**地**构建**容器镜像的，从 `Dockerfile` 顶部开始，按顺序为每条指令创建**一层叠加层**，并把每步生成的文件加入。

构建镜像时，Docker 等工具也会使用**内部缓存**。如果自上次构建以来某个文件没有变更，它会**重用**上次创建的那一层，而不是再次复制文件并从头创建新层。

仅仅避免复制文件并不会带来太多改进，但因为该步骤使用了缓存，它就可以**在下一步中继续使用缓存**。例如，安装依赖的这条指令也能使用缓存：

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

包含包依赖的文件**不会频繁变更**。仅复制该文件，Docker 就能在这一步**使用缓存**。

随后，Docker 还能**对下一步**（下载并安装依赖）**使用缓存**。这正是我们**节省大量时间**的地方。✨ ...并避免无聊的等待。😪😆

下载并安装依赖**可能需要几分钟**，而使用**缓存**则**最多只需几秒**。

而且在开发中你会反复构建镜像来验证代码变更是否生效，累计节省的时间会很多。

接着，在 `Dockerfile` 的末尾附近我们再复制所有代码。因为这是**变化最频繁**的部分，把它放在后面，这样几乎所有在它之后的步骤都不会使用到缓存。

```Dockerfile
COPY ./app /code/app
```

### 构建 Docker 镜像 { #build-the-docker-image }

现在所有文件都就位了，开始构建容器镜像。

* 进入项目目录（`Dockerfile` 所在位置，包含 `app` 目录）
* 构建你的 FastAPI 镜像：

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | 提示

注意末尾的 `.`，它等价于 `./`，用于告诉 Docker 使用哪个目录来构建容器镜像。

此处就是当前目录（`.`）。

///

### 启动 Docker 容器 { #start-the-docker-container }

* 基于你的镜像运行一个容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 检查一下 { #check-it }

你应该能在容器暴露的 URL 访问它，例如：[http://192.168.99.100/items/5?q=somequery](http://192.168.99.100/items/5?q=somequery) 或 [http://127.0.0.1/items/5?q=somequery](http://127.0.0.1/items/5?q=somequery)（或其他等价地址，取决于你的 Docker 主机）。

你会看到类似内容：

```JSON
{"item_id": 5, "q": "somequery"}
```

## 交互式 API 文档 { #interactive-api-docs }

现在你可以访问 [http://192.168.99.100/docs](http://192.168.99.100/docs) 或 [http://127.0.0.1/docs](http://127.0.0.1/docs)（或其他等价地址，取决于你的 Docker 主机）。

你将看到自动生成的交互式 API 文档（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 备选 API 文档 { #alternative-api-docs }

你还可以访问 [http://192.168.99.100/redoc](http://192.168.99.100/redoc) 或 [http://127.0.0.1/redoc](http://127.0.0.1/redoc)（或其他等价地址，取决于你的 Docker 主机）。

你将看到备选的自动文档（由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 使用单文件 FastAPI 构建 Docker 镜像 { #build-a-docker-image-with-a-single-file-fastapi }

如果你的 FastAPI 是单个文件，例如没有 `./app` 目录、只有 `main.py`，你的文件结构可能如下：

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

然后你只需要在 `Dockerfile` 中修改相应路径来复制该文件：

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. 直接将 `main.py` 复制到 `/code`（没有 `./app` 目录）。

2. 使用 `fastapi run` 来运行单文件 `main.py` 中的应用。

当你把文件传给 `fastapi run` 时，它会自动检测这是一个单文件而不是包，并知道如何导入并服务你的 FastAPI 应用。😎

## 部署概念 { #deployment-concepts }

我们再从容器的角度讨论一些相同的[部署概念](concepts.md)。

容器主要是简化应用**构建与部署**流程的工具，但它们并不强制采用某种特定方式来处理这些**部署概念**，可选策略有多种。

**好消息**是，不同策略下都有方式覆盖所有部署概念。🎉

让我们从容器角度回顾这些**部署概念**：

* HTTPS
* 启动时运行
* 失败重启
* 复制（运行的进程数）
* 内存
* 启动前的前置步骤

## HTTPS { #https }

如果我们只关注 FastAPI 应用的**容器镜像**（以及后续运行的**容器**），HTTPS 通常由**外部**的其他工具处理。

它可以是另一个容器，例如使用 [Traefik](https://traefik.io/)，处理 **HTTPS** 并**自动**获取**证书**。

/// tip | 提示

Traefik 与 Docker、Kubernetes 等都有集成，因此为容器设置和配置 HTTPS 非常容易。

///

或者，HTTPS 也可能由云服务商作为其服务之一提供（应用仍运行在容器中）。

## 启动时运行与重启 { #running-on-startup-and-restarts }

通常会有另一个工具负责**启动并运行**你的容器。

它可以是直接的 **Docker**、**Docker Compose**、**Kubernetes**、某个**云服务**等。

在大多数（或全部）情况下，都有简单选项可以在开机时运行容器并在失败时启用重启。例如，在 Docker 中是命令行选项 `--restart`。

如果不使用容器，要让应用开机自启并带重启可能繁琐且困难。但在**容器**场景下，这种功能通常默认就包含了。✨

## 复制 - 进程数 { #replication-number-of-processes }

如果你有一个由 **Kubernetes**、Docker Swarm Mode、Nomad 或其他类似的复杂系统管理的、在多台机器上运行的分布式容器<dfn title="被配置为以某种方式连接并协同工作的多台机器">集群</dfn>，那么你很可能会希望在**集群层面**来**处理复制**，而不是在每个容器中使用**进程管理**（比如让 Uvicorn 运行多个 workers）。

像 Kubernetes 这样的分布式容器管理系统通常都有某种内置方式来处理**容器复制**，同时对传入请求进行**负载均衡**。这一切都在**集群层面**完成。

在这些情况下，你可能希望如[上文所述](#dockerfile)那样**从头构建 Docker 镜像**，安装依赖，并仅运行**单个 Uvicorn 进程**，而不是使用多个 Uvicorn workers。

### 负载均衡器 { #load-balancer }

使用容器时，通常会有某个组件**监听主端口**。它可能是另一个同时充当 **TLS 终止代理**以处理 **HTTPS** 的容器，或类似工具。

由于该组件会承接请求的**负载**并以（期望）**均衡**的方式在 workers 间分发，它也常被称为**负载均衡器**。

/// tip | 提示

用于 HTTPS 的**TLS 终止代理**组件通常也会是**负载均衡器**。

///

使用容器时，你用来启动和管理容器的系统本身就已有内部工具，将来自该**负载均衡器**（也可能是**TLS 终止代理**）的**网络通信**（例如 HTTP 请求）传递到你的应用容器中。

### 一个负载均衡器 - 多个 worker 容器 { #one-load-balancer-multiple-worker-containers }

在 **Kubernetes** 等分布式容器管理系统中，使用其内部网络机制，允许在主**端口**上监听的单个**负载均衡器**将通信（请求）转发给可能**多个**运行你应用的容器。

这些运行你应用的容器通常每个只有**一个进程**（例如，一个运行 FastAPI 应用的 Uvicorn 进程）。它们都是**相同的容器**，运行相同的东西，但每个都有自己的进程、内存等。这样你就能在 CPU 的**不同核心**，甚至在**不同机器**上利用**并行化**。

分布式容器系统配合**负载均衡器**会把请求**轮流分配**到每个应用容器。因此，每个请求都可能由多个**副本容器**之一来处理。

通常，这个**负载均衡器**还能处理发往集群中*其他*应用的请求（例如不同域名，或不同的 URL 路径前缀），并将通信转发到运行*那个其他*应用的正确容器。

### 每个容器一个进程 { #one-process-per-container }

在这种场景下，你大概率希望**每个容器只有一个（Uvicorn）进程**，因为你已经在集群层面处理了复制。

因此，这种情况下你**不希望**在容器内再启多个 workers（例如通过 `--workers` 命令行选项）。你会希望每个容器仅有一个**单独的 Uvicorn 进程**（但可能会有多个容器）。

在容器内再放一个进程管理器（就像启多个 workers 一样）只会引入**不必要的复杂性**，而这些你很可能已经在集群系统中处理了。

### 具有多个进程和特殊情况的容器 { #containers-with-multiple-processes-and-special-cases }

当然，也有一些**特殊情况**，你可能希望让**一个容器**里运行多个 **Uvicorn worker 进程**。

在这些情况下，你可以使用 `--workers` 命令行选项来设置要运行的 worker 数量：

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. 这里我们使用 `--workers` 命令行选项将 worker 数量设置为 4。

以下是这种做法可能合理的一些示例：

#### 一个简单的应用 { #a-simple-app }

如果你的应用**足够简单**，可以在**单台服务器**（不是集群）上运行，你可能会希望在容器内有一个进程管理器。

#### Docker Compose { #docker-compose }

如果你使用 **Docker Compose** 部署到**单台服务器**（不是集群），那么你不会有一个简单的方法在保留共享网络与**负载均衡**的同时管理容器复制（通过 Docker Compose）。

这种情况下，你可能希望用**单个容器**，由**进程管理器**在容器内启动**多个 worker 进程**。

---

要点是，这些都**不是**你必须盲目遵循的**铁律**。你可以用这些思路来**评估你自己的场景**，并决定最适合你的系统的方法，看看如何管理以下概念：

* 安全 - HTTPS
* 启动时运行
* 重启
* 复制（运行的进程数）
* 内存
* 启动前的前置步骤

## 内存 { #memory }

如果你**每个容器只运行一个进程**，那么每个容器消耗的内存将更容易定义、较为稳定且有限（如果有复制则为多个容器）。

接着，你可以在容器管理系统（例如 **Kubernetes**）的配置中设置同样的内存限制与需求。这样它就能在**可用的机器**上**复制容器**，同时考虑容器所需的内存量以及集群中机器可用的内存量。

如果你的应用很**简单**，这可能**不成问题**，你也许不需要设置严格的内存上限。但如果你**使用大量内存**（例如使用**机器学习**模型），你应该检查自己的内存消耗，并调整**每台机器**上运行的**容器数量**（也许还需要为集群增加机器）。

如果你**每个容器运行多个进程**，你需要确保启动的进程数量不会**消耗超过可用的内存**。

## 启动前的前置步骤与容器 { #previous-steps-before-starting-and-containers }

如果你在使用容器（如 Docker、Kubernetes），你可以采用两种主要方式。

### 多个容器 { #multiple-containers }

如果你有**多个容器**，可能每个容器运行一个**单独进程**（例如在 **Kubernetes** 集群中），那么你可能希望使用一个**单独的容器**来执行**前置步骤**，在一个容器中运行一个进程，**在**启动那些复制的 worker 容器**之前**完成。

/// note | 注意

如果你使用 Kubernetes，这通常会是一个 [Init Container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)。

///

如果在你的用例中，**并行多次**运行这些前置步骤没有问题（例如你不是在跑数据库迁移，而只是检查数据库是否就绪），那么你也可以把这些步骤放在每个容器中，在启动主进程之前执行。

### 单个容器 { #single-container }

如果你的架构较为简单，使用一个**单个容器**，其后再启动多个**worker 进程**（或者也只有一个进程），那么你可以在同一个容器中，在启动应用进程之前执行这些前置步骤。

### 基础 Docker 镜像 { #base-docker-image }

曾经有一个官方的 FastAPI Docker 镜像：[tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)。但它现在已被弃用。⛔️

你大概率**不应该**使用这个基础镜像（或任何其它类似的镜像）。

如果你使用 **Kubernetes**（或其他）并且已经在集群层面设置**复制**、使用多个**容器**，那么在这些情况下，最好如上所述**从头构建镜像**：[为 FastAPI 构建 Docker 镜像](#build-a-docker-image-for-fastapi)。

如果你需要多个 workers，可以直接使用 `--workers` 命令行选项。

/// note | 技术细节

这个 Docker 镜像创建于 Uvicorn 还不支持管理与重启失效 workers 的时期，那时需要用 Gunicorn 搭配 Uvicorn，这引入了不少复杂度，只是为了让 Gunicorn 管理并重启 Uvicorn 的 worker 进程。

但现在 Uvicorn（以及 `fastapi` 命令）已经支持使用 `--workers`，因此没有理由不自己构建基础镜像（代码量几乎一样 😅）。

///

## 部署容器镜像 { #deploy-the-container-image }

得到容器（Docker）镜像后，有多种方式可以部署。

例如：

* 在单台服务器上使用 **Docker Compose**
* 使用 **Kubernetes** 集群
* 使用 Docker Swarm Mode 集群
* 使用 Nomad 等其他工具
* 使用云服务，接收你的容器镜像并部署

## 使用 `uv` 的 Docker 镜像 { #docker-image-with-uv }

如果你使用 [uv](https://github.com/astral-sh/uv) 来安装和管理项目，可以参考他们的 [uv Docker 指南](https://docs.astral.sh/uv/guides/integration/docker/)。

## 回顾 { #recap }

使用容器系统（例如 **Docker** 与 **Kubernetes**）后，处理所有**部署概念**会变得相当直接：

* HTTPS
* 启动时运行
* 失败重启
* 复制（运行的进程数）
* 内存
* 启动前的前置步骤

在大多数情况下，你可能不想使用任何基础镜像，而是基于官方 Python Docker 镜像**从头构建容器镜像**。

注意 `Dockerfile` 中指令的**顺序**并利用好**Docker 缓存**，可以**最小化构建时间**，以最大化生产力（并避免无聊）。😎



---

# Source: docs/deployment/fastapicloud.md


# FastAPI Cloud { #fastapi-cloud }

你可以用**一条命令**将你的 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。🚀

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI 会自动检测你的 FastAPI 应用并将其部署到云端。如果你尚未登录，浏览器会自动打开以完成认证流程。

就这样！现在你可以通过该 URL 访问你的应用。✨

## 关于 FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 由 **FastAPI** 背后的作者与团队打造。

它让你以最小的投入完成 API 的**构建**、**部署**与**访问**。

它把使用 FastAPI 构建应用时的**开发者体验**，同样带到将应用**部署**到云上的过程。🎉

它还会替你处理部署应用时大多数需要的事项，例如：

* HTTPS
* 副本、基于请求的自动伸缩
* 等等

FastAPI Cloud 是 *FastAPI and friends* 开源项目的主要赞助方与资金提供者。✨

## 部署到其他云服务商 { #deploy-to-other-cloud-providers }

FastAPI 是开源的，并基于标准。你可以将 FastAPI 应用部署到你选择的任意云服务商。

按照你所选云服务商的指南部署 FastAPI 应用即可。🤓

## 部署到你自己的服务器 { #deploy-your-own-server }

在后面的**部署**指南中，我也会讲解所有细节，帮助你理解幕后发生了什么、需要做什么，以及如何自行部署 FastAPI 应用，包括部署到你自己的服务器。🤓



---

# Source: docs/deployment/https.md


# 关于 HTTPS { #about-https }

人们很容易认为 HTTPS 仅仅是“启用”或“未启用”的东西。

但实际情况比这复杂得多。

/// tip | 提示

如果你很赶时间或不在乎，请继续阅读后续章节，它们会提供逐步的教程，告诉你怎么使用不同技术把一切都配置好。

///

要从用户的视角**了解 HTTPS 的基础知识**，请查看 [https://howhttps.works/](https://howhttps.works/)。

现在，从**开发人员的视角**，在了解 HTTPS 时需要记住以下几点：

* 要使用 HTTPS，**服务器**需要拥有由**第三方**生成的**"证书(certificate)"**。
    * 这些证书实际上是从第三方**获取**的，而不是“生成”的。
* 证书有**生命周期**。
    * 它们会**过期**。
    * 然后它们需要**更新**，**再次从第三方获取**。
* 连接的加密发生在 **TCP 层**。
    * 这是 HTTP 协议**下面的一层**。
    * 因此，**证书和加密**处理是在 **HTTP之前**完成的。
* **TCP 不知道域名**。 仅仅知道 IP 地址。
    * 有关所请求的 **特定域名** 的信息位于 **HTTP 数据**中。
* **HTTPS 证书**“证明”**某个域名**，但协议和加密发生在 TCP 层，在知道正在处理哪个域名**之前**。
* **默认情况下**，这意味着你**每个 IP 地址只能拥有一个 HTTPS 证书**。
    * 无论你的服务器有多大，或者服务器上的每个应用程序有多小。
    * 不过，对此有一个**解决方案**。
* **TLS** 协议（在 HTTP 之下的 TCP 层处理加密的协议）有一个**扩展**，称为 **[<abbr title="Server Name Indication - 服务器名称指示">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)**。
    * SNI 扩展允许一台服务器（具有 **单个 IP 地址**）拥有 **多个 HTTPS 证书** 并提供 **多个 HTTPS 域名/应用程序**。
    * 为此，服务器上会有**单独**的一个组件（程序）侦听**公共 IP 地址**，这个组件必须拥有服务器中的**所有 HTTPS 证书**。
* **获得安全连接后**，通信协议**仍然是HTTP**。
    * 内容是 **加密过的**，即使它们是通过 **HTTP 协议** 发送的。

通常的做法是在服务器上运行**一个程序/HTTP 服务器**并**管理所有 HTTPS 部分**：接收**加密的 HTTPS 请求**， 将 **解密的 HTTP 请求** 发送到在同一服务器中运行的实际 HTTP 应用程序（在本例中为 **FastAPI** 应用程序），从应用程序中获取 **HTTP 响应**， 使用适当的 **HTTPS 证书**对其进行加密并使用 **HTTPS** 将其发送回客户端。 此服务器通常被称为 **[TLS 终止代理(TLS Termination Proxy)](https://en.wikipedia.org/wiki/TLS_termination_proxy)**。

你可以用作 TLS 终止代理的一些选项包括：

* Traefik（也可以处理证书更新）
* Caddy（也可以处理证书更新）
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

在 Let's Encrypt 之前，这些 **HTTPS 证书** 由受信任的第三方出售。

过去，获得这些证书的过程非常繁琐，需要大量的文书工作，而且证书非常昂贵。

但随后 **[Let's Encrypt](https://letsencrypt.org/)** 创建了。

它是 Linux 基金会的一个项目。 它以自动方式免费提供 **HTTPS 证书**。 这些证书可以使用所有符合标准的安全加密，并且有效期很短（大约 3 个月），因此**安全性实际上更好**，因为它们的生命周期缩短了。

域可以被安全地验证并自动生成证书。 这还允许自动更新这些证书。

我们的想法是自动获取和更新这些证书，以便你可以永远免费拥有**安全的 HTTPS**。

## 面向开发人员的 HTTPS { #https-for-developers }

这里有一个 HTTPS API 看起来是什么样的示例，我们会分步说明，并且主要关注对开发人员重要的部分。

### 域名 { #domain-name }

第一步我们要先**获取**一些**域名(Domain Name)**。 然后可以在 DNS 服务器（可能是你的同一家云服务商提供的）中配置它。

你可能拥有一个云服务器（虚拟机）或类似的东西，并且它会有一个<dfn title="不会随时间改变。非动态的。">固定</dfn> **公共IP地址**。

在 DNS 服务器中，你可以配置一条记录（一个 `A record`）以将 **你的域名** 指向你服务器的公共 **IP 地址**。

这个操作一般只需要在最开始执行一次。

/// tip | 提示

域名这部分发生在 HTTPS 之前，由于这一切都依赖于域名和 IP 地址，所以先在这里提一下。

///

### DNS { #dns }

现在让我们关注真正的 HTTPS 部分。

首先，浏览器将通过 **DNS 服务器** 查询**域名的IP** 是什么，在本例中为 `someapp.example.com`。

DNS 服务器会告诉浏览器使用某个特定的 **IP 地址**。 这将是你在 DNS 服务器中为你的服务器配置的公共 IP 地址。

<img src="/img/deployment/https/https01.drawio.svg">

### TLS 握手开始 { #tls-handshake-start }

然后，浏览器将在**端口 443**（HTTPS 端口）上与该 IP 地址进行通信。

通信的第一部分只是建立客户端和服务器之间的连接并决定它们将使用的加密密钥等。

<img src="/img/deployment/https/https02.drawio.svg">

客户端和服务器之间建立 TLS 连接的过程称为 **TLS 握手**。

### 带有 SNI 扩展的 TLS { #tls-with-sni-extension }

**服务器中只有一个进程**可以侦听特定 **IP 地址**的特定 **端口**。 可能有其他进程在同一 IP 地址的其他端口上侦听，但每个 IP 地址和端口组合只有一个进程。

TLS (HTTPS) 默认使用端口`443`。 这就是我们需要的端口。

由于只有一个进程可以监听此端口，因此监听端口的进程将是 **TLS 终止代理**。

TLS 终止代理可以访问一个或多个 **TLS 证书**（HTTPS 证书）。

使用上面讨论的 **SNI 扩展**，TLS 终止代理将检查应该用于此连接的可用 TLS (HTTPS) 证书，并使用与客户端期望的域名相匹配的证书。

在这种情况下，它将使用`someapp.example.com`的证书。

<img src="/img/deployment/https/https03.drawio.svg">

客户端已经**信任**生成该 TLS 证书的实体（在本例中为 Let's Encrypt，但我们稍后会看到），因此它可以**验证**该证书是否有效。

然后，通过使用证书，客户端和 TLS 终止代理 **决定如何加密** **TCP 通信** 的其余部分。 这就完成了 **TLS 握手** 部分。

此后，客户端和服务器就拥有了**加密的 TCP 连接**，这就是 TLS 提供的功能。 然后他们可以使用该连接来启动实际的 **HTTP 通信**。

这就是 **HTTPS**，它只是 **安全 TLS 连接** 内的普通 **HTTP**，而不是纯粹的（未加密的）TCP 连接。

/// tip | 提示

请注意，通信加密发生在 **TCP 层**，而不是 HTTP 层。

///

### HTTPS 请求 { #https-request }

现在客户端和服务器（特别是浏览器和 TLS 终止代理）具有 **加密的 TCP 连接**，它们可以开始 **HTTP 通信**。

接下来，客户端发送一个 **HTTPS 请求**。 这其实只是一个通过 TLS 加密连接的 HTTP 请求。

<img src="/img/deployment/https/https04.drawio.svg">

### 解密请求 { #decrypt-the-request }

TLS 终止代理将使用协商好的加密算法**解密请求**，并将**（解密的）HTTP 请求**传输到运行应用程序的进程（例如运行 FastAPI 应用的 Uvicorn 进程）。

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP 响应 { #http-response }

应用程序将处理请求并向 TLS 终止代理发送**（未加密）HTTP 响应**。

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS 响应 { #https-response }

然后，TLS 终止代理将使用之前协商的加密算法（以`someapp.example.com`的证书开头）对响应进行加密，并将其发送回浏览器。

接下来，浏览器将验证响应是否有效和是否使用了正确的加密密钥等。然后它会**解密响应**并处理它。

<img src="/img/deployment/https/https07.drawio.svg">

客户端（浏览器）将知道响应来自正确的服务器，因为它使用了他们之前使用 **HTTPS 证书** 协商出的加密算法。

### 多个应用程序 { #multiple-applications }

在同一台（或多台）服务器中，可能存在**多个应用程序**，例如其他 API 程序或数据库。

只有一个进程可以处理特定的 IP 和端口（在我们的示例中为 TLS 终止代理），但其他应用程序/进程也可以在服务器上运行，只要它们不尝试使用相同的 **公共 IP 和端口的组合**。

<img src="/img/deployment/https/https08.drawio.svg">

这样，TLS 终止代理就可以为多个应用程序处理**多个域名**的 HTTPS 和证书，然后在每种情况下将请求传输到正确的应用程序。

### 证书更新 { #certificate-renewal }

在未来的某个时候，每个证书都会**过期**（大约在获得证书后 3 个月）。

然后，会有另一个程序（在某些情况下是另一个程序，在某些情况下可能是同一个 TLS 终止代理）与 Let's Encrypt 通信并更新证书。

<img src="/img/deployment/https/https.drawio.svg">

**TLS 证书** **与域名相关联**，而不是与 IP 地址相关联。

因此，要更新证书，更新程序需要向权威机构（Let's Encrypt）**证明**它确实**“拥有”并控制该域名**。

有多种方法可以做到这一点，并适应不同的应用需求。 一些流行的方式是：

* **修改一些DNS记录**。
    * 为此，续订程序需要支持 DNS 提供商的 API，因此，要看你使用的 DNS 提供商是否提供这一功能。
* **在与域名关联的公共 IP 地址上作为服务器运行**（至少在证书获取过程中）。
    * 正如我们上面所说，只有一个进程可以监听特定的 IP 和端口。
    * 这就是当同一个 TLS 终止代理还负责证书续订过程时它非常有用的原因之一。
    * 否则，你可能需要暂时停止 TLS 终止代理，启动续订程序以获取证书，然后使用 TLS 终止代理配置它们，然后重新启动 TLS 终止代理。 这并不理想，因为你的应用程序在 TLS 终止代理关闭期间将不可用。

在仍然为应用提供服务的同时完成整个更新流程，是你想要用 TLS 终止代理拥有一个**单独系统来处理 HTTPS**，而不是直接在应用服务器（例如 Uvicorn）上使用 TLS 证书的主要原因之一。

## 代理转发请求头 { #proxy-forwarded-headers }

当使用代理来处理 HTTPS 时，你的**应用服务器**（例如通过 FastAPI CLI 运行的 Uvicorn）对 HTTPS 过程并不了解，它只通过纯 HTTP 与 **TLS 终止代理**通信。

这个**代理**通常会在将请求转发给**应用服务器**之前，临时设置一些 HTTP 请求头，以便让应用服务器知道该请求是由代理**转发**过来的。

/// note | 技术细节

这些代理请求头包括：

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

不过，由于**应用服务器**并不知道自己位于受信任的**代理**之后，默认情况下，它不会信任这些请求头。

但你可以配置**应用服务器**去信任由**代理**发送的这些*转发*请求头。如果你在使用 FastAPI CLI，可以使用 *CLI 选项* `--forwarded-allow-ips` 指定它应该信任哪些 IP 发来的这些*转发*请求头。

例如，如果**应用服务器**只接收来自受信任**代理**的通信，你可以设置 `--forwarded-allow-ips="*"`，让它信任所有传入的 IP，因为它只会接收来自**代理**所使用 IP 的请求。

这样，应用就能知道自己的公共 URL、是否使用 HTTPS、域名等信息。

这在需要正确处理重定向等场景时很有用。

/// tip | 提示

你可以在文档中了解更多：[在代理之后 - 启用代理转发请求头](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers)

///

## 回顾 { #recap }

拥有**HTTPS** 非常重要，并且在大多数情况下相当**关键**。 作为开发人员，你围绕 HTTPS 所做的大部分努力就是**理解这些概念**以及它们的工作原理。

一旦你了解了**面向开发人员的 HTTPS** 的基础知识，你就可以轻松组合和配置不同的工具，以帮助你以简单的方式管理一切。

在接下来的一些章节中，我将向你展示几个为 **FastAPI** 应用程序设置 **HTTPS** 的具体示例。 🔒



---

# Source: docs/deployment/index.md


# 部署 { #deployment }

部署 **FastAPI** 应用程序相对容易。

## 部署是什么意思 { #what-does-deployment-mean }

**部署**应用程序意味着执行必要的步骤以使其**可供用户使用**。

对于**Web API**来说，通常涉及将其放到一台**远程机器**中，搭配一个性能和稳定性都不错的**服务器程序**，以便你的**用户**可以高效地**访问**你的应用程序，而不会出现中断或其他问题。

这与**开发**阶段形成鲜明对比，在**开发**阶段，你不断更改代码、破坏代码、修复代码，来回停止和重启开发服务器等。

## 部署策略 { #deployment-strategies }

根据你的使用场景和使用的工具，有多种方法可以实现此目的。

你可以使用一些工具自行**部署服务器**，你也可以使用能为你完成部分工作的**云服务**，或其他可能的选项。

例如，我们（FastAPI 团队）构建了 [**FastAPI Cloud**](https://fastapicloud.com)，让将 FastAPI 应用部署到云端尽可能流畅，并且保持与使用 FastAPI 开发时相同的开发者体验。

我将向你展示在部署 **FastAPI** 应用程序时你可能应该记住的一些主要概念（尽管其中大部分适用于任何其他类型的 Web 应用程序）。

在接下来的部分中，你将看到更多需要记住的细节以及一些技巧。 ✨



---

# Source: docs/deployment/manually.md


# 手动运行服务器 { #run-a-server-manually }

## 使用 `fastapi run` 命令 { #use-the-fastapi-run-command }

简而言之，使用 `fastapi run` 来运行你的 FastAPI 应用程序：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

这在大多数情况下都能正常运行。😎

例如，你可以使用该命令在容器、服务器等环境中启动你的 **FastAPI** 应用。

## ASGI 服务器 { #asgi-servers }

让我们深入了解一些细节。

FastAPI 使用了一种用于构建 Python Web 框架和服务器的标准，称为 <abbr title="Asynchronous Server Gateway Interface - 异步服务器网关接口">ASGI</abbr>。FastAPI 本质上是一个 ASGI Web 框架。

要在远程服务器上运行 **FastAPI** 应用（或任何其他 ASGI 应用），你需要一个 ASGI 服务器程序，例如 **Uvicorn**。它是 `fastapi` 命令默认使用的 ASGI 服务器。

除此之外，还有其他一些可选的 ASGI 服务器，例如：

* [Uvicorn](https://www.uvicorn.dev/): 高性能 ASGI 服务器。
* [Hypercorn](https://hypercorn.readthedocs.io/): 与 HTTP/2 和 Trio 等兼容的 ASGI 服务器。
* [Daphne](https://github.com/django/daphne): 为 Django Channels 构建的 ASGI 服务器。
* [Granian](https://github.com/emmett-framework/granian): 基于 Rust 的 HTTP 服务器，专为 Python 应用设计。

## 服务器主机和服务器程序 { #server-machine-and-server-program }

关于名称，有一个小细节需要记住。 💡

“**服务器**”一词通常用于指远程/云计算机（物理机或虚拟机）以及在该计算机上运行的程序（例如 Uvicorn）。

请记住，当你一般读到“服务器”这个名词时，它可能指的是这两者之一。

当提到远程主机时，通常将其称为**服务器**，但也称为**机器**(machine)、**VM**（虚拟机）、**节点**。 这些都是指某种类型的远程计算机，通常运行 Linux，你可以在其中运行程序。

## 安装服务器程序 { #install-the-server-program }

当你安装 FastAPI 时，它自带一个生产环境服务器——Uvicorn，并且你可以使用 `fastapi run` 命令来启动它。

不过，你也可以手动安装 ASGI 服务器。

请确保你创建并激活一个[虚拟环境](../virtual-environments.md)，然后再安装服务器应用程序。

例如，要安装 Uvicorn，可以运行以下命令：

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

类似的流程也适用于任何其他 ASGI 服务器程序。

/// tip | 提示

通过添加 `standard` 选项，Uvicorn 将安装并使用一些推荐的额外依赖项。

其中包括 `uvloop`，这是 `asyncio` 的高性能替代方案，能够显著提升并发性能。

当你使用 `pip install "fastapi[standard]"` 安装 FastAPI 时，实际上也会安装 `uvicorn[standard]`。

///

## 运行服务器程序 { #run-the-server-program }

如果你手动安装了 ASGI 服务器，通常需要以特定格式传递一个导入字符串，以便服务器能够正确导入你的 FastAPI 应用：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | 注意

命令 `uvicorn main:app` 的含义如下：

* `main`：指的是 `main.py` 文件（即 Python “模块”）。
* `app`：指的是 `main.py` 文件中通过 `app = FastAPI()` 创建的对象。

它等价于以下导入语句：

```Python
from main import app
```

///

每种 ASGI 服务器程序通常都会有类似的命令，你可以在它们的官方文档中找到更多信息。

/// warning | 警告

Uvicorn 和其他服务器支持 `--reload` 选项，该选项在开发过程中非常有用。

但 `--reload` 选项会消耗更多资源，且相对不稳定。

它对于**开发阶段**非常有帮助，但在**生产环境**中**不应该**使用。

///

## 部署概念 { #deployment-concepts }

这些示例运行服务器程序（例如 Uvicorn），启动**单个进程**，在所有 IP（`0.0.0.0`）上监听预定义端口（例如`80`）。

这是基本思路。 但你可能需要处理一些其他事情，例如：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 开始前的步骤

在接下来的章节中，我将向你详细介绍每个概念、如何思考它们，以及一些具体示例以及处理它们的策略。 🚀



---

# Source: docs/deployment/server-workers.md


# 服务器工作进程（Workers） - 使用 Uvicorn 的多工作进程模式 { #server-workers-uvicorn-with-workers }

让我们回顾一下之前的部署概念：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* **复制（运行的进程数）**
* 内存
* 启动前的先前步骤

到目前为止，在文档中的所有教程中，您可能一直是在运行一个**服务器程序**，例如使用 `fastapi` 命令来启动 Uvicorn，而它默认运行的是**单进程模式**。

部署应用程序时，您可能希望进行一些**进程复制**，以利用**多核** CPU 并能够处理更多请求。

正如您在上一章有关[部署概念](concepts.md)中看到的，您可以使用多种策略。

在本章节中，我将向您展示如何使用 `fastapi` 命令或直接使用 `uvicorn` 命令以**多工作进程模式**运行 **Uvicorn**。

/// note | 注意

如果您正在使用容器，例如 Docker 或 Kubernetes，我将在下一章中告诉您更多相关信息：[容器中的 FastAPI - Docker](docker.md)。

比较特别的是，在 **Kubernetes** 环境中运行时，您通常**不需要**使用多个工作进程，而是**每个容器运行一个 Uvicorn 进程**。不过，我会在本章节的后续部分详细介绍这一点。

///

## 多个工作进程 { #multiple-workers }

您可以使用 `--workers` 命令行选项来启动多个工作进程：

//// tab | `fastapi`

如果您使用 `fastapi` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

如果您更想要直接使用 `uvicorn` 命令：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

这里唯一的新选项是 `--workers` 告诉 Uvicorn 启动 4 个工作进程。

您还可以看到它显示了每个进程的 **PID**，父进程（这是**进程管理器**）的 PID 为`27365`，每个工作进程的 PID 为：`27368`、`27369`， `27370`和`27367`。

## 部署概念 { #deployment-concepts }

在这里，您学习了如何使用多个**工作进程（workers）**来让应用程序的执行**并行化**，充分利用 CPU 的**多核性能**，并能够处理**更多的请求**。

从上面的部署概念列表来看，使用worker主要有助于**复制**部分，并对**重新启动**有一点帮助，但您仍然需要照顾其他部分：

* **安全 - HTTPS**
* **启动时运行**
* ***重新启动***
* 复制（运行的进程数）
* **内存**
* **启动之前的先前步骤**

## 容器和 Docker { #containers-and-docker }

在关于 [容器中的 FastAPI - Docker](docker.md) 的下一章中，我将介绍一些可用于处理其他**部署概念**的策略。

我将向您展示如何**从零开始构建自己的镜像**，以运行一个单独的 Uvicorn 进程。这个过程相对简单，并且在使用 **Kubernetes** 等分布式容器管理系统时，这通常是您需要采取的方法。

## 回顾 { #recap }

您可以在使用 `fastapi` 或 `uvicorn` 命令时，通过 `--workers` CLI 选项启用多个工作进程（workers），以充分利用**多核 CPU**，以**并行运行多个进程**。

如果您要设置**自己的部署系统**，同时自己处理其他部署概念，则可以使用这些工具和想法。

请查看下一章，了解带有容器（例如 Docker 和 Kubernetes）的 **FastAPI**。 您将看到这些工具也有简单的方法来解决其他**部署概念**。 ✨



---

# Source: docs/deployment/versions.md


# 关于 FastAPI 版本 { #about-fastapi-versions }

**FastAPI** 已在许多应用程序和系统的生产环境中使用。 并且测试覆盖率保持在100%。 但其开发进度仍在快速推进。

经常添加新功能，定期修复错误，并且代码仍在持续改进。

这就是为什么当前版本仍然是`0.x.x`，这反映出每个版本都可能有Breaking changes。 这遵循[语义版本控制](https://semver.org/)的约定。

你现在就可以使用 **FastAPI** 创建生产环境应用程序（你可能已经这样做了一段时间），你只需确保使用的版本可以与其余代码正确配合即可。

## 固定你的 `fastapi` 版本 { #pin-your-fastapi-version }

你应该做的第一件事是将你正在使用的 **FastAPI** 版本“固定”到你知道适用于你的应用程序的特定最新版本。

例如，假设你在应用程序中使用版本`0.112.0`。

如果你使用`requirements.txt`文件，你可以使用以下命令指定版本：

```txt
fastapi[standard]==0.112.0
```

这意味着你将使用版本`0.112.0`。

或者你也可以将其固定为：

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

这意味着你将使用`0.112.0`或更高版本，但低于`0.113.0`，例如，版本`0.112.2`仍会被接受。

如果你使用任何其他工具来管理你的安装，例如 `uv`、Poetry、Pipenv 或其他工具，它们都有一种定义包的特定版本的方法。

## 可用版本 { #available-versions }

你可以在[发行说明](../release-notes.md)中查看可用版本（例如查看当前最新版本）。

## 关于版本 { #about-versions }

遵循语义版本控制约定，任何低于`1.0.0`的版本都可能会添加 breaking changes。

FastAPI 还遵循这样的约定：任何"PATCH"版本更改都是为了bug修复和non-breaking changes。

/// tip | 提示

"PATCH"是最后一个数字，例如，在`0.2.3`中，PATCH版本是`3`。

///

因此，你应该能够固定到如下版本：

```txt
fastapi>=0.45.0,<0.46.0
```

"MINOR"版本中会添加breaking changes和新功能。

/// tip | 提示

"MINOR"是中间的数字，例如，在`0.2.3`中，MINOR版本是`2`。

///

## 升级FastAPI版本 { #upgrading-the-fastapi-versions }

你应该为你的应用程序添加测试。

使用 **FastAPI** 编写测试非常简单（感谢 Starlette），请参考文档：[测试](../tutorial/testing.md)

添加测试后，你可以将 **FastAPI** 版本升级到更新版本，并通过运行测试来确保所有代码都能正常工作。

如果一切正常，或者在进行必要的更改之后，并且所有测试都通过了，那么你可以将`fastapi`固定到新的版本。

## 关于Starlette { #about-starlette }

你不应该固定`starlette`的版本。

不同版本的 **FastAPI** 将使用特定的较新版本的 Starlette。

因此，**FastAPI** 自己可以使用正确的 Starlette 版本。

## 关于 Pydantic { #about-pydantic }

Pydantic 包含针对 **FastAPI** 的测试及其自己的测试，因此 Pydantic 的新版本（`1.0.0`以上）始终与 FastAPI 兼容。

你可以将 Pydantic 固定到任何高于 `1.0.0` 且适合你的版本。

例如：

```txt
pydantic>=2.7.0,<3.0.0
```



---

# Source: docs/editor-support.md


# 编辑器支持 { #editor-support }

官方的 [FastAPI 扩展](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode)为你的 FastAPI 开发流程带来增强，包括*路径操作*的发现与导航、部署到 FastAPI Cloud，以及实时日志流式传输。

有关该扩展的更多详情，请参阅其 [GitHub 仓库](https://github.com/fastapi/fastapi-vscode)中的 README。

## 安装与配置 { #setup-and-installation }

**FastAPI 扩展**同时适用于 [VS Code](https://code.visualstudio.com/) 和 [Cursor](https://www.cursor.com/)。你可以在各编辑器的扩展面板中直接搜索 “FastAPI”，并选择由 **FastAPI Labs** 发布的扩展进行安装。该扩展也适用于基于浏览器的编辑器，例如 [vscode.dev](https://vscode.dev) 和 [github.dev](https://github.dev)。

### 应用发现 { #application-discovery }

默认情况下，扩展会通过扫描实例化了 `FastAPI()` 的文件，自动发现工作区中的 FastAPI 应用。如果你的项目结构无法自动检测，你可以通过 `pyproject.toml` 中的 `[tool.fastapi]` 或 VS Code 设置项 `fastapi.entryPoint` 来指定入口点，使用模块表示法（例如 `myapp.main:app`）。

## 功能 { #features }

- **Path Operation 资源管理器** - 侧边栏树状视图展示应用中的所有 <dfn title="路由，端点">*路径操作*</dfn>。点击可跳转至任一路由或 router 的定义。
- **路由搜索** - 使用 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>（macOS 上为 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>）按路径、方法或名称进行搜索。
- **CodeLens 导航** - 测试客户端调用（例如 `client.get('/items')`）上方的可点击链接，可跳转到匹配的*路径操作*，在测试与实现之间快速往返。
- **部署到 FastAPI Cloud** - 一键将你的应用部署到 [FastAPI Cloud](https://fastapicloud.com/)。
- **应用日志流式传输** - 从部署在 FastAPI Cloud 的应用中实时流式获取日志，并支持按级别过滤与文本搜索。

如果你想先熟悉扩展功能，可以打开命令面板（<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>，macOS 上为 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>），选择 “Welcome: Open walkthrough...”，然后选择 “Get started with FastAPI” 演练。



---

# Source: docs/environment-variables.md


# 环境变量 { #environment-variables }


/// tip | 提示

如果你已经知道什么是“环境变量”并且知道如何使用它们，你可以放心跳过这一部分。

///

环境变量（也称为“**env var**”）是一个独立于 Python 代码**之外**的变量，它存在于**操作系统**中，可以被你的 Python 代码（或其他程序）读取。

环境变量对于处理应用程序**设置**、作为 Python **安装**的一部分等方面非常有用。

## 创建和使用环境变量 { #create-and-use-env-vars }

你在 **shell（终端）**中就可以**创建**和使用环境变量，并不需要用到 Python：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 你可以使用以下命令创建一个名为 MY_NAME 的环境变量
$ export MY_NAME="Wade Wilson"

// 然后，你可以在其他程序中使用它，例如
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 创建一个名为 MY_NAME 的环境变量
$ $Env:MY_NAME = "Wade Wilson"

// 在其他程序中使用它，例如
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## 在 Python 中读取环境变量 { #read-env-vars-in-python }

你也可以在 Python **之外**的终端中创建环境变量（或使用任何其他方法），然后在 Python 中**读取**它们。

例如，你可以创建一个名为 `main.py` 的文件，其中包含以下内容：

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | 提示

第二个参数是 [`os.getenv()`](https://docs.python.org/3.8/library/os.html#os.getenv) 的默认返回值。

如果没有提供，默认值为 `None`，这里我们提供 `"World"` 作为默认值。

///

然后你可以调用这个 Python 程序：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 这里我们还没有设置环境变量
$ python main.py

// 因为我们没有设置环境变量，所以我们得到的是默认值

Hello World from Python

// 但是如果我们事先创建过一个环境变量
$ export MY_NAME="Wade Wilson"

// 然后再次调用程序
$ python main.py

// 现在就可以读取到环境变量了

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 这里我们还没有设置环境变量
$ python main.py

// 因为我们没有设置环境变量，所以我们得到的是默认值

Hello World from Python

// 但是如果我们事先创建过一个环境变量
$ $Env:MY_NAME = "Wade Wilson"

// 然后再次调用程序
$ python main.py

// 现在就可以读取到环境变量了

Hello Wade Wilson from Python
```

</div>

////

由于环境变量可以在代码之外设置、但可以被代码读取，并且不必与其他文件一起存储（提交到 `git`），因此通常用于配置或**设置**。

你还可以为**特定的程序调用**创建特定的环境变量，该环境变量仅对该程序可用，且仅在其运行期间有效。

要实现这一点，只需在同一行内、程序本身之前创建它：

<div class="termy">

```console
// 在这个程序调用的同一行中创建一个名为 MY_NAME 的环境变量
$ MY_NAME="Wade Wilson" python main.py

// 现在就可以读取到环境变量了

Hello Wade Wilson from Python

// 在此之后这个环境变量将不会依然存在
$ python main.py

Hello World from Python
```

</div>

/// tip | 提示

你可以在 [The Twelve-Factor App: 配置](https://12factor.net/config) 中了解更多信息。

///

## 类型和验证 { #types-and-validation }

这些环境变量只能处理**文本字符串**，因为它们是处于 Python 范畴之外的，必须与其他程序和操作系统的其余部分兼容（甚至与不同的操作系统兼容，如 Linux、Windows、macOS）。

这意味着从环境变量中读取的**任何值**在 Python 中都将是一个 `str`，任何类型转换或验证都必须在代码中完成。

你将在[高级用户指南 - 设置和环境变量](./advanced/settings.md)中了解更多关于使用环境变量处理**应用程序设置**的信息。

## `PATH` 环境变量 { #path-environment-variable }

有一个**特殊的**环境变量称为 **`PATH`**，操作系统（Linux、macOS、Windows）用它来查找要运行的程序。

`PATH` 变量的值是一个长字符串，由 Linux 和 macOS 上的冒号 `:` 分隔的目录组成，而在 Windows 上则是由分号 `;` 分隔的。

例如，`PATH` 环境变量可能如下所示：

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

这意味着系统应该在以下目录中查找程序：

-   `/usr/local/bin`
-   `/usr/bin`
-   `/bin`
-   `/usr/sbin`
-   `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

这意味着系统应该在以下目录中查找程序：

-   `C:\Program Files\Python312\Scripts`
-   `C:\Program Files\Python312`
-   `C:\Windows\System32`

////

当你在终端中输入一个**命令**时，操作系统会在 `PATH` 环境变量中列出的**每个目录**中**查找**程序。

例如，当你在终端中输入 `python` 时，操作系统会在该列表中的**第一个目录**中查找名为 `python` 的程序。

如果找到了，那么操作系统将**使用它**；否则，操作系统会继续在**其他目录**中查找。

### 安装 Python 和更新 `PATH` { #installing-python-and-updating-the-path }

安装 Python 时，可能会询问你是否要更新 `PATH` 环境变量。

//// tab | Linux, macOS

假设你安装 Python 并最终将其安装在了目录 `/opt/custompython/bin` 中。

如果你同意更新 `PATH` 环境变量，那么安装程序将会将 `/opt/custompython/bin` 添加到 `PATH` 环境变量中。

它看起来大概会像这样：

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

如此一来，当你在终端中输入 `python` 时，系统会在 `/opt/custompython/bin` 中找到 Python 程序（最后一个目录）并使用它。

////

//// tab | Windows

假设你安装 Python 并最终将其安装在了目录 `C:\opt\custompython\bin` 中。

如果你同意更新 `PATH` 环境变量，那么安装程序将会将 `C:\opt\custompython\bin` 添加到 `PATH` 环境变量中。

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

如此一来，当你在终端中输入 `python` 时，系统会在 `C:\opt\custompython\bin` 中找到 Python 程序（最后一个目录）并使用它。

////

因此，如果你输入：

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

系统会在 `/opt/custompython/bin` 中**找到** `python` 程序并运行它。

这和输入以下命令大致等价：

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

系统会在 `C:\opt\custompython\bin\python` 中**找到** `python` 程序并运行它。

这和输入以下命令大致等价：

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

当学习[虚拟环境](virtual-environments.md)时，这些信息将会很有用。

## 结论 { #conclusion }

通过这个教程，你应该对**环境变量**是什么以及如何在 Python 中使用它们有了基本的了解。

你也可以在[环境变量 - 维基百科](https://en.wikipedia.org/wiki/Environment_variable)中了解更多关于它们的信息。

在许多情况下，环境变量的用途和适用性并不是很明显。但是在开发过程中，它们会在许多不同的场景中出现，因此了解它们是很有必要的。

例如，你将在下一节关于[虚拟环境](virtual-environments.md)中需要这些信息。



---

# Source: docs/fastapi-cli.md


# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - 命令行接口">CLI</abbr>** 是一个命令行程序，你可以用它来部署和运行你的 FastAPI 应用、管理 FastAPI 项目，等等。

当你安装 FastAPI（例如使用 `pip install "fastapi[standard]"`）时，会附带一个可以在终端中运行的命令行程序。

要在开发环境中运行你的 FastAPI 应用，可以使用 `fastapi dev` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | 提示

在生产环境中，你会使用 `fastapi run` 而不是 `fastapi dev`。🚀

///

在内部，**FastAPI CLI** 使用 [Uvicorn](https://www.uvicorn.dev)，这是一个高性能、适用于生产环境的 ASGI 服务器。😎

`fastapi` CLI 会尝试自动检测要运行的 FastAPI 应用，默认假设它是文件 `main.py` 中名为 `app` 的对象（或少数其他变体）。

但你也可以显式配置要使用的应用。

## 在 `pyproject.toml` 中配置应用的 `entrypoint` { #configure-the-app-entrypoint-in-pyproject-toml }

你可以在 `pyproject.toml` 文件中配置应用的位置，例如：

```toml
[tool.fastapi]
entrypoint = "main:app"
```

这个 `entrypoint` 会告诉 `fastapi` 命令按如下方式导入应用：

```python
from main import app
```

如果你的代码结构如下：

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

那么你可以将 `entrypoint` 设置为：

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

这等价于：

```python
from backend.main import app
```

### 带路径或使用 `--entrypoint` CLI 选项的 `fastapi dev` { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

你也可以把文件路径传给 `fastapi dev` 命令，它会猜测要使用的 FastAPI 应用对象：

```console
$ fastapi dev main.py
```

或者，你也可以给 `fastapi dev` 命令传入 `--entrypoint` 选项：

```console
$ fastapi dev --entrypoint main:app
```

但每次运行 `fastapi` 命令都需要记得传入正确的路径或 entrypoint。

另外，其他工具可能找不到它，例如 [VS Code 扩展](editor-support.md) 或 [FastAPI Cloud](https://fastapicloud.com)，因此推荐在 `pyproject.toml` 中使用 `entrypoint`。

## `fastapi dev` { #fastapi-dev }

当你运行 `fastapi dev` 时，它将以开发模式运行。

默认情况下，它会启用**自动重载**，因此当你更改代码时，它会自动重新加载服务器。该功能是资源密集型的，且相较不启用时更不稳定，因此你应该仅在开发环境下使用它。它还会监听 IP 地址 `127.0.0.1`，这是你的机器仅与自身通信的 IP（`localhost`）。

## `fastapi run` { #fastapi-run }

当你运行 `fastapi run` 时，它默认以生产环境模式运行。

默认情况下，**自动重载是禁用的**。它将监听 IP 地址 `0.0.0.0`，即所有可用的 IP 地址，这样任何能够与该机器通信的人都可以公开访问它。这通常是你在生产环境中运行它的方式，例如在容器中运行。

在大多数情况下，你会（且应该）有一个“终止代理”在上层为你处理 HTTPS，这取决于你如何部署应用程序，你的服务提供商可能会为你处理此事，或者你可能需要自己设置。

/// tip | 提示

你可以在[部署文档](deployment/index.md)中了解更多。

///



---

# Source: docs/features.md


# 特性 { #features }

## FastAPI 特性 { #fastapi-features }

**FastAPI** 提供了以下内容：

### 基于开放标准 { #based-on-open-standards }

* [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification) 用于创建 API，包含对<dfn title="也称为：端点、路由">路径</dfn> <dfn title="也称为 HTTP 方法，如 POST、GET、PUT、DELETE">操作</dfn>、参数、请求体、安全等的声明。
* 使用 [**JSON Schema**](https://json-schema.org/) 自动生成数据模型文档（因为 OpenAPI 本身就是基于 JSON Schema 的）。
* 经过了缜密的研究后围绕这些标准而设计。并非狗尾续貂。
* 这也允许了在很多语言中自动**生成客户端代码**。

### 自动生成文档 { #automatic-docs }

交互式 API 文档以及具探索性 web 界面。因为该框架是基于 OpenAPI，所以有很多可选项，FastAPI 默认自带两个交互式 API 文档。

* [**Swagger UI**](https://github.com/swagger-api/swagger-ui)，可交互式操作，能在浏览器中直接调用和测试你的 API。

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 另外的 API 文档：[**ReDoc**](https://github.com/Rebilly/ReDoc)。

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 就是现代 Python { #just-modern-python }

全部都基于标准的 **Python 类型** 声明（感谢 Pydantic）。没有新的语法需要学习。只需要标准的现代 Python。

如果你需要2分钟来学习如何使用 Python 类型（即使你不使用 FastAPI），看看这个简短的教程：[Python 类型](python-types.md)。

编写带有类型标注的标准 Python：

```Python
from datetime import date

from pydantic import BaseModel

# 将变量声明为 str
# 并在函数内获得编辑器支持
def main(user_id: str):
    return user_id


# 一个 Pydantic 模型
class User(BaseModel):
    id: int
    name: str
    joined: date
```

可以像这样来使用：

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```


/// note | 注意

`**second_user_data` 意思是：

直接将 `second_user_data` 字典的键和值作为 key-value 参数传入，等同于：`User(id=4, name="Mary", joined="2018-11-30")`

///

### 编辑器支持 { #editor-support }

整个框架都被设计得易于使用且直观，所有的决定都在开发之前就在多个编辑器上进行了测试，来确保最佳的开发体验。

在 Python 开发者调查中，我们能看到[被使用最多的功能之一是“自动补全”](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features)。

整个 **FastAPI** 框架就是基于这一点的。任何地方都可以进行自动补全。

你几乎不需要经常回来看文档。

在这里，你的编辑器可能会这样帮助你：

* 在 [Visual Studio Code](https://code.visualstudio.com/) 中:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* 在 [PyCharm](https://www.jetbrains.com/pycharm/) 中:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

你将能进行代码补全，这是在之前你可能曾认为不可能的事。例如，在来自请求 JSON 体（可能是嵌套的）中的键 `price`。

不会再输错键名，来回翻看文档，或者来回滚动寻找你最后使用的 `username` 或者 `user_name`。

### 简洁 { #short }

任何类型都有合理的**默认值**，任何地方都有可选配置。所有的参数被微调，来满足你的需求，定义成你需要的 API。

但是默认情况下，一切都能**“顺利工作”**。

### 验证 { #validation }

* 校验大部分（甚至所有？）的 Python **数据类型**，包括：
    * JSON 对象 (`dict`)。
    * JSON 数组 (`list`) 定义成员类型。
    * 字符串 (`str`) 字段，定义最小或最大长度。
    * 数字 (`int`, `float`) 有最大值和最小值，等等。

* 校验更特殊的类型，比如：
    * URL。
    * Email。
    * UUID。
    * ...及其他。

所有的校验都由完善且强大的 **Pydantic** 处理。

### 安全性及身份验证 { #security-and-authentication }

集成了安全性和身份验证。不需要在数据库或数据模型上作出任何妥协。

OpenAPI 中定义的所有安全模式，包括：

* HTTP 基本认证。
* **OAuth2**（也使用 **JWT tokens**）。在 [使用 JWT 的 OAuth2](tutorial/security/oauth2-jwt.md) 查看教程。
* API 密钥，在:
    * 请求头。
    * 查询参数。
    * Cookies，等等。

加上来自 Starlette（包括 **session cookies**）的所有安全特性。

所有的这些都是可复用的工具和组件，可以轻松与你的系统，数据仓库，关系型以及 NoSQL 数据库等等集成。

### 依赖注入 { #dependency-injection }

FastAPI 有一个使用非常简单，但是非常强大的<dfn title='也称为 "components"、"resources"、"services"、"providers"'><strong>依赖注入</strong></dfn>系统。

* 甚至依赖也可以有依赖，创建一个层级或者**“图”依赖**。
* 所有**自动化处理**都由框架完成。
* 所有的依赖关系都可以从请求中获取数据，并且**增加了路径操作**约束和自动文档生成。
* 即使是在依赖项中定义的*路径操作*参数也会**自动验证**。
* 支持复杂的用户身份认证系统，**数据库连接**等等。
* **不依赖**数据库，前端等。但是和它们集成很简单。

### 无限制的“插件” { #unlimited-plug-ins }

或者说，导入并使用你需要的代码，而不需要它们。

任何集成都被设计得被易于使用（用依赖关系），你可以用和*路径操作*相同的结构和语法，在两行代码中为你的应用创建一个“插件”。

### 测试 { #tested }

* 100% <dfn title="自动测试的代码量">测试覆盖</dfn>。
* 代码库100% <dfn title="Python 类型注解，有了这个你的编辑器和外部工具可以给你更好的支持">类型标注</dfn>。
* 用于生产应用。

## Starlette 特性 { #starlette-features }

**FastAPI** 与 [**Starlette**](https://www.starlette.dev/) 完全兼容（并基于它构建）。所以，你有的其他的 Starlette 代码也能正常工作。

`FastAPI` 实际上是 `Starlette` 的一个子类。所以，如果你已经知道或者使用 Starlette，大部分的功能会以相同的方式工作。

通过 **FastAPI** 你可以获得所有 **Starlette** 的特性（FastAPI 就像加强版的 Starlette）：

* 令人惊叹的性能。它是[Python 可用的最快的框架之一，和 **NodeJS** 及 **Go** 相当](https://github.com/encode/starlette#performance)。
* **支持 WebSocket**。
* 进程内后台任务。
* Startup 和 shutdown 事件。
* 测试客户端基于 HTTPX。
* **CORS**、GZip、静态文件、流响应。
* 支持 **Session 和 Cookie**。
* 100% 测试覆盖率。
* 代码库 100% 类型标注。

## Pydantic 特性 { #pydantic-features }

**FastAPI** 与 [**Pydantic**](https://docs.pydantic.dev/) 完全兼容（并基于它构建）。所以，你有的其他的 Pydantic 代码也能正常工作。

兼容包括基于 Pydantic 的外部库，例如用于数据库的 <abbr title="Object-Relational Mapper - 对象关系映射">ORM</abbr>s、<abbr title="Object-Document Mapper - 对象文档映射">ODM</abbr>s。

这也意味着在很多情况下，你可以将从请求中获得的相同对象**直接传到数据库**，因为所有的验证都是自动的。

反之亦然，在很多情况下，你也可以将从数据库中获取的对象**直接传到客户端**。

通过 **FastAPI** 你可以获得所有 **Pydantic**（FastAPI 基于 Pydantic 做了所有的数据处理）：

* **不烧脑**：
    * 没有新的模式定义 micro-language 需要学习。
    * 如果你知道 Python 类型，你就知道如何使用 Pydantic。
* 和你 **<abbr title="Integrated Development Environment - 集成开发环境: 类似于代码编辑器">IDE</abbr>/<dfn title="一个检查代码错误的程序">linter</dfn>/brain** 适配:
    * 因为 pydantic 数据结构仅仅是你定义的类的实例；自动补全，linting，mypy 以及你的直觉应该可以和你验证的数据一起正常工作。
* 验证**复杂结构**:
    * 使用分层的 Pydantic 模型，Python `typing` 的 `List` 和 `Dict` 等等。
    * 验证器使我们能够简单清楚地将复杂的数据模式定义、检查并记录为 JSON Schema。
    * 你可以拥有深度**嵌套的 JSON** 对象并对它们进行验证和注释。
* **可扩展**:
    * Pydantic 允许定义自定义数据类型或者你可以用验证器装饰器对被装饰的模型上的方法扩展验证。
* 100% 测试覆盖率。



---

# Source: docs/help-fastapi.md


# 帮助 { #help }

你想帮助 FastAPI，或获取 FastAPI 的帮助吗？

有很多非常简单的方式可以帮忙并获得帮助。

## 订阅新闻邮件 { #subscribe-to-the-newsletter }

你可以订阅（不频繁的）[**FastAPI and friends** 新闻邮件](newsletter.md)，获取如下更新：

* FastAPI 及其小伙伴的新闻 🚀
* 指南 📝
* 功能 ✨
* 破坏性更改 🚨
* 使用技巧 ✅

## 在线关注 FastAPI { #follow-fastapi-online }

你可以在以下平台关注 **FastAPI**：

* [**X / Twitter** 上的 @fastapi](https://x.com/fastapi)
* [**Bluesky** 上的 @fastapi.tiangolo.com](https://bsky.app/profile/fastapi.tiangolo.com)
* [**LinkedIn** 上的 FastAPI](https://www.linkedin.com/company/fastapi/)

## 在 GitHub 上为 **FastAPI** 加星 { #star-fastapi-in-github }

你可以在 GitHub 上为 FastAPI 点亮「星标」（点击右上角的星形按钮）：[https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)。⭐️

加星后，其他用户更容易发现它，并看到它已经对其他人有帮助。

## 关注 GitHub 资源库的版本发布 { #watch-the-github-repository-for-releases }

你可以在 GitHub 上「关注」FastAPI（点击右上角的「watch」按钮）：[https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)。👀

在那里你可以选择「Releases only」。

这样做之后，每当 **FastAPI** 发布包含 Bug 修复和新功能的新版本时，你都会收到通知（邮件）。

## 关注作者 { #follow-the-author }

你可以关注[我（Sebastián Ramírez / `tiangolo`）](https://tiangolo.com)，作者本人，在以下平台，获取我发布的关于 FastAPI 及其小伙伴的消息：

* [@tiangolo 在 **GitHub** 上](https://github.com/tiangolo)。
* [@tiangolo 在 **X (Twitter)** 上](https://x.com/tiangolo)
* [@tiangolo.com 在 **Bluesky** 上](https://bsky.app/profile/tiangolo.com)
* [@tiangolo 在 **LinkedIn** 上](https://www.linkedin.com/in/tiangolo/)。

## 在 GitHub 上帮别人解答问题 { #help-others-with-questions-in-github }

你可以尝试在 [GitHub Discussions](https://github.com/fastapi/fastapi/discussions/categories/questions?discussions_q=category%3AQuestions+is%3Aunanswered) 中帮助他人解答问题。

很多情况下，你也许已经知道这些问题的答案了。🤓

如果你帮助了很多人解答问题，你会成为官方的 [FastAPI 专家](fastapi-people.md#fastapi-experts)。🎉

只要记住，最重要的是：尽量友善。🤗

### 如何提供帮助 { #how-to-help }

请参照这里的[帮助指南](https://tiangolo.com/open-source/help/#help-others-with-questions-in-github)。

## 提问 { #ask-questions }

你可以在 GitHub 资源库中[创建一个新问题（Question）](https://github.com/fastapi/fastapi/discussions/new?category=questions)，例如：

* 提出一个**问题**或关于某个**问题**的求助。
* 建议一个新的**功能**。

## 加入聊天 { #join-the-chat }

加入 👥 [Discord 聊天服务器](https://discord.gg/VQjSZaeJmf) 👥，和 FastAPI 社区的小伙伴们一起交流。

/// tip | 提示

关于问题，请在 GitHub Discussions 中提问，这样更有机会得到帮助。

聊天仅用于其他日常交流。

///

### 别在聊天里提问 { #dont-use-the-chat-for-questions }

请记住，聊天更偏向“自由交流”，很容易提出过于笼统、难以回答的问题，因此你可能收不到解答。

在 GitHub 中，模板会引导你写出恰当的问题，从而更容易获得好的回答，甚至在提问之前就能自己解决。

聊天系统中的对话也不像 GitHub 那样容易搜索，它们会淹没消失。



---

# Source: docs/history-design-future.md


# 历史、设计、未来 { #history-design-and-future }

不久前，[曾有 **FastAPI** 用户问过](https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920)：

> 这个项目有怎样的历史？好像它只用了几周就从默默无闻变得众所周知...

在此，我们简单回顾一下 **FastAPI** 的历史。

## 备选方案 { #alternatives }

有那么几年，我曾领导数个开发团队为诸多复杂需求创建各种 API，这些需求包括机器学习、分布系统、异步任务、NoSQL 数据库等领域。

作为工作的一部分，我需要调研很多备选方案、还要测试并且使用这些备选方案。

**FastAPI** 其实只是延续了这些前辈的历史。

正如[备选方案](alternatives.md)一章所述：

<blockquote markdown="1">
没有大家之前所做的工作，**FastAPI** 就不会存在。

以前创建的这些工具为它的出现提供了灵感。

在那几年中，我一直回避创建新的框架。首先，我尝试使用各种框架、插件、工具解决 **FastAPI** 现在的功能。

但到了一定程度之后，我别无选择，只能从之前的工具中汲取最优思路，并以尽量好的方式把这些思路整合在一起，使用之前甚至是不支持的语言特性（Python 3.6+ 的类型提示），从而创建一个能满足我所有需求的框架。
</blockquote>

## 调研 { #investigation }

通过使用之前所有的备选方案，我有机会从它们之中学到了很多东西，获取了很多想法，并以我和我的开发团队能想到的最好方式把这些思路整合成一体。

例如，大家都清楚，在理想状态下，它应该基于标准的 Python 类型提示。

而且，最好的方式是使用现有的标准。

因此，甚至在开发 **FastAPI** 前，我就花了几个月的时间研究 OpenAPI、JSON Schema、OAuth2 等规范。深入理解它们之间的关系、重叠及区别之处。

## 设计 { #design }

然后，我又花了一些时间从用户角度（使用 FastAPI 的开发者）设计了开发者 **API**。

同时，我还在最流行的 Python 代码编辑器中测试了很多思路，包括 PyCharm、VS Code、基于 Jedi 的编辑器。

根据最新 [Python 开发者调研报告](https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools)显示，这几种编辑器覆盖了约 80% 的用户。

也就是说，**FastAPI** 针对差不多 80% 的 Python 开发者使用的编辑器进行了测试，而且其它大多数编辑器的工作方式也与之类似，因此，**FastAPI** 的优势几乎能在所有编辑器上体现。

通过这种方式，我就能找到尽可能减少代码重复的最佳方式，进而实现处处都有自动补全、类型提示与错误检查等支持。

所有这些都是为了给开发者提供最佳的开发体验。

## 需求项 { #requirements }

经过测试多种备选方案，我最终决定使用 [**Pydantic**](https://docs.pydantic.dev/)，并充分利用它的优势。

我甚至为它做了不少贡献，让它完美兼容了 JSON Schema，支持多种方式定义约束声明，并基于多个编辑器，改进了它对编辑器支持（类型检查、自动补全）。

在开发期间，我还为 [**Starlette**](https://www.starlette.dev/) 做了不少贡献，这是另一个关键需求项。

## 开发 { #development }

当我启动 **FastAPI** 开发的时候，绝大多数部件都已经就位，设计已经定义，需求项和工具也已经准备就绪，相关标准与规范的知识储备也非常清晰而新鲜。

## 未来 { #future }

至此，**FastAPI** 及其理念已经为很多人所用。

对于很多用例，它比以前很多备选方案都更适用。

很多开发者和开发团队已经依赖 **FastAPI** 开发他们的项目（包括我和我的团队）。

但，**FastAPI** 仍有很多改进的余地，也还需要添加更多的功能。

**FastAPI** 前景光明。

在此，我们衷心感谢[你的帮助](help-fastapi.md)。



---

# Source: docs/how-to/authentication-error-status-code.md


# 使用旧的 403 认证错误状态码 { #use-old-403-authentication-error-status-codes }

在 FastAPI `0.122.0` 版本之前，当内置的安全工具在认证失败后向客户端返回错误时，会使用 HTTP 状态码 `403 Forbidden`。

从 FastAPI `0.122.0` 版本开始，它们改用更合适的 HTTP 状态码 `401 Unauthorized`，并在响应中返回合理的 `WWW-Authenticate` 头，遵循 HTTP 规范，[RFC 7235](https://datatracker.ietf.org/doc/html/rfc7235#section-3.1)、[RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized)。

但如果由于某些原因你的客户端依赖旧行为，你可以在你的安全类中重写方法 `make_not_authenticated_error` 来回退到旧行为。

例如，你可以创建一个 `HTTPBearer` 的子类，使其返回 `403 Forbidden` 错误，而不是默认的 `401 Unauthorized` 错误：

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | 提示

注意该函数返回的是异常实例，而不是直接抛出它。抛出操作由其余的内部代码完成。

///



---

# Source: docs/how-to/conditional-openapi.md


# 按条件配置 OpenAPI { #conditional-openapi }

如果需要，你可以使用设置和环境变量，按环境有条件地配置 OpenAPI，甚至完全禁用它。

## 关于安全、API 和文档 { #about-security-apis-and-docs }

在生产环境隐藏文档界面并不应该成为保护 API 的方式。

这并不会给你的 API 增加任何额外的安全性，*路径操作* 仍然会在原来的位置可用。

如果你的代码里有安全漏洞，它仍然存在。

隐藏文档只会让理解如何与 API 交互变得更困难，也可能让你在生产环境中调试更困难。这大体上可以被视为一种 [通过隐藏实现安全](https://en.wikipedia.org/wiki/Security_through_obscurity) 的做法。

如果你想保护你的 API，有很多更好的措施，例如：

- 确保为请求体和响应定义完善的 Pydantic 模型。
- 使用依赖配置所需的权限和角色。
- 绝不要存储明文密码，只存储密码哈希。
- 实现并使用成熟的密码学工具，比如 pwdlib 和 JWT 令牌等。
- 在需要的地方使用 OAuth2 作用域添加更细粒度的权限控制。
- ...等。

尽管如此，你可能确实有非常特定的用例，需要在某些环境（例如生产环境）禁用 API 文档，或根据环境变量的配置来决定。

## 基于设置和环境变量的条件式 OpenAPI { #conditional-openapi-from-settings-and-env-vars }

你可以很容易地使用相同的 Pydantic 设置来配置生成的 OpenAPI 和文档 UI。

例如：

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

这里我们声明了设置项 `openapi_url`，其默认值同样是 `"/openapi.json"`。

然后在创建 `FastAPI` 应用时使用它。

接着，你可以通过把环境变量 `OPENAPI_URL` 设为空字符串来禁用 OpenAPI（包括文档 UI），例如：

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后如果你访问 `/openapi.json`、`/docs` 或 `/redoc`，就会得到一个 `404 Not Found` 错误，例如：

```JSON
{
    "detail": "Not Found"
}
```



---

# Source: docs/how-to/configure-swagger-ui.md


# 配置 Swagger UI { #configure-swagger-ui }

你可以配置一些额外的 [Swagger UI 参数](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)。

如果需要配置它们，可以在创建 `FastAPI()` 应用对象时或调用 `get_swagger_ui_html()` 函数时传递 `swagger_ui_parameters` 参数。

`swagger_ui_parameters` 接受一个字典，该字典会直接传递给 Swagger UI。

FastAPI会将这些配置转换为 **JSON**，使其与 JavaScript 兼容，因为这是 Swagger UI 需要的。

## 禁用语法高亮 { #disable-syntax-highlighting }

比如，你可以禁用 Swagger UI 中的语法高亮。

当没有改变设置时，语法高亮默认启用：

<img src="/img/tutorial/extending-openapi/image02.png">

但是你可以通过设置 `syntaxHighlight` 为 `False` 来禁用它：

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...在此之后，Swagger UI 将不再显示语法高亮：

<img src="/img/tutorial/extending-openapi/image03.png">

## 改变主题 { #change-the-theme }

同样地，你也可以通过设置键 `"syntaxHighlight.theme"` 来设置语法高亮主题（注意中间有一个点）：

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

这个配置会改变语法高亮颜色主题：

<img src="/img/tutorial/extending-openapi/image04.png">

## 改变默认 Swagger UI 参数 { #change-default-swagger-ui-parameters }

FastAPI 包含了一些默认配置参数，适用于大多数用例。

其包括这些默认配置参数：

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

你可以通过在 `swagger_ui_parameters` 中设置不同的值来覆盖它们。

比如，如果要禁用 `deepLinking`，你可以像这样传递设置到 `swagger_ui_parameters` 中：

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## 其他 Swagger UI 参数 { #other-swagger-ui-parameters }

查看所有其他可用的配置，请阅读官方的 [Swagger UI 参数文档](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)。

## JavaScript-only 配置 { #javascript-only-settings }

Swagger UI 同样允许使用 **JavaScript-only** 配置对象（例如，JavaScript 函数）。

FastAPI 包含这些 JavaScript-only 的 `presets` 设置：

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

这些是 **JavaScript** 对象，而不是字符串，所以你不能直接从 Python 代码中传递它们。

如果你需要像这样使用 JavaScript-only 配置，你可以使用上述方法之一。覆盖所有 Swagger UI *路径操作* 并手动编写任何你需要的 JavaScript。



---

# Source: docs/how-to/custom-docs-ui-assets.md


# 自托管自定义文档 UI 静态资源 { #custom-docs-ui-static-assets-self-hosting }

API 文档使用 Swagger UI 和 ReDoc，它们各自需要一些 JavaScript 和 CSS 文件。

默认情况下，这些文件从一个 <abbr title="Content Delivery Network - 内容分发网络: 一种服务，通常由多台服务器组成，用于提供静态文件，如 JavaScript 和 CSS。它常用于从更接近客户端的服务器提供这些文件，从而提升性能。">CDN</abbr> 提供。

不过你可以自定义：可以指定特定的 CDN，或自行提供这些文件。

## 为 JavaScript 和 CSS 自定义 CDN { #custom-cdn-for-javascript-and-css }

假设你想使用不同的 <abbr title="Content Delivery Network - 内容分发网络">CDN</abbr>，例如使用 `https://unpkg.com/`。

如果你所在的国家/地区屏蔽了某些 URL，这会很有用。

### 关闭自动文档 { #disable-the-automatic-docs }

第一步是关闭自动文档，因为默认它们会使用默认的 CDN。

要关闭它们，在创建 `FastAPI` 应用时将其 URL 设为 `None`：

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### 包含自定义文档 { #include-the-custom-docs }

现在你可以为自定义文档创建*路径操作*。

你可以复用 FastAPI 的内部函数来创建文档的 HTML 页面，并传入所需参数：

- `openapi_url`：文档 HTML 页面获取你的 API 的 OpenAPI 模式的 URL。这里可以使用 `app.openapi_url` 属性。
- `title`：你的 API 标题。
- `oauth2_redirect_url`：这里可以使用 `app.swagger_ui_oauth2_redirect_url` 来使用默认值。
- `swagger_js_url`：你的 Swagger UI 文档 HTML 获取**JavaScript** 文件的 URL。这里是自定义的 CDN URL。
- `swagger_css_url`：你的 Swagger UI 文档 HTML 获取**CSS** 文件的 URL。这里是自定义的 CDN URL。

ReDoc 也类似...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | 提示

`swagger_ui_redirect` 的*路径操作*是在你使用 OAuth2 时的一个辅助。

如果你把 API 与某个 OAuth2 提供方集成，你就可以完成认证并带着获取到的凭据回到 API 文档里。然后使用真实的 OAuth2 认证与之交互。

Swagger UI 会在幕后为你处理这些，但它需要这个“重定向”辅助路径。

///

### 创建一个路径操作进行测试 { #create-a-path-operation-to-test-it }

现在，为了测试一切是否正常，创建一个*路径操作*：

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### 测试 { #test-it }

现在，你应该可以访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)，并刷新页面，页面会从新的 CDN 加载这些资源。

## 为文档自托管 JavaScript 和 CSS { #self-hosting-javascript-and-css-for-docs }

如果你需要在离线、无法访问互联网或仅在局域网内时，应用仍能工作，那么自托管 JavaScript 和 CSS 会很有用。

这里你将看到如何在同一个 FastAPI 应用中自行提供这些文件，并配置文档使用它们。

### 项目文件结构 { #project-file-structure }

假设你的项目文件结构如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

现在创建一个目录来存放这些静态文件。

你的新文件结构可能如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### 下载文件 { #download-the-files }

下载文档需要的静态文件，并将它们放到 `static/` 目录中。

你通常可以右键点击每个链接，选择类似“将链接另存为...”的选项。

Swagger UI 使用以下文件：

- [`swagger-ui-bundle.js`](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js)
- [`swagger-ui.css`](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css)

而 ReDoc 使用以下文件：

- [`redoc.standalone.js`](https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js)

之后，你的文件结构可能如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### 提供静态文件 { #serve-the-static-files }

- 导入 `StaticFiles`。
- 在特定路径上“挂载”一个 `StaticFiles()` 实例。

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### 测试静态文件 { #test-the-static-files }

启动你的应用，并访问 [http://127.0.0.1:8000/static/redoc.standalone.js](http://127.0.0.1:8000/static/redoc.standalone.js)。

你应该会看到一个非常长的 **ReDoc** 的 JavaScript 文件。

它可能以如下内容开头：

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

这就确认了你的应用能够提供静态文件，并且你把文档所需的静态文件放在了正确的位置。

现在我们可以配置应用，让文档使用这些静态文件。

### 为静态文件关闭自动文档 { #disable-the-automatic-docs-for-static-files }

和使用自定义 CDN 一样，第一步是关闭自动文档，因为默认情况下它们会使用 CDN。

要关闭它们，在创建 `FastAPI` 应用时将其 URL 设为 `None`：

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### 为静态文件包含自定义文档 { #include-the-custom-docs-for-static-files }

同样地，现在你可以为自定义文档创建*路径操作*。

你可以再次复用 FastAPI 的内部函数来创建文档的 HTML 页面，并传入所需参数：

- `openapi_url`：文档 HTML 页面获取你的 API 的 OpenAPI 模式的 URL。这里可以使用 `app.openapi_url` 属性。
- `title`：你的 API 标题。
- `oauth2_redirect_url`：这里可以使用 `app.swagger_ui_oauth2_redirect_url` 来使用默认值。
- `swagger_js_url`：你的 Swagger UI 文档 HTML 获取**JavaScript** 文件的 URL。**这是现在由你的应用自己提供的那个**。
- `swagger_css_url`：你的 Swagger UI 文档 HTML 获取**CSS** 文件的 URL。**这是现在由你的应用自己提供的那个**。

ReDoc 也类似...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | 提示

`swagger_ui_redirect` 的*路径操作*是在你使用 OAuth2 时的一个辅助。

如果你把 API 与某个 OAuth2 提供方集成，你就可以完成认证并带着获取到的凭据回到 API 文档里。然后使用真实的 OAuth2 认证与之交互。

Swagger UI 会在幕后为你处理这些，但它需要这个“重定向”辅助路径。

///

### 创建一个路径操作测试静态文件 { #create-a-path-operation-to-test-static-files }

现在，为了测试一切是否正常，创建一个*路径操作*：

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### 测试静态文件 UI { #test-static-files-ui }

现在，你可以断开 WiFi，访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)，并刷新页面。

即使没有互联网，你也能看到 API 的文档并与之交互。



---

# Source: docs/how-to/custom-request-and-route.md


# 自定义 Request 和 APIRoute 类 { #custom-request-and-apiroute-class }

在某些情况下，你可能想要重写 `Request` 和 `APIRoute` 类使用的逻辑。

尤其是，当你本来会把这些逻辑放到中间件里时，这是一个不错的替代方案。

例如，如果你想在应用处理之前读取或操作请求体。

/// danger | 危险

这是一个“高级”特性。

如果你刚开始使用 **FastAPI**，可以先跳过本节。

///

## 使用场景 { #use-cases }

一些使用场景包括：

* 将非 JSON 的请求体转换为 JSON（例如 [`msgpack`](https://msgpack.org/index.html)）。
* 解压缩使用 gzip 压缩的请求体。
* 自动记录所有请求体日志。

## 处理自定义请求体编码 { #handling-custom-request-body-encodings }

来看如何用自定义的 `Request` 子类来解压 gzip 请求。

以及一个 `APIRoute` 子类来使用该自定义请求类。

### 创建自定义 `GzipRequest` 类 { #create-a-custom-gziprequest-class }

/// tip | 提示

这是一个演示工作原理的示例。如果你需要 Gzip 支持，可以直接使用提供的 [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware)。

///

首先，我们创建一个 `GzipRequest` 类，它会重写 `Request.body()` 方法：当请求头中存在相应标记时对请求体进行解压。

如果请求头中没有 `gzip`，则不会尝试解压。

这样，同一个路由类即可同时处理 gzip 压缩和未压缩的请求。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### 创建自定义 `GzipRoute` 类 { #create-a-custom-gziproute-class }

接着，我们创建 `fastapi.routing.APIRoute` 的自定义子类来使用 `GzipRequest`。

这次，我们会重写 `APIRoute.get_route_handler()` 方法。

该方法返回一个函数，这个函数负责接收请求并返回响应。

这里我们用它把原始请求包装为 `GzipRequest`。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | 技术细节

`Request` 拥有 `request.scope` 属性，它就是一个 Python `dict`，包含与请求相关的元数据。

`Request` 还包含 `request.receive`，它是一个用于“接收”请求体的函数。

`scope` 字典和 `receive` 函数都是 ASGI 规范的一部分。

创建一个新的 `Request` 实例需要这两样：`scope` 和 `receive`。

想了解更多关于 `Request` 的信息，请查看 [Starlette 的 Request 文档](https://www.starlette.dev/requests/)。

///

由 `GzipRequest.get_route_handler` 返回的函数唯一不同之处是把 `Request` 转换为 `GzipRequest`。

这样，在传给我们的*路径操作*之前，`GzipRequest` 会（在需要时）负责解压数据。

之后，其余处理逻辑完全相同。

但由于我们修改了 `GzipRequest.body`，在 **FastAPI** 需要读取时，请求体会被自动解压。

## 在异常处理器中访问请求体 { #accessing-the-request-body-in-an-exception-handler }

/// tip | 提示

要解决类似问题，使用 `RequestValidationError` 的自定义处理器中的 `body` 往往更简单（[处理错误](../tutorial/handling-errors.md#use-the-requestvalidationerror-body)）。

但本示例同样有效，并展示了如何与内部组件交互。

///

我们也可以用相同的方法在异常处理器中访问请求体。

所需仅是在 `try`/`except` 块中处理请求：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

如果发生异常，`Request` 实例仍在作用域内，因此我们可以在处理错误时读取并使用请求体：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## 在路由器中自定义 `APIRoute` 类 { #custom-apiroute-class-in-a-router }

你也可以设置 `APIRouter` 的 `route_class` 参数：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

在此示例中，`router` 下的*路径操作*将使用自定义的 `TimedRoute` 类，响应中会多一个 `X-Response-Time` 头，包含生成响应所用的时间：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}



---

# Source: docs/how-to/extending-openapi.md


# 扩展 OpenAPI { #extending-openapi }

在某些情况下，你可能需要修改生成的 OpenAPI 架构（schema）。

本节将介绍如何实现。

## 常规流程 { #the-normal-process }

常规（默认）流程如下。

`FastAPI` 应用（实例）有一个 `.openapi()` 方法，预期返回 OpenAPI 架构。

在创建应用对象时，会注册一个用于 `/openapi.json`（或你在 `openapi_url` 中设置的路径）的路径操作。

它只会返回一个 JSON 响应，内容是应用 `.openapi()` 方法的结果。

默认情况下，`.openapi()` 方法会检查属性 `.openapi_schema` 是否已有内容，若有则直接返回。

如果没有，则使用 `fastapi.openapi.utils.get_openapi` 工具函数生成。

该 `get_openapi()` 函数接收以下参数：

- `title`：OpenAPI 标题，显示在文档中。
- `version`：你的 API 版本，例如 `2.5.0`。
- `openapi_version`：使用的 OpenAPI 规范版本。默认是最新的 `3.1.0`。
- `summary`：API 的简短摘要。
- `description`：API 的描述，可包含 Markdown，并会展示在文档中。
- `routes`：应用的路由，来自 `app.routes`。FastAPI 使用它们来收集已注册的路径操作，包括来自已包含路由器的那些。

/// tip | 技术细节

`app.routes` 是一个更底层的路由树。它可能包含 FastAPI 在内部用于包含的路由器的候选路由，而不仅仅是最终的 `APIRoute` 对象。

你仍然可以把 `app.routes` 传给 `get_openapi()`。FastAPI 会遍历这棵路由树来收集实际生效的路径操作。

///

/// note | 注意

参数 `summary` 仅在 OpenAPI 3.1.0 及更高版本中可用，FastAPI 0.99.0 及以上版本支持。

///

## 覆盖默认值 { #overriding-the-defaults }

基于以上信息，你可以用同一个工具函数生成 OpenAPI 架构，并按需覆盖其中的各个部分。

例如，让我们添加 [ReDoc 的 OpenAPI 扩展以包含自定义 Logo](https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo)。

### 常规 **FastAPI** { #normal-fastapi }

首先，像平常一样编写你的 **FastAPI** 应用：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### 生成 OpenAPI 架构 { #generate-the-openapi-schema }

然后，在一个 `custom_openapi()` 函数中使用同一个工具函数生成 OpenAPI 架构：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### 修改 OpenAPI 架构 { #modify-the-openapi-schema }

现在你可以添加 ReDoc 扩展，在 OpenAPI 架构的 `info` “对象”中加入自定义 `x-logo`：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### 缓存 OpenAPI 架构 { #cache-the-openapi-schema }

你可以把 `.openapi_schema` 属性当作“缓存”，用来存储已生成的架构。

这样一来，应用每次打开 API 文档时就不必重新生成架构。

它只会生成一次，后续请求都会使用同一份缓存的架构。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### 覆盖方法 { #override-the-method }

现在你可以用你的新函数替换 `.openapi()` 方法。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### 验证 { #check-it }

当你访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) 时，你会看到已使用你的自定义 Logo（本例中为 **FastAPI** 的 Logo）：

<img src="/img/tutorial/extending-openapi/image01.png">



---

# Source: docs/how-to/general.md


# 通用 - 如何操作 - 诀窍 { #general-how-to-recipes }

这里是一些指向文档中其他部分的链接，用于解答一般性或常见问题。

## 数据过滤 - 安全性 { #filter-data-security }

为确保不返回超过需要的数据，请阅读 [教程 - 响应模型 - 返回类型](../tutorial/response-model.md) 文档。

## 优化响应性能 - 响应模型 - 返回类型 { #optimize-response-performance-response-model-return-type }

在返回 JSON 数据时优化性能，请使用返回类型或响应模型，这样 Pydantic 会在 Rust 侧处理到 JSON 的序列化，而无需经过 Python。更多内容请阅读 [教程 - 响应模型 - 返回类型](../tutorial/response-model.md) 文档。

## 文档的标签 - OpenAPI { #documentation-tags-openapi }

在文档界面中添加**路径操作**的标签和进行分组，请阅读 [教程 - 路径操作配置 - Tags](../tutorial/path-operation-configuration.md#tags) 文档。

## 文档的概要和描述 - OpenAPI { #documentation-summary-and-description-openapi }

在文档界面中添加**路径操作**的概要和描述，请阅读 [教程 - 路径操作配置 - Summary 和 Description](../tutorial/path-operation-configuration.md#summary-and-description) 文档。

## 文档的响应描述 - OpenAPI { #documentation-response-description-openapi }

在文档界面中定义并显示响应描述，请阅读 [教程 - 路径操作配置 - 响应描述](../tutorial/path-operation-configuration.md#response-description) 文档。

## 文档弃用**路径操作** - OpenAPI { #documentation-deprecate-a-path-operation-openapi }

在文档界面中显示弃用的**路径操作**，请阅读 [教程 - 路径操作配置 - 弃用](../tutorial/path-operation-configuration.md#deprecate-a-path-operation) 文档。

## 将任何数据转换为 JSON 兼容格式 { #convert-any-data-to-json-compatible }

要将任何数据转换为 JSON 兼容格式，请阅读 [教程 - JSON 兼容编码器](../tutorial/encoder.md) 文档。

## OpenAPI 元数据 - 文档 { #openapi-metadata-docs }

要添加 OpenAPI 的元数据，包括许可证、版本、联系方式等，请阅读 [教程 - 元数据和文档 URL](../tutorial/metadata.md) 文档。

## OpenAPI 自定义 URL { #openapi-custom-url }

要自定义 OpenAPI 的 URL（或删除它），请阅读 [教程 - 元数据和文档 URL](../tutorial/metadata.md#openapi-url) 文档。

## OpenAPI 文档 URL { #openapi-docs-urls }

要更改自动生成的文档用户界面所使用的 URL，请阅读 [教程 - 元数据和文档 URL](../tutorial/metadata.md#docs-urls)。



---

# Source: docs/how-to/graphql.md


# GraphQL { #graphql }

由于 **FastAPI** 基于 **ASGI** 标准，因此很容易集成任何也兼容 ASGI 的 **GraphQL** 库。

你可以在同一个应用中将常规的 FastAPI *路径操作* 与 GraphQL 结合使用。

/// tip | 提示

**GraphQL** 解决一些非常特定的用例。

与常见的 **Web API** 相比，它有各自的**优点**和**缺点**。

请确保评估在你的用例中，这些**好处**是否足以弥补这些**缺点**。 🤓

///

## GraphQL 库 { #graphql-libraries }

以下是一些支持 **ASGI** 的 **GraphQL** 库。你可以将它们与 **FastAPI** 一起使用：

* [Strawberry](https://strawberry.rocks/) 🍓
    * 提供 [面向 FastAPI 的文档](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * 提供 [面向 FastAPI 的文档](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * 提供用于 ASGI 集成的 [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/)
* [Graphene](https://graphene-python.org/)
    * 可配合 [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) 使用

## 使用 Strawberry 的 GraphQL { #graphql-with-strawberry }

如果你需要或想要使用 **GraphQL**，[**Strawberry**](https://strawberry.rocks/) 是**推荐**的库，因为它的设计与 **FastAPI** 最为接近，全部基于**类型注解**。

根据你的用例，你可能会更喜欢其他库，但如果你问我，我大概率会建议你先试试 **Strawberry**。

下面是一个将 Strawberry 与 FastAPI 集成的小预览：

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

你可以在 [Strawberry 文档](https://strawberry.rocks/) 中了解更多信息。

还有关于 [将 Strawberry 与 FastAPI 结合使用](https://strawberry.rocks/docs/integrations/fastapi) 的文档。

## Starlette 中较早的 `GraphQLApp` { #older-graphqlapp-from-starlette }

早期版本的 Starlette 包含一个 `GraphQLApp` 类，用于与 [Graphene](https://graphene-python.org/) 集成。

它已在 Starlette 中被弃用，但如果你的代码使用了它，你可以轻松**迁移**到 [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)，它覆盖相同的用例，且接口**几乎完全一致**。

/// tip | 提示

如果你需要 GraphQL，我仍然建议看看 [Strawberry](https://strawberry.rocks/)，因为它基于类型注解而不是自定义类和类型。

///

## 了解更多 { #learn-more }

你可以在 [GraphQL 官方文档](https://graphql.org/) 中了解更多关于 **GraphQL** 的内容。

你也可以通过上面的链接阅读各个库的更多信息。



---

# Source: docs/how-to/index.md


# 如何操作 - 诀窍 { #how-to-recipes }

在这里，你将看到关于**多个主题**的不同诀窍或“如何操作”指南。

这些方法多数是**相互独立**的，在大多数情况下，你只需在这些内容适用于**你的项目**时才需要学习它们。

如果某些内容看起来对你的项目有用，请继续查阅，否则请直接跳过它们。

/// tip | 提示

如果你想以系统的方式**学习 FastAPI**（推荐），请阅读 [教程 - 用户指南](../tutorial/index.md) 的每一章节。

///



---

# Source: docs/how-to/migrate-from-pydantic-v1-to-pydantic-v2.md


# 从 Pydantic v1 迁移到 Pydantic v2 { #migrate-from-pydantic-v1-to-pydantic-v2 }

如果你有一个较旧的 FastAPI 应用，可能在使用 Pydantic v1。

FastAPI 0.100.0 同时支持 Pydantic v1 和 v2，会使用你已安装的任一版本。

FastAPI 0.119.0 引入了在 Pydantic v2 内部以 `pydantic.v1` 形式对 Pydantic v1 的部分支持，以便于迁移到 v2。

FastAPI 0.126.0 移除了对 Pydantic v1 的支持，但在一段时间内仍支持 `pydantic.v1`。

FastAPI 0.128.0 也移除了对 `pydantic.v1` 的支持，因此最新版本的 FastAPI 需要 Pydantic v2。

/// warning | 警告

从 **Python 3.14** 开始，Pydantic 团队不再为最新的 Python 版本提供 Pydantic v1 的支持。

这也包括 `pydantic.v1`，在 Python 3.14 及更高版本中不再受支持。

如果你想使用 Python 的最新特性，需要确保使用 Pydantic v2。

///

如果你的旧 FastAPI 应用在用 Pydantic v1，这里将向你展示如何迁移到 Pydantic v2，以及 **FastAPI 0.119.0 中的功能** 可帮助你渐进式迁移。

## 官方指南 { #official-guide }

Pydantic 有一份从 v1 迁移到 v2 的官方[迁移指南](https://docs.pydantic.dev/latest/migration/)。

其中包含变更内容、校验如何更准确更严格、可能的注意事项等。

你可以阅读以更好地了解变更。

## 测试 { #tests }

请确保你的应用有[测试](../tutorial/testing.md)，并在持续集成（CI）中运行它们。

这样你就可以升级并确保一切仍按预期工作。

## `bump-pydantic` { #bump-pydantic }

在很多情况下，如果你使用的是未做自定义的常规 Pydantic 模型，可以将从 Pydantic v1 迁移到 v2 的大部分过程自动化。

你可以使用同一 Pydantic 团队提供的[`bump-pydantic`](https://github.com/pydantic/bump-pydantic)。

该工具会帮助你自动修改大部分需要变更的代码。

之后运行测试检查是否一切正常。如果正常，你就完成了。😎

## v2 中的 Pydantic v1 { #pydantic-v1-in-v2 }

Pydantic v2 以子模块 `pydantic.v1` 的形式包含了 Pydantic v1 的全部内容。但在 Python 3.13 以上的版本中不再受支持。

这意味着你可以安装最新的 Pydantic v2，并从该子模块导入并使用旧的 Pydantic v1 组件，就像安装了旧版 Pydantic v1 一样。

{* ../../docs_src/pydantic_v1_in_v2/tutorial001_an_py310.py hl[1,4] *}

### FastAPI 对 v2 中 Pydantic v1 的支持 { #fastapi-support-for-pydantic-v1-in-v2 }

/// warning | 警告

此 FastAPI 对 `pydantic.v1` 模型的支持是在 **FastAPI 0.119.0** 中添加的，并在 **FastAPI 0.128.0** 中移除。它原本是为了迁移到 Pydantic v2 而提供的临时辅助。

在当前版本的 FastAPI 中，在你的应用里使用 `pydantic.v1` 模型会引发错误。

本节其余部分描述的临时支持仅在那些较旧版本中可用。

///

自 FastAPI 0.119.0 起，FastAPI 也对 Pydantic v2 内的 Pydantic v1 提供了部分支持，以便迁移到 v2。

因此，你可以将 Pydantic 升级到最新的 v2，并将导入改为使用 `pydantic.v1` 子模块，在很多情况下就能直接工作。

{* ../../docs_src/pydantic_v1_in_v2/tutorial002_an_py310.py hl[2,5,15] *}

/// warning | 警告

请注意，由于 Pydantic 团队自 Python 3.14 起不再在较新的 Python 版本中支持 Pydantic v1，使用 `pydantic.v1` 在 Python 3.14 及更高版本中也不受支持。

///

### 同一应用中同时使用 Pydantic v1 与 v2 { #pydantic-v1-and-v2-on-the-same-app }

Pydantic 不支持在一个 Pydantic v2 模型的字段中定义 Pydantic v1 模型，反之亦然。

```mermaid
graph TB
    subgraph "❌ Not Supported"
        direction TB
        subgraph V2["Pydantic v2 Model"]
            V1Field["Pydantic v1 Model"]
        end
        subgraph V1["Pydantic v1 Model"]
            V2Field["Pydantic v2 Model"]
        end
    end

    style V2 fill:#f9fff3
    style V1 fill:#fff6f0
    style V1Field fill:#fff6f0
    style V2Field fill:#f9fff3
```

...但是，你可以在同一个应用中分别使用 Pydantic v1 和 v2 的独立模型。

```mermaid
graph TB
    subgraph "✅ Supported"
        direction TB
        subgraph V2["Pydantic v2 Model"]
            V2Field["Pydantic v2 Model"]
        end
        subgraph V1["Pydantic v1 Model"]
            V1Field["Pydantic v1 Model"]
        end
    end

    style V2 fill:#f9fff3
    style V1 fill:#fff6f0
    style V1Field fill:#fff6f0
    style V2Field fill:#f9fff3
```

在某些情况下，甚至可以在 FastAPI 应用的同一个路径操作中同时使用 Pydantic v1 和 v2 模型：

{* ../../docs_src/pydantic_v1_in_v2/tutorial003_an_py310.py hl[2:3,6,12,21:22] *}

在上面的示例中，输入模型是 Pydantic v1 模型，输出模型（在 `response_model=ItemV2` 中定义）是 Pydantic v2 模型。

### Pydantic v1 参数 { #pydantic-v1-parameters }

如果你需要在 Pydantic v1 模型中使用 FastAPI 特有的参数工具，如 `Body`、`Query`、`Form` 等，在完成向 Pydantic v2 的迁移前，可以从 `fastapi.temp_pydantic_v1_params` 导入它们：

{* ../../docs_src/pydantic_v1_in_v2/tutorial004_an_py310.py hl[4,18] *}

### 分步迁移 { #migrate-in-steps }

/// warning | 警告

下面描述的在同一应用中同时使用 Pydantic v1 和 v2 模型进行渐进式迁移，只适用于 **FastAPI 0.119.0 到 0.127.x**。它已在 **FastAPI 0.128.0** 中移除，最新版本需要 **Pydantic v2** 模型。

///

/// tip | 提示

优先尝试 `bump-pydantic`，如果测试通过且可行，那么你就用一个命令完成了。✨

///

如果 `bump-pydantic` 不适用于你的场景，你可以在同一应用中同时支持 Pydantic v1 和 v2 模型，逐步迁移到 Pydantic v2。

你可以首先将 Pydantic 升级到最新的 v2，并将所有模型的导入改为使用 `pydantic.v1`。

然后按模块或分组，逐步把模型从 Pydantic v1 迁移到 v2。🚶



---

# Source: docs/how-to/separate-openapi-schemas.md


# 是否为输入和输出分别生成 OpenAPI JSON Schema { #separate-openapi-schemas-for-input-and-output-or-not }


自从发布了 **Pydantic v2**，生成的 OpenAPI 比之前更精确、更**正确**了。😎

事实上，在某些情况下，对于同一个 Pydantic 模型，OpenAPI 中会根据是否带有**默认值**，为输入和输出分别生成**两个 JSON Schema**。

我们来看看它如何工作，以及在需要时如何修改。

## 用于输入和输出的 Pydantic 模型 { #pydantic-models-for-input-and-output }

假设你有一个带有默认值的 Pydantic 模型，例如：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### 输入用的模型 { #model-for-input }

如果你像下面这样把该模型用作输入：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...那么 `description` 字段将**不是必填项**，因为它的默认值是 `None`。

### 文档中的输入模型 { #input-model-in-docs }

你可以在文档中确认，`description` 字段没有**红色星号**，也就是未被标记为必填：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### 输出用的模型 { #model-for-output }

但如果你把同一个模型用作输出，例如：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...那么因为 `description` 有默认值，即使你**不返回该字段**，它仍然会有这个**默认值**。

### 输出响应数据的模型 { #model-for-output-response-data }

如果你在文档中交互并查看响应，即使代码没有给某个 `description` 字段赋值，JSON 响应中仍包含默认值（`null`）：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

这意味着它**总会有值**，只是有时该值可能为 `None`（在 JSON 中是 `null`）。

这也意味着，使用你的 API 的客户端无需检查该值是否存在，他们可以**假设该字段总会存在**，只是有时它会是默认值 `None`。

在 OpenAPI 中描述这一点的方式，是把该字段标记为**必填**，因为它总会存在。

因此，一个模型的 JSON Schema 会根据它用于**输入还是输出**而有所不同：

- 用于**输入**时，`description` **不是必填**
- 用于**输出**时，它是**必填**（并且可能为 `None`，在 JSON 中为 `null`）

### 文档中的输出模型 { #model-for-output-in-docs }

你也可以在文档中查看输出模型，`name` 和 `description` **都**被**红色星号**标记为**必填**：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### 文档中的输入/输出模型 { #model-for-input-and-output-in-docs }

如果你查看 OpenAPI 中可用的所有 Schema（JSON Schema），你会看到有两个，一个是 `Item-Input`，一个是 `Item-Output`。

对于 `Item-Input`，`description` **不是必填**，没有红色星号。

但对于 `Item-Output`，`description` 是**必填**，带有红色星号。

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

借助 **Pydantic v2** 的这个特性，你的 API 文档会更**精确**，如果你有自动生成的客户端和 SDK，它们也会更精确，带来更好的**开发者体验**和一致性。🎉

## 不要分离 Schema { #do-not-separate-schemas }

当然，在某些情况下，你可能希望**输入和输出使用同一个 schema**。

最常见的情形是：你已经有一些自动生成的客户端代码/SDK，你暂时不想更新所有这些自动生成的客户端代码/SDK（也许未来会，但不是现在）。

这种情况下，你可以在 **FastAPI** 中通过参数 `separate_input_output_schemas=False` 禁用该特性。

/// note | 注意

对 `separate_input_output_schemas` 的支持是在 FastAPI `0.102.0` 中添加的。🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### 文档中输入/输出使用同一 Schema 的模型 { #same-schema-for-input-and-output-models-in-docs }

现在该模型的输入和输出将只使用一个 schema，即 `Item`，并且其中的 `description` **不是必填**：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>



---

# Source: docs/how-to/testing-database.md


# 测试数据库 { #testing-a-database }

你可以在[SQLModel 文档](https://sqlmodel.tiangolo.com/)中学习数据库、SQL 和 SQLModel。🤓

这里有一个[在 FastAPI 中使用 SQLModel 的小教程](https://sqlmodel.tiangolo.com/tutorial/fastapi/)。✨

该教程包含一个关于[测试 SQL 数据库](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/)的章节。😎



---

# Source: docs/index.md


---
include_yaml:
  sponsors: data/sponsors.yml
---

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/zh"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI 框架，高性能，易于学习，高效编码，生产可用</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**文档**： [https://fastapi.tiangolo.com/zh](https://fastapi.tiangolo.com/zh)

**源码**： [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI 是一个用于构建 API 的现代、快速（高性能）的 Web 框架，使用 Python 并基于标准的 Python 类型提示。

关键特性：

* **快速**：极高性能，可与 **NodeJS** 和 **Go** 并肩（归功于 Starlette 和 Pydantic）。[最快的 Python 框架之一](#performance)。
* **高效编码**：功能开发速度提升约 200% ～ 300%。*
* **更少 bug**：人为（开发者）错误减少约 40%。*
* **直观**：极佳的编辑器支持。处处皆可<dfn title="也被称为：自动完成、自动补全、IntelliSense">自动补全</dfn>。更少的调试时间。
* **易用**：为易用和易学而设计。更少的文档阅读时间。
* **简短**：最小化代码重复。一次参数声明即可获得多种功能。更少的 bug。
* **健壮**：生产可用级代码。并带有自动生成的交互式文档。
* **标准化**：基于（并完全兼容）API 的开放标准：[OpenAPI](https://github.com/OAI/OpenAPI-Specification)（以前称为 Swagger）和 [JSON Schema](https://json-schema.org/)。

<small>* 基于某内部开发团队在构建生产应用时的测试估算。</small>

## 赞助商 { #sponsors }

<!-- sponsors -->

### Keystone 赞助商 { #keystone-sponsor }

<div class="fastapi-sponsors fastapi-sponsors--keystone">
{% for sponsor in sponsors.keystone -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--keystone" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}"></a>
{% endfor -%}
</div>

### 金牌赞助商 { #gold-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--gold">
{% for sponsor in sponsors.gold -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--gold" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor -%}
</div>

### 银牌赞助商 { #silver-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--silver">
{% for sponsor in sponsors.silver -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--silver" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor %}
</div>

<!-- /sponsors -->

[其他赞助商](https://fastapi.tiangolo.com/zh/fastapi-people/#sponsors)

## 评价 { #opinions }

<!-- only-mkdocs -->
<div class="fastapi-opinions" data-fastapi-opinions>
  <div class="fastapi-opinions__tabs" role="tablist" aria-label="Companies using FastAPI">
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-microsoft" aria-controls="fo-panel-microsoft" aria-selected="true" tabindex="0">
      <span class="fastapi-opinions__mark"><img src="/img/logos/microsoft.svg" alt="Microsoft" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-uber" aria-controls="fo-panel-uber" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/uber.svg" alt="Uber" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-netflix" aria-controls="fo-panel-netflix" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/netflix.svg" alt="Netflix" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-cisco" aria-controls="fo-panel-cisco" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/cisco.svg" alt="Cisco" loading="lazy"></span>
    </button>
  </div>

  <div class="fastapi-opinions__panel" id="fo-panel-microsoft" role="tabpanel" aria-labelledby="fo-tab-microsoft" tabindex="0">
    <blockquote class="fastapi-opinions__quote">“我最近大量使用 <strong>FastAPI</strong>。我实际上计划把它用于我团队在 <strong>微软的机器学习（ML）服务</strong>。其中一些正在集成进核心 <strong>Windows</strong> 产品以及一些 <strong>Office</strong> 产品。”</blockquote>
    <div class="fastapi-opinions__attr">— Kabir Khan，<strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26">(参考)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-uber" role="tabpanel" aria-labelledby="fo-tab-uber" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">“我们采用了 <strong>FastAPI</strong> 库来启动一个可查询获取<strong>预测结果</strong>的 <strong>REST</strong> 服务器。” <em>[用于 Ludwig]</em></blockquote>
    <div class="fastapi-opinions__attr">— Piero Molino，Yaroslav Dudin，Sai Sumanth Miryala，<strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/">(参考)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-netflix" role="tabpanel" aria-labelledby="fo-tab-netflix" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">“<strong>Netflix</strong> 很高兴宣布开源我们的<strong>危机管理</strong>编排框架：<strong>Dispatch</strong>！” <em>[使用 FastAPI 构建]</em></blockquote>
    <div class="fastapi-opinions__attr">— Kevin Glisson，Marc Vilanova，Forest Monsen，<strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072">(参考)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-cisco" role="tabpanel" aria-labelledby="fo-tab-cisco" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">“如果有人正在构建生产级的 Python API，我强烈推荐 <strong>FastAPI</strong>。它<strong>设计优雅</strong>、<strong>使用简单</strong>且<strong>高度可扩展</strong> —— 它已经成为我们 API 优先开发战略中的<strong>关键组件</strong>。”</blockquote>
    <div class="fastapi-opinions__attr">— Deon Pillsbury，<strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/">(参考)</a></div>
  </div>
</div>
<!-- /only-mkdocs -->

<div class="only-github" markdown="1">

「_[...] 我最近大量使用 **FastAPI**。[...] 我实际上计划把它用于我团队在 **微软的机器学习（ML）服务**。其中一些正在集成进核心 **Windows** 产品以及一些 **Office** 产品。_」

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(参考)</small></a></div>

---

「_我们采用 **FastAPI** 库来启动一个可查询以获取**预测结果**的 **REST** 服务器。[用于 Ludwig]_」

<div style="text-align: right; margin-right: 10%;">Piero Molino，Yaroslav Dudin，Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(参考)</small></a></div>

---

「_**Netflix** 很高兴宣布开源我们的**危机管理**编排框架：**Dispatch**！[使用 **FastAPI** 构建]_」

<div style="text-align: right; margin-right: 10%;">Kevin Glisson，Marc Vilanova，Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(参考)</small></a></div>

---

「_如果有人正在构建生产级的 Python API，我强烈推荐 **FastAPI**。它**设计优雅**、**使用简单**且**高度可扩展**，它已经成为我们 API 优先开发战略中的**关键组件**，并驱动了许多自动化和服务，比如我们的 Virtual TAC Engineer。_」

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(参考)</small></a></div>

---

</div>

## FastAPI 大会 { #fastapi-conf }

[**FastAPI Conf '26**](https://fastapiconf.com) 将于 **2026 年 10 月 28 日** 在 **荷兰阿姆斯特丹** 举行。来自源头的 FastAPI 干货。🎤

<a class="fastapi-feature-banner" href="https://fastapiconf.com"><img src="https://fastapi.tiangolo.com/img/fastapi-conf.jpeg" alt="FastAPI Conf '26 - 2026 年 10 月 28 日 - 荷兰阿姆斯特丹"></a>

## FastAPI 迷你纪录片 { #fastapi-mini-documentary }

在 2025 年末发布了一部 [FastAPI 迷你纪录片](https://www.youtube.com/watch?v=mpR8ngthqiE)，你可以在线观看：

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI 迷你纪录片"></a>

## **Typer**，命令行中的 FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你要开发一个用于终端而不是 Web API 的 <abbr title="Command Line Interface - 命令行界面">CLI</abbr> 应用，看看 [**Typer**](https://typer.tiangolo.com/)。

**Typer** 是 FastAPI 的小同胞。它的目标是成为**命令行中的 FastAPI**。⌨️ 🚀

## 依赖 { #requirements }

FastAPI 站在巨人的肩膀之上：

* [Starlette](https://www.starlette.dev/) 负责 Web 部分。
* [Pydantic](https://docs.pydantic.dev/) 负责数据部分。

## 安装 { #installation }

创建并激活一个 [虚拟环境](https://fastapi.tiangolo.com/zh/virtual-environments/)，然后安装 FastAPI：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**注意**: 请确保把 `"fastapi[standard]"` 用引号包起来，以保证在所有终端中都能正常工作。

## 示例 { #example }

### 创建 { #create-it }

创建文件 `main.py`，内容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>或者使用 <code>async def</code>...</summary>

如果你的代码里会用到 `async` / `await`，请使用 `async def`：

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**注意**:

如果你不确定，请查看文档中 _"In a hurry?"_ 章节的 [`async` 和 `await`](https://fastapi.tiangolo.com/zh/async/#in-a-hurry) 部分。

</details>

### 运行 { #run-it }

用下面的命令运行服务器：

<div class="termy">

```console
$ fastapi dev

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>关于命令 <code>fastapi dev</code>...</summary>

`fastapi dev` 命令会读取你的 `main.py` 文件，检测其中的 **FastAPI** 应用，并使用 [Uvicorn](https://www.uvicorn.dev) 启动服务器。

默认情况下，`fastapi dev` 会在本地开发时启用自动重载。

你可以在 [FastAPI CLI 文档](https://fastapi.tiangolo.com/zh/fastapi-cli/) 中了解更多。

</details>

### 检查 { #check-it }

用浏览器打开 [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)。

你会看到如下 JSON 响应：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已经创建了一个 API，它可以：

* 在路径 `/` 和 `/items/{item_id}` 接收 HTTP 请求。
* 以上两个路径都接受 `GET` <em>操作</em>（也称为 HTTP <em>方法</em>）。
* 路径 `/items/{item_id}` 有一个应为 `int` 的<em>路径参数</em> `item_id`。
* 路径 `/items/{item_id}` 有一个可选的 `str` 类型<em>查询参数</em> `q`。

### 交互式 API 文档 { #interactive-api-docs }

现在访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到自动生成的交互式 API 文档（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 可选的 API 文档 { #alternative-api-docs }

然后访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

你会看到另一个自动生成的文档（由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 示例升级 { #example-upgrade }

现在修改 `main.py` 文件来接收来自 `PUT` 请求的请求体。

借助 Pydantic，使用标准的 Python 类型来声明请求体。

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` 服务器会自动重载。

### 交互式 API 文档升级 { #interactive-api-docs-upgrade }

现在访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

* 交互式 API 文档会自动更新，并包含新的请求体：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 点击「Try it out」按钮，它允许你填写参数并直接与 API 交互：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然后点击「Execute」按钮，界面会与你的 API 通信、发送参数、获取结果并在屏幕上展示：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 可选文档升级 { #alternative-api-docs-upgrade }

再访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

* 可选文档同样会体现新的查询参数和请求体：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 总结 { #recap }

总之，你只需要把参数、请求体等的类型作为函数参数**声明一次**。

这些都使用标准的现代 Python 类型即可。

你不需要学习新的语法、某个特定库的方法或类等。

只需要标准的 **Python**。

例如，一个 `int`：

```Python
item_id: int
```

或者更复杂的 `Item` 模型：

```Python
item: Item
```

...通过一次声明，你将获得：

* 编辑器支持，包括：
    * 自动补全。
    * 类型检查。
* 数据校验：
    * 当数据无效时自动生成清晰的错误信息。
    * 即便是多层嵌套的 JSON 对象也会进行校验。
* <dfn title="也被称为：序列化、解析、编组">转换</dfn>输入数据：从网络读取到 Python 数据和类型。读取来源：
    * JSON。
    * 路径参数。
    * 查询参数。
    * Cookies。
    * Headers。
    * Forms。
    * Files。
* <dfn title="也被称为：序列化、解析、编组">转换</dfn>输出数据：从 Python 数据和类型转换为网络数据（JSON）：
    * 转换 Python 类型（`str`、`int`、`float`、`bool`、`list` 等）。
    * `datetime` 对象。
    * `UUID` 对象。
    * 数据库模型。
    * ...以及更多。
* 自动生成的交互式 API 文档，包括两种可选的用户界面：
    * Swagger UI。
    * ReDoc。

---

回到之前的代码示例，**FastAPI** 将会：

* 校验 `GET` 和 `PUT` 请求的路径中是否包含 `item_id`。
* 校验 `GET` 和 `PUT` 请求中的 `item_id` 是否为 `int` 类型。
    * 如果不是，客户端会看到清晰有用的错误信息。
* 对于 `GET` 请求，检查是否存在名为 `q` 的可选查询参数（如 `http://127.0.0.1:8000/items/foo?q=somequery`）。
    * 因为参数 `q` 被声明为 `= None`，所以它是可选的。
    * 如果没有 `None`，它就是必需的（就像 `PUT` 情况下的请求体）。
* 对于发送到 `/items/{item_id}` 的 `PUT` 请求，把请求体作为 JSON 读取：
    * 检查是否存在必需属性 `name`，且为 `str`。
    * 检查是否存在必需属性 `price`，且为 `float`。
    * 检查是否存在可选属性 `is_offer`，如果存在则应为 `bool`。
    * 对于多层嵌套的 JSON 对象，同样适用。
* 自动完成 JSON 的读取与输出转换。
* 使用 OpenAPI 记录所有内容，可用于：
    * 交互式文档系统。
    * 多语言的客户端代码自动生成系统。
* 直接提供 2 种交互式文档 Web 界面。

---

我们只是浅尝辄止，但你已经大致了解其工作方式了。

尝试把这一行：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...从：

```Python
        ... "item_name": item.name ...
```

...改为：

```Python
        ... "item_price": item.price ...
```

...看看你的编辑器如何自动补全属性并知道它们的类型：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

更多包含更多特性的完整示例，请参阅 <a href="https://fastapi.tiangolo.com/zh/tutorial/">教程 - 用户指南</a>。

**剧透警告**：教程 - 用户指南包括：

* 来自不同位置的**参数**声明：**headers**、**cookies**、**form 字段**和**文件**。
* 如何设置**校验约束**，如 `maximum_length` 或 `regex`。
* 功能强大且易用的 **<dfn title="也被称为：组件、资源、提供者、服务、可注入项">依赖注入</dfn>** 系统。
* 安全与认证，包括对 **OAuth2**、**JWT tokens** 和 **HTTP Basic** 认证的支持。
* 更高级（但同样简单）的 **多层嵌套 JSON 模型** 声明技巧（得益于 Pydantic）。
* 通过 [Strawberry](https://strawberry.rocks) 等库进行 **GraphQL** 集成。
* 许多额外特性（归功于 Starlette），例如：
    * **WebSockets**
    * 基于 HTTPX 和 `pytest` 的极其简单的测试
    * **CORS**
    * **Cookie Sessions**
    * ...以及更多。

### 部署你的应用（可选） { #deploy-your-app-optional }

你可以选择用一条命令将 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。🚀

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI 会自动检测你的 FastAPI 应用并将其部署到云端。如果你尚未登录，浏览器会打开以完成认证流程。

就这样！现在你可以通过该 URL 访问你的应用了。✨

#### 关于 FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 由 **FastAPI** 的同一位作者和团队打造。

它让你以最小的工作量就能**构建**、**部署**并**访问**一个 API。

它把用 FastAPI 构建应用时的**开发者体验**带到了部署到云上的过程。🎉

FastAPI Cloud 是「FastAPI and friends」开源项目的主要赞助方和资金提供者。✨

#### 部署到其他云厂商 { #deploy-to-other-cloud-providers }

FastAPI 是开源且基于标准的。你可以部署 FastAPI 应用到你选择的任意云厂商。

按照你的云厂商的指南部署 FastAPI 应用即可。🤓

## 性能 { #performance }

独立机构 TechEmpower 的基准测试显示，运行在 Uvicorn 下的 **FastAPI** 应用是 [最快的 Python 框架之一](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)，仅次于 Starlette 和 Uvicorn 本身（FastAPI 内部使用它们）。(*)

想了解更多，请参阅 [基准测试](https://fastapi.tiangolo.com/zh/benchmarks/) 章节。

## 依赖项 { #dependencies }

FastAPI 依赖 Pydantic 和 Starlette。

### `standard` 依赖 { #standard-dependencies }

当你通过 `pip install "fastapi[standard]"` 安装 FastAPI 时，会包含 `standard` 组的一些可选依赖：

Pydantic 使用：

* [`email-validator`](https://github.com/JoshData/python-email-validator) - 用于 email 校验。

Starlette 使用：

* [`httpx`](https://www.python-httpx.org) - 使用 `TestClient` 时需要。
* [`jinja2`](https://jinja.palletsprojects.com) - 使用默认模板配置时需要。
* [`python-multipart`](https://github.com/Kludex/python-multipart) - 使用 `request.form()` 支持表单<dfn title="将 HTTP 请求中的字符串转换为 Python 数据">「解析」</dfn>时需要。

FastAPI 使用：

* [`uvicorn`](https://www.uvicorn.dev) - 加载并提供你的应用的服务器。包含 `uvicorn[standard]`，其中包含高性能服务所需的一些依赖（例如 `uvloop`）。
* `fastapi-cli[standard]` - 提供 `fastapi` 命令。
    * 其中包含 `fastapi-cloud-cli`，它允许你将 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。

### 不包含 `standard` 依赖 { #without-standard-dependencies }

如果你不想包含这些 `standard` 可选依赖，可以使用 `pip install fastapi`，而不是 `pip install "fastapi[standard]"`。

### 不包含 `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

如果你想安装带有 standard 依赖但不包含 `fastapi-cloud-cli` 的 FastAPI，可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"`。

### 其他可选依赖 { #additional-optional-dependencies }

还有一些你可能想安装的可选依赖。

额外的 Pydantic 可选依赖：

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - 用于配置管理。
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - 用于在 Pydantic 中使用的额外类型。

额外的 FastAPI 可选依赖：

* [`orjson`](https://github.com/ijl/orjson) - 使用 `ORJSONResponse` 时需要。
* [`ujson`](https://github.com/esnme/ultrajson) - 使用 `UJSONResponse` 时需要。

## 许可协议 { #license }

该项目遵循 MIT 许可协议。



---

# Source: docs/learn/index.md


# 学习 { #learn }

以下是学习 **FastAPI** 的介绍部分和教程。

您可以认为这是一本 **书**，一门 **课程**，是 **官方** 且推荐的学习FastAPI的方法。😎



---

# Source: docs/project-generation.md


# FastAPI全栈模板 { #full-stack-fastapi-template }


模板通常带有特定的设置，但它们被设计为灵活且可定制。这样你可以根据项目需求进行修改和调整，使其成为很好的起点。🏁

你可以使用此模板开始，它已经为你完成了大量的初始设置、安全性、数据库以及一些 API 端点。

GitHub 仓库：[Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## FastAPI全栈模板 - 技术栈和特性 { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/zh) 用于 Python 后端 API。
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) 用于 Python 与 SQL 数据库的交互（ORM）。
  - 🔍 [Pydantic](https://docs.pydantic.dev)，FastAPI 使用，用于数据验证与配置管理。
  - 💾 [PostgreSQL](https://www.postgresql.org) 作为 SQL 数据库。
- 🚀 [React](https://react.dev) 用于前端。
  - 💃 使用 TypeScript、hooks、Vite 以及现代前端技术栈的其他部分。
  - 🎨 [Tailwind CSS](https://tailwindcss.com) 与 [shadcn/ui](https://ui.shadcn.com) 用于前端组件。
  - 🤖 自动生成的前端客户端。
  - 🧪 [Playwright](https://playwright.dev) 用于端到端测试。
  - 🦇 支持暗黑模式。
- 🐋 [Docker Compose](https://www.docker.com) 用于开发与生产。
- 🔒 默认启用安全的密码哈希。
- 🔑 JWT（JSON Web Token）认证。
- 📫 基于邮箱的密码找回。
- ✅ 使用 [Pytest](https://pytest.org) 进行测试。
- 📞 [Traefik](https://traefik.io) 用作反向代理/负载均衡。
- 🚢 使用 Docker Compose 的部署指南，包括如何设置前端 Traefik 代理以自动处理 HTTPS 证书。
- 🏭 基于 GitHub Actions 的 CI（持续集成）与 CD（持续部署）。



---

# Source: docs/python-types.md


# Python 类型提示简介 { #python-types-intro }

Python 支持可选的“类型提示”（也叫“类型注解”）。

这些 **“类型提示”** 或注解是一种特殊语法，用来声明变量的<dfn title="例如：str、int、float、bool">类型</dfn>。

通过为变量声明类型，编辑器和工具可以为你提供更好的支持。

这只是一个关于 Python 类型提示的**快速入门/复习**。它只涵盖与 **FastAPI** 一起使用所需的最少部分...实际上非常少。

**FastAPI** 完全基于这些类型提示构建，它们带来了许多优势和好处。

但即使你从不使用 **FastAPI**，了解一些类型提示也会让你受益。

/// note | 注意

如果你已经是 Python 专家，并且对类型提示了如指掌，可以跳到下一章。

///

## 动机 { #motivation }

让我们从一个简单的例子开始：

{* ../../docs_src/python_types/tutorial001_py310.py *}

运行这个程序会输出：

```
John Doe
```

这个函数做了下面这些事情：

* 接收 `first_name` 和 `last_name`。
* 通过 `title()` 将每个参数的第一个字母转换为大写。
* 用一个空格将它们<dfn title="把它们合在一起成为一个，内容一个接在另一个后面。">拼接</dfn>起来。

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### 修改它 { #edit-it }

这是一个非常简单的程序。

但现在想象你要从零开始写它。

在某个时刻你开始定义函数，并且准备好了参数...

接下来你需要调用“那个把首字母变大写的方法”。

是 `upper`？是 `uppercase`？`first_uppercase`？还是 `capitalize`？

然后，你试试程序员的老朋友——编辑器的自动补全。

你输入函数的第一个参数 `first_name`，再输入一个点（`.`），然后按下 `Ctrl+Space` 触发补全。

但很遗憾，没有什么有用的提示：

<img src="/img/python-types/image01.png">

### 添加类型 { #add-types }

我们来改前一个版本的一行代码。

我们会把这个片段，也就是函数参数，从：

```Python
    first_name, last_name
```

改成：

```Python
    first_name: str, last_name: str
```

就是这样。

这些就是“类型提示”：

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

这和声明默认值不同，比如：

```Python
    first_name="john", last_name="doe"
```

这是两码事。

我们用的是冒号（`:`），不是等号（`=`）。

而且添加类型提示通常不会改变代码本来的行为。

现在，再想象你又在编写这个函数了，不过这次加上了类型提示。

在同样的位置，你用 `Ctrl+Space` 触发自动补全，就能看到：

<img src="/img/python-types/image02.png">

这样，你可以滚动查看选项，直到找到那个“看着眼熟”的：

<img src="/img/python-types/image03.png">

## 更多动机 { #more-motivation }

看这个已经带有类型提示的函数：

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

因为编辑器知道变量的类型，你不仅能得到补全，还能获得错误检查：

<img src="/img/python-types/image04.png">

现在你知道需要修复它，用 `str(age)` 把 `age` 转成字符串：

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## 声明类型 { #declaring-types }

你刚刚看到的是声明类型提示的主要位置：函数参数。

这也是你在 **FastAPI** 中使用它们的主要场景。

### 简单类型 { #simple-types }

你不仅可以声明 `str`，还可以声明所有标准的 Python 类型。

例如：

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` 模块 { #typing-module }

在一些额外的用例中，你可能需要从标准库的 `typing` 模块导入内容。比如当你想声明“任意类型”时，可以使用 `typing` 中的 `Any`：

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### 泛型类型 { #generic-types }

有些类型可以在方括号中接收“类型参数”（type parameters），用于声明其内部值的类型。比如“字符串列表”可以写为 `list[str]`。

这些能接收类型参数的类型称为**泛型类型**（Generic types）或**泛型**（Generics）。

你可以把相同的内建类型作为泛型使用（带方括号和内部类型）：

* `list`
* `tuple`
* `set`
* `dict`

#### 列表 { #list }

例如，我们来定义一个由 `str` 组成的 `list` 变量。

用同样的冒号（`:`）语法声明变量。

类型写 `list`。

因为 list 是一种包含内部类型的类型，把内部类型写在方括号里：

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// note | 注意

方括号中的这些内部类型称为“类型参数”（type parameters）。

在这个例子中，`str` 是传给 `list` 的类型参数。

///

这表示：“变量 `items` 是一个 `list`，并且列表中的每一个元素都是 `str`”。

这样，即使是在处理列表中的元素时，编辑器也能给你提供支持：

<img src="/img/python-types/image05.png">

没有类型的话，这几乎是不可能做到的。

注意，变量 `item` 是列表 `items` 中的一个元素。

即便如此，编辑器仍然知道它是 `str`，并为此提供支持。

#### 元组和集合 { #tuple-and-set }

声明 `tuple` 和 `set` 的方式类似：

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

这表示：

* 变量 `items_t` 是一个含有 3 个元素的 `tuple`，分别是一个 `int`、另一个 `int`，以及一个 `str`。
* 变量 `items_s` 是一个 `set`，其中每个元素的类型是 `bytes`。

#### 字典 { #dict }

定义 `dict` 时，需要传入 2 个类型参数，用逗号分隔。

第一个类型参数用于字典的键。

第二个类型参数用于字典的值：

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

这表示：

* 变量 `prices` 是一个 `dict`：
    * 这个 `dict` 的键是 `str` 类型（比如，每个条目的名称）。
    * 这个 `dict` 的值是 `float` 类型（比如，每个条目的价格）。

#### Union { #union }

你可以声明一个变量可以是**若干种类型**中的任意一种，比如既可以是 `int` 也可以是 `str`。

定义时使用<dfn title='也叫“按位或运算符（bitwise or operator）”，但这里与该含义无关'>竖线（`|`）</dfn>把两种类型分开。

这称为“联合类型”（union），因为变量可以是这两类类型集合的并集中的任意一个。

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

这表示 `item` 可以是 `int` 或 `str`。

#### 可能为 `None` { #possibly-none }

你可以声明一个值的类型是某种类型（比如 `str`），但它也可能是 `None`。

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

使用 `str | None` 而不是仅仅 `str`，可以让编辑器帮助你发现把值当成总是 `str` 的错误（实际上它也可能是 `None`）。

### 类作为类型 { #classes-as-types }

你也可以把类声明为变量的类型。

假设你有一个名为 `Person` 的类，带有 name：

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

然后你可以声明一个变量是 `Person` 类型：

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

接着，你会再次获得所有的编辑器支持：

<img src="/img/python-types/image06.png">

注意，这表示“`one_person` 是类 `Person` 的一个**实例**（instance）”。

它并不表示“`one_person` 是名为 `Person` 的**类**（class）”。

## Pydantic 模型 { #pydantic-models }

[Pydantic](https://docs.pydantic.dev/) 是一个用于执行数据校验的 Python 库。

你将数据的“结构”声明为带有属性的类。

每个属性都有一个类型。

然后你用一些值创建这个类的实例，它会校验这些值，并在需要时把它们转换为合适的类型，返回一个包含所有数据的对象。

你还能对这个结果对象获得完整的编辑器支持。

下面是来自 Pydantic 官方文档的一个示例：

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// note | 注意

要了解更多关于 [Pydantic 的信息，请查看其文档](https://docs.pydantic.dev/)。

///

**FastAPI** 完全建立在 Pydantic 之上。

你会在[教程 - 用户指南](tutorial/index.md)中看到更多的实战示例。

## 带元数据注解的类型提示 { #type-hints-with-metadata-annotations }

Python 还提供了一个特性，可以使用 `Annotated` 在这些类型提示中放入**额外的<dfn title="关于数据的数据，此处指关于类型的信息，例如描述。">元数据</dfn>**。

你可以从 `typing` 导入 `Annotated`。

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python 本身不会对这个 `Annotated` 做任何处理。对于编辑器和其他工具，类型仍然是 `str`。

但你可以在 `Annotated` 中为 **FastAPI** 提供额外的元数据，来描述你希望应用如何行为。

重要的是要记住：传给 `Annotated` 的**第一个*类型参数***才是**实际类型**。其余的只是给其他工具用的元数据。

现在你只需要知道 `Annotated` 的存在，并且它是标准 Python。😎

稍后你会看到它有多么**强大**。

/// tip | 提示

这是**标准 Python**，这意味着你仍然可以在编辑器里获得**尽可能好的开发体验**，并能和你用来分析、重构代码的工具良好协作等。✨

同时你的代码也能与许多其他 Python 工具和库高度兼容。🚀

///

## **FastAPI** 中的类型提示 { #type-hints-in-fastapi }

**FastAPI** 利用这些类型提示来完成多件事情。

在 **FastAPI** 中，用类型提示来声明参数，你将获得：

* **编辑器支持**。
* **类型检查**。

...并且 **FastAPI** 会使用相同的声明来：

* **定义要求**：从请求路径参数、查询参数、请求头、请求体、依赖等。
* **转换数据**：把请求中的数据转换为所需类型。
* **校验数据**：对于每个请求：
    * 当数据无效时，自动生成返回给客户端的**错误**。
* 使用 OpenAPI **记录** API：
    * 然后用于自动生成交互式文档界面。

这些听起来可能有点抽象。别担心。你会在[教程 - 用户指南](tutorial/index.md)中看到所有这些的实际效果。

重要的是，通过使用标准的 Python 类型，而且只在一个地方声明（而不是添加更多类、装饰器等），**FastAPI** 会为你完成大量工作。

/// note | 注意

如果你已经读完整个教程，又回来想进一步了解类型，一个不错的资源是 [`mypy` 的“速查表”](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)。

///



---

# Source: docs/resources/index.md


# 资源 { #resources }

更多资源、外部链接等。✈️



---

# Source: docs/translation-banner.md


/// details | 🌐 由 AI 与人类协作翻译

本翻译由人类引导的 AI 生成。🤝

可能存在误解原意或不够自然等问题。🤖

你可以通过[帮助我们更好地引导 AI LLM](https://fastapi.tiangolo.com/zh/contributing/#translations)来改进此翻译。

[英文版本](ENGLISH_VERSION_URL)

///



---

# Source: docs/tutorial/background-tasks.md


# 后台任务 { #background-tasks }

你可以定义在返回响应后运行的后台任务。

这对需要在请求之后执行的操作很有用，但客户端不必在接收响应之前等待操作完成。

包括这些例子：

* 执行操作后发送的电子邮件通知：
    * 由于连接到电子邮件服务器并发送电子邮件往往很“慢”（几秒钟），您可以立即返回响应并在后台发送电子邮件通知。
* 处理数据：
    * 例如，假设您收到的文件必须经过一个缓慢的过程，您可以返回一个"Accepted"(HTTP 202)响应并在后台处理它。

## 使用 `BackgroundTasks` { #using-backgroundtasks }

首先导入 `BackgroundTasks` 并在 *路径操作函数* 中使用类型声明 `BackgroundTasks` 定义一个参数：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** 会创建一个 `BackgroundTasks` 类型的对象并作为该参数传入。

## 创建一个任务函数 { #create-a-task-function }

创建要作为后台任务运行的函数。

它只是一个可以接收参数的标准函数。

它可以是 `async def` 或普通的 `def` 函数，**FastAPI** 知道如何正确处理。

在这种情况下，任务函数将写入一个文件（模拟发送电子邮件）。

由于写操作不使用 `async` 和 `await`，我们用普通的 `def` 定义函数：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## 添加后台任务 { #add-the-background-task }

在你的 *路径操作函数* 里，用 `.add_task()` 方法将任务函数传到 *后台任务* 对象中：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` 接收以下参数：

* 在后台运行的任务函数(`write_notification`)。
* 应按顺序传递给任务函数的任意参数序列(`email`)。
* 应传递给任务函数的任意关键字参数(`message="some notification"`)。

## 依赖注入 { #dependency-injection }

使用 `BackgroundTasks` 也适用于依赖注入系统，你可以在多个级别声明 `BackgroundTasks` 类型的参数：在 *路径操作函数* 里，在依赖中(可依赖)，在子依赖中，等等。

**FastAPI** 知道在每种情况下该做什么以及如何复用同一对象，因此所有后台任务被合并在一起并且随后在后台运行：

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

该示例中，信息会在响应发出 *之后* 被写到 `log.txt` 文件。

如果请求中有查询，它将在后台任务中写入日志。

然后另一个在 *路径操作函数* 生成的后台任务会使用路径参数 `email` 写入一条信息。

## 技术细节 { #technical-details }

`BackgroundTasks` 类直接来自 [`starlette.background`](https://www.starlette.dev/background/)。

它被直接导入/包含到FastAPI以便你可以从 `fastapi` 导入，并避免意外从 `starlette.background` 导入备用的 `BackgroundTask` (后面没有 `s`)。

通过仅使用 `BackgroundTasks` (而不是 `BackgroundTask`)，使得能将它作为 *路径操作函数* 的参数 ，并让**FastAPI**为您处理其余部分, 就像直接使用 `Request` 对象。

在FastAPI中仍然可以单独使用 `BackgroundTask`，但您必须在代码中创建对象，并返回包含它的Starlette `Response`。

更多细节查看 [Starlette 后台任务的官方文档](https://www.starlette.dev/background/)。

## 告诫 { #caveat }

如果您需要执行繁重的后台计算，并且不一定需要由同一进程运行（例如，您不需要共享内存、变量等），那么使用其他更大的工具（如 [Celery](https://docs.celeryq.dev)）可能更好。

它们往往需要更复杂的配置，即消息/作业队列管理器，如RabbitMQ或Redis，但它们允许您在多个进程中运行后台任务，甚至是在多个服务器中。

但是，如果您需要从同一个**FastAPI**应用程序访问变量和对象，或者您需要执行小型后台任务（如发送电子邮件通知），您只需使用 `BackgroundTasks` 即可。

## 回顾 { #recap }

导入并使用 `BackgroundTasks` 通过 *路径操作函数* 中的参数和依赖项来添加后台任务。



---

# Source: docs/tutorial/bigger-applications.md


# 更大的应用 - 多个文件 { #bigger-applications-multiple-files }

如果你正在开发一个应用程序或 Web API，很少会将所有的内容都放在一个文件中。

**FastAPI** 提供了一个方便的工具，可以在保持所有灵活性的同时构建你的应用程序。

/// note | 注意

如果你来自 Flask，那这将相当于 Flask 的 Blueprints。

///

## 一个文件结构示例 { #an-example-file-structure }

假设你的文件结构如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | 提示

上面有几个 `__init__.py` 文件：每个目录或子目录中都有一个。

这就是能将代码从一个文件导入到另一个文件的原因。

例如，在 `app/main.py` 中，你可以有如下一行：

```
from app.routers import items
```

///

* `app` 目录包含了所有内容。并且它有一个空文件 `app/__init__.py`，因此它是一个「Python 包」（「Python 模块」的集合）：`app`。
* 它包含一个 `app/main.py` 文件。由于它位于一个 Python 包（一个包含 `__init__.py` 文件的目录）中，因此它是该包的一个「模块」：`app.main`。
* 还有一个 `app/dependencies.py` 文件，就像 `app/main.py` 一样，它是一个「模块」：`app.dependencies`。
* 有一个子目录 `app/routers/` 包含另一个 `__init__.py` 文件，因此它是一个「Python 子包」：`app.routers`。
* 文件 `app/routers/items.py` 位于 `app/routers/` 包中，因此它是一个子模块：`app.routers.items`。
* 同样适用于 `app/routers/users.py`，它是另一个子模块：`app.routers.users`。
* 还有一个子目录 `app/internal/` 包含另一个 `__init__.py` 文件，因此它是又一个「Python 子包」：`app.internal`。
* `app/internal/admin.py` 是另一个子模块：`app.internal.admin`。

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

带有注释的同一文件结构：

```bash
.
├── app                  # 「app」是一个 Python 包
│   ├── __init__.py      # 这个文件使「app」成为一个 Python 包
│   ├── main.py          # 「main」模块，例如 import app.main
│   ├── dependencies.py  # 「dependencies」模块，例如 import app.dependencies
│   └── routers          # 「routers」是一个「Python 子包」
│   │   ├── __init__.py  # 使「routers」成为一个「Python 子包」
│   │   ├── items.py     # 「items」子模块，例如 import app.routers.items
│   │   └── users.py     # 「users」子模块，例如 import app.routers.users
│   └── internal         # 「internal」是一个「Python 子包」
│       ├── __init__.py  # 使「internal」成为一个「Python 子包」
│       └── admin.py     # 「admin」子模块，例如 import app.internal.admin
```

## `APIRouter` { #apirouter }

假设专门用于处理用户逻辑的文件是位于 `/app/routers/users.py` 的子模块。

你希望将与用户相关的*路径操作*与其他代码分开，以使其井井有条。

但它仍然是同一 **FastAPI** 应用程序/web API 的一部分（它是同一「Python 包」的一部分）。

你可以使用 `APIRouter` 为该模块创建*路径操作*。

### 导入 `APIRouter` { #import-apirouter }

你可以导入它并通过与 `FastAPI` 类相同的方式创建一个「实例」：

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### 使用 `APIRouter` 的*路径操作* { #path-operations-with-apirouter }

然后你可以使用它来声明*路径操作*。

使用方式与 `FastAPI` 类相同：

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

你可以将 `APIRouter` 视为一个「迷你 `FastAPI`」类。

所有相同的选项都得到支持。

所有相同的 `parameters`、`responses`、`dependencies`、`tags` 等等。

/// tip | 提示

在此示例中，该变量被命名为 `router`，但你可以根据你的想法自由命名。

///

我们将在主 `FastAPI` 应用中包含该 `APIRouter`，但首先，让我们来看看依赖项和另一个 `APIRouter`。

## 依赖项 { #dependencies }

我们了解到我们将需要一些在应用程序的好几个地方所使用的依赖项。

因此，我们将它们放在它们自己的 `dependencies` 模块（`app/dependencies.py`）中。

现在我们将使用一个简单的依赖项来读取一个自定义的 `X-Token` 请求首部：

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | 提示

我们正在使用虚构的请求首部来简化此示例。

但在实际情况下，使用集成的[安全性实用工具](security/index.md)会得到更好的效果。

///

## 其他使用 `APIRouter` 的模块 { #another-module-with-apirouter }

假设你在位于 `app/routers/items.py` 的模块中还有专门用于处理应用程序中「项目」的端点。

你具有以下*路径操作*：

* `/items/`
* `/items/{item_id}`

这和 `app/routers/users.py` 的结构完全相同。

但是我们想变得更聪明并简化一些代码。

我们知道此模块中的所有*路径操作*都有相同的：

* 路径 `prefix`：`/items`。
* `tags`：（仅有一个 `items` 标签）。
* 额外的 `responses`。
* `dependencies`：它们都需要我们创建的 `X-Token` 依赖项。

因此，我们可以将其添加到 `APIRouter` 中，而不是将其添加到每个路径操作中。

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

由于每个*路径操作*的路径都必须以 `/` 开头，例如：

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...前缀不能以 `/` 作为结尾。

因此，本例中的前缀为 `/items`。

我们还可以添加一个 `tags` 列表和额外的 `responses` 列表，这些参数将应用于此路由器中包含的所有*路径操作*。

我们可以添加一个 `dependencies` 列表，这些依赖项将被添加到路由器中的所有*路径操作*中，并将针对向它们发起的每个请求执行/解决。

/// tip | 提示

请注意，和[*路径操作装饰器*中的依赖项](dependencies/dependencies-in-path-operation-decorators.md)很类似，没有值会被传递给你的*路径操作函数*。

///

最终结果是项目相关的路径现在为：

* `/items/`
* `/items/{item_id}`

...如我们所愿。

* 它们将被标记为仅包含单个字符串 `"items"` 的标签列表。
    * 这些「标签」对于自动化交互式文档系统（使用 OpenAPI）特别有用。
* 所有的路径操作都将包含预定义的 `responses`。
* 所有的这些*路径操作*都将在自身之前计算/执行 `dependencies` 列表。
    * 如果你还在一个具体的*路径操作*中声明了依赖项，**它们也会被执行**。
    * 路由器的依赖项最先执行，然后是[装饰器中的 `dependencies`](dependencies/dependencies-in-path-operation-decorators.md)，再然后是普通的参数依赖项。
    * 你还可以添加[具有 `scopes` 的 `Security` 依赖项](../advanced/security/oauth2-scopes.md)。

/// tip | 提示

在 `APIRouter`中具有 `dependencies` 可以用来，例如，对一整组的*路径操作*要求身份认证。即使这些依赖项并没有分别添加到每个路径操作中。

///

/// tip | 提示

`prefix`、`tags`、`responses` 以及 `dependencies` 参数只是（和其他很多情况一样）**FastAPI** 的一个用于帮助你避免代码重复的功能。

///

### 导入依赖项 { #import-the-dependencies }

这些代码位于 `app.routers.items` 模块，`app/routers/items.py` 文件中。

我们需要从 `app.dependencies` 模块即 `app/dependencies.py` 文件中获取依赖函数。

因此，我们通过 `..` 对依赖项使用了相对导入：

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### 相对导入如何工作 { #how-relative-imports-work }

/// tip | 提示

如果你完全了解导入的工作原理，请从下面的下一部分继续。

///

一个单点 `.`，例如：

```Python
from .dependencies import get_token_header
```

表示：

* 从该模块（`app/routers/items.py` 文件）所在的同一个包（`app/routers/` 目录）开始...
* 找到 `dependencies` 模块（一个位于 `app/routers/dependencies.py` 的虚构文件）...
* 然后从中导入函数 `get_token_header`。

但是该文件并不存在，我们的依赖项位于 `app/dependencies.py` 文件中。

请记住我们的程序/文件结构是怎样的：

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

两个点 `..`，例如：

```Python
from ..dependencies import get_token_header
```

表示：

* 从该模块（`app/routers/items.py` 文件）所在的同一个包（`app/routers/` 目录）开始...
* 跳转到其父包（`app/` 目录）...
* 在该父包中，找到 `dependencies` 模块（位于 `app/dependencies.py` 的文件）...
* 然后从中导入函数 `get_token_header`。

正常工作了！🎉

---

同样，如果我们使用了三个点 `...`，例如：

```Python
from ...dependencies import get_token_header
```

那将意味着：

* 从该模块（`app/routers/items.py` 文件）所在的同一个包（`app/routers/` 目录）开始...
* 跳转到其父包（`app/` 目录）...
* 然后跳转到该包的父包（该父包并不存在，`app` 已经是最顶层的包 😱）...
* 在该父包中，找到 `dependencies` 模块（位于 `app/dependencies.py` 的文件）...
* 然后从中导入函数 `get_token_header`。

这将引用 `app/` 的往上一级，带有其自己的 `__init __.py` 等文件的某个包。但是我们并没有这个包。因此，这将在我们的示例中引发错误。🚨

但是现在你知道了它的工作原理，因此无论它们多么复杂，你都可以在自己的应用程序中使用相对导入。🤓

### 添加一些自定义的 `tags`、`responses` 和 `dependencies` { #add-some-custom-tags-responses-and-dependencies }

我们不打算在每个*路径操作*中添加前缀 `/items` 或 `tags =["items"]`，因为我们将它们添加到了 `APIRouter` 中。

但是我们仍然可以添加*更多*将会应用于特定的*路径操作*的 `tags`，以及一些特定于该*路径操作*的额外 `responses`：

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | 提示

最后的这个路径操作将包含标签的组合：`["items", "custom"]`。

并且在文档中也会有两个响应，一个用于 `404`，一个用于 `403`。

///

## `FastAPI` 主体 { #the-main-fastapi }

现在，让我们来看看位于 `app/main.py` 的模块。

在这里你导入并使用 `FastAPI` 类。

这将是你的应用程序中将所有内容联结在一起的主文件。

并且由于你的大部分逻辑现在都存在于其自己的特定模块中，因此主文件的内容将非常简单。

### 导入 `FastAPI` { #import-fastapi }

你可以像平常一样导入并创建一个 `FastAPI` 类。

我们甚至可以声明[全局依赖项](dependencies/global-dependencies.md)，它会和每个 `APIRouter` 的依赖项组合在一起：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### 导入 `APIRouter` { #import-the-apirouter }

现在，我们导入具有 `APIRouter` 的其他子模块：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

由于文件 `app/routers/users.py` 和 `app/routers/items.py` 是同一 Python 包 `app` 一个部分的子模块，因此我们可以使用单个点 ` .` 通过「相对导入」来导入它们。

### 导入是如何工作的 { #how-the-importing-works }

这段代码：

```Python
from .routers import items, users
```

表示：

* 从该模块（`app/main.py` 文件）所在的同一个包（`app/` 目录）开始...
* 寻找 `routers` 子包（位于 `app/routers/` 的目录）...
* 从该包中，导入子模块 `items` (位于 `app/routers/items.py` 的文件) 以及 `users` (位于 `app/routers/users.py` 的文件)...

`items` 模块将具有一个 `router` 变量（`items.router`）。这与我们在 `app/routers/items.py` 文件中创建的变量相同，它是一个 `APIRouter` 对象。

然后我们对 `users` 模块进行相同的操作。

我们也可以像这样导入它们：

```Python
from app.routers import items, users
```

/// note | 注意

第一个版本是「相对导入」：

```Python
from .routers import items, users
```

第二个版本是「绝对导入」：

```Python
from app.routers import items, users
```

要了解有关 Python 包和模块的更多信息，请查阅[关于 Modules 的 Python 官方文档](https://docs.python.org/3/tutorial/modules.html)。

///

### 避免名称冲突 { #avoid-name-collisions }

我们将直接导入 `items` 子模块，而不是仅导入其 `router` 变量。

这是因为我们在 `users` 子模块中也有另一个名为 `router` 的变量。

如果我们一个接一个地导入，例如：

```Python
from .routers.items import router
from .routers.users import router
```

来自 `users` 的 `router` 将覆盖来自 `items` 中的 `router`，我们将无法同时使用它们。

因此，为了能够在同一个文件中使用它们，我们直接导入子模块：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### 包含 `users` 和 `items` 的 `APIRouter` { #include-the-apirouters-for-users-and-items }

现在，让我们来包含来自 `users` 和 `items` 子模块的 `router`。

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// note | 注意

`users.router` 包含了 `app/routers/users.py` 文件中的 `APIRouter`。

`items.router` 包含了 `app/routers/items.py` 文件中的 `APIRouter`。

///

使用 `app.include_router()`，我们可以将每个 `APIRouter` 添加到主 `FastAPI` 应用程序中。

它将包含来自该路由器的所有路由作为其一部分。

/// note | 技术细节

当在主应用中包含路由器时，FastAPI 会保留原始的 `APIRouter` 及其 `APIRoute` 处于活动状态。

这意味着自定义的 `APIRouter` 和 `APIRoute` 子类在被包含之后仍然能够参与工作。

///

/// tip | 提示

包含路由器时，你不必担心性能问题。

这被设计为轻量级的，并且避免给每个请求增加开销。

因此，它不会影响性能。⚡

///

### 包含一个有自定义 `prefix`、`tags`、`responses` 和 `dependencies` 的 `APIRouter` { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

现在，假设你的组织为你提供了 `app/internal/admin.py` 文件。

它包含一个带有一些由你的组织在多个项目之间共享的管理员*路径操作*的 `APIRouter`。

对于此示例，它将非常简单。但是假设由于它是与组织中的其他项目所共享的，因此我们无法对其进行修改，以及直接在 `APIRouter` 中添加 `prefix`、`dependencies`、`tags` 等：

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

但是我们仍然希望在包含 `APIRouter` 时设置一个自定义的 `prefix`，以便其所有*路径操作*以 `/admin` 开头，我们希望使用本项目已经有的 `dependencies` 保护它，并且我们希望它包含自定义的 `tags` 和 `responses`。

我们可以通过将这些参数传递给 `app.include_router()` 来完成所有的声明，而不必修改原始的 `APIRouter`：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

这样，原始的 `APIRouter` 将保持不变，因此我们仍然可以与组织中的其他项目共享相同的 `app/internal/admin.py` 文件。

结果是在我们的应用程序中，来自 `admin` 模块的每个*路径操作*都将具有：

* `/admin` 前缀 。
* `admin` 标签。
* `get_token_header` 依赖项。
* `418` 响应。 🍵

但这只会影响我们应用中的 `APIRouter`，而不会影响使用它的任何其他代码。

因此，举例来说，其他项目能够以不同的身份认证方法使用相同的 `APIRouter`。

### 包含一个*路径操作* { #include-a-path-operation }

我们还可以直接将*路径操作*添加到 `FastAPI` 应用中。

这里我们这样做了...只是为了表明我们可以做到🤷：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

它将与通过 `app.include_router()` 添加的所有其他*路径操作*一起正常运行。

/// note | 非常技术细节

**注意**：这是一个非常技术性的细节，你也许可以**直接跳过**。

---

`APIRouter` 并不是「挂载」的，它们并没有和应用程序的其余部分隔离。

这是因为我们希望在 OpenAPI 模式和用户界面中包含它们的*路径操作*。

FastAPI 会保留原始的路由器和路径操作处于活动状态，并在处理请求和生成 OpenAPI 时组合路由器的前缀、依赖项、标签、响应以及其他元数据。

///

## 在 `pyproject.toml` 中配置 `entrypoint` { #configure-the-entrypoint-in-pyproject-toml }

因为你的 FastAPI `app` 对象位于 `app/main.py` 中，你可以在 `pyproject.toml` 中这样配置 `entrypoint`：

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

等价于像这样导入：

```python
from app.main import app
```

这样 `fastapi` 命令就知道到哪里去找到你的应用了。

/// Note | 注意

你也可以把路径传给命令，比如：

```console
$ fastapi dev app/main.py
```

但是每次调用 `fastapi` 命令时，你都需要记得传入正确的路径。

另外，其他工具可能找不到它，比如 [VS Code 扩展](../editor-support.md) 或 [FastAPI Cloud](https://fastapicloud.com)，因此推荐在 `pyproject.toml` 中使用 `entrypoint`。

///

## 查看自动化的 API 文档 { #check-the-automatic-api-docs }

现在，运行你的应用：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后打开位于 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 的文档。

你将看到使用了正确路径（和前缀）和正确标签的自动化 API 文档，包括了来自所有子模块的路径：

<img src="/img/tutorial/bigger-applications/image01.png">

## 多次使用不同的 `prefix` 包含同一个路由器 { #include-the-same-router-multiple-times-with-different-prefix }

你也可以在*同一*路由器上使用不同的前缀来多次使用 `.include_router()`。

在有些场景这可能有用，例如以不同的前缀公开同一个的 API，比方说 `/api/v1` 和 `/api/latest`。

这是一个你可能并不真正需要的高级用法，但万一你有需要了就能够用上。

## 在另一个 `APIRouter` 中包含一个 `APIRouter` { #include-an-apirouter-in-another }

与在 `FastAPI` 应用程序中包含 `APIRouter` 的方式相同，你也可以在另一个 `APIRouter` 中包含 `APIRouter`，通过：

```Python
router.include_router(other_router)
```

你可以在将 `router` 包含到 `FastAPI` 应用之前或之后执行此操作。FastAPI 仍然会在路由和 OpenAPI 中包含 `other_router` 中的*路径操作*。

同样适用于之后添加到这些路由器的*路径操作*。它们也会通过先前的包含可见。

/// warning | 技术细节

在包含路由器之后，避免直接修改 `router.routes`。FastAPI 将路由器的包含视为「实时」的，因此原始路由器及其路由会继续参与路由和 OpenAPI 生成。

使用文档化的 API（例如路径操作装饰器和 `.include_router()`）来添加路由和路由器。

将 `router.routes` 视为较低层级的路由树，它可以包含路由定义和被包含的路由器；避免把它当作最终路径操作的扁平列表来依赖。

///



---

# Source: docs/tutorial/body.md


# 请求体 { #request-body }

当你需要从客户端（比如浏览器）向你的 API 发送数据时，会把它作为**请求体**发送。

**请求体**是客户端发送给你的 API 的数据。**响应体**是你的 API 发送给客户端的数据。

你的 API 几乎总是需要发送**响应体**。但客户端不一定总是要发送**请求体**，有时它们只请求某个路径，可能带一些查询参数，但不会发送请求体。

使用 [Pydantic](https://docs.pydantic.dev/) 模型来声明**请求体**，能充分利用它的功能和优点。

/// note | 注意

发送数据应使用以下之一：`POST`（最常见）、`PUT`、`DELETE` 或 `PATCH`。

规范中没有定义用 `GET` 请求发送请求体的行为，但 FastAPI 仍支持这种方式，只用于非常复杂/极端的用例。

由于不推荐，在使用 `GET` 时，Swagger UI 的交互式文档不会显示请求体的文档，而且中间的代理可能也不支持它。

///

## 导入 Pydantic 的 `BaseModel` { #import-pydantics-basemodel }

首先，你需要从 `pydantic` 中导入 `BaseModel`：

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## 创建数据模型 { #create-your-data-model }

然后，把数据模型声明为继承 `BaseModel` 的类。

使用 Python 标准类型声明所有属性：

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


与声明查询参数一样，包含默认值的模型属性是可选的，否则就是必选的。把默认值设为 `None` 可使其变为可选。

例如，上述模型声明如下 JSON "`object`"（即 Python `dict`）：

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...由于 `description` 和 `tax` 是可选的（默认值为 `None`），下面的 JSON "`object`" 也有效：

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 声明为参数 { #declare-it-as-a-parameter }

使用与声明路径和查询参数相同的方式，把它添加至*路径操作*：

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...并把其类型声明为你创建的模型 `Item`。

## 结果 { #results }

仅使用这些 Python 类型声明，**FastAPI** 就可以：

* 以 JSON 形式读取请求体。
* （在必要时）把请求体转换为对应的类型。
* 校验数据。
    * 数据无效时返回清晰的错误信息，并指出错误数据的确切位置和内容。
* 把接收的数据赋值给参数 `item`。
    * 因为你把函数中的参数类型声明为 `Item`，所以还能获得所有属性及其类型的编辑器支持（补全等）。
* 为你的模型生成 [JSON Schema](https://json-schema.org) 定义，如果对你的项目有意义，还可以在其他地方使用它们。
* 这些 schema 会成为生成的 OpenAPI Schema 的一部分，并被自动文档的 <abbr title="User Interfaces - 用户界面">UIs</abbr> 使用。

## 自动文档 { #automatic-docs }

你的模型的 JSON Schema 会成为生成的 OpenAPI Schema 的一部分，并显示在交互式 API 文档中：

<img src="/img/tutorial/body/image01.png">

并且，还会用于需要它们的每个*路径操作*的 API 文档中：

<img src="/img/tutorial/body/image02.png">

## 编辑器支持 { #editor-support }

在编辑器中，函数内部你会在各处得到类型提示与补全（如果接收的不是 Pydantic 模型，而是 `dict`，就不会有这样的支持）：

<img src="/img/tutorial/body/image03.png">

还支持检查错误的类型操作：

<img src="/img/tutorial/body/image04.png">

这并非偶然，整个框架都是围绕这种设计构建的。

并且在设计阶段、实现之前就进行了全面测试，以确保它能在所有编辑器中正常工作。

我们甚至对 Pydantic 本身做了一些改动以支持这些功能。

上面的截图来自 [Visual Studio Code](https://code.visualstudio.com)。

但使用 [PyCharm](https://www.jetbrains.com/pycharm/) 和大多数其他 Python 编辑器，你也会获得相同的编辑器支持：

<img src="/img/tutorial/body/image05.png">

/// tip | 提示

如果你使用 [PyCharm](https://www.jetbrains.com/pycharm/) 作为编辑器，可以使用 [Pydantic PyCharm 插件](https://github.com/koxudaxi/pydantic-pycharm-plugin/)。

它能改进对 Pydantic 模型的编辑器支持，包括：

* 自动补全
* 类型检查
* 代码重构
* 查找
* 代码审查

///

## 使用模型 { #use-the-model }

在函数内部直接访问模型对象的所有属性：

{* ../../docs_src/body/tutorial002_py310.py *}

## 请求体 + 路径参数 { #request-body-path-parameters }

可以同时声明路径参数和请求体。

**FastAPI** 能识别与**路径参数**匹配的函数参数应该**从路径中获取**，而声明为 Pydantic 模型的函数参数应该**从请求体中获取**。

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## 请求体 + 路径 + 查询参数 { #request-body-path-query-parameters }

也可以同时声明**请求体**、**路径**和**查询**参数。

**FastAPI** 会分别识别它们，并从正确的位置获取数据。

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

函数参数按如下规则进行识别：

* 如果该参数也在**路径**中声明了，它就是路径参数。
* 如果该参数是（`int`、`float`、`str`、`bool` 等）**单一类型**，它会被当作**查询**参数。
* 如果该参数的类型声明为 **Pydantic 模型**，它会被当作请求**体**。

/// note | 注意

FastAPI 会根据默认值 `= None` 知道 `q` 的值不是必填的。

`str | None` 并不是 FastAPI 用来判断是否必填的依据；是否必填由是否有默认值 `= None` 决定。

但添加这些类型注解可以让你的编辑器提供更好的支持并检测错误。

///

## 不使用 Pydantic { #without-pydantic }

即便不使用 Pydantic 模型也能使用 **Body** 参数。详见[请求体 - 多参数：请求体中的单值](body-multiple-params.md#singular-values-in-body)。



---

# Source: docs/tutorial/body-fields.md


# 请求体 - 字段 { #body-fields }

与在*路径操作函数*中使用 `Query`、`Path` 、`Body` 声明校验与元数据的方式一样，可以使用 Pydantic 的 `Field` 在 Pydantic 模型内部声明校验和元数据。

## 导入 `Field` { #import-field }

首先，从 Pydantic 中导入 `Field`：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}

/// warning | 警告

注意，与从 `fastapi` 导入 `Query`，`Path`、`Body` 不同，要直接从 `pydantic` 导入 `Field` 。

///

## 声明模型属性 { #declare-model-attributes }

然后，使用 `Field` 定义模型的属性：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` 的工作方式和 `Query`、`Path`、`Body` 相同，参数也相同。

/// note | 技术细节

实际上，`Query`、`Path` 以及你接下来会看到的其它对象，会创建公共 `Param` 类的子类的对象，而 `Param` 本身是 Pydantic 中 `FieldInfo` 的子类。

Pydantic 的 `Field` 返回也是 `FieldInfo` 的类实例。

`Body` 直接返回的也是 `FieldInfo` 的子类的对象。后文还会介绍一些 `Body` 的子类。

注意，从 `fastapi` 导入的 `Query`、`Path` 等对象实际上都是返回特殊类的函数。

///

/// tip | 提示

注意，模型属性的类型、默认值及 `Field` 的代码结构与*路径操作函数*的参数相同，只不过是用 `Field` 替换了`Path`、`Query`、`Body`。

///

## 添加更多信息 { #add-extra-information }

`Field`、`Query`、`Body` 等对象里可以声明更多信息，并且 JSON Schema 中也会集成这些信息。

*声明示例*一章中将详细介绍添加更多信息的知识。

/// warning | 警告

传递给 `Field` 的额外键也会出现在你的应用生成的 OpenAPI 架构中。
由于这些键不一定属于 OpenAPI 规范的一部分，某些 OpenAPI 工具（例如 [OpenAPI 验证器](https://validator.swagger.io/)）可能无法处理你生成的架构。

///

## 小结 { #recap }

Pydantic 的 `Field` 可以为模型属性声明更多校验和元数据。

传递 JSON Schema 元数据还可以使用更多关键字参数。



---

# Source: docs/tutorial/body-multiple-params.md


# 请求体 - 多个参数 { #body-multiple-parameters }

既然我们已经知道了如何使用 `Path` 和 `Query`，下面让我们来了解一下请求体声明的更高级用法。

## 混合使用 `Path`、`Query` 和请求体参数 { #mix-path-query-and-body-parameters }

首先，毫无疑问地，你可以随意地混合使用 `Path`、`Query` 和请求体参数声明，**FastAPI** 会知道该如何处理。

你还可以通过将默认值设置为 `None` 来将请求体参数声明为可选参数：

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | 注意

请注意，在这种情况下，将从请求体获取的 `item` 是可选的。因为它的默认值为 `None`。

///

## 多个请求体参数 { #multiple-body-parameters }

在上面的示例中，*路径操作*将期望一个具有 `Item` 的属性的 JSON 请求体，就像：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

但是你也可以声明多个请求体参数，例如 `item` 和 `user`：

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

在这种情况下，**FastAPI** 将注意到该函数中有多个请求体参数（两个 Pydantic 模型参数）。

因此，它将使用参数名称作为请求体中的键（字段名称），并期望一个类似于以下内容的请求体：

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | 注意

请注意，即使 `item` 的声明方式与之前相同，但现在它被期望通过 `item` 键内嵌在请求体中。

///

**FastAPI** 将自动对请求中的数据进行转换，因此 `item` 参数将接收指定的内容，`user` 参数也是如此。

它将执行对复合数据的校验，并且像现在这样为 OpenAPI 模式和自动化文档对其进行记录。

## 请求体中的单一值 { #singular-values-in-body }

与使用 `Query` 和 `Path` 为查询参数和路径参数定义额外数据的方式相同，**FastAPI** 提供了一个同等的 `Body`。

例如，为了扩展先前的模型，你可能决定除了 `item` 和 `user` 之外，还想在同一请求体中具有另一个键 `importance`。

如果你就按原样声明它，因为它是一个单一值，**FastAPI** 将假定它是一个查询参数。

但是你可以使用 `Body` 指示 **FastAPI** 将其作为请求体的另一个键进行处理。

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

在这种情况下，**FastAPI** 将期望像这样的请求体：

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

同样的，它将转换数据类型，校验，生成文档等。

## 多个请求体参数和查询参数 { #multiple-body-params-and-query }

当然，除了请求体参数外，你还可以在任何需要的时候声明额外的查询参数。

由于默认情况下单一值会被解释为查询参数，因此你不必显式地添加 `Query`，你可以这样写：

```Python
q: str | None = None
```

比如：

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// note | 注意

`Body` 同样具有与 `Query`、`Path` 以及其他后面将看到的类完全相同的额外校验和元数据参数。

///

## 嵌入单个请求体参数 { #embed-a-single-body-parameter }

假设你只有一个来自 Pydantic 模型 `Item` 的请求体参数 `item`。

默认情况下，**FastAPI** 将直接期望这样的请求体。

但是，如果你希望它期望一个拥有 `item` 键并在值中包含模型内容的 JSON，就像在声明额外的请求体参数时所做的那样，则可以使用一个特殊的 `Body` 参数 `embed`：

```Python
item: Annotated[Item, Body(embed=True)]
```

比如：

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

在这种情况下，**FastAPI** 将期望像这样的请求体：

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

而不是：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## 总结 { #recap }

你可以添加多个请求体参数到*路径操作函数*中，即使一个请求只能有一个请求体。

但是 **FastAPI** 会处理它，在函数中为你提供正确的数据，并在*路径操作*中校验并记录正确的模式。

你还可以声明将作为请求体的一部分所接收的单一值。

你还可以指示 **FastAPI** 在仅声明了一个请求体参数的情况下，将原本的请求体嵌入到一个键中。



---

# Source: docs/tutorial/body-nested-models.md


# 请求体 - 嵌套模型 { #body-nested-models }

使用 **FastAPI**，你可以定义、校验、记录文档并使用任意深度嵌套的模型（归功于Pydantic）。

## List 字段 { #list-fields }

你可以将一个属性定义为一个子类型。例如，Python `list`：

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

这将使 `tags` 成为一个由元素组成的列表。不过它没有声明每个元素的类型。

## 带类型参数的 List 字段 { #list-fields-with-type-parameter }

不过，Python 有一种用于声明具有内部类型（类型参数）的列表的特定方式：

### 声明带类型参数的 `list` { #declare-a-list-with-a-type-parameter }

要声明具有类型参数（内部类型）的类型，例如 `list`、`dict`、`tuple`，使用方括号 `[` 和 `]` 传入内部类型作为「类型参数」：

```Python
my_list: list[str]
```

这完全是用于类型声明的标准 Python 语法。

对具有内部类型的模型属性也使用相同的标准语法。

因此，在我们的示例中，我们可以将 `tags` 明确地指定为一个「字符串列表」：

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Set 类型 { #set-types }

但是随后我们考虑了一下，意识到标签不应该重复，它们很大可能会是唯一的字符串。

而 Python 有一种用于保存唯一元素集合的特殊数据类型 `set`。

然后我们可以将 `tags` 声明为一个由字符串组成的 set：

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

这样，即使你收到带有重复数据的请求，这些数据也会被转换为一组唯一项。

而且，每当你输出该数据时，即使源数据有重复，它们也将作为一组唯一项输出。

并且还会被相应地标注 / 记录文档。

## 嵌套模型 { #nested-models }

Pydantic 模型的每个属性都具有类型。

但是这个类型本身可以是另一个 Pydantic 模型。

因此，你可以声明拥有特定属性名称、类型和校验的深度嵌套的 JSON 对象。

上述这些都可以任意的嵌套。

### 定义子模型 { #define-a-submodel }

例如，我们可以定义一个 `Image` 模型：

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### 将子模型用作类型 { #use-the-submodel-as-a-type }

然后我们可以将其用作一个属性的类型：

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

这意味着 **FastAPI** 将期望类似于以下内容的请求体：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

再一次，仅仅进行这样的声明，你将通过 **FastAPI** 获得：

* 对被嵌入的模型也适用的编辑器支持（自动补全等）
* 数据转换
* 数据校验
* 自动生成文档

## 特殊的类型和校验 { #special-types-and-validation }

除了普通的单一值类型（如 `str`、`int`、`float` 等）外，你还可以使用从 `str` 继承的更复杂的单一值类型。

要了解所有的可用选项，请查看 [Pydantic 的类型概览](https://docs.pydantic.dev/latest/concepts/types/)。你将在下一章节中看到一些示例。

例如，在 `Image` 模型中我们有一个 `url` 字段，我们可以把它声明为 Pydantic 的 `HttpUrl`，而不是 `str`：

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

该字符串将被检查是否为有效的 URL，并在 JSON Schema / OpenAPI 文档中进行记录。

## 带有一组子模型的属性 { #attributes-with-lists-of-submodels }

你还可以将 Pydantic 模型用作 `list`、`set` 等的子类型：

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

这将期望（转换，校验，记录文档等）下面这样的 JSON 请求体：

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// note | 注意

请注意 `images` 键现在具有一个 image 对象列表是如何发生的。

///

## 深度嵌套模型 { #deeply-nested-models }

你可以定义任意深度的嵌套模型：

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// note | 注意

请注意 `Offer` 拥有一个 `Item` 列表，而反过来 `Item` 又有一个可选的 `Image` 列表是如何发生的。

///

## 纯列表请求体 { #bodies-of-pure-lists }

如果你期望的 JSON 请求体的最外层是一个 JSON `array`（即 Python `list`），则可以在路径操作函数的参数中声明此类型，就像声明 Pydantic 模型一样：

```Python
images: list[Image]
```

例如：

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## 无处不在的编辑器支持 { #editor-support-everywhere }

你可以随处获得编辑器支持。

即使是列表中的元素：

<img src="/img/tutorial/body-nested-models/image01.png">

如果你直接使用 `dict` 而不是 Pydantic 模型，那你将无法获得这种编辑器支持。

但是你根本不必担心这两者，传入的字典会自动被转换，你的输出也会自动被转换为 JSON。

## 任意 `dict` 构成的请求体 { #bodies-of-arbitrary-dicts }

你也可以将请求体声明为使用某类型的键和其他类型值的 `dict`。

无需事先知道有效的字段/属性（在使用 Pydantic 模型的场景）名称是什么。

如果你想接收一些尚且未知的键，这将很有用。

---

其他有用的场景是当你想要接收其他类型的键时，例如 `int`。

这也是我们在接下来将看到的。

在下面的例子中，你将接受任意键为 `int` 类型并且值为 `float` 类型的 `dict`：

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip | 提示

请记住 JSON 仅支持将 `str` 作为键。

但是 Pydantic 具有自动转换数据的功能。

这意味着，即使你的 API 客户端只能将字符串作为键发送，只要这些字符串内容仅包含整数，Pydantic 就会对其进行转换并校验。

然后你接收的名为 `weights` 的 `dict` 实际上将具有 `int` 类型的键和 `float` 类型的值。

///

## 总结 { #recap }

使用 **FastAPI** 你可以拥有 Pydantic 模型提供的极高灵活性，同时保持代码的简单、简短和优雅。

而且还具有下列好处：

* 编辑器支持（处处皆可自动补全！）
* 数据转换（也被称为解析/序列化）
* 数据校验
* 模式文档
* 自动生成的文档



---

# Source: docs/tutorial/body-updates.md


# 请求体 - 更新数据 { #body-updates }

## 用 `PUT` 替换式更新 { #update-replacing-with-put }

更新数据可以使用 [HTTP `PUT`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT) 操作。

把输入数据转换为以 JSON 格式存储的数据（比如，使用 NoSQL 数据库时），可以使用 `jsonable_encoder`。例如，把 `datetime` 转换为 `str`。

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` 用于接收替换现有数据的数据。

### 关于替换的警告 { #warning-about-replacing }

用 `PUT` 把数据项 `bar` 更新为以下请求体时：

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

因为其中未包含已存储的属性 `"tax": 20.2`，输入模型会取 `"tax": 10.5` 的默认值。

因此，保存的数据会带有这个“新的” `tax` 值 `10.5`。

## 用 `PATCH` 进行部分更新 { #partial-updates-with-patch }

也可以使用 [HTTP `PATCH`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH) 操作对数据进行*部分*更新。

也就是说，你只需发送想要更新的数据，其余数据保持不变。

/// note | 注意

`PATCH` 没有 `PUT` 知名，也没那么常用。

很多团队甚至只用 `PUT` 实现部分更新。

你可以**随意**选择如何使用它们，**FastAPI** 不做任何限制。

但本指南会大致展示它们的预期用法。

///

### 使用 Pydantic 的 `exclude_unset` 参数 { #using-pydantics-exclude-unset-parameter }

如果要接收部分更新，建议在 Pydantic 模型的 `.model_dump()` 中使用 `exclude_unset` 参数。

比如，`item.model_dump(exclude_unset=True)`。

这会生成一个 `dict`，只包含创建 `item` 模型时显式设置的数据，不包含默认值。

然后再用它生成一个只含已设置（在请求中发送）数据、且省略默认值的 `dict`：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### 使用 Pydantic 的 `update` 参数 { #using-pydantics-update-parameter }

接下来，用 `.model_copy()` 为已有模型创建副本，并传入 `update` 参数，值为包含更新数据的 `dict`。

例如，`stored_item_model.model_copy(update=update_data)`：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### 部分更新小结 { #partial-updates-recap }

简而言之，应用部分更新应当：

* （可选）使用 `PATCH` 而不是 `PUT`。
* 提取已存储的数据。
* 把该数据放入 Pydantic 模型。
* 生成不含输入模型默认值的 `dict`（使用 `exclude_unset`）。
    * 这样只会更新用户实际设置的值，而不会用模型中的默认值覆盖已存储的值。
* 为已存储的模型创建副本，用接收到的部分更新数据更新其属性（使用 `update` 参数）。
* 把模型副本转换为可存入数据库的形式（比如，使用 `jsonable_encoder`）。
    * 这类似于再次调用模型的 `.model_dump()` 方法，但会确保（并转换）值为可转换为 JSON 的数据类型，例如把 `datetime` 转换为 `str`。
* 把数据保存至数据库。
* 返回更新后的模型。

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | 提示

实际上，HTTP `PUT` 也可以使用同样的技巧。

但这里用 `PATCH` 举例，因为它就是为这种用例设计的。

///

/// note | 注意

注意，输入模型仍会被验证。

因此，如果希望接收的部分更新可以省略所有属性，则需要一个所有属性都标记为可选（带默认值或 `None`）的模型。

为了区分用于**更新**（全部可选）和用于**创建**（必填）的模型，可以参考[更多模型](extra-models.md) 中介绍的思路。

///



---

# Source: docs/tutorial/cookie-param-models.md


# Cookie 参数模型 { #cookie-parameter-models }

如果你有一组相关的 **cookie**，你可以创建一个 **Pydantic 模型**来声明它们。🍪

这将允许你在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证方式和元数据。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

/// tip | 提示

此技术同样适用于 `Query` 、 `Cookie` 和 `Header` 。😎

///

## 带有 Pydantic 模型的 Cookie { #cookies-with-a-pydantic-model }

在 **Pydantic** 模型中声明所需的 **cookie** 参数，然后将参数声明为 `Cookie` ：

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** 将从请求中接收到的 **cookie** 中**提取**出**每个字段**的数据，并提供你定义的 Pydantic 模型。

## 查看文档 { #check-the-docs }

你可以在文档 UI 的 `/docs` 中查看定义的 cookie：

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | 注意

请记住，由于**浏览器**以特殊方式**处理 cookie**，并在后台进行操作，因此它们**不会**轻易允许 **JavaScript** 访问这些 cookie。

如果你访问 `/docs` 的 **API 文档 UI**，你将能够查看你*路径操作*的 cookie **文档**。

但是即使你**填写数据**并点击“执行”，由于文档界面使用 **JavaScript**，cookie 将不会被发送。而你会看到一条**错误**消息，就好像你没有输入任何值一样。

///

## 禁止额外的 Cookie { #forbid-extra-cookies }

在某些特殊使用情况下（可能并不常见），你可能希望**限制**你想要接收的 cookie。

你的 API 现在可以控制自己的 <dfn title="只是个玩笑，别当真。和 cookie 同意无关，不过连 API 现在都能拒绝可怜的 cookie，挺好玩的。来，吃块小饼干吧。🍪">cookie 同意</dfn>。🤪🍪

你可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

如果客户端尝试发送一些**额外的 cookie**，他们将收到**错误**响应。

可怜的 cookie 通知条，费尽心思为了获得你的同意，却被<dfn title="又是个玩笑，别理我。给你的小饼干配点咖啡吧。☕">API 拒绝了</dfn>。🍪

例如，如果客户端尝试发送一个值为 `good-list-please` 的 `santa_tracker` cookie，客户端将收到一个**错误**响应，告知他们 `santa_tracker` <dfn title="圣诞老人不赞成没有小饼干。🎅 好吧，不再讲 cookie 的笑话了。">cookie 是不允许的</dfn>：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## 总结 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中声明 <dfn title="临走前再吃一块小饼干吧。🍪">**cookie**</dfn>。😎



---

# Source: docs/tutorial/cookie-params.md


# Cookie 参数 { #cookie-parameters }

定义 `Cookie` 参数与定义 `Query` 和 `Path` 参数一样。

## 导入 `Cookie` { #import-cookie }

首先，导入 `Cookie`：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## 声明 `Cookie` 参数 { #declare-cookie-parameters }

声明 `Cookie` 参数的方式与声明 `Query` 和 `Path` 参数相同。

你可以定义默认值，以及所有额外的验证或注解参数：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 技术细节

`Cookie` 、`Path` 、`Query` 是**兄弟类**，都继承自共用的 `Param` 类。

注意，从 `fastapi` 导入的 `Query`、`Path`、`Cookie` 等对象，实际上是返回特殊类的函数。

///

/// note | 注意

必须使用 `Cookie` 声明 cookie 参数，否则该参数会被解释为查询参数。

///

/// note | 注意

请注意，由于**浏览器会以特殊方式并在幕后处理 cookies**，它们**不会**轻易允许**JavaScript**访问它们。

如果你前往位于 `/docs` 的**API 文档界面**，你可以看到你的*路径操作*中有关 cookies 的**文档**。

但即使你**填写了数据**并点击 "Execute"，由于文档界面依赖于**JavaScript**工作，cookies 也不会被发送，你会看到一个**错误**消息，好像你没有填写任何值一样。

///

## 小结 { #recap }

使用 `Cookie` 声明 cookie 参数的方式与 `Query` 和 `Path` 相同。



---

# Source: docs/tutorial/cors.md


# CORS（跨域资源共享） { #cors-cross-origin-resource-sharing }

[CORS 或者「跨域资源共享」](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) 指浏览器中运行的前端拥有与后端通信的 JavaScript 代码，而后端处于与前端不同的「源」的情况。

## 源 { #origin }

源是协议（`http`，`https`）、域（`myapp.com`，`localhost`，`localhost.tiangolo.com`）以及端口（`80`、`443`、`8080`）的组合。

因此，这些都是不同的源：

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

即使它们都在 `localhost` 中，但是它们使用不同的协议或者端口，所以它们都是不同的「源」。

## 步骤 { #steps }

假设你的浏览器中有一个前端运行在 `http://localhost:8080`，并且它的 JavaScript 正在尝试与运行在 `http://localhost` 的后端通信（因为我们没有指定端口，浏览器会采用默认的端口 `80`）。

然后，浏览器会向 `:80` 的后端发送一个 HTTP `OPTIONS` 请求，如果后端发送适当的 headers 来授权来自这个不同源（`http://localhost:8080`）的通信，那么运行在 `:8080` 的浏览器就会允许前端中的 JavaScript 向 `:80` 的后端发送请求。

为此，`:80` 的后端必须有一个「允许的源」列表。

在这种情况下，它必须包含 `http://localhost:8080`，这样 `:8080` 的前端才能正常工作。

## 通配符 { #wildcards }

也可以使用 `"*"`（一个「通配符」）声明这个列表，表示全部都是允许的。

但这仅允许某些类型的通信，不包括所有涉及凭据的内容：比如 Cookies，以及那些使用 Bearer 令牌的 Authorization 请求头等。

因此，为了一切都能正常工作，最好显式地指定允许的源。

## 使用 `CORSMiddleware` { #use-corsmiddleware }

你可以在 **FastAPI** 应用中使用 `CORSMiddleware` 来配置它。

* 导入 `CORSMiddleware`。
* 创建一个允许的源列表（由字符串组成）。
* 将其作为「中间件」添加到你的 **FastAPI** 应用中。

你也可以指定后端是否允许：

* 凭证（Authorization 请求头、Cookies 等）。
* 特定的 HTTP 方法（`POST`，`PUT`）或者使用通配符 `"*"` 允许所有方法。
* 特定的 HTTP 请求头或者使用通配符 `"*"` 允许所有请求头。

{* ../../docs_src/cors/tutorial001_py310.py hl[2,6:11,13:19] *}

默认情况下，这个 `CORSMiddleware` 实现所使用的默认参数较为保守，所以你需要显式地启用特定的源、方法或者 headers，以便浏览器能够在跨域上下文中使用它们。

支持以下参数：

* `allow_origins` - 一个允许跨域请求的源列表。例如 `['https://example.org', 'https://www.example.org']`。你可以使用 `['*']` 允许任何源。
* `allow_origin_regex` - 一个正则表达式字符串，匹配的源允许跨域请求。例如 `'https://.*\.example\.org'`。
* `allow_methods` - 一个允许跨域请求的 HTTP 方法列表。默认为 `['GET']`。你可以使用 `['*']` 来允许所有标准方法。
* `allow_headers` - 一个允许跨域请求的 HTTP 请求头列表。默认为 `[]`。你可以使用 `['*']` 允许所有的请求头。`Accept`、`Accept-Language`、`Content-Language` 以及 `Content-Type` 这几个请求头在[简单 CORS 请求](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests)中总是被允许。
* `allow_credentials` - 指示跨域请求支持 cookies。默认是 `False`。

    当 `allow_credentials` 设为 `True` 时，`allow_origins`、`allow_methods` 和 `allow_headers` 都不能设为 `['*']`。它们必须[显式指定](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards)。

* `expose_headers` - 指示可以被浏览器访问的响应头。默认为 `[]`。
* `max_age` - 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 `600`。

中间件响应两种特定类型的 HTTP 请求...

### CORS 预检请求 { #cors-preflight-requests }

这是些带有 `Origin` 和 `Access-Control-Request-Method` 请求头的 `OPTIONS` 请求。

在这种情况下，中间件将拦截传入的请求并进行响应，出于提供信息的目的返回一个使用了适当的 CORS headers 的 `200` 或 `400` 响应。

### 简单请求 { #simple-requests }

任何带有 `Origin` 请求头的请求。在这种情况下，中间件将像平常一样传递请求，但是在响应中包含适当的 CORS headers。

## 更多信息 { #more-info }

更多关于 <abbr title="Cross-Origin Resource Sharing - 跨域资源共享">CORS</abbr> 的信息，请查看 [Mozilla CORS 文档](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)。

/// note | 技术细节

你也可以使用 `from starlette.middleware.cors import CORSMiddleware`。

出于方便，**FastAPI** 在 `fastapi.middleware` 中为开发者提供了几个中间件。但是大多数可用的中间件都是直接来自 Starlette。

///



---

# Source: docs/tutorial/debugging.md


# 调试 { #debugging }

你可以在编辑器中连接调试器，例如使用 Visual Studio Code 或 PyCharm。

## 调用 `uvicorn` { #call-uvicorn }

在你的 FastAPI 应用中直接导入 `uvicorn` 并运行：

{* ../../docs_src/debugging/tutorial001_py310.py hl[1,15] *}

### 关于 `__name__ == "__main__"` { #about-name-main }

`__name__ == "__main__"` 的主要目的是使用以下代码调用文件时执行一些代码：

<div class="termy">

```console
$ python myapp.py
```

</div>

而当其它文件导入它时并不会被调用，像这样：

```Python
from myapp import app
```

#### 更多细节 { #more-details }

假设你的文件命名为 `myapp.py`。

如果你这样运行：

<div class="termy">

```console
$ python myapp.py
```

</div>

那么文件中由 Python 自动创建的内部变量 `__name__`，会将字符串 `"__main__"` 作为值。

所以，这一段：

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

会运行。

---

如果你是导入这个模块（文件）就不会这样。

因此，如果你的另一个文件 `importer.py` 像这样：

```Python
from myapp import app

# 其他一些代码
```

在这种情况下，`myapp.py` 内部自动创建的变量 `__name__` 不会有值 `"__main__"`。

所以，这一行：

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

不会被执行。

/// note | 注意

更多信息请检查 [Python 官方文档](https://docs.python.org/3/library/__main__.html).

///

## 使用你的调试器运行代码 { #run-your-code-with-your-debugger }

由于是从代码直接运行的 Uvicorn 服务器，所以你可以从调试器直接调用 Python 程序（你的 FastAPI 应用）。

---

例如，你可以在 Visual Studio Code 中：

* 进入到「调试」面板。
* 「添加配置...」。
* 选中「Python」
* 使用选项 "`Python: Current File (Integrated Terminal)`" 运行调试器。

然后它会使用你的 **FastAPI** 代码开启服务器，停在断点处，等等。

看起来可能是这样：

<img src="/img/tutorial/debugging/image01.png">

---

如果使用 PyCharm，你可以：

* 打开「运行」菜单。
* 选中「调试...」。
* 然后出现一个上下文菜单。
* 选择要调试的文件（本例中的 `main.py`）。

然后它会使用你的 **FastAPI** 代码开启服务器，停在断点处，等等。

看起来可能是这样：

<img src="/img/tutorial/debugging/image02.png">



---

# Source: docs/tutorial/dependencies/classes-as-dependencies.md


# 类作为依赖项 { #classes-as-dependencies }

在深入探究 **依赖注入** 系统之前，让我们升级之前的例子。

## 来自前一个例子的`dict` { #a-dict-from-the-previous-example }

在前面的例子中, 我们从依赖项 ("可依赖对象") 中返回了一个 `dict`:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

但是后面我们在路径操作函数的参数 `commons` 中得到了一个 `dict`。

我们知道编辑器不能为 `dict` 提供很多支持(比如补全)，因为编辑器不知道 `dict` 的键和值类型。

对此，我们可以做的更好...

## 什么构成了依赖项 { #what-makes-a-dependency }

到目前为止，你看到的依赖项都被声明为函数。

但这并不是声明依赖项的唯一方法(尽管它可能是更常见的方法)。

关键因素是依赖项应该是 "可调用对象"。

Python 中的 "**可调用对象**" 是指任何 Python 可以像函数一样 "调用" 的对象。

所以，如果你有一个对象 `something` (可能*不是*一个函数)，你可以 "调用" 它(执行它)，就像：

```Python
something()
```

或者

```Python
something(some_argument, some_keyword_argument="foo")
```

这就是 "可调用对象"。

## 类作为依赖项 { #classes-as-dependencies_1 }

你可能会注意到，要创建一个 Python 类的实例，你可以使用相同的语法。

举个例子:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

在这个例子中, `fluffy` 是一个 `Cat` 类的实例。

为了创建 `fluffy`，你调用了 `Cat` 。

所以，Python 类也是 **可调用对象**。

因此，在 **FastAPI** 中，你可以使用一个 Python 类作为一个依赖项。

实际上 FastAPI 检查的是它是一个 "可调用对象"（函数，类或其他任何类型）以及定义的参数。

如果你在 **FastAPI** 中传递一个 "可调用对象" 作为依赖项，它将分析该 "可调用对象" 的参数，并以处理路径操作函数的参数的方式来处理它们。包括子依赖项。

这也适用于完全没有参数的可调用对象。这与不带参数的路径操作函数一样。

所以，我们可以将上面的依赖项 "可依赖对象" `common_parameters` 更改为类 `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

注意用于创建类实例的 `__init__` 方法：

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...它与我们以前的 `common_parameters` 具有相同的参数：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

这些参数就是 **FastAPI** 用来 "处理" 依赖项的。

在两个例子下，都有：

* 一个可选的 `q` 查询参数，是 `str` 类型。
* 一个 `skip` 查询参数，是 `int` 类型，默认值为 `0`。
* 一个 `limit` 查询参数，是 `int` 类型，默认值为 `100`。

在两个例子下，数据都将被转换、验证、在 OpenAPI schema 上文档化，等等。

## 使用它 { #use-it }

现在，你可以使用这个类来声明你的依赖项了。

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** 调用 `CommonQueryParams` 类。这将创建该类的一个 "实例"，该实例将作为参数 `commons` 被传递给你的函数。

## 类型注解 vs `Depends` { #type-annotation-vs-depends }

注意，我们在上面的代码中编写了两次`CommonQueryParams`：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 未使用 Annotated

/// tip | 提示

尽可能使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

最后的 `CommonQueryParams`:

```Python
... Depends(CommonQueryParams)
```

...实际上是 **FastAPI** 用来知道依赖项是什么的。

FastAPI 将从依赖项中提取声明的参数，这才是 FastAPI 实际调用的。

---

在本例中，第一个 `CommonQueryParams` ：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ 未使用 Annotated

/// tip | 提示

尽可能使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams ...
```

////

...对于 **FastAPI** 没有任何特殊的意义。FastAPI 不会使用它进行数据转换、验证等 (因为对于这，它使用 `Depends(CommonQueryParams)`)。

你实际上可以只这样编写:

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 未使用 Annotated

/// tip | 提示

尽可能使用 `Annotated` 版本。

///

```Python
commons = Depends(CommonQueryParams)
```

////

..就像:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

但是声明类型是被鼓励的，因为那样你的编辑器就会知道将传递什么作为参数 `commons` ，然后它可以帮助你完成代码，类型检查，等等：

<img src="/img/tutorial/dependencies/image02.png">

## 快捷方式 { #shortcut }

但是你可以看到，我们在这里有一些代码重复了，编写了`CommonQueryParams`两次：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 未使用 Annotated

/// tip | 提示

尽可能使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** 为这些情况提供了一个快捷方式，在这些情况下，依赖项 *明确地* 是一个类，**FastAPI** 将 "调用" 它来创建类本身的一个实例。

对于这些特定的情况，你可以按如下操作：

不是写成这样：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 未使用 Annotated

/// tip | 提示

尽可能使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...而是这样写:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ 未使用 Annotated

/// tip | 提示

尽可能使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends()
```

////

你声明依赖项作为参数的类型，并使用 `Depends()` 作为该函数的参数的 "默认" 值(在 `=` 之后)，而在 `Depends()` 中没有任何参数，而不是在 `Depends(CommonQueryParams)` 中*再次*编写完整的类。

同样的例子看起来像这样：

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

... **FastAPI** 会知道怎么处理。

/// tip | 提示

如果这看起来更加混乱而不是更加有帮助，那么请忽略它，你不*需要*它。

这只是一个快捷方式。因为 **FastAPI** 关心的是帮助你减少代码重复。

///



---

# Source: docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md


# 路径操作装饰器依赖项 { #dependencies-in-path-operation-decorators }

有时，我们并不需要在*路径操作函数*中使用依赖项的返回值。

或者说，有些依赖项不返回值。

但仍要执行或解析该依赖项。

对于这种情况，不必在声明*路径操作函数*的参数时使用 `Depends`，而是可以在*路径操作装饰器*中添加一个由 `dependencies` 组成的 `list`。

## 在*路径操作装饰器*中添加 `dependencies` 参数 { #add-dependencies-to-the-path-operation-decorator }

*路径操作装饰器*支持可选参数 `dependencies`。

该参数的值是由 `Depends()` 组成的 `list`：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

路径操作装饰器依赖项的执行或解析方式和普通依赖项一样，但就算这些依赖项会返回值，它们的值也不会传递给*路径操作函数*。

/// tip | 提示

有些编辑器会检查代码中没使用过的函数参数，并显示错误提示。

在*路径操作装饰器*中使用 `dependencies` 参数，可以确保在执行依赖项的同时，避免编辑器/工具报错。

使用路径装饰器依赖项还可以避免开发新人误会代码中包含无用的未使用参数。

///

/// note | 注意

本例中，使用的是自定义响应头 `X-Key` 和 `X-Token`。

但实际开发中，尤其是在实现安全措施时，最好使用 FastAPI 内置的[安全工具（下一章）](../security/index.md)。

///

## 依赖项错误和返回值 { #dependencies-errors-and-return-values }

路径装饰器依赖项也可以使用普通的依赖项*函数*。

### 依赖项的需求项 { #dependency-requirements }

路径装饰器依赖项可以声明请求的需求项（比如响应头）或其他子依赖项：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### 触发异常 { #raise-exceptions }

路径装饰器依赖项与正常的依赖项一样，可以 `raise` 异常：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### 返回值 { #return-values }

无论路径装饰器依赖项是否返回值，路径操作都不会使用这些值。

因此，可以复用在其他位置使用过的、（能返回值的）普通依赖项，即使没有使用这个值，也会执行该依赖项：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## 为一组路径操作定义依赖项 { #dependencies-for-a-group-of-path-operations }

稍后，[大型应用 - 多文件](../../tutorial/bigger-applications.md)一章中会介绍如何使用多个文件创建大型应用程序，在这一章中，您将了解到如何为一组*路径操作*声明单个 `dependencies` 参数。

## 全局依赖项 { #global-dependencies }

接下来，我们将学习如何为 `FastAPI` 应用程序添加全局依赖项，创建应用于每个*路径操作*的依赖项。



---

# Source: docs/tutorial/dependencies/dependencies-with-yield.md


# 使用 yield 的依赖项 { #dependencies-with-yield }

FastAPI 支持那些在完成后执行一些<dfn title="有时也称为：“退出代码”、“清理代码”、“拆卸代码”、“关闭代码”、“上下文管理器退出代码”等">额外步骤</dfn>的依赖项。

为此，使用 `yield` 而不是 `return`，并把这些额外步骤（代码）写在后面。

/// tip | 提示

确保在每个依赖里只使用一次 `yield`。

///

/// note | 技术细节

任何可以与以下装饰器一起使用的函数：

* [`@contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) 或
* [`@contextlib.asynccontextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager)

都可以作为 **FastAPI** 的依赖项。

实际上，FastAPI 在内部就是用的这两个装饰器。

///

## 使用 `yield` 的数据库依赖项 { #a-database-dependency-with-yield }

例如，你可以用这种方式创建一个数据库会话，并在完成后将其关闭。

在创建响应之前，只会执行 `yield` 语句及其之前的代码：

{* ../../docs_src/dependencies/tutorial007_py310.py hl[2:4] *}

`yield` 产生的值会注入到 *路径操作* 和其他依赖项中：

{* ../../docs_src/dependencies/tutorial007_py310.py hl[4] *}

`yield` 语句后面的代码会在响应之后执行：

{* ../../docs_src/dependencies/tutorial007_py310.py hl[5:6] *}

/// tip | 提示

你可以使用 `async` 或普通函数。

**FastAPI** 会像处理普通依赖一样对它们进行正确处理。

///

## 同时使用 `yield` 和 `try` 的依赖项 { #a-dependency-with-yield-and-try }

如果你在带有 `yield` 的依赖中使用了 `try` 代码块，那么当使用该依赖时抛出的任何异常你都会收到。

例如，如果在中间的某处代码中（在另一个依赖或在某个 *路径操作* 中）发生了数据库事务“回滚”或产生了其他异常，你会在你的依赖中收到这个异常。

因此，你可以在该依赖中用 `except SomeException` 来捕获这个特定异常。

同样地，你可以使用 `finally` 来确保退出步骤一定会被执行，无论是否发生异常。

{* ../../docs_src/dependencies/tutorial007_py310.py hl[3,5] *}

## 使用 `yield` 的子依赖项 { #sub-dependencies-with-yield }

你可以声明任意大小和形状的子依赖及其“树”，其中任意一个或全部都可以使用 `yield`。

**FastAPI** 会确保每个带有 `yield` 的依赖中的“退出代码”按正确的顺序运行。

例如，`dependency_c` 可以依赖 `dependency_b`，而 `dependency_b` 则依赖 `dependency_a`：

{* ../../docs_src/dependencies/tutorial008_an_py310.py hl[6,14,22] *}

并且它们都可以使用 `yield`。

在这种情况下，`dependency_c` 在执行其退出代码时需要 `dependency_b`（此处命名为 `dep_b`）的值仍然可用。

而 `dependency_b` 又需要 `dependency_a`（此处命名为 `dep_a`）的值在其退出代码中可用。

{* ../../docs_src/dependencies/tutorial008_an_py310.py hl[18:19,26:27] *}

同样地，你可以将一些依赖用 `yield`，另一些用 `return`，并让其中一些依赖依赖于另一些。

你也可以有一个依赖需要多个带有 `yield` 的依赖，等等。

你可以拥有任何你想要的依赖组合。

**FastAPI** 将确保一切都按正确的顺序运行。

/// note | 技术细节

这要归功于 Python 的[上下文管理器](https://docs.python.org/3/library/contextlib.html)。

**FastAPI** 在内部使用它们来实现这一点。

///

## 同时使用 `yield` 和 `HTTPException` 的依赖项 { #dependencies-with-yield-and-httpexception }

你已经看到可以在带有 `yield` 的依赖中使用 `try` 块尝试执行一些代码，然后在 `finally` 之后运行一些退出代码。

你也可以使用 `except` 来捕获引发的异常并对其进行处理。

例如，你可以抛出一个不同的异常，如 `HTTPException`。

/// tip | 提示

这是一种相对高级的技巧，在大多数情况下你并不需要使用它，因为你可以在应用的其他代码中（例如在 *路径操作函数* 里）抛出异常（包括 `HTTPException`）。

但是如果你需要，它就在这里。🤓

///

{* ../../docs_src/dependencies/tutorial008b_an_py310.py hl[18:22,31] *}

如果你想捕获异常并基于它创建一个自定义响应，请创建一个[自定义异常处理器](../handling-errors.md#install-custom-exception-handlers)。

## 同时使用 `yield` 和 `except` 的依赖项 { #dependencies-with-yield-and-except }

如果你在带有 `yield` 的依赖中使用 `except` 捕获了一个异常，并且你没有再次抛出它（或抛出一个新异常），FastAPI 将无法察觉发生过异常，就像普通的 Python 代码那样：

{* ../../docs_src/dependencies/tutorial008c_an_py310.py hl[15:16] *}

在这种情况下，客户端会像预期那样看到一个 *HTTP 500 Internal Server Error* 响应，因为我们没有抛出 `HTTPException` 或类似异常，但服务器将**没有任何日志**或其他关于错误是什么的提示。😱

### 在带有 `yield` 和 `except` 的依赖中务必 `raise` { #always-raise-in-dependencies-with-yield-and-except }

如果你在带有 `yield` 的依赖中捕获到了一个异常，除非你抛出另一个 `HTTPException` 或类似异常，**否则你应该重新抛出原始异常**。

你可以使用 `raise` 重新抛出同一个异常：

{* ../../docs_src/dependencies/tutorial008d_an_py310.py hl[17] *}

现在客户端仍会得到同样的 *HTTP 500 Internal Server Error* 响应，但服务器日志中会有我们自定义的 `InternalError`。😎

## 使用 `yield` 的依赖项的执行 { #execution-of-dependencies-with-yield }

执行顺序大致如下图所示。时间轴从上到下，每一列都代表交互或执行代码的一部分。

```mermaid
sequenceDiagram

participant client as Client
participant handler as Exception handler
participant dep as Dep with yield
participant operation as Path Operation
participant tasks as Background tasks

    Note over client,operation: Can raise exceptions, including HTTPException
    client ->> dep: Start request
    Note over dep: Run code up to yield
    opt raise Exception
        dep -->> handler: Raise Exception
        handler -->> client: HTTP error response
    end
    dep ->> operation: Run dependency, e.g. DB session
    opt raise
        operation -->> dep: Raise Exception (e.g. HTTPException)
        opt handle
            dep -->> dep: Can catch exception, raise a new HTTPException, raise other exception
        end
        handler -->> client: HTTP error response
    end

    operation ->> client: Return response to client
    Note over client,operation: Response is already sent, can't change it anymore
    opt Tasks
        operation -->> tasks: Send background tasks
    end
    opt Raise other exception
        tasks -->> tasks: Handle exceptions in the background task code
    end
```

/// note | 注意

只会向客户端发送**一次响应**。它可能是某个错误响应，或者是来自 *路径操作* 的响应。

在其中一个响应发送之后，就不能再发送其他响应了。

///

/// tip | 提示

如果你在 *路径操作函数* 的代码中引发任何异常，它都会被传递给带有 `yield` 的依赖项，包括 `HTTPException`。在大多数情况下，你会希望在带有 `yield` 的依赖中重新抛出相同的异常或一个新的异常，以确保它被正确处理。

///

## 提前退出与 `scope` { #early-exit-and-scope }

通常，带有 `yield` 的依赖的退出代码会在响应发送给客户端**之后**执行。

但如果你知道在从 *路径操作函数* 返回之后不再需要使用该依赖，你可以使用 `Depends(scope="function")` 告诉 FastAPI：应当在 *路径操作函数* 返回后、但在**响应发送之前**关闭该依赖。

{* ../../docs_src/dependencies/tutorial008e_an_py310.py hl[12,16] *}

`Depends()` 接收一个 `scope` 参数，可为：

* `"function"`：在处理请求的 *路径操作函数* 之前启动依赖，在 *路径操作函数* 结束后结束依赖，但在响应发送给客户端**之前**。因此，依赖函数将围绕这个*路径操作函数*执行。
* `"request"`：在处理请求的 *路径操作函数* 之前启动依赖（与使用 `"function"` 时类似），但在响应发送给客户端**之后**结束。因此，依赖函数将围绕这个**请求**与响应周期执行。

如果未指定且依赖包含 `yield`，则默认 `scope` 为 `"request"`。

### 子依赖的 `scope` { #scope-for-sub-dependencies }

当你声明一个 `scope="request"`（默认）的依赖时，任何子依赖也需要有 `"request"` 的 `scope`。

但一个 `scope` 为 `"function"` 的依赖可以有 `scope` 为 `"function"` 和 `"request"` 的子依赖。

这是因为任何依赖都需要能够在子依赖之前运行其退出代码，因为它的退出代码中可能还需要使用这些子依赖。

```mermaid
sequenceDiagram

participant client as Client
participant dep_req as Dep scope="request"
participant dep_func as Dep scope="function"
participant operation as Path Operation

    client ->> dep_req: Start request
    Note over dep_req: Run code up to yield
    dep_req ->> dep_func: Pass dependency
    Note over dep_func: Run code up to yield
    dep_func ->> operation: Run path operation with dependency
    operation ->> dep_func: Return from path operation
    Note over dep_func: Run code after yield
    Note over dep_func: ✅ Dependency closed
    dep_func ->> client: Send response to client
    Note over client: Response sent
    Note over dep_req: Run code after yield
    Note over dep_req: ✅ Dependency closed
```

## 包含 `yield`、`HTTPException`、`except` 和后台任务的依赖项 { #dependencies-with-yield-httpexception-except-and-background-tasks }

带有 `yield` 的依赖项随着时间演进以涵盖不同的用例并修复了一些问题。

如果你想了解在不同 FastAPI 版本中发生了哪些变化，可以在进阶指南中阅读更多：[高级依赖项 —— 包含 `yield`、`HTTPException`、`except` 和后台任务的依赖项](../../advanced/advanced-dependencies.md#dependencies-with-yield-httpexception-except-and-background-tasks)。

## 上下文管理器 { #context-managers }

### 什么是“上下文管理器” { #what-are-context-managers }

“上下文管理器”是你可以在 `with` 语句中使用的任意 Python 对象。

例如，[你可以用 `with` 来读取文件](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)：

```Python
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
```

在底层，`open("./somefile.txt")` 会创建一个“上下文管理器”对象。

当 `with` 代码块结束时，它会确保文件被关闭，即使期间发生了异常。

当你用 `yield` 创建一个依赖时，**FastAPI** 会在内部为它创建一个上下文管理器，并与其他相关工具结合使用。

### 在带有 `yield` 的依赖中使用上下文管理器 { #using-context-managers-in-dependencies-with-yield }

/// warning | 警告

这算是一个“高级”概念。

如果你刚开始使用 **FastAPI**，现在可以先跳过。

///

在 Python 中，你可以通过[创建一个带有 `__enter__()` 和 `__exit__()` 方法的类](https://docs.python.org/3/reference/datamodel.html#context-managers)来创建上下文管理器。

你也可以在 **FastAPI** 的带有 `yield` 的依赖中通过在依赖函数内部使用
`with` 或 `async with` 语句来使用它们：

{* ../../docs_src/dependencies/tutorial010_py310.py hl[1:9,13] *}

/// tip | 提示

另一种创建上下文管理器的方式是：

* [`@contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) 或
* [`@contextlib.asynccontextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager)

用它们去装饰一个只包含单个 `yield` 的函数。

这正是 **FastAPI** 在内部处理带有 `yield` 的依赖时所使用的方式。

但你不需要（也不应该）为 FastAPI 的依赖去使用这些装饰器。FastAPI 会在内部为你处理好。

///



---

# Source: docs/tutorial/dependencies/global-dependencies.md


# 全局依赖项 { #global-dependencies }

有时，我们要为整个应用添加依赖项。

通过与[将 `dependencies` 添加到*路径操作装饰器*](dependencies-in-path-operation-decorators.md) 类似的方式，可以把依赖项添加至整个 `FastAPI` 应用。

这样一来，就可以为所有*路径操作*应用该依赖项：

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}

[将 `dependencies` 添加到*路径操作装饰器*](dependencies-in-path-operation-decorators.md) 一章的思路均适用于全局依赖项， 在本例中，这些依赖项可以用于应用中的所有*路径操作*。

## 为一组路径操作定义依赖项 { #dependencies-for-groups-of-path-operations }

稍后，[大型应用 - 多文件](../../tutorial/bigger-applications.md)一章中会介绍如何使用多个文件创建大型应用程序，在这一章中，你将了解到如何为一组*路径操作*声明单个 `dependencies` 参数。



---

# Source: docs/tutorial/dependencies/index.md


# 依赖项 { #dependencies }

**FastAPI** 提供了简单直观但功能强大的**<dfn title="也称为：组件、资源、提供者、服务、可注入项">依赖注入</dfn>**系统。

它被设计得非常易用，能让任何开发者都能轻松把其他组件与 **FastAPI** 集成。

## 什么是「依赖注入」 { #what-is-dependency-injection }

在编程中，**「依赖注入」**指的是，你的代码（本文中为*路径操作函数*）声明其运行所需并要使用的东西：“依赖”。

然后，由该系统（本文中为 **FastAPI**）负责执行所有必要的逻辑，为你的代码提供这些所需的依赖（“注入”依赖）。

当你需要以下内容时，这非常有用：

* 共享业务逻辑（同一段代码逻辑反复复用）
* 共享数据库连接
* 实施安全、认证、角色权限等要求
* 以及更多其他内容...

同时尽量减少代码重复。

## 第一步 { #first-steps }

先来看一个非常简单的例子。它现在简单到几乎没什么用。

但这样我们就可以专注于**依赖注入**系统是如何工作的。

### 创建依赖项，或“dependable” { #create-a-dependency-or-dependable }

首先关注依赖项。

它只是一个函数，且可以接收与*路径操作函数*相同的所有参数：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8:9] *}

大功告成。

**2 行**。

它的形式和结构与所有*路径操作函数*相同。

你可以把它当作没有“装饰器”（没有 `@app.get("/some-path")`）的*路径操作函数*。

而且它可以返回任何你想要的内容。

本例中的依赖项预期接收：

* 类型为 `str` 的可选查询参数 `q`
* 类型为 `int` 的可选查询参数 `skip`，默认值 `0`
* 类型为 `int` 的可选查询参数 `limit`，默认值 `100`

然后它只需返回一个包含这些值的 `dict`。

/// note | 注意

FastAPI 在 0.95.0 版本中新增了对 `Annotated` 的支持（并开始推荐使用）。

如果你的版本较旧，尝试使用 `Annotated` 会报错。

在使用 `Annotated` 之前，请确保[升级 FastAPI 版本](../../deployment/versions.md#upgrading-the-fastapi-versions)到至少 0.95.1。

///

### 导入 `Depends` { #import-depends }

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[3] *}

### 在“dependant”中声明依赖项 { #declare-the-dependency-in-the-dependant }

与在*路径操作函数*的参数中使用 `Body`、`Query` 等相同，给参数使用 `Depends` 来声明一个新的依赖项：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[13,18] *}

虽然你在函数参数中使用 `Depends` 的方式与 `Body`、`Query` 等相同，但 `Depends` 的工作方式略有不同。

这里只能给 `Depends` 传入一个参数。

这个参数必须是类似函数的可调用对象。

你不需要直接调用它（不要在末尾加括号），只需将其作为参数传给 `Depends()`。

该函数接收的参数与*路径操作函数*的参数相同。

/// tip | 提示

下一章会介绍除了函数之外，还有哪些“东西”可以用作依赖项。

///

接收到新的请求时，**FastAPI** 会负责：

* 用正确的参数调用你的依赖项（“dependable”）函数
* 获取函数返回的结果
* 将该结果赋值给你的*路径操作函数*中的参数

```mermaid
graph TB

common_parameters(["common_parameters"])
read_items["/items/"]
read_users["/users/"]

common_parameters --> read_items
common_parameters --> read_users
```

这样，你只需编写一次共享代码，**FastAPI** 会在你的*路径操作*中为你调用它。

/// tip | 提示

注意，无需创建专门的类并传给 **FastAPI** 去“注册”之类的操作。

只要把它传给 `Depends`，**FastAPI** 就知道该怎么做了。

///

## 共享 `Annotated` 依赖项 { #share-annotated-dependencies }

在上面的示例中，你会发现这里有一点点**代码重复**。

当你需要使用 `common_parameters()` 这个依赖时，你必须写出完整的带类型注解和 `Depends()` 的参数：

```Python
commons: Annotated[dict, Depends(common_parameters)]
```

但因为我们使用了 `Annotated`，可以把这个 `Annotated` 的值存到一个变量里，在多个地方复用：

{* ../../docs_src/dependencies/tutorial001_02_an_py310.py hl[12,16,21] *}

/// tip | 提示

这只是标准的 Python，叫做“类型别名”，并不是 **FastAPI** 特有的。

但因为 **FastAPI** 基于 Python 标准（包括 `Annotated`），你就可以在代码里使用这个技巧。😎

///

这些依赖会照常工作，而**最棒的是**，**类型信息会被保留**，这意味着你的编辑器依然能提供**自动补全**、**行内报错**等。同样适用于 `mypy` 等其他工具。

当你在**大型代码库**中，在**很多*路径操作***里反复使用**相同的依赖**时，这会特别有用。

## 要不要使用 `async`？ { #to-async-or-not-to-async }

由于依赖项也会由 **FastAPI** 调用（与*路径操作函数*相同），因此定义函数时同样的规则也适用。

你可以使用 `async def` 或普通的 `def`。

你可以在普通的 `def` *路径操作函数*中声明 `async def` 的依赖项；也可以在异步的 `async def` *路径操作函数*中声明普通的 `def` 依赖项，等等。

都没关系，**FastAPI** 知道该怎么处理。

/// note | 注意

如果不了解异步，请参阅文档中关于 `async` 和 `await` 的章节：[异步：*“着急了？”*](../../async.md#in-a-hurry)。

///

## 与 OpenAPI 集成 { #integrated-with-openapi }

依赖项及子依赖项中声明的所有请求、验证和需求都会集成到同一个 OpenAPI 模式中。

因此，交互式文档中也会包含这些依赖项的所有信息：

<img src="/img/tutorial/dependencies/image01.png">

## 簡单用法 { #simple-usage }

观察一下就会发现，只要*路径*和*操作*匹配，就会使用声明的*路径操作函数*。随后，**FastAPI** 会用正确的参数调用该函数，并从请求中提取数据。

事实上，所有（或大多数）Web 框架的工作方式都是这样的。

你从不会直接调用这些函数。它们由你的框架（此处为 **FastAPI**）调用。

通过依赖注入系统，你还可以告诉 **FastAPI**，你的*路径操作函数*还“依赖”某些应在*路径操作函数*之前执行的内容，**FastAPI** 会负责执行它并“注入”结果。

“依赖注入”的其他常见术语包括：

* 资源（resources）
* 提供方（providers）
* 服务（services）
* 可注入（injectables）
* 组件（components）

## **FastAPI** 插件 { #fastapi-plug-ins }

可以使用**依赖注入**系统构建集成和“插件”。但实际上，根本**不需要创建“插件”**，因为通过依赖项可以声明无限多的集成与交互，使其可用于*路径操作函数*。

依赖项可以用非常简单直观的方式创建，你只需导入所需的 Python 包，用*字面意义上的*几行代码就能把它们与你的 API 函数集成起来。

在接下来的章节中，你会看到关于关系型数据库、NoSQL 数据库、安全等方面的示例。

## **FastAPI** 兼容性 { #fastapi-compatibility }

依赖注入系统的简洁让 **FastAPI** 能与以下内容兼容：

* 各类关系型数据库
* NoSQL 数据库
* 外部包
* 外部 API
* 认证与授权系统
* API 使用监控系统
* 响应数据注入系统
* 等等...

## 简单而强大 { #simple-and-powerful }

虽然**层级式依赖注入系统**的定义与使用非常简单，但它依然非常强大。

你可以定义依赖其他依赖项的依赖项。

最终会构建出一个依赖项的层级树，**依赖注入**系统会处理所有这些依赖（及其子依赖），并在每一步提供（注入）相应的结果。

例如，假设你有 4 个 API 路径操作（*端点*）：

* `/items/public/`
* `/items/private/`
* `/users/{user_id}/activate`
* `/items/pro/`

你可以仅通过依赖项及其子依赖项为它们添加不同的权限要求：

```mermaid
graph TB

current_user(["current_user"])
active_user(["active_user"])
admin_user(["admin_user"])
paying_user(["paying_user"])

public["/items/public/"]
private["/items/private/"]
activate_user["/users/{user_id}/activate"]
pro_items["/items/pro/"]

current_user --> active_user
active_user --> admin_user
active_user --> paying_user

current_user --> public
active_user --> private
admin_user --> activate_user
paying_user --> pro_items
```

## 与 **OpenAPI** 集成 { #integrated-with-openapi_1 }

在声明需求的同时，所有这些依赖项也会为你的*路径操作*添加参数、验证等内容。

**FastAPI** 会负责把这些全部添加到 OpenAPI 模式中，以便它们显示在交互式文档系统里。



---

# Source: docs/tutorial/dependencies/sub-dependencies.md


# 子依赖项 { #sub-dependencies }

FastAPI 支持创建含**子依赖项**的依赖项。

并且，可以按需声明任意**深度**的子依赖项嵌套层级。

**FastAPI** 负责处理解析不同深度的子依赖项。

## 第一层依赖项 “dependable” { #first-dependency-dependable }

你可以创建一个第一层依赖项（“dependable”），如下：

{* ../../docs_src/dependencies/tutorial005_an_py310.py hl[8:9] *}

这段代码声明了类型为 `str` 的可选查询参数 `q`，然后返回这个查询参数。

这个函数很简单（不过也没什么用），但却有助于让我们专注于了解子依赖项的工作方式。

## 第二层依赖项，“dependable”和“dependant” { #second-dependency-dependable-and-dependant }

接下来，创建另一个依赖项函数（一个“dependable”），并同时为它自身再声明一个依赖项（因此它同时也是一个“dependant”）：

{* ../../docs_src/dependencies/tutorial005_an_py310.py hl[13] *}

这里重点说明一下声明的参数：

* 尽管该函数自身是依赖项（“dependable”），但还声明了另一个依赖项（它“依赖”于其他对象）
    * 该函数依赖 `query_extractor`, 并把 `query_extractor` 的返回值赋给参数 `q`
* 同时，该函数还声明了类型是 `str` 的可选 cookie（`last_query`）
    * 用户未提供查询参数 `q` 时，则使用上次使用后保存在 cookie 中的查询

## 使用依赖项 { #use-the-dependency }

接下来，就可以使用依赖项：

{* ../../docs_src/dependencies/tutorial005_an_py310.py hl[23] *}

/// note | 注意

注意，这里在*路径操作函数*中只声明了一个依赖项，即 `query_or_cookie_extractor` 。

但 **FastAPI** 必须先处理 `query_extractor`，以便在调用 `query_or_cookie_extractor` 时使用 `query_extractor` 返回的结果。

///

```mermaid
graph TB

query_extractor(["query_extractor"])
query_or_cookie_extractor(["query_or_cookie_extractor"])

read_query["/items/"]

query_extractor --> query_or_cookie_extractor --> read_query
```

## 多次使用同一个依赖项 { #using-the-same-dependency-multiple-times }

如果在同一个*路径操作* 多次声明了同一个依赖项，例如，多个依赖项共用一个子依赖项，**FastAPI** 在处理同一请求时，只调用一次该子依赖项。

FastAPI 不会为同一个请求多次调用同一个依赖项，而是把依赖项的返回值进行<dfn title="用于存储已计算/生成的值，以便复用而无需再次计算的实用工具/系统">「缓存」</dfn>，并把它传递给同一请求中所有需要使用该返回值的「依赖项」。

在高级使用场景中，如果不想使用「缓存」值，而是为需要在同一请求的每一步操作（多次）中都实际调用依赖项，可以把 `Depends` 的参数 `use_cache` 的值设置为 `False`:

//// tab | Python 3.10+

```Python hl_lines="1"
async def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):
    return {"fresh_value": fresh_value}
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip | 提示

尽可能优先使用 `Annotated` 版本。

///

```Python hl_lines="1"
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```

////

## 小结 { #recap }

千万别被本章里这些花里胡哨的词藻吓倒了，其实**依赖注入**系统非常简单。

依赖注入无非是与*路径操作函数*一样的函数罢了。

但它依然非常强大，能够声明任意嵌套深度的「图」或树状的依赖结构。

/// tip | 提示

这些简单的例子现在看上去虽然没有什么实用价值，

但在**安全**一章中，您会了解到这些例子的用途，

以及这些例子所能节省的代码量。

///



---

# Source: docs/tutorial/encoder.md


# JSON 兼容编码器 { #json-compatible-encoder }

在某些情况下，您可能需要将数据类型（如Pydantic模型）转换为与JSON兼容的数据类型（如`dict`、`list`等）。

比如，如果您需要将其存储在数据库中。

对于这种要求， **FastAPI**提供了`jsonable_encoder()`函数。

## 使用`jsonable_encoder` { #using-the-jsonable-encoder }

让我们假设你有一个数据库名为`fake_db`，它只能接收与JSON兼容的数据。

例如，它不接收`datetime`这类的对象，因为这些对象与JSON不兼容。

因此，`datetime`对象必须转换为包含[ISO 格式](https://en.wikipedia.org/wiki/ISO_8601)的`str`类型对象。

同样，这个数据库也不会接收Pydantic模型（带有属性的对象），而只接收`dict`。

对此你可以使用`jsonable_encoder`。

它接收一个对象，比如Pydantic模型，并会返回一个JSON兼容的版本：

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

在这个例子中，它将Pydantic模型转换为`dict`，并将`datetime`转换为`str`。

调用它的结果后就可以使用Python标准编码中的[`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps)。

这个操作不会返回一个包含JSON格式（作为字符串）数据的庞大的`str`。它将返回一个Python标准数据结构（例如`dict`），其值和子值都与JSON兼容。

/// note | 注意

`jsonable_encoder`实际上是**FastAPI**内部用来转换数据的。但是它在许多其他场景中也很有用。

///



---

# Source: docs/tutorial/extra-data-types.md


# 额外数据类型 { #extra-data-types }

到目前为止，你一直在使用常见的数据类型，如:

* `int`
* `float`
* `str`
* `bool`

但是你也可以使用更复杂的数据类型。

你仍然会拥有现在已经看到的相同的特性:

* 很棒的编辑器支持。
* 传入请求的数据转换。
* 响应数据转换。
* 数据验证。
* 自动注解和文档。

## 其他数据类型 { #other-data-types }

下面是一些你可以使用的其他数据类型:

* `UUID`:
    * 一种标准的 "通用唯一标识符" ，在许多数据库和系统中用作ID。
    * 在请求和响应中将以 `str` 表示。
* `datetime.datetime`:
    * 一个 Python `datetime.datetime`.
    * 在请求和响应中将表示为 ISO 8601 格式的 `str` ，比如: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * Python `datetime.date`.
    * 在请求和响应中将表示为 ISO 8601 格式的 `str` ，比如: `2008-09-15`.
* `datetime.time`:
    * 一个 Python `datetime.time`.
    * 在请求和响应中将表示为 ISO 8601 格式的 `str` ，比如:  `14:23:55.003`.
* `datetime.timedelta`:
    * 一个 Python `datetime.timedelta`.
    * 在请求和响应中将表示为 `float` 代表总秒数。
    * Pydantic 也允许将其表示为 "ISO 8601 时间差异编码", [查看文档了解更多信息](https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers)。
* `frozenset`:
    * 在请求和响应中，作为 `set` 对待：
        * 在请求中，列表将被读取，消除重复，并将其转换为一个 `set`。
        * 在响应中 `set` 将被转换为 `list` 。
        * 产生的模式将指定那些 `set` 的值是唯一的 (使用 JSON Schema 的 `uniqueItems`)。
* `bytes`:
    * 标准的 Python `bytes`。
    * 在请求和响应中被当作 `str` 处理。
    * 生成的模式将指定这个 `str` 是 `binary` "格式"。
* `Decimal`:
    * 标准的 Python `Decimal`。
    * 在请求和响应中被当做 `float` 一样处理。
* 你可以在这里检查所有有效的 Pydantic 数据类型: [Pydantic data types](https://docs.pydantic.dev/latest/usage/types/types/)。

## 例子 { #example }

下面是一个*路径操作*的示例，其中的参数使用了上面的一些类型。

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

注意，函数内的参数有原生的数据类型，你可以，例如，执行正常的日期操作，如:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}



---

# Source: docs/tutorial/extra-models.md


# 更多模型 { #extra-models }


书接上文，多个关联模型这种情况很常见。

特别是用户模型，因为：

* **输入模型**应该含密码
* **输出模型**不应含密码
* **数据库模型**可能需要包含哈希后的密码

/// danger | 危险

不要存储用户的明文密码。始终只存储之后可用于校验的“安全哈希”。

如果你还不了解，可以在[安全性章节](security/simple-oauth2.md#password-hashing)中学习什么是“密码哈希”。

///

## 多个模型 { #multiple-models }

下面的代码展示了不同模型处理密码字段的方式，及使用位置的大致思路：

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### 关于 `**user_in.model_dump()` { #about-user-in-model-dump }

#### Pydantic 的 `.model_dump()` { #pydantics-model-dump }

`user_in` 是类 `UserIn` 的 Pydantic 模型。

Pydantic 模型有 `.model_dump()` 方法，会返回包含模型数据的 `dict`。

因此，如果使用如下方式创建 Pydantic 对象 `user_in`：

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

就能以如下方式调用：

```Python
user_dict = user_in.model_dump()
```

现在，变量 `user_dict` 中的是包含数据的 `dict`（它是 `dict`，不是 Pydantic 模型对象）。

以如下方式调用：

```Python
print(user_dict)
```

输出的就是 Python `dict`：

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### 解包 `dict` { #unpacking-a-dict }

把 `dict`（如 `user_dict`）以 `**user_dict` 形式传递给函数（或类），Python 会执行“解包”。它会把 `user_dict` 的键和值作为关键字参数直接传递。

因此，接着上面的 `user_dict` 继续编写如下代码：

```Python
UserInDB(**user_dict)
```

就会生成如下结果：

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

或更精准，直接使用 `user_dict`（无论它将来包含什么字段）：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 用另一个模型的内容生成 Pydantic 模型 { #a-pydantic-model-from-the-contents-of-another }

上例中 ，从 `user_in.model_dump()` 中得到了 `user_dict`，下面的代码：

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

等效于：

```Python
UserInDB(**user_in.model_dump())
```

...因为 `user_in.model_dump()` 是 `dict`，在传递给 `UserInDB` 时，把 `**` 加在 `user_in.model_dump()` 前，可以让 Python 进行解包。

这样，就可以用其它 Pydantic 模型中的数据生成 Pydantic 模型。

#### 解包 `dict` 并添加额外关键字参数 { #unpacking-a-dict-and-extra-keywords }

接下来，继续添加关键字参数 `hashed_password=hashed_password`，例如：

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...输出结果如下：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | 警告

配套的辅助函数 `fake_password_hasher` 和 `fake_save_user` 仅用于演示可能的数据流，当然并不提供真实的安全性。

///

## 减少重复 { #reduce-duplication }

减少代码重复是 **FastAPI** 的核心思想之一。

代码重复会导致 bug、安全问题、代码失步等问题（更新了某个位置的代码，但没有同步更新其它位置的代码）。

上面的这些模型共享了大量数据，拥有重复的属性名和类型。

我们可以做得更好。

声明 `UserBase` 模型作为其它模型的基类。然后，用该类衍生出继承其属性（类型声明、校验等）的子类。

所有数据转换、校验、文档等功能仍将正常运行。

这样，就可以仅声明模型之间的差异部分（具有明文的 `password`、具有 `hashed_password` 以及不包括密码）：

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` 或 `anyOf` { #union-or-anyof }

响应可以声明为两个或多个类型的 `Union`，即该响应可以是这些类型中的任意一种。

在 OpenAPI 中会用 `anyOf` 表示。

为此，请使用 Python 标准类型提示 [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union)：

/// note | 注意

定义 [`Union`](https://docs.pydantic.dev/latest/concepts/types/#unions) 类型时，要把更具体的类型写在前面，然后是不太具体的类型。下例中，更具体的 `PlaneItem` 位于 `Union[PlaneItem, CarItem]` 中的 `CarItem` 之前。

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10 中的 `Union` { #union-in-python-3-10 }

在这个示例中，我们把 `Union[PlaneItem, CarItem]` 作为参数 `response_model` 的值传入。

因为这是作为“参数的值”而不是放在“类型注解”中，所以即使在 Python 3.10 也必须使用 `Union`。

如果是在类型注解中，我们就可以使用竖线：

```Python
some_variable: PlaneItem | CarItem
```

但如果把它写成赋值 `response_model=PlaneItem | CarItem`，就会报错，因为 Python 会尝试在 `PlaneItem` 和 `CarItem` 之间执行一个“无效的运算”，而不是把它当作类型注解来解析。

## 模型列表 { #list-of-models }

同样地，你可以声明由对象列表构成的响应。

为此，请使用标准的 Python `list`：

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## 任意 `dict` 的响应 { #response-with-arbitrary-dict }

你也可以使用普通的任意 `dict` 来声明响应，只需声明键和值的类型，无需使用 Pydantic 模型。

如果你事先不知道有效的字段/属性名（Pydantic 模型需要预先知道字段）时，这很有用。

此时，可以使用 `dict`：

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## 小结 { #recap }

针对不同场景，可以随意使用不同的 Pydantic 模型并通过继承复用。

当一个实体需要具备不同的“状态”时，无需只为该实体定义一个数据模型。例如，用户“实体”就可能有包含 `password`、包含 `password_hash` 以及不含密码等多种状态。



---

# Source: docs/tutorial/first-steps.md


# 第一步 { #first-steps }


最简单的 FastAPI 文件可能像下面这样：

{* ../../docs_src/first_steps/tutorial001_py310.py *}

将其复制到 `main.py` 文件中。

运行实时服务器：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

在输出中，会有一行信息像下面这样：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

该行显示了你的应用在本机所提供服务的 URL 地址。

### 查看 { #check-it }

打开浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)。

你将看到如下的 JSON 响应：

```JSON
{"message": "Hello World"}
```

### 交互式 API 文档 { #interactive-api-docs }

跳转到 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你将会看到自动生成的交互式 API 文档（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 可选的 API 文档 { #alternative-api-docs }

前往 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

你将会看到可选的自动生成文档 （由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** 使用定义 API 的 **OpenAPI** 标准将你的所有 API 转换成「模式」。

#### 「模式」 { #schema }

「模式」是对事物的一种定义或描述。它并非具体的实现代码，而只是抽象的描述。

#### API「模式」 { #api-schema }

在这种场景下，[OpenAPI](https://github.com/OAI/OpenAPI-Specification) 是一种规定如何定义 API 模式的规范。

「模式」的定义包括你的 API 路径，以及它们可能使用的参数等等。

#### 数据「模式」 { #data-schema }

「模式」这个术语也可能指的是某些数据比如 JSON 的结构。

在这种情况下，它可以表示 JSON 的属性及其具有的数据类型，等等。

#### OpenAPI 和 JSON Schema { #openapi-and-json-schema }

OpenAPI 为你的 API 定义 API 模式。该模式中包含了你的 API 发送和接收的数据的定义（或称为「模式」），这些定义通过 JSON 数据模式标准 **JSON Schema** 所生成。

#### 查看 `openapi.json` { #check-the-openapi-json }

如果你对原始的 OpenAPI 模式长什么样子感到好奇，FastAPI 自动生成了包含所有 API 描述的 JSON（模式）。

你可以直接在：[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) 看到它。

它将显示以如下内容开头的 JSON：

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPI 的用途 { #what-is-openapi-for }

驱动 FastAPI 内置的 2 个交互式文档系统的正是 OpenAPI 模式。

并且还有数十种替代方案，它们全部都基于 OpenAPI。你可以轻松地将这些替代方案中的任何一种添加到使用 **FastAPI** 构建的应用程序中。

你还可以使用它自动生成与你的 API 进行通信的客户端代码。例如 web 前端，移动端或物联网嵌入程序。

### 在 `pyproject.toml` 中配置应用 `entrypoint` { #configure-the-app-entrypoint-in-pyproject-toml }

你可以在 `pyproject.toml` 文件中配置应用的位置，例如：

```toml
[tool.fastapi]
entrypoint = "main:app"
```

该 `entrypoint` 会告诉 `fastapi` 命令按如下方式导入应用：

```python
from main import app
```

如果你的代码结构如下：

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

那么你可以将 `entrypoint` 设置为：

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

这等价于：

```python
from backend.main import app
```

### 带路径或使用 `--entrypoint` CLI 选项的 `fastapi dev` { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

你也可以把文件路径传给 `fastapi dev` 命令，它会尝试推断要使用的 FastAPI 应用对象：

```console
$ fastapi dev main.py
```

或者，你也可以给 `fastapi dev` 命令传入 `--entrypoint` 选项：

```console
$ fastapi dev --entrypoint main:app
```

但这样每次调用 `fastapi` 命令时都需要记得传入正确的路径/entrypoint。

另外，其他工具可能无法找到它，例如 [VS Code 扩展](../editor-support.md) 或 [FastAPI Cloud](https://fastapicloud.com)，因此推荐在 `pyproject.toml` 中使用 `entrypoint`。

### 部署你的应用（可选） { #deploy-your-app-optional }

你可以选择用一条命令将 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。🚀

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI 会自动检测你的 FastAPI 应用并将其部署到云端。如果你尚未登录，浏览器会打开以完成认证流程。

就这些！现在你可以通过该 URL 访问你的应用了。✨

## 分步概括 { #recap-step-by-step }

### 步骤 1：导入 `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` 是一个为你的 API 提供了所有功能的 Python 类。

/// note | 技术细节

`FastAPI` 是直接从 `Starlette` 继承的类。

你可以通过 `FastAPI` 使用所有的 [Starlette](https://www.starlette.dev/) 的功能。

///

### 步骤 2：创建一个 `FastAPI`「实例」 { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

这里的变量 `app` 会是 `FastAPI` 类的一个「实例」。

这个实例将是创建你所有 API 的主要交互对象。

### 步骤 3：创建一个*路径操作* { #step-3-create-a-path-operation }

#### 路径 { #path }

这里的「路径」指的是 URL 中从第一个 `/` 起的后半部分。

所以，在一个这样的 URL 中：

```
https://example.com/items/foo
```

...路径会是：

```
/items/foo
```

/// note | 注意

「路径」也通常被称为「端点」或「路由」。

///

开发 API 时，「路径」是用来分离「关注点」和「资源」的主要手段。

#### 操作 { #operation }

这里的「操作」指的是一种 HTTP「方法」。

下列之一：

* `POST`
* `GET`
* `PUT`
* `DELETE`

...以及更少见的几种：

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

在 HTTP 协议中，你可以使用以上的其中一种（或多种）「方法」与每个路径进行通信。

---

在开发 API 时，你通常使用特定的 HTTP 方法去执行特定的行为。

通常使用：

* `POST`：创建数据。
* `GET`：读取数据。
* `PUT`：更新数据。
* `DELETE`：删除数据。

因此，在 OpenAPI 中，每一个 HTTP 方法都被称为「操作」。

我们也打算称呼它们为「操作」。

#### 定义一个*路径操作装饰器* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")` 告诉 **FastAPI** 在它下方的函数负责处理如下访问请求：

* 请求路径为 `/`
* 使用 <dfn title="一种 HTTP GET 方法"><code>get</code> 操作</dfn>

/// note | `@decorator` 信息

`@something` 语法在 Python 中被称为「装饰器」。

像一顶漂亮的装饰帽一样，将它放在一个函数的上方（我猜测这个术语的命名就是这么来的）。

装饰器接收位于其下方的函数并且用它完成一些工作。

在我们的例子中，这个装饰器告诉 **FastAPI** 位于其下方的函数对应着**路径** `/` 加上 `get` **操作**。

它是一个「**路径操作装饰器**」。

///

你也可以使用其他的操作：

* `@app.post()`
* `@app.put()`
* `@app.delete()`

以及更少见的：

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | 提示

你可以随意使用任何一个操作（HTTP方法）。

**FastAPI** 没有强制要求操作有任何特定的含义。

此处提供的信息仅作为指导，而不是要求。

比如，当使用 GraphQL 时通常你所有的动作都通过 `POST` 一种方法执行。

///

### 步骤 4：定义**路径操作函数** { #step-4-define-the-path-operation-function }

这是我们的「**路径操作函数**」：

* **路径**：是 `/`。
* **操作**：是 `get`。
* **函数**：是位于「装饰器」下方的函数（位于 `@app.get("/")` 下方）。

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

这是一个 Python 函数。

每当 **FastAPI** 接收一个使用 `GET` 方法访问 URL「`/`」的请求时这个函数会被调用。

在这个例子中，它是一个 `async` 函数。

---

你也可以将其定义为常规函数而不使用 `async def`:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | 注意

如果你不知道两者的区别，请查阅 [并发: *赶时间吗？*](../async.md#in-a-hurry)。

///

### 步骤 5：返回内容 { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

你可以返回一个 `dict`、`list`，像 `str`、`int` 一样的单个值，等等。

你还可以返回 Pydantic 模型（稍后你将了解更多）。

还有许多其他将会自动转换为 JSON 的对象和模型（包括 ORM 对象等）。尝试下使用你最喜欢的一种，它很有可能已经被支持。

### 步骤 6：部署 { #step-6-deploy-it }

用一条命令将你的应用部署到 **[FastAPI Cloud](https://fastapicloud.com)**：`fastapi deploy`。🎉

#### 关于 FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 由 **FastAPI** 的作者和团队打造。

它以最小的投入简化了 **构建**、**部署** 和 **访问** API 的流程。

它把使用 FastAPI 构建应用的相同**开发者体验**带到了将应用**部署**到云端的过程。🎉

FastAPI Cloud 是 *FastAPI 及其朋友们* 开源项目的主要赞助和资金提供方。✨

#### 部署到其他云服务商 { #deploy-to-other-cloud-providers }

FastAPI 是开源并基于标准的。你可以将 FastAPI 应用部署到你选择的任何云服务商。

按照你的云服务商的指南部署 FastAPI 应用即可。🤓

## 总结 { #recap }

* 导入 `FastAPI`。
* 创建一个 `app` 实例。
* 编写一个**路径操作装饰器**，如 `@app.get("/")`。
* 定义一个**路径操作函数**，如 `def root(): ...`。
* 使用命令 `fastapi dev` 运行开发服务器。
* 可选：使用 `fastapi deploy` 部署你的应用。



---

# Source: docs/tutorial/frontend.md


# 前端 { #frontend }

你可以使用 `app.frontend()`（或 `router.frontend()`）来提供静态前端应用。

这对会生成静态文件的前端工具很有用，例如使用 Vite 的 React、TanStack Router、Astro、Vue、Svelte、Angular、Solid 等。

使用这些工具时，通常会有一个构建前端的步骤，命令类似：

```bash
npm run build
```

它会生成一个类似 `./dist/` 的目录，里面包含你的前端文件。

你可以使用 `app.frontend()` 按照这些前端框架所需的约定来提供该目录。

**FastAPI** 会先检查*路径操作*。只有在没有普通路由匹配时，才会检查前端文件，因此你的 API 不会受到影响。

## 提供前端服务 { #serve-a-frontend }

构建前端之后，例如使用 `npm run build`，将生成的文件放入一个目录，例如 `dist`。

你的项目结构可能如下所示：

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

然后使用 `app.frontend()` 提供服务：

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

这样，对 `/assets/app.js` 的请求可以提供 `dist/assets/app.js`。

如果你还有一个 **FastAPI** *路径操作*，则*路径操作*优先。

## 客户端路由 { #client-side-routing }

许多前端应用，包括**单页应用**（SPA），都会使用客户端路由。像 `/dashboard/settings` 这样的路径可能并不是一个真实文件，而是由框架负责处理。

因此，如果直接访问该 URL（而不是通过应用内导航访问），后端应该从 `index.html` 提供前端应用，这样前端框架就可以处理客户端路由。

为此，使用 `fallback="index.html"`：

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** 只会对看起来像浏览器导航的 `GET` 和 `HEAD` 请求使用此 fallback。缺失的 JavaScript、CSS 和图片等文件仍会返回 `404`。

对于其他方法的请求，例如 `POST` 或 `PUT`，如果路径只匹配前端 fallback，也会返回 `404`。常规 **FastAPI** *路径操作*仍然比前端路由具有更高优先级。

/// tip | 提示

默认情况下，`fallback` 的值为 `fallback="auto"`。在大多数情况下，你不需要指定 `fallback`。详情见下文。

///

这正是许多使用客户端路由的前端应用所需的行为，例如使用 TanStack Router 的 React、Vue、Angular、SvelteKit 或 Solid。

## 自定义 404 页面 { #custom-404-page }

你也可以为缺失的前端路径提供一个静态 `404.html` 页面：

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

该响应会保持 `404` 状态码。

在这种情况下，**FastAPI** 不会为缺失的前端路径提供 `index.html`，而是返回 `404.html` 文件。

/// tip | 提示

默认情况下，`fallback` 的值为 `fallback="auto"`。这样，如果找到 `404.html` 文件，它会自动用作 fallback。

因此，通常你可以省略 `fallback` 参数。

///

这对会为每个页面生成静态 HTML 文件的前端工具很有用，例如 Astro。

## 自动 Fallback { #fallback-auto }

默认情况下，`app.frontend()` 使用 `fallback="auto"`。

如果前端目录中存在 `404.html` 文件，缺失的前端路径会以状态码 `404` 提供该文件。

否则，如果存在 `index.html` 文件，缺失的浏览器导航路径会提供 `index.html`，这正是许多使用客户端路由的前端应用所期望的行为。

因此，在大多数情况下，你可以使用 `app.frontend("/", directory="dist")`，而无需指定 `fallback` 参数。

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## 禁用 Fallback { #disable-fallback }

如果你不想为缺失的前端路径提供 fallback 文件，请使用 `fallback=None`：

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

这样，缺失的前端路径会返回普通的 `404`。

## 检查目录 { #check-directory }

默认情况下，`app.frontend()` 会在应用创建时检查目录是否存在。

这有助于尽早发现配置错误。例如，如果前端构建输出目录缺失，**FastAPI** 会在启动时抛出错误。

如果你的前端文件会稍后创建，例如在应用对象创建之后由单独的构建步骤创建，请设置 `check_dir=False`：

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

使用 `check_dir=False` 时，**FastAPI** 不会在应用创建时检查目录。如果在处理请求时配置的目录仍然缺失，**FastAPI** 会在那时抛出错误。

## 与 `APIRouter` 一起使用 { #use-it-with-apirouter }

你也可以将前端文件添加到一个 `APIRouter`，并使用前缀包含它：

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

在这个示例中，前端路径会在 `/app` 下提供服务。

应用中的任何常规*路径操作*仍会优先，包括其他 router 中的路径操作。

## 依赖项和中间件 { #dependencies-and-middleware }

前端响应在普通 **FastAPI** 应用内部运行，因此 HTTP 中间件会应用于它们。

来自 app、`APIRouter` 和 `include_router()` 的依赖项也会应用于前端响应。这可用于通过 cookie 身份验证或类似方式保护前端。

## 仅限静态构建输出 { #static-build-output-only }

`app.frontend()` 提供的是你的前端构建已经生成的文件。

它不会运行服务端渲染。它适用于生成静态文件的前端框架，而不适用于需要在服务器上为每个请求进行动态渲染的框架。



---

# Source: docs/tutorial/handling-errors.md


# 处理错误 { #handling-errors }

某些情况下，需要向使用你的 API 的客户端返回错误提示。

这里所谓的客户端包括前端浏览器、他人的代码、物联网设备等。

你可能需要告诉客户端：

* 客户端没有执行该操作的权限
* 客户端没有访问该资源的权限
* 客户端要访问的项目不存在
* 等等

遇到这些情况时，通常要返回 **400** 范围内（400 至 499）的 **HTTP 状态码**。

这与 200 HTTP 状态码（200 至 299）类似。那些“200”状态码表示请求在某种程度上“成功”。

而 400 范围内的状态码表示客户端发生了错误。

大家都知道**「404 Not Found」**错误，还有调侃这个错误的笑话吧？

## 使用 `HTTPException` { #use-httpexception }

向客户端返回 HTTP 错误响应，可以使用 `HTTPException`。

### 导入 `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### 在代码中触发 `HTTPException` { #raise-an-httpexception-in-your-code }

`HTTPException` 是额外包含了和 API 有关数据的常规 Python 异常。

因为是 Python 异常，所以不能 `return`，只能 `raise`。

这也意味着，如果你在*路径操作函数*里调用的某个工具函数内部触发了 `HTTPException`，那么*路径操作函数*中后续的代码将不会继续执行，请求会立刻终止，并把 `HTTPException` 的 HTTP 错误发送给客户端。

在介绍依赖项与安全的章节中，你可以更直观地看到用 `raise` 异常代替 `return` 值的优势。

本例中，客户端用不存在的 `ID` 请求 `item` 时，触发状态码为 `404` 的异常：

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### 响应结果 { #the-resulting-response }

请求为 `http://example.com/items/foo`（`item_id` 为 `"foo"`）时，客户端会接收到 HTTP 状态码 200 及如下 JSON 响应结果：

```JSON
{
  "item": "The Foo Wrestlers"
}
```

但如果客户端请求 `http://example.com/items/bar`（不存在的 `item_id` `"bar"`），则会接收到 HTTP 状态码 404（“未找到”错误）及如下 JSON 响应结果：

```JSON
{
  "detail": "Item not found"
}
```

/// tip | 提示

触发 `HTTPException` 时，可以用参数 `detail` 传递任何能转换为 JSON 的值，不仅限于 `str`。

还支持传递 `dict`、`list` 等数据结构。

**FastAPI** 能自动处理这些数据，并将之转换为 JSON。

///

## 添加自定义响应头 { #add-custom-headers }

有些场景下要为 HTTP 错误添加自定义响应头。例如，出于某些类型的安全需要。

一般情况下你可能不会在代码中直接使用它。

但在某些高级场景中需要时，你可以添加自定义响应头：

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## 安装自定义异常处理器 { #install-custom-exception-handlers }

可以使用[与 Starlette 相同的异常处理工具](https://www.starlette.dev/exceptions/)添加自定义异常处理器。

假设有一个自定义异常 `UnicornException`（你自己或你使用的库可能会 `raise` 它）。

并且你希望用 FastAPI 在全局处理该异常。

此时，可以用 `@app.exception_handler()` 添加自定义异常处理器：

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

这里，请求 `/unicorns/yolo` 时，路径操作会触发 `UnicornException`。

但该异常将会被 `unicorn_exception_handler` 处理。

你会收到清晰的错误信息，HTTP 状态码为 `418`，JSON 内容如下：

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 技术细节

也可以使用 `from starlette.requests import Request` 和 `from starlette.responses import JSONResponse`。

**FastAPI** 提供了与 `starlette.responses` 相同的 `fastapi.responses` 作为便捷方式，但大多数可用的响应都直接来自 Starlette。`Request` 也是如此。

///

## 覆盖默认异常处理器 { #override-the-default-exception-handlers }

**FastAPI** 自带了一些默认异常处理器。

当你触发 `HTTPException`，或者请求中包含无效数据时，这些处理器负责返回默认的 JSON 响应。

你也可以用自己的处理器覆盖它们。

### 覆盖请求验证异常 { #override-request-validation-exceptions }

请求中包含无效数据时，**FastAPI** 内部会触发 `RequestValidationError`。

它也内置了该异常的默认处理器。

要覆盖它，导入 `RequestValidationError`，并用 `@app.exception_handler(RequestValidationError)` 装饰你的异常处理器。

异常处理器会接收 `Request` 和该异常。

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

现在，访问 `/items/foo` 时，默认的 JSON 错误为：

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

将得到如下文本内容：

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### 覆盖 `HTTPException` 错误处理器 { #override-the-httpexception-error-handler }

同理，也可以覆盖 `HTTPException` 的处理器。

例如，只为这些错误返回纯文本响应，而不是 JSON：

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | 技术细节

还可以使用 `from starlette.responses import PlainTextResponse`。

**FastAPI** 提供了与 `starlette.responses` 相同的 `fastapi.responses` 作为便捷方式，但大多数可用的响应都直接来自 Starlette。

///

/// warning | 警告

请注意，`RequestValidationError` 包含发生验证错误的文件名和行号信息，你可以在需要时将其记录到日志中以提供相关信息。

但这也意味着，如果你只是将其直接转换为字符串并返回，可能会泄露一些关于系统的细节信息。因此，这里的代码会提取并分别显示每个错误。

///

### 使用 `RequestValidationError` 的请求体 { #use-the-requestvalidationerror-body }

`RequestValidationError` 包含其接收到的带有无效数据的请求体 `body`。

开发时，你可以用它来记录请求体、调试错误，或返回给用户等。

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

现在试着发送一个无效的 `item`，例如：

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

收到的响应会告诉你数据无效，并包含收到的请求体：

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI 的 `HTTPException` vs Starlette 的 `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** 也提供了自有的 `HTTPException`。

**FastAPI** 的 `HTTPException` 错误类继承自 Starlette 的 `HTTPException` 错误类。

它们之间的唯一区别是，**FastAPI** 的 `HTTPException` 在 `detail` 字段中接受任意可转换为 JSON 的数据，而 Starlette 的 `HTTPException` 只接受字符串。

因此，你可以继续像平常一样在代码中触发 **FastAPI** 的 `HTTPException`。

但注册异常处理器时，应该注册到来自 Starlette 的 `HTTPException`。

这样做是为了，当 Starlette 的内部代码、扩展或插件触发 Starlette `HTTPException` 时，你的处理器能够捕获并处理它。

本例中，为了在同一份代码中同时使用两个 `HTTPException`，将 Starlette 的异常重命名为 `StarletteHTTPException`：

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### 复用 **FastAPI** 的异常处理器 { #reuse-fastapis-exception-handlers }

如果你想在使用该异常的同时使用 **FastAPI** 的相同默认异常处理器，可以从 `fastapi.exception_handlers` 导入并复用这些默认处理器：

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

虽然本例只是用非常夸张的信息打印了错误，但足以说明：你可以使用该异常，然后直接复用默认的异常处理器。



---

# Source: docs/tutorial/header-param-models.md


# Header 参数模型 { #header-parameter-models }

如果您有一组相关的 **header 参数**，您可以创建一个 **Pydantic 模型**来声明它们。

这将允许您在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证和元数据。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

## 使用 Pydantic 模型的 Header 参数 { #header-parameters-with-a-pydantic-model }

在 **Pydantic 模型**中声明所需的 **header 参数**，然后将参数声明为 `Header` :

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** 将从请求中接收到的 **headers** 中**提取**出**每个字段**的数据，并提供您定义的 Pydantic 模型。

## 查看文档 { #check-the-docs }

您可以在文档 UI 的 `/docs` 中查看所需的 headers：

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 禁止额外的 Headers { #forbid-extra-headers }

在某些特殊使用情况下（可能并不常见），您可能希望**限制**您想要接收的 headers。

您可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

如果客户尝试发送一些**额外的 headers**，他们将收到**错误**响应。

例如，如果客户端尝试发送一个值为 `plumbus` 的 `tool` header，客户端将收到一个**错误**响应，告知他们 header 参数 `tool` 是不允许的：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## 禁用下划线转换 { #disable-convert-underscores }

与常规的 header 参数相同，当参数名中包含下划线时，会**自动转换为连字符**。

例如，如果你的代码中有一个名为 `save_data` 的 header 参数，那么预期的 HTTP 头将是 `save-data`，并且在文档中也会以这种形式显示。

如果由于某些原因你需要禁用这种自动转换，你也可以在用于 header 参数的 Pydantic 模型中进行设置。

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | 警告

在将 `convert_underscores` 设为 `False` 之前，请注意某些 HTTP 代理和服务器不允许使用带下划线的 headers。

///

## 总结 { #summary }

您可以使用 **Pydantic 模型**在 **FastAPI** 中声明 **headers**。😎



---

# Source: docs/tutorial/header-params.md


# Header 参数 { #header-parameters }

定义 `Header` 参数的方式与定义 `Query`、`Path`、`Cookie` 参数相同。

## 导入 `Header` { #import-header }

首先，导入 `Header`：

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## 声明 `Header` 参数 { #declare-header-parameters }

然后，使用和 `Path`、`Query`、`Cookie` 一样的结构定义 header 参数。

第一个值是默认值，还可以传递所有验证参数或注释参数：

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | 技术细节

`Header` 是 `Path`、`Query`、`Cookie` 的**兄弟类**，都继承自共用的 `Param` 类。

注意，从 `fastapi` 导入的 `Query`、`Path`、`Header` 等对象，实际上是返回特殊类的函数。

///

/// note

必须使用 `Header` 声明 header 参数，否则该参数会被解释为查询参数。

///

## 自动转换 { #automatic-conversion }

`Header` 比 `Path`、`Query` 和 `Cookie` 提供了更多功能。

大部分标准请求头用**连字符**分隔，即**减号**（`-`）。

但是 `user-agent` 这样的变量在 Python 中是无效的。

因此，默认情况下，`Header` 把参数名中的字符由下划线（`_`）改为连字符（`-`）来提取并存档请求头 。

同时，HTTP 的请求头不区分大小写，可以使用 Python 标准样式（即 **snake_case**）进行声明。

因此，可以像在 Python 代码中一样使用 `user_agent` ，无需把首字母大写为 `User_Agent` 等形式。

如需禁用下划线自动转换为连字符，可以把 `Header` 的 `convert_underscores` 参数设置为 `False`：

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning

注意，使用 `convert_underscores = False` 要慎重，有些 HTTP 代理和服务器不支持使用带有下划线的请求头。

///

## 重复的请求头 { #duplicate-headers }

有时，可能需要接收重复的请求头。即同一个请求头有多个值。

类型声明中可以使用 `list` 定义多个请求头。

使用 Python `list` 可以接收重复请求头所有的值。

例如，声明 `X-Token` 多次出现的请求头，可以写成这样：

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

与*路径操作*通信时，以下面的方式发送两个 HTTP 请求头：

```
X-Token: foo
X-Token: bar
```

响应结果是：

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## 小结 { #recap }

使用 `Header` 声明请求头的方式与 `Query`、`Path` 、`Cookie` 相同。

不用担心变量中的下划线，**FastAPI** 可以自动转换。



---

# Source: docs/tutorial/index.md


# 教程 - 用户指南 { #tutorial-user-guide }

本教程将一步步向你展示如何使用 **FastAPI** 的绝大部分特性。

各个章节的内容循序渐进，但是又围绕着单独的主题，所以你可以直接跳转到某个章节以解决你的特定 API 需求。

本教程同样可以作为将来的参考手册，所以你可以随时回到本教程并查阅你需要的内容。

## 运行代码 { #run-the-code }

所有代码片段都可以复制后直接使用（它们实际上是经过测试的 Python 文件）。

要运行任何示例，请将代码复制到 `main.py` 文件中，然后启动 `fastapi dev`：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

**强烈建议**你在本地编写或复制代码，对其进行编辑并运行。

在编辑器中使用 FastAPI 会真正地展现出它的优势：只需要编写很少的代码，所有的类型检查，代码补全等等。

---

## 安装 FastAPI { #install-fastapi }

第一个步骤是安装 FastAPI。

请确保你创建并激活一个[虚拟环境](../virtual-environments.md)，然后**安装 FastAPI**：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | 注意

当你使用 `pip install "fastapi[standard]"` 安装时，它会附带一些默认的可选标准依赖项，其中包括 `fastapi-cloud-cli`，它可以让你部署到 [FastAPI Cloud](https://fastapicloud.com)。

如果你不想安装这些可选依赖，可以选择安装 `pip install fastapi`。

如果你想安装标准依赖但不包含 `fastapi-cloud-cli`，可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"` 安装。

///

/// tip | 提示

FastAPI 提供了一个[VS Code 官方扩展](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode)（也支持 Cursor），包含众多功能，例如路径操作浏览器、路径操作搜索、测试中的 CodeLens 导航（从测试跳转到定义），以及从编辑器内进行 FastAPI Cloud 部署和查看日志。

///

## 进阶用户指南 { #advanced-user-guide }

在本**教程-用户指南**之后，你可以阅读**进阶用户指南**。

**进阶用户指南**以本教程为基础，使用相同的概念，并教授一些额外的特性。

但是你应该先阅读**教程-用户指南**（即你现在正在阅读的内容）。

教程经过精心设计，使你可以仅通过**教程-用户指南**来开发一个完整的应用程序，然后根据你的需要，使用**进阶用户指南**中的一些其他概念，以不同的方式来扩展它。



---

# Source: docs/tutorial/metadata.md


# 元数据和文档 URL { #metadata-and-docs-urls }

你可以在 **FastAPI** 应用程序中自定义多个元数据配置。

## API 元数据 { #metadata-for-api }

你可以在设置 OpenAPI 规范和自动 API 文档 UI 中使用的以下字段：

| 参数 | 类型 | 描述 |
|------------|------|-------------|
| `title` | `str` | API 的标题。 |
| `summary` | `str` | API 的简短摘要。 <small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small> |
| `description` | `str` | API 的简短描述。可以使用 Markdown。 |
| `version` | `str` | API 的版本。这是你自己的应用程序的版本，而不是 OpenAPI 的版本。例如 `2.5.0`。 |
| `terms_of_service` | `str` | API 服务条款的 URL。如果提供，则必须是 URL。 |
| `contact` | `dict` | 公开的 API 的联系信息。它可以包含多个字段。<details><summary><code>contact</code> 字段</summary><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>联系人/组织的识别名称。</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>指向联系信息的 URL。必须采用 URL 格式。</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>联系人/组织的电子邮件地址。必须采用电子邮件地址的格式。</td></tr></tbody></table></details> |
| `license_info` | `dict` | 公开的 API 的许可证信息。它可以包含多个字段。<details><summary><code>license_info</code> 字段</summary><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>必须</strong>（如果设置了 <code>license_info</code>）。用于 API 的许可证名称。</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API 的 [SPDX](https://spdx.org/licenses/) 许可证表达式。字段 <code>identifier</code> 与字段 <code>url</code> 互斥。<small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>用于 API 的许可证的 URL。必须采用 URL 格式。</td></tr></tbody></table></details> |

你可以按如下方式设置它们：

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | 提示

你可以在 `description` 字段中编写 Markdown，它会在输出中渲染。

///

通过这样设置，自动 API 文档看起来会像：

<img src="/img/tutorial/metadata/image01.png">

## 许可证标识符 { #license-identifier }

自 OpenAPI 3.1.0 和 FastAPI 0.99.0 起，你还可以在 `license_info` 中使用 `identifier` 而不是 `url`。

例如：

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## 标签元数据 { #metadata-for-tags }

你也可以通过参数 `openapi_tags` 为用于分组路径操作的不同标签添加额外的元数据。

它接收一个列表，列表中每个标签对应一个字典。

每个字典可以包含：

* `name`（**必填**）：一个 `str`，与在你的*路径操作*和 `APIRouter` 的 `tags` 参数中使用的标签名相同。
* `description`：一个 `str`，该标签的简短描述。可以使用 Markdown，并会显示在文档 UI 中。
* `externalDocs`：一个 `dict`，描述外部文档，包含：
    * `description`：一个 `str`，该外部文档的简短描述。
    * `url`（**必填**）：一个 `str`，该外部文档的 URL。

### 创建标签元数据 { #create-metadata-for-tags }

让我们在带有标签的示例中为 `users` 和 `items` 试一下。

创建标签元数据并把它传递给 `openapi_tags` 参数：

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

注意你可以在描述内使用 Markdown，例如「login」会显示为粗体（**login**）以及「fancy」会显示为斜体（_fancy_）。

/// tip | 提示

不必为你使用的所有标签都添加元数据。

///

### 使用你的标签 { #use-your-tags }

将 `tags` 参数和*路径操作*（以及 `APIRouter`）一起使用，将其分配给不同的标签：

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// note | 注意

阅读更多关于标签的信息[路径操作配置](path-operation-configuration.md#tags)。

///

### 查看文档 { #check-the-docs }

如果你现在查看文档，它们会显示所有附加的元数据：

<img src="/img/tutorial/metadata/image02.png">

### 标签顺序 { #order-of-tags }

每个标签元数据字典的顺序也定义了在文档用户界面显示的顺序。

例如按照字母顺序，即使 `users` 排在 `items` 之后，它也会显示在前面，因为我们将它的元数据添加为列表内的第一个字典。

## OpenAPI URL { #openapi-url }

默认情况下，OpenAPI 模式服务于 `/openapi.json`。

但是你可以通过参数 `openapi_url` 对其进行配置。

例如，将其设置为服务于 `/api/v1/openapi.json`：

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

如果你想完全禁用 OpenAPI 模式，可以将其设置为 `openapi_url=None`，这样也会禁用使用它的文档用户界面。

## 文档 URLs { #docs-urls }

你可以配置两个文档用户界面，包括：

* **Swagger UI**：服务于 `/docs`。
    * 可以使用参数 `docs_url` 设置它的 URL。
    * 可以通过设置 `docs_url=None` 禁用它。
* **ReDoc**：服务于 `/redoc`。
    * 可以使用参数 `redoc_url` 设置它的 URL。
    * 可以通过设置 `redoc_url=None` 禁用它。

例如，设置 Swagger UI 服务于 `/documentation` 并禁用 ReDoc：

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}



---

# Source: docs/tutorial/middleware.md


# 中间件 { #middleware }

你可以向 **FastAPI** 应用添加中间件。

“中间件”是一个函数，它会在每个特定的*路径操作*处理每个**请求**之前运行，也会在返回每个**响应**之前运行。

* 它接收你的应用的每一个**请求**。
* 然后它可以对这个**请求**做一些事情或者执行任何需要的代码。
* 然后它将这个**请求**传递给应用程序的其他部分（某个*路径操作*）处理。
* 之后它获取应用程序生成的**响应**（由某个*路径操作*产生）。
* 它可以对该**响应**做一些事情或者执行任何需要的代码。
* 然后它返回这个**响应**。

/// note | 技术细节

如果你有使用 `yield` 的依赖，依赖中的退出代码会在中间件之后运行。

如果有任何后台任务（会在[后台任务](background-tasks.md)一节中介绍，你稍后会看到），它们会在所有中间件之后运行。

///

## 创建中间件 { #create-a-middleware }

要创建中间件，你可以在函数的顶部使用装饰器 `@app.middleware("http")`。

中间件函数会接收：

* `request`。
* 一个函数 `call_next`，它会把 `request` 作为参数接收。
    * 这个函数会把 `request` 传递给相应的*路径操作*。
    * 然后它返回由相应*路径操作*生成的 `response`。
* 在返回之前，你可以进一步修改 `response`。

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip

请记住可以[使用 `X-` 前缀](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)添加专有自定义请求头。

但是如果你有希望让浏览器中的客户端可见的自定义请求头，你需要把它们加到你的 CORS 配置（[CORS（跨域资源共享）](cors.md)）的 `expose_headers` 参数中，参见 [Starlette 的 CORS 文档](https://www.starlette.dev/middleware/#corsmiddleware)。

///

/// note | 技术细节

你也可以使用 `from starlette.requests import Request`。

**FastAPI** 为了开发者方便提供了该对象，但它直接来自 Starlette。

///

### 在 `response` 之前与之后 { #before-and-after-the-response }

你可以在任何*路径操作*接收 `request` 之前，添加要与该 `request` 一起运行的代码。

也可以在生成 `response` 之后、返回之前添加代码。

例如，你可以添加一个自定义请求头 `X-Process-Time`，其值为处理请求并生成响应所花费的秒数：

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip

这里我们使用 [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) 而不是 `time.time()`，因为在这类场景中它可能更精确。🤓

///

## 多个中间件的执行顺序 { #multiple-middleware-execution-order }

当你使用 `@app.middleware()` 装饰器或 `app.add_middleware()` 方法添加多个中间件时，每个新中间件都会包裹应用，形成一个栈。最后添加的中间件是“最外层”的，最先添加的是“最内层”的。

在请求路径上，最外层的中间件先运行。

在响应路径上，它最后运行。

例如：

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

这会产生如下执行顺序：

* 请求：MiddlewareB → MiddlewareA → 路由

* 响应：路由 → MiddlewareA → MiddlewareB

这种栈式行为确保中间件按可预测且可控的顺序执行。

## 其他中间件 { #other-middlewares }

你可以稍后在[高级用户指南：高级中间件](../advanced/middleware.md)中阅读更多关于其他中间件的内容。

你将在下一节中了解如何使用中间件处理 <abbr title="Cross-Origin Resource Sharing - 跨域资源共享">CORS</abbr>。



---

# Source: docs/tutorial/path-operation-configuration.md


# 路径操作配置 { #path-operation-configuration }


*路径操作装饰器*支持多种配置参数。

/// warning | 警告

注意：以下参数应直接传递给*路径操作装饰器*，不能传递给*路径操作函数*。

///

## 响应状态码 { #response-status-code }

可以在*路径操作*的响应中定义（HTTP）`status_code`。

可以直接传递 `int` 代码，比如 `404`。

如果记不住数字码的含义，也可以用 `status` 的快捷常量：

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

该状态码会用于响应中，并会被添加到 OpenAPI 概图。

/// note | 技术细节

也可以使用 `from starlette import status` 导入状态码。

**FastAPI** 提供的 `fastapi.status` 与 `starlette.status` 相同，方便你作为开发者使用。实际上它直接来自 Starlette。

///

## 标签 { #tags }

可以通过传入由 `str` 组成的 `list`（通常只有一个 `str`）的参数 `tags`，为*路径操作*添加标签：

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

OpenAPI 概图会自动添加标签，供 API 文档接口使用：

<img src="/img/tutorial/path-operation-configuration/image01.png">

### 使用 Enum 的标签 { #tags-with-enums }

如果你的应用很大，可能会积累出很多标签，你会希望确保相关的*路径操作*始终使用相同的标签。

这种情况下，把标签存放在 `Enum` 中会更合适。

**FastAPI** 对此的支持与使用普通字符串相同：

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## 摘要和描述 { #summary-and-description }

可以添加 `summary` 和 `description`：

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## 从 docstring 获取描述 { #description-from-docstring }

描述内容比较长且占用多行时，可以在函数的 <dfn title="作为函数内部的第一个表达式（不赋给任何变量）的多行字符串，用于文档用途">文档字符串</dfn> 中声明*路径操作*的描述，**FastAPI** 会从中读取。

文档字符串支持 [Markdown](https://en.wikipedia.org/wiki/Markdown)，能正确解析和显示 Markdown 的内容，但要注意文档字符串的缩进。

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

它会在交互式文档中使用：

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 响应描述 { #response-description }

`response_description` 参数用于定义响应的描述说明：

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// note | 注意

注意，`response_description` 只用于描述响应，`description` 一般则用于描述*路径操作*。

///

/// tip | 提示

OpenAPI 规定每个*路径操作*都要有响应描述。

如果没有定义响应描述，**FastAPI** 则自动生成内容为 "Successful response" 的响应描述。

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## 弃用*路径操作* { #deprecate-a-path-operation }

如果需要把*路径操作*标记为<dfn title="过时，建议不要使用">弃用</dfn>，但不删除它，可以传入 `deprecated` 参数：

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

API 文档会把该路径操作标记为弃用：

<img src="/img/tutorial/path-operation-configuration/image04.png">

下图显示了正常*路径操作*与弃用*路径操作* 的区别：

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 小结 { #recap }

通过传递参数给*路径操作装饰器*，即可轻松地配置*路径操作*、添加元数据。



---

# Source: docs/tutorial/path-params.md


# 路径参数 { #path-parameters }

你可以使用与 Python 字符串格式化相同的语法声明路径“参数”或“变量”：

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

路径参数 `item_id` 的值会作为参数 `item_id` 传递给你的函数。

运行示例并访问 [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo)，可获得如下响应：

```JSON
{"item_id":"foo"}
```

## 声明路径参数的类型 { #path-parameters-with-types }

使用 Python 标准类型注解，声明路径操作函数中路径参数的类型：

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

本例把 `item_id` 的类型声明为 `int`。

/// tip | 提示

类型声明将为函数提供错误检查、代码补全等编辑器支持。

///

## 数据<dfn title="也称为：序列化、解析、编组">转换</dfn> { #data-conversion }

运行示例并访问 [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3)，返回的响应如下：

```JSON
{"item_id":3}
```

/// tip | 提示

注意，函数接收并返回的值是 `3`（ `int`），不是 `"3"`（`str`）。

**FastAPI** 通过类型声明自动进行请求的<dfn title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">解析</dfn>。

///

## 数据校验 { #data-validation }

通过浏览器访问 [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo)，接收如下 HTTP 错误信息：

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

这是因为路径参数 `item_id` 的值（`"foo"`）的类型不是 `int`。

值的类型不是 `int` 而是浮点数（`float`）时也会显示同样的错误，比如： [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

/// tip | 提示

**FastAPI** 使用同样的 Python 类型声明实现了数据校验。

注意，上面的错误清晰地指出了未通过校验的具体位置。

这在开发调试与 API 交互的代码时非常有用。

///

## 文档 { #documentation }

访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)，查看自动生成的交互式 API 文档：

<img src="/img/tutorial/path-params/image01.png">

/// tip | 提示

还是使用 Python 类型声明，**FastAPI** 提供了（集成 Swagger UI 的）自动交互式文档。

注意，路径参数的类型是整数。

///

## 基于标准的好处，备选文档 { #standards-based-benefits-alternative-documentation }

**FastAPI** 使用 [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md) 生成概图，所以能兼容很多工具。

因此，**FastAPI** 还内置了 ReDoc 生成的备选 API 文档，可在此查看 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)：

<img src="/img/tutorial/path-params/image02.png">

同样，还有很多兼容工具，包括多种语言的代码生成工具。

## Pydantic { #pydantic }

所有数据校验都由 [Pydantic](https://docs.pydantic.dev/) 在幕后完成，因此你能从中获得所有好处。而且你可以放心。

同样，`str`、`float`、`bool` 以及很多复合数据类型都可以使用类型声明。

接下来的章节会介绍其中的好几种。

## 顺序很重要 { #order-matters }

有时，*路径操作*中的路径是写死的。

比如要使用 `/users/me` 获取当前用户的数据。

然后还要使用 `/users/{user_id}`，通过用户 ID 获取指定用户的数据。

由于*路径操作*是按顺序依次运行的，因此，一定要在 `/users/{user_id}` 之前声明 `/users/me` ：

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

否则，`/users/{user_id}` 将匹配 `/users/me`，FastAPI 会**认为**正在接收值为 `"me"` 的 `user_id` 参数。

同样，你不能重复定义一个路径操作：

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

由于路径首先匹配，始终会使用第一个定义的。

## 预设值 { #predefined-values }

路径操作使用 Python 的 <abbr title="Enumeration - 枚举">`Enum`</abbr> 类型接收预设的路径参数。

### 创建 `Enum` 类 { #create-an-enum-class }

导入 `Enum` 并创建继承自 `str` 和 `Enum` 的子类。

通过从 `str` 继承，API 文档就能把值的类型定义为**字符串**，并且能正确渲染。

然后，创建包含固定值的类属性，这些固定值是可用的有效值：

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | 提示

**AlexNet**、**ResNet**、**LeNet** 是机器学习<dfn title="技术上来说是深度学习模型架构">模型</dfn>的名字。

///

### 声明路径参数 { #declare-a-path-parameter }

使用 Enum 类（`ModelName`）创建使用类型注解的路径参数：

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### 查看文档 { #check-the-docs }

API 文档会显示预定义路径参数的可用值：

<img src="/img/tutorial/path-params/image03.png">

### 使用 Python 枚举 { #working-with-python-enumerations }

路径参数的值是一个枚举成员。

#### 比较枚举成员 { #compare-enumeration-members }

可以将其与枚举类 `ModelName` 中的枚举成员进行比较：

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### 获取枚举值 { #get-the-enumeration-value }

使用 `model_name.value` 或通用的 `your_enum_member.value` 获取实际的值（本例中为 `str`）：

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | 提示

使用 `ModelName.lenet.value` 也能获取值 `"lenet"`。

///

#### 返回枚举成员 { #return-enumeration-members }

即使嵌套在 JSON 请求体里（例如，`dict`），也可以从路径操作返回枚举成员。

返回给客户端之前，会把枚举成员转换为对应的值（本例中为字符串）：

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

客户端中的 JSON 响应如下：

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## 包含路径的路径参数 { #path-parameters-containing-paths }

假设路径操作的路径为 `/files/{file_path}`。

但需要 `file_path` 中也包含路径，比如，`home/johndoe/myfile.txt`。

此时，该文件的 URL 是这样的：`/files/home/johndoe/myfile.txt`。

### OpenAPI 支持 { #openapi-support }

OpenAPI 不支持声明包含路径的路径参数，因为这会导致测试和定义更加困难。

不过，仍可使用 Starlette 内置工具在 **FastAPI** 中实现这一功能。

而且不影响文档正常运行，但是不会添加该参数包含路径的说明。

### 路径转换器 { #path-convertor }

直接使用 Starlette 的选项声明包含路径的路径参数：

```
/files/{file_path:path}
```

本例中，参数名为 `file_path`，结尾部分的 `:path` 说明该参数应匹配路径。

用法如下：

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | 提示

注意，包含 `/home/johndoe/myfile.txt` 的路径参数要以斜杠（`/`）开头。

本例中的 URL 是 `/files//home/johndoe/myfile.txt`。注意，`files` 和 `home` 之间要使用双斜杠（`//`）。

///

## 小结 { #recap }

通过简短、直观的 Python 标准类型声明，**FastAPI** 可以获得：

- 编辑器支持：错误检查，代码自动补全等
- 数据 "<dfn title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">解析</dfn>"
- 数据校验
- API 注解和自动文档

只需要声明一次即可。

这可能是除了性能以外，**FastAPI** 与其它框架相比的主要优势。



---

# Source: docs/tutorial/path-params-numeric-validations.md


# 路径参数和数值校验 { #path-parameters-and-numeric-validations }

与使用 `Query` 为查询参数声明更多的校验和元数据的方式相同，你也可以使用 `Path` 为路径参数声明相同类型的校验和元数据。

## 导入 `Path` { #import-path }

首先，从 `fastapi` 导入 `Path`，并导入 `Annotated`：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// note | 注意

FastAPI 在 0.95.0 版本添加了对 `Annotated` 的支持（并开始推荐使用它）。

如果你使用的是更旧的版本，尝试使用 `Annotated` 会报错。

请确保在使用 `Annotated` 之前，将 FastAPI 版本[升级](../deployment/versions.md#upgrading-the-fastapi-versions)到至少 0.95.1。

///

## 声明元数据 { #declare-metadata }

你可以声明与 `Query` 相同的所有参数。

例如，要为路径参数 `item_id` 声明 `title` 元数据值，你可以这样写：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | 注意

路径参数总是必需的，因为它必须是路径的一部分。即使你将其声明为 `None` 或设置了默认值，也不会产生任何影响，它依然始终是必需参数。

///

## 按需对参数排序 { #order-the-parameters-as-you-need }

/// tip | 提示

如果你使用 `Annotated`，这点可能不那么重要或必要。

///

假设你想要将查询参数 `q` 声明为必需的 `str`。

并且你不需要为该参数声明其他内容，所以实际上不需要用到 `Query`。

但是你仍然需要为路径参数 `item_id` 使用 `Path`。并且出于某些原因你不想使用 `Annotated`。

如果你将带有“默认值”的参数放在没有“默认值”的参数之前，Python 会报错。

不过你可以重新排序，让没有默认值的参数（查询参数 `q`）放在最前面。

对 **FastAPI** 来说这无关紧要。它会通过参数的名称、类型和默认值声明（`Query`、`Path` 等）来检测参数，而不关心顺序。

因此，你可以将函数声明为：

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

但请记住，如果你使用 `Annotated`，你就不会遇到这个问题，因为你没有使用 `Query()` 或 `Path()` 作为函数参数的默认值。

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## 按需对参数排序的技巧 { #order-the-parameters-as-you-need-tricks }

/// tip | 提示

如果你使用 `Annotated`，这点可能不那么重要或必要。

///

这里有一个小技巧，可能会很方便，但你并不会经常需要它。

如果你想要：

* 在没有 `Query` 且没有任何默认值的情况下声明查询参数 `q`
* 使用 `Path` 声明路径参数 `item_id`
* 让它们的顺序与上面不同
* 不使用 `Annotated`

...Python 为此有一个小的特殊语法。

在函数的第一个参数位置传入 `*`。

Python 不会对这个 `*` 做任何事，但它会知道之后的所有参数都应该作为关键字参数（键值对）来调用，也被称为 <abbr title="来自：K-ey W-ord Arg-uments"><code>kwargs</code></abbr>。即使它们没有默认值。

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### 使用 `Annotated` 更好 { #better-with-annotated }

请记住，如果你使用 `Annotated`，因为你没有使用函数参数的默认值，所以你不会有这个问题，你大概率也不需要使用 `*`。

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## 数值校验：大于等于 { #number-validations-greater-than-or-equal }

使用 `Query` 和 `Path`（以及你稍后会看到的其他类）你可以声明数值约束。

在这里，使用 `ge=1` 后，`item_id` 必须是一个整数，值要「`g`reater than or `e`qual」1。

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## 数值校验：大于和小于等于 { #number-validations-greater-than-and-less-than-or-equal }

同样适用于：

* `gt`：大于（`g`reater `t`han）
* `le`：小于等于（`l`ess than or `e`qual）

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## 数值校验：浮点数、大于和小于 { #number-validations-floats-greater-than-and-less-than }

数值校验同样适用于 `float` 值。

能够声明 <abbr title="greater than - 大于"><code>gt</code></abbr> 而不仅仅是 <abbr title="greater than or equal - 大于等于"><code>ge</code></abbr> 在这里变得很重要。例如，你可以要求一个值必须大于 `0`，即使它小于 `1`。

因此，`0.5` 将是有效值。但是 `0.0` 或 `0` 不是。

对于 <abbr title="less than - 小于"><code>lt</code></abbr> 也是一样的。

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## 总结 { #recap }

你能够以与[查询参数和字符串校验](query-params-str-validations.md)相同的方式使用 `Query`、`Path`（以及其他你还没见过的类）声明元数据和字符串校验。

而且你还可以声明数值校验：

* `gt`：大于（`g`reater `t`han）
* `ge`：大于等于（`g`reater than or `e`qual）
* `lt`：小于（`l`ess `t`han）
* `le`：小于等于（`l`ess than or `e`qual）

/// note | 注意

`Query`、`Path` 以及你后面会看到的其他类，都是一个通用 `Param` 类的子类。

它们都共享相同的参数，用于你已看到的额外校验和元数据。

///

/// note | 技术细节

当你从 `fastapi` 导入 `Query`、`Path` 和其他对象时，它们实际上是函数。

当被调用时，它们会返回同名类的实例。

也就是说，你导入的是函数 `Query`。当你调用它时，它会返回一个同名的 `Query` 类的实例。

之所以使用这些函数（而不是直接使用类），是为了让你的编辑器不要因为它们的类型而标记错误。

这样你就可以使用常规的编辑器和编码工具，而不必添加自定义配置来忽略这些错误。

///



---

# Source: docs/tutorial/query-param-models.md


# 查询参数模型 { #query-parameter-models }

如果你有一组具有相关性的**查询参数**，你可以创建一个 **Pydantic 模型**来声明它们。

这将允许你在**多个地方**去**复用模型**，并且一次性为所有参数声明验证和元数据。😎

/// note | 注意

FastAPI 从 `0.115.0` 版本开始支持这个特性。🤓

///

## 使用 Pydantic 模型的查询参数 { #query-parameters-with-a-pydantic-model }

在一个 **Pydantic 模型**中声明你需要的**查询参数**，然后将参数声明为 `Query`：

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** 将会从请求的**查询参数**中**提取**出**每个字段**的数据，并将其提供给你定义的 Pydantic 模型。

## 查看文档 { #check-the-docs }

你可以在 `/docs` 页面的 UI 中查看查询参数：

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 禁止额外的查询参数 { #forbid-extra-query-parameters }

在一些特殊的使用场景中（可能不是很常见），你可能希望**限制**你要接收的查询参数。

你可以使用 Pydantic 的模型配置来 `forbid` 任何 `extra` 字段：

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

假设有一个客户端尝试在**查询参数**中发送一些**额外的**数据，它将会收到一个**错误**响应。

例如，如果客户端尝试发送一个值为 `plumbus` 的 `tool` 查询参数，如：

```http
https://example.com/items/?limit=10&tool=plumbus
```

他们将收到一个**错误**响应，告诉他们查询参数 `tool` 是不允许的：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## 总结 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中声明**查询参数**。😎

/// tip | 提示

剧透警告：你也可以使用 Pydantic 模型来声明 cookie 和 headers，但你将在本教程的后面部分阅读到这部分内容。🤫

///



---

# Source: docs/tutorial/query-params.md


# 查询参数 { #query-parameters }


声明的参数不是路径参数时，路径操作函数会把该参数自动解释为“查询”参数。

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

查询字符串是键值对的集合，这些键值对位于 URL 的 `?` 之后，以 `&` 分隔。

例如，以下 URL 中：

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...查询参数为：

* `skip`：值为 `0`
* `limit`：值为 `10`

这些值都是 URL 的组成部分，因此，它们的类型“本应”是字符串。

但声明 Python 类型（上例中为 `int`）之后，这些值就会转换为声明的类型，并进行类型校验。

所有应用于路径参数的流程也适用于查询参数：

* （显而易见的）编辑器支持
* 数据<dfn title="将来自 HTTP 请求的字符串转换为 Python 数据">"解析"</dfn>
* 数据校验
* 自动文档

## 默认值 { #defaults }

查询参数不是路径的固定内容，它是可选的，还支持默认值。

上例用 `skip=0` 和 `limit=10` 设定默认值。

访问 URL：

```
http://127.0.0.1:8000/items/
```

与访问以下地址相同：

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

但如果访问：

```
http://127.0.0.1:8000/items/?skip=20
```

查询参数的值就是：

* `skip=20`：在 URL 中设定的值
* `limit=10`：使用默认值

## 可选参数 { #optional-parameters }

同理，把默认值设为 `None` 即可声明可选的查询参数：

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

本例中，查询参数 `q` 是可选的，默认值为 `None`。

/// tip | 提示

注意，**FastAPI** 可以识别出 `item_id` 是路径参数，`q` 不是路径参数，而是查询参数。

///

## 查询参数类型转换 { #query-parameter-type-conversion }

参数还可以声明为 `bool` 类型，FastAPI 会自动转换参数类型：

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

本例中，访问：

```
http://127.0.0.1:8000/items/foo?short=1
```

或

```
http://127.0.0.1:8000/items/foo?short=True
```

或

```
http://127.0.0.1:8000/items/foo?short=true
```

或

```
http://127.0.0.1:8000/items/foo?short=on
```

或

```
http://127.0.0.1:8000/items/foo?short=yes
```

或其它任意大小写形式（大写、首字母大写等），函数接收的 `short` 参数都是布尔值 `True`。否则为 `False`。


## 多个路径和查询参数 { #multiple-path-and-query-parameters }

**FastAPI** 可以识别同时声明的多个路径参数和查询参数。

而且声明查询参数的顺序并不重要。

FastAPI 通过参数名进行检测：

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## 必选查询参数 { #required-query-parameters }

为不是路径参数的参数声明默认值（至此，仅有查询参数），该参数就不是必选的了。

如果只想把参数设为可选，但又不想指定参数的值，则要把默认值设为 `None`。

如果要把查询参数设置为必选，就不要声明默认值：

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

这里的查询参数 `needy` 是类型为 `str` 的必选查询参数。

在浏览器中打开如下 URL：

```
http://127.0.0.1:8000/items/foo-item
```

...因为路径中没有必选参数 `needy`，返回的响应中会显示如下错误信息：

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

`needy` 是必选参数，因此要在 URL 中设置值：

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...这样就正常了：

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

当然，把一些参数定义为必选，为另一些参数设置默认值，再把其它参数定义为可选，这些操作都是可以的：

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

本例中有 3 个查询参数：

* `needy`，必选的 `str` 类型参数
* `skip`，默认值为 `0` 的 `int` 类型参数
* `limit`，可选的 `int` 类型参数

/// tip | 提示

还可以像在[路径参数](path-params.md#predefined-values)中那样使用 `Enum`。

///



---

# Source: docs/tutorial/query-params-str-validations.md


# 查询参数和字符串校验 { #query-parameters-and-string-validations }


**FastAPI** 允许你为参数声明额外的信息和校验。

让我们以下面的应用为例：

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

查询参数 `q` 的类型为 `str | None`，这意味着它是 `str` 类型，但也可以是 `None`。其默认值确实为 `None`，所以 FastAPI 会知道它不是必填的。

/// note | 注意

FastAPI 会因为默认值 `= None` 而知道 `q` 的值不是必填的。

将类型标注为 `str | None` 能让你的编辑器提供更好的辅助和错误检测。

///

## 额外校验 { #additional-validation }

我们打算添加约束：即使 `q` 是可选的，但只要提供了该参数，**其长度不能超过 50 个字符**。

### 导入 `Query` 和 `Annotated` { #import-query-and-annotated }

为此，先导入：

- 从 `fastapi` 导入 `Query`
- 从 `typing` 导入 `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// note | 注意

FastAPI 在 0.95.0 版本中添加了对 `Annotated` 的支持（并开始推荐使用）。

如果你的版本更旧，使用 `Annotated` 会报错。

在使用 `Annotated` 之前，请确保先[升级 FastAPI 版本](../deployment/versions.md#upgrading-the-fastapi-versions)到至少 0.95.1。

///

## 在 `q` 参数的类型中使用 `Annotated` { #use-annotated-in-the-type-for-the-q-parameter }

还记得我之前在[Python 类型简介](../python-types.md#type-hints-with-metadata-annotations)中说过可以用 `Annotated` 给参数添加元数据吗？

现在正是与 FastAPI 搭配使用它的时候。🚀

我们之前的类型标注是：

```Python
q: str | None = None
```

我们要做的是用 `Annotated` 把它包起来，变成：

```Python
q: Annotated[str | None] = None
```

这两种写法含义相同，`q` 是一个可以是 `str` 或 `None` 的参数，默认是 `None`。

现在进入更有趣的部分。🎉

## 在 `q` 的 `Annotated` 中添加 `Query` { #add-query-to-annotated-in-the-q-parameter }

有了 `Annotated` 之后，我们就可以放入更多信息（本例中是额外的校验）。在 `Annotated` 中添加 `Query`，并把参数 `max_length` 设为 `50`：

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

注意默认值依然是 `None`，所以该参数仍是可选的。

但现在把 `Query(max_length=50)` 放到 `Annotated` 里，我们就在告诉 FastAPI，这个值需要**额外校验**，最大长度为 50 个字符。😎

/// tip | 提示

这里用的是 `Query()`，因为这是一个**查询参数**。稍后我们还会看到 `Path()`、`Body()`、`Header()` 和 `Cookie()`，它们也接受与 `Query()` 相同的参数。

///

FastAPI 现在会：

- 对数据进行**校验**，确保最大长度为 50 个字符
- 当数据无效时向客户端展示**清晰的错误**
- 在 OpenAPI 模式的*路径操作*中**记录**该参数（因此会出现在**自动文档 UI** 中）

## 另一种（旧的）方式：把 `Query` 作为默认值 { #alternative-old-query-as-the-default-value }

早期版本的 FastAPI（<dfn title="早于 2023-03">0.95.0</dfn> 之前）要求你把 `Query` 作为参数的默认值，而不是放在 `Annotated` 里。你很可能会在别处看到这种写法，所以我也给你解释一下。

/// tip | 提示

对于新代码以及在可能的情况下，请按上文所述使用 `Annotated`。它有多项优势（如下所述），没有劣势。🍰

///

像这样把 `Query()` 作为函数参数的默认值，并把参数 `max_length` 设为 50：

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

由于这种情况下（不使用 `Annotated`）我们必须把函数中的默认值 `None` 替换为 `Query()`，因此需要通过参数 `Query(default=None)` 来设置默认值，它起到同样的作用（至少对 FastAPI 来说）。

所以：

```Python
q: str | None = Query(default=None)
```

...会让参数变成可选，默认值为 `None`，等同于：

```Python
q: str | None = None
```

但使用 `Query` 的版本会显式把它声明为一个查询参数。

然后，我们可以向 `Query` 传入更多参数。本例中是适用于字符串的 `max_length` 参数：

```Python
q: str | None = Query(default=None, max_length=50)
```

这会校验数据、在数据无效时展示清晰的错误，并在 OpenAPI 模式的*路径操作*中记录该参数。

### 在默认值中使用 `Query` 或在 `Annotated` 中使用 `Query` { #query-as-the-default-value-or-in-annotated }

注意，当你在 `Annotated` 中使用 `Query` 时，不能再给 `Query` 传 `default` 参数。

相反，应使用函数参数本身的实际默认值。否则会不一致。

例如，下面这样是不允许的：

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...因为不清楚默认值应该是 `"rick"` 还是 `"morty"`。

因此，你应该这样用（推荐）：

```Python
q: Annotated[str, Query()] = "rick"
```

...或者在旧代码库中你会见到：

```Python
q: str = Query(default="rick")
```

### `Annotated` 的优势 { #advantages-of-annotated }

**推荐使用 `Annotated`**，而不是把 `Query` 放在函数参数的默认值里，这样做在多方面都**更好**。🤓

函数参数的**默认值**就是**真正的默认值**，这与 Python 的直觉更一致。😌

你可以在**其他地方**不通过 FastAPI **直接调用**这个函数，而且它会**按预期工作**。如果有**必填**参数（没有默认值），你的**编辑器**会报错提示；如果在运行时没有传入必填参数，**Python** 也会报错。

当你不使用 `Annotated` 而是使用**（旧的）默认值风格**时，如果你在**其他地方**不通过 FastAPI 调用该函数，你必须**记得**给函数传参，否则得到的值会和预期不同（例如得到 `QueryInfo` 之类的对象而不是 `str`）。而你的编辑器不会报错，Python 也不会在调用时报错，只有在函数内部的操作出错时才会暴露问题。

由于 `Annotated` 可以包含多个元数据标注，你甚至可以用同一个函数与其他工具配合，例如 [Typer](https://typer.tiangolo.com/)。🚀

## 添加更多校验 { #add-more-validations }

你还可以添加 `min_length` 参数：

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## 添加正则表达式 { #add-regular-expressions }

你可以定义一个参数必须匹配的 <dfn title="正则表达式（regex 或 regexp）是用于定义字符串搜索模式的字符序列。">正则表达式</dfn> `pattern`：

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

这个特定的正则表达式通过以下规则检查接收到的参数值：

- `^`：必须以接下来的字符开头，前面没有其他字符。
- `fixedquery`：值必须精确等于 `fixedquery`。
- `$`：到此结束，在 `fixedquery` 之后没有更多字符。

如果你对这些**「正则表达式」**概念感到迷茫，不必担心。对很多人来说这都是个难点。你仍然可以在不使用正则表达式的情况下做很多事情。

现在你知道了，一旦需要时，你可以在 **FastAPI** 中直接使用它们。

## 默认值 { #default-values }

当然，你也可以使用 `None` 以外的默认值。

假设你想要声明查询参数 `q` 的 `min_length` 为 `3`，并且默认值为 `"fixedquery"`：

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | 注意

任何类型的默认值（包括 `None`）都会让该参数变为可选（非必填）。

///

## 必填参数 { #required-parameters }

当我们不需要声明更多校验或元数据时，只需不声明默认值就可以让查询参数 `q` 成为必填参数，例如：

```Python
q: str
```

而不是：

```Python
q: str | None = None
```

但现在我们用 `Query` 来声明它，例如：

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

因此，在使用 `Query` 的同时需要把某个值声明为必填时，只需不声明默认值：

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### 必填，但可以为 `None` { #required-can-be-none }

你可以声明一个参数可以接收 `None`，但它仍然是必填的。这将强制客户端必须发送一个值，即使该值是 `None`。

为此，你可以声明 `None` 是有效类型，但不声明默认值：

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## 查询参数列表 / 多个值 { #query-parameter-list-multiple-values }

当你用 `Query` 显式地定义查询参数时，你还可以声明它接收一个值列表，换句话说，接收多个值。

例如，要声明一个可在 URL 中出现多次的查询参数 `q`，你可以这样写：

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

然后，访问如下 URL：

```
http://localhost:8000/items/?q=foo&q=bar
```

你会在*路径操作函数*的*函数参数* `q` 中以一个 Python `list` 的形式接收到多个 `q` *查询参数* 的值（`foo` 和 `bar`）。

因此，该 URL 的响应将会是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | 提示

要声明类型为 `list` 的查询参数（如上例），你需要显式地使用 `Query`，否则它会被解释为请求体。

///

交互式 API 文档会相应更新，以支持多个值：

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 具有默认值的查询参数列表 / 多个值 { #query-parameter-list-multiple-values-with-defaults }

你还可以定义在没有给定值时的默认 `list`：

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

如果你访问：

```
http://localhost:8000/items/
```

`q` 的默认值将为：`["foo", "bar"]`，你的响应会是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### 只使用 `list` { #using-just-list }

你也可以直接使用 `list`，而不是 `list[str]`：

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | 注意

请记住，在这种情况下 FastAPI 不会检查列表的内容。

例如，`list[int]` 会检查（并记录到文档）列表的内容必须是整数。但仅用 `list` 不会。

///

## 声明更多元数据 { #declare-more-metadata }

你可以添加更多有关该参数的信息。

这些信息会包含在生成的 OpenAPI 中，并被文档用户界面和外部工具使用。

/// note | 注意

请记住，不同的工具对 OpenAPI 的支持程度可能不同。

其中一些可能还不会展示所有已声明的额外信息，尽管在大多数情况下，缺失的功能已经在计划开发中。

///

你可以添加 `title`：

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

以及 `description`：

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## 别名参数 { #alias-parameters }

假设你想要参数名为 `item-query`。

像这样：

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

但 `item-query` 不是有效的 Python 变量名。

最接近的有效名称是 `item_query`。

但你仍然需要它在 URL 中就是 `item-query`...

这时可以用 `alias` 参数声明一个别名，FastAPI 会用该别名在 URL 中查找参数值：

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## 弃用参数 { #deprecating-parameters }

现在假设你不再喜欢这个参数了。

由于还有客户端在使用它，你不得不保留一段时间，但你希望文档清楚地将其展示为<dfn title="已过时，不推荐使用">已弃用</dfn>。

那么将参数 `deprecated=True` 传给 `Query`：

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

文档将会像下面这样展示它：

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 从 OpenAPI 中排除参数 { #exclude-parameters-from-openapi }

要把某个查询参数从生成的 OpenAPI 模式中排除（从而也不会出现在自动文档系统中），将 `Query` 的参数 `include_in_schema` 设为 `False`：

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## 自定义校验 { #custom-validation }

有些情况下你需要做一些无法通过上述参数完成的**自定义校验**。

在这些情况下，你可以使用**自定义校验函数**，该函数会在正常校验之后应用（例如，在先校验值是 `str` 之后）。

你可以在 `Annotated` 中使用 [Pydantic 的 `AfterValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator) 来实现。

/// tip | 提示

Pydantic 还有 [`BeforeValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator) 等。🤓

///

例如，这个自定义校验器会检查条目 ID 是否以 `isbn-`（用于 <abbr title="International Standard Book Number - 国际标准书号">ISBN</abbr> 书号）或 `imdb-`（用于 <abbr title="Internet Movie Database - 互联网电影数据库: 一个包含电影信息的网站">IMDB</abbr> 电影 URL 的 ID）开头：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// note | 注意

这在 Pydantic 2 或更高版本中可用。😎

///

/// tip | 提示

如果你需要进行任何需要与**外部组件**通信的校验，例如数据库或其他 API，你应该改用 **FastAPI 依赖项**，稍后你会学到它们。

这些自定义校验器用于只需检查请求中**同一份数据**即可完成的事情。

///

### 理解这段代码 { #understand-that-code }

关键点仅仅是：在 `Annotated` 中使用带函数的 **`AfterValidator`**。不感兴趣可以跳过这一节。🤸

---

但如果你对这个具体示例好奇，并且还愿意继续看，这里有一些额外细节。

#### 字符串与 `value.startswith()` { #string-with-value-startswith }

注意到了吗？字符串的 `value.startswith()` 可以接收一个元组，它会检查元组中的每个值：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### 一个随机条目 { #a-random-item }

使用 `data.items()` 我们会得到一个包含每个字典项键和值的元组的 <dfn title="可以用 for 循环迭代的对象，例如 list、set 等">可迭代对象</dfn>。

我们用 `list(data.items())` 把这个可迭代对象转换成一个真正的 `list`。

然后用 `random.choice()` 可以从该列表中获取一个**随机值**，也就是一个 `(id, name)` 的元组。它可能像 `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")` 这样。

接着我们把这个元组的**两个值**分别赋给变量 `id` 和 `name`。

所以，即使用户没有提供条目 ID，他们仍然会收到一个随机推荐。

...而我们把这些都放在**一行简单的代码**里完成。🤯 你不爱 Python 吗？🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## 总结 { #recap }

你可以为参数声明额外的校验和元数据。

通用的校验和元数据：

- `alias`
- `title`
- `description`
- `deprecated`

字符串特有的校验：

- `min_length`
- `max_length`
- `pattern`

也可以使用 `AfterValidator` 进行自定义校验。

在这些示例中，你看到了如何为 `str` 值声明校验。

参阅下一章节，了解如何为其他类型（例如数值）声明校验。



---

# Source: docs/tutorial/request-files.md


# 请求文件 { #request-files }

你可以使用 `File` 定义由客户端上传的文件。

/// note | 注意

要接收上传的文件，请先安装 [`python-multipart`](https://github.com/Kludex/python-multipart)。

请确保你创建一个[虚拟环境](../virtual-environments.md)、激活它，然后安装，例如：

```console
$ pip install python-multipart
```

这是因为上传文件是以「表单数据」发送的。

///

## 导入 `File` { #import-file }

从 `fastapi` 导入 `File` 和 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## 定义 `File` 参数 { #define-file-parameters }

像为 `Body` 或 `Form` 一样创建文件参数：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// note | 注意

`File` 是直接继承自 `Form` 的类。

但要注意，从 `fastapi` 导入的 `Query`、`Path`、`File` 等项，实际上是返回特定类的函数。

///

/// tip | 提示

声明文件体必须使用 `File`，否则，这些参数会被当作查询参数或请求体（JSON）参数。

///

文件将作为「表单数据」上传。

如果把*路径操作函数*参数的类型声明为 `bytes`，**FastAPI** 会为你读取文件，并以 `bytes` 的形式接收其内容。

请注意，这意味着整个内容会存储在内存中，适用于小型文件。

不过，在很多情况下，使用 `UploadFile` 会更有优势。

## 含 `UploadFile` 的文件参数 { #file-parameters-with-uploadfile }

将文件参数的类型声明为 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

与 `bytes` 相比，使用 `UploadFile` 有多项优势：

* 无需在参数的默认值中使用 `File()`。
* 它使用“spooled”文件：
    * 文件会先存储在内存中，直到达到最大上限，超过该上限后会写入磁盘。
* 因此，非常适合处理图像、视频、大型二进制等大文件，而不会占用所有内存。
* 你可以获取上传文件的元数据。
* 它提供 [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) 的 `async` 接口。
* 它暴露了一个实际的 Python [`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) 对象，你可以直接传给期望「file-like」对象的其他库。

### `UploadFile` { #uploadfile }

`UploadFile` 的属性如下：

* `filename`：上传的原始文件名字符串（`str`），例如 `myimage.jpg`。
* `content_type`：内容类型（MIME 类型 / 媒体类型）的字符串（`str`），例如 `image/jpeg`。
* `file`：[`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile)（一个 [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) 对象）。这是实际的 Python 文件对象，你可以直接传递给其他期望「file-like」对象的函数或库。

`UploadFile` 具有以下 `async` 方法。它们都会在底层调用对应的文件方法（使用内部的 `SpooledTemporaryFile`）。

* `write(data)`：将 `data` (`str` 或 `bytes`) 写入文件。
* `read(size)`：读取文件中 `size` (`int`) 个字节/字符。
* `seek(offset)`：移动到文件中字节位置 `offset` (`int`)。
    * 例如，`await myfile.seek(0)` 会移动到文件开头。
    * 如果你先运行过 `await myfile.read()`，然后需要再次读取内容时，这尤其有用。
* `close()`：关闭文件。

由于这些方法都是 `async` 方法，你需要对它们使用 await。

例如，在 `async` *路径操作函数* 内，你可以这样获取内容：

```Python
contents = await myfile.read()
```

如果是在普通 `def` *路径操作函数* 内，你可以直接访问 `UploadFile.file`，例如：

```Python
contents = myfile.file.read()
```

/// note | `async` 技术细节

当你使用这些 `async` 方法时，**FastAPI** 会在线程池中运行相应的文件方法并等待其完成。

///

/// note | Starlette 技术细节

**FastAPI** 的 `UploadFile` 直接继承自 **Starlette** 的 `UploadFile`，但添加了一些必要的部分，使其与 **Pydantic** 以及 FastAPI 的其他部分兼容。

///

## 什么是「表单数据」 { #what-is-form-data }

HTML 表单（`<form></form>`）向服务器发送数据的方式通常会对数据使用一种「特殊」的编码，这与 JSON 不同。

**FastAPI** 会确保从正确的位置读取这些数据，而不是从 JSON 中读取。

/// note | 技术细节

当不包含文件时，来自表单的数据通常使用「媒体类型」`application/x-www-form-urlencoded` 编码。

但当表单包含文件时，会编码为 `multipart/form-data`。如果你使用 `File`，**FastAPI** 会知道需要从请求体的正确位置获取文件。

如果你想进一步了解这些编码和表单字段，请参阅 [<abbr title="Mozilla Developer Network - Mozilla 开发者网络">MDN</abbr> 关于 `POST` 的 Web 文档](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST)。

///

/// warning | 警告

你可以在一个*路径操作*中声明多个 `File` 和 `Form` 参数，但不能同时声明希望以 JSON 接收的 `Body` 字段，因为此时请求体会使用 `multipart/form-data` 编码，而不是 `application/json`。

这不是 **FastAPI** 的限制，而是 HTTP 协议的一部分。

///

## 可选文件上传 { #optional-file-upload }

你可以通过使用标准类型注解并将 `None` 作为默认值的方式将一个文件参数设为可选:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## 带有额外元数据的 `UploadFile` { #uploadfile-with-additional-metadata }

你也可以将 `File()` 与 `UploadFile` 一起使用，例如，设置额外的元数据:

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## 多文件上传 { #multiple-file-uploads }

可以同时上传多个文件。

它们会被关联到同一个通过「表单数据」发送的「表单字段」。

要实现这一点，声明一个由 `bytes` 或 `UploadFile` 组成的列表（`List`）：

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

接收的也是含 `bytes` 或 `UploadFile` 的列表（`list`）。

/// note | 技术细节

也可以使用 `from starlette.responses import HTMLResponse`。

`fastapi.responses` 其实与 `starlette.responses` 相同，只是为了方便开发者调用。实际上，大多数 **FastAPI** 的响应都直接从 Starlette 调用。

///

### 带有额外元数据的多文件上传 { #multiple-file-uploads-with-additional-metadata }

和之前的方式一样，你可以为 `File()` 设置额外参数，即使是 `UploadFile`：

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## 小结 { #recap }

使用 `File`、`bytes` 和 `UploadFile` 来声明在请求中上传的文件，它们以表单数据发送。



---

# Source: docs/tutorial/request-form-models.md


# 表单模型 { #form-models }

你可以在 FastAPI 中使用 **Pydantic 模型**声明**表单字段**。

/// note | 注意

要使用表单，首先安装 [`python-multipart`](https://github.com/Kludex/python-multipart)。

确保你创建一个[虚拟环境](../virtual-environments.md)，激活它，然后再安装，例如：

```console
$ pip install python-multipart
```

///

/// note | 注意

自 FastAPI 版本 `0.113.0` 起支持此功能。🤓

///

## 表单的 Pydantic 模型 { #pydantic-models-for-forms }

你只需声明一个 **Pydantic 模型**，其中包含你希望接收的**表单字段**，然后将参数声明为 `Form`：

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** 将从请求中的**表单数据**中**提取**出**每个字段**的数据，并提供你定义的 Pydantic 模型。

## 检查文档 { #check-the-docs }

你可以在文档 UI 中验证它，地址为 `/docs`：

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 禁止额外的表单字段 { #forbid-extra-form-fields }

在某些特殊使用情况下（可能并不常见），你可能希望将表单字段**限制**为仅在 Pydantic 模型中声明过的字段，并**禁止**任何**额外**的字段。

/// note | 注意

自 FastAPI 版本 `0.114.0` 起支持此功能。🤓

///

你可以使用 Pydantic 的模型配置来 `forbid` 任何 `extra` 字段：

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

如果客户端尝试发送一些额外的数据，他们将收到**错误**响应。

例如，客户端尝试发送如下表单字段：

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

他们将收到一条错误响应，表明字段 `extra` 不被允许：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## 总结 { #summary }

你可以使用 Pydantic 模型在 FastAPI 中声明表单字段。😎



---

# Source: docs/tutorial/request-forms.md


# 表单数据 { #form-data }

当你需要接收表单字段而不是 JSON 时，可以使用 `Form`。

/// note | 注意

要使用表单，首先安装 [`python-multipart`](https://github.com/Kludex/python-multipart)。

请先创建并激活一个[虚拟环境](../virtual-environments.md)，然后再进行安装，例如：

```console
$ pip install python-multipart
```

///

## 导入 `Form` { #import-form }

从 `fastapi` 导入 `Form`：

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## 定义 `Form` 参数 { #define-form-parameters }

创建表单参数的方式与 `Body` 或 `Query` 相同：

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

例如，在 OAuth2 规范的一种使用方式（称为“密码流”）中，要求将 `username` 和 `password` 作为表单字段发送。

<dfn title="规范">规范</dfn>要求这些字段必须精确命名为 `username` 和 `password`，并且作为表单字段发送，而不是 JSON。

使用 `Form` 可以像使用 `Body`（以及 `Query`、`Path`、`Cookie`）一样声明相同的配置，包括校验、示例、别名（例如将 `username` 写成 `user-name`）等。

/// note | 注意

`Form` 是直接继承自 `Body` 的类。

///

/// tip | 提示

要声明表单请求体，必须显式使用 `Form`，否则这些参数会被当作查询参数或请求体（JSON）参数。

///

## 关于 "表单字段" { #about-form-fields }

HTML 表单（`<form></form>`）向服务器发送数据时通常会对数据使用一种“特殊”的编码方式，这与 JSON 不同。

**FastAPI** 会确保从正确的位置读取这些数据，而不是从 JSON 中读取。

/// note | 技术细节

表单数据通常使用“媒体类型” `application/x-www-form-urlencoded` 进行编码。

但当表单包含文件时，会编码为 `multipart/form-data`。你将在下一章阅读如何处理文件。

如果你想了解更多关于这些编码和表单字段的信息，请参阅 [<abbr title="Mozilla Developer Network - Mozilla 开发者网络">MDN</abbr> Web 文档的 `POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST)。

///

/// warning | 警告

你可以在一个*路径操作*中声明多个 `Form` 参数，但不能同时再声明要接收为 JSON 的 `Body` 字段，因为此时请求体会使用 `application/x-www-form-urlencoded` 而不是 `application/json` 进行编码。

这不是 **FastAPI** 的限制，而是 HTTP 协议的一部分。

///

## 小结 { #recap }

使用 `Form` 来声明表单数据输入参数。



---

# Source: docs/tutorial/request-forms-and-files.md


# 请求表单与文件 { #request-forms-and-files }

FastAPI 支持同时使用 `File` 和 `Form` 定义文件和表单字段。

/// note | 注意

接收上传的文件和/或表单数据，首先安装 [`python-multipart`](https://github.com/Kludex/python-multipart)。

请先创建并激活一个[虚拟环境](../virtual-environments.md)，然后再安装，例如：

```console
$ pip install python-multipart
```

///

## 导入 `File` 与 `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## 定义 `File` 与 `Form` 参数 { #define-file-and-form-parameters }

创建文件和表单参数的方式与 `Body` 和 `Query` 一样：

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

文件和表单字段作为表单数据上传与接收。

并且你可以将部分文件声明为 `bytes`，将部分文件声明为 `UploadFile`。

/// warning | 警告

可在一个*路径操作*中声明多个 `File` 与 `Form` 参数，但不能同时声明要接收 JSON 的 `Body` 字段。因为此时请求体的编码为 `multipart/form-data`，不是 `application/json`。

这不是 **FastAPI** 的问题，而是 HTTP 协议的规定。

///

## 小结 { #recap }

在同一个请求中接收数据和文件时，应同时使用 `File` 和 `Form`。



---

# Source: docs/tutorial/response-model.md


# 响应模型 - 返回类型 { #response-model-return-type }

你可以通过为*路径操作函数*的**返回类型**添加注解来声明用于响应的类型。

和为输入数据在函数**参数**里做类型注解的方式相同，你可以使用 Pydantic 模型、`list`、`dict`、以及整数、布尔值等标量类型。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI 会使用这个返回类型来：

* 对返回数据进行**校验**。
    * 如果数据无效（例如缺少某个字段），这意味着你的应用代码有问题，没有返回应有的数据，FastAPI 将返回服务器错误而不是返回错误的数据。这样你和你的客户端都可以确定会收到期望的数据及其结构。
* 在 OpenAPI 的*路径操作*中为响应添加**JSON Schema**。
    * 它会被**自动文档**使用。
    * 它也会被自动客户端代码生成工具使用。
* 使用 Pydantic 将返回数据**序列化**为 JSON。Pydantic 使用**Rust**编写，因此会**快很多**。

但更重要的是：

* 它会将输出数据**限制并过滤**为返回类型中定义的内容。
    * 这对**安全性**尤为重要，下面会进一步介绍。

## `response_model` 参数 { #response-model-parameter }

在一些情况下，你需要或希望返回的数据与声明的类型不完全一致。

例如，你可能希望**返回一个字典**或数据库对象，但**将其声明为一个 Pydantic 模型**。这样 Pydantic 模型就会为你返回的对象（例如字典或数据库对象）完成文档、校验等工作。

如果你添加了返回类型注解，工具和编辑器会（正确地）报错，提示你的函数返回的类型（例如 `dict`）与声明的类型（例如一个 Pydantic 模型）不同。

在这些情况下，你可以使用*路径操作装饰器*参数 `response_model`，而不是返回类型。

你可以在任意*路径操作*中使用 `response_model` 参数：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等等。

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | 注意

注意，`response_model` 是「装饰器」方法（`get`、`post` 等）的一个参数。不是你的*路径操作函数*的参数，不像所有查询参数和请求体那样。

///

`response_model` 接收的类型与为 Pydantic 模型字段声明的类型相同，因此它可以是一个 Pydantic 模型，也可以是一个由 Pydantic 模型组成的 `list`，例如 `List[Item]`。

FastAPI 会使用这个 `response_model` 来完成数据文档、校验等，并且还会将输出数据**转换并过滤**为其类型声明。

/// tip | 提示

如果你的编辑器、mypy 等进行严格类型检查，你可以将函数返回类型声明为 `Any`。

这样你告诉编辑器你是有意返回任意类型。但 FastAPI 仍会使用 `response_model` 做数据文档、校验、过滤等工作。

///

### `response_model` 的优先级 { #response-model-priority }

如果你同时声明了返回类型和 `response_model`，`response_model` 会具有优先级并由 FastAPI 使用。

这样，即使你返回的类型与响应模型不同，你也可以为函数添加正确的类型注解，供编辑器和 mypy 等工具使用。同时你仍然可以让 FastAPI 使用 `response_model` 进行数据校验、文档等。

你也可以使用 `response_model=None` 来禁用该*路径操作*的响应模型生成；当你为一些不是有效 Pydantic 字段的东西添加类型注解时，可能需要这样做，下面的章节会有示例。

## 返回与输入相同的数据 { #return-the-same-input-data }

这里我们声明一个 `UserIn` 模型，它包含一个明文密码：

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// note | 注意

要使用 `EmailStr`，首先安装 [`email-validator`](https://github.com/JoshData/python-email-validator)。

请先创建并激活一个[虚拟环境](../virtual-environments.md)，然后安装，例如：

```console
$ pip install email-validator
```

或者：

```console
$ pip install "pydantic[email]"
```

///

我们使用这个模型来声明输入，同时也用相同的模型来声明输出：

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

现在，每当浏览器使用密码创建用户时，API 会在响应中返回相同的密码。

在这个场景下，这可能不算问题，因为发送密码的是同一个用户。

但如果我们在其他*路径操作*中使用相同的模型，就可能会把用户的密码发送给每个客户端。

/// danger | 危险

除非你非常清楚所有注意事项并确实知道自己在做什么，否则永远不要存储用户的明文密码，也不要像这样在响应中发送它。

///

## 添加输出模型 { #add-an-output-model }

相反，我们可以创建一个包含明文密码的输入模型和一个不包含它的输出模型：

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

这里，即使我们的*路径操作函数*返回的是包含密码的同一个输入用户：

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...我们仍将 `response_model` 声明为不包含密码的 `UserOut` 模型：

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

因此，**FastAPI** 会负责过滤掉输出模型中未声明的所有数据（使用 Pydantic）。

### `response_model` 还是返回类型 { #response-model-or-return-type }

在这个例子中，因为两个模型不同，如果我们将函数返回类型注解为 `UserOut`，编辑器和工具会抱怨我们返回了无效类型，因为它们是不同的类。

这就是为什么在这个例子里我们必须在 `response_model` 参数中声明它。

...但继续往下读，看看如何更好地处理这种情况。

## 返回类型与数据过滤 { #return-type-and-data-filtering }

延续上一个例子。我们希望**用一种类型来注解函数**，但希望从函数返回的内容实际上可以**包含更多数据**。

我们希望 FastAPI 继续使用响应模型来**过滤**数据。这样即使函数返回了更多数据，响应也只会包含响应模型中声明的字段。

在上一个例子中，因为类不同，我们不得不使用 `response_model` 参数。但这也意味着我们无法从编辑器和工具处获得对函数返回类型的检查支持。

不过在大多数需要这样做的场景里，我们只是希望模型像这个例子中那样**过滤/移除**一部分数据。

在这些场景里，我们可以使用类和继承，既利用函数的**类型注解**获取更好的编辑器和工具支持，又能获得 FastAPI 的**数据过滤**。

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

这样一来，我们既能从编辑器和 mypy 获得工具支持（这段代码在类型上是正确的），也能从 FastAPI 获得数据过滤。

这是如何做到的？我们来看看。🤓

### 类型注解与工具链 { #type-annotations-and-tooling }

先看看编辑器、mypy 和其他工具会如何看待它。

`BaseUser` 有基础字段。然后 `UserIn` 继承自 `BaseUser` 并新增了 `password` 字段，因此它包含了两个模型的全部字段。

我们把函数返回类型注解为 `BaseUser`，但实际上返回的是一个 `UserIn` 实例。

编辑器、mypy 和其他工具不会对此抱怨，因为在类型系统里，`UserIn` 是 `BaseUser` 的子类，这意味着当期望 `BaseUser` 时，返回 `UserIn` 是*合法*的。

### FastAPI 的数据过滤 { #fastapi-data-filtering }

对于 FastAPI，它会查看返回类型并确保你返回的内容**只**包含该类型中声明的字段。

FastAPI 在内部配合 Pydantic 做了多项处理，确保不会把类继承的这些规则用于返回数据的过滤，否则你可能会返回比预期多得多的数据。

这样，你就能兼得两方面的优势：带有**工具支持**的类型注解和**数据过滤**。

## 在文档中查看 { #see-it-in-the-docs }

当你查看自动文档时，你会看到输入模型和输出模型都会有各自的 JSON Schema：

<img src="/img/tutorial/response-model/image01.png">

并且两个模型都会用于交互式 API 文档：

<img src="/img/tutorial/response-model/image02.png">

## 其他返回类型注解 { #other-return-type-annotations }

有些情况下你会返回一些不是有效 Pydantic 字段的内容，并在函数上做了相应注解，只是为了获得工具链（编辑器、mypy 等）的支持。

### 直接返回 Response { #return-a-response-directly }

最常见的情况是[直接返回 Response，详见进阶文档](../advanced/response-directly.md)。

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

这个简单场景 FastAPI 会自动处理，因为返回类型注解是 `Response`（或其子类）。

工具也会满意，因为 `RedirectResponse` 和 `JSONResponse` 都是 `Response` 的子类，所以类型注解是正确的。

### 注解 Response 的子类 { #annotate-a-response-subclass }

你也可以在类型注解中使用 `Response` 的子类：

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

这同样可行，因为 `RedirectResponse` 是 `Response` 的子类，FastAPI 会自动处理这个简单场景。

### 无效的返回类型注解 { #invalid-return-type-annotations }

但当你返回其他任意对象（如数据库对象）而它不是有效的 Pydantic 类型，并在函数中按此进行了注解时，FastAPI 会尝试基于该类型注解创建一个 Pydantic 响应模型，但会失败。

如果你有一个在多个类型之间的<dfn title="多个类型的联合表示“这些类型中的任意一个”。">联合类型</dfn>，其中一个或多个不是有效的 Pydantic 类型，也会发生同样的情况，例如这个会失败 💥：

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...它失败是因为该类型注解不是 Pydantic 类型，也不只是单个 `Response` 类或其子类，而是 `Response` 与 `dict` 的联合类型（任意其一）。

### 禁用响应模型 { #disable-response-model }

延续上面的例子，你可能不想要 FastAPI 执行默认的数据校验、文档、过滤等。

但你可能仍然想在函数上保留返回类型注解，以获得编辑器和类型检查器（如 mypy）的支持。

在这种情况下，你可以通过设置 `response_model=None` 来禁用响应模型生成：

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

这会让 FastAPI 跳过响应模型的生成，这样你就可以按需使用任意返回类型注解，而不会影响你的 FastAPI 应用。🤓

## 响应模型的编码参数 { #response-model-encoding-parameters }

你的响应模型可以具有默认值，例如：

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None`（或在 Python 3.10 中的 `str | None = None`）默认值为 `None`。
* `tax: float = 10.5` 默认值为 `10.5`。
* `tags: List[str] = []` 默认值为一个空列表：`[]`。

但如果它们并没有被实际存储，你可能希望在结果中省略这些默认值。

例如，当你在 NoSQL 数据库中保存了具有许多可选属性的模型，但又不想发送充满默认值的冗长 JSON 响应。

### 使用 `response_model_exclude_unset` 参数 { #use-the-response-model-exclude-unset-parameter }

你可以设置*路径操作装饰器*参数 `response_model_exclude_unset=True`：

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

这样响应中将不会包含那些默认值，而只包含实际设置的值。

因此，如果你向该*路径操作*请求 ID 为 `foo` 的商品，响应（不包括默认值）将为：

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// note | 注意

你还可以使用：

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

详见 [Pydantic 文档](https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict)中对 `exclude_defaults` 和 `exclude_none` 的说明。

///

#### 默认字段有实际值的数据 { #data-with-values-for-fields-with-defaults }

但是，如果你的数据在具有默认值的模型字段中有实际的值，例如 ID 为 `bar` 的项：

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

这些值将包含在响应中。

#### 具有与默认值相同值的数据 { #data-with-the-same-values-as-the-defaults }

如果数据具有与默认值相同的值，例如 ID 为 `baz` 的项：

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI 足够聪明（实际上是 Pydantic 足够聪明）去认识到，即使 `description`、`tax` 和 `tags` 的值与默认值相同，它们也是被显式设置的（而不是取自默认值）。

因此，它们将包含在 JSON 响应中。

/// tip | 提示

请注意默认值可以是任何值，而不仅是 `None`。

它们可以是一个列表（`[]`）、值为 `10.5` 的 `float`，等等。

///

### `response_model_include` 和 `response_model_exclude` { #response-model-include-and-response-model-exclude }

你还可以使用*路径操作装饰器*的 `response_model_include` 和 `response_model_exclude` 参数。

它们接收一个由属性名 `str` 组成的 `set`，用于包含（忽略其他）或排除（包含其他）这些属性。

当你只有一个 Pydantic 模型，并且想要从输出中移除一些数据时，这可以作为一种快捷方式。

/// tip | 提示

但仍然推荐使用上面的思路，使用多个类，而不是这些参数。

因为即使你使用 `response_model_include` 或 `response_model_exclude` 省略了一些属性，你的应用在 OpenAPI（和文档）中生成的 JSON Schema 仍然会是完整模型。

这同样适用于类似的 `response_model_by_alias`。

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | 提示

`{"name", "description"}` 语法创建一个包含这两个值的 `set`。

等同于 `set(["name", "description"])`。

///

#### 使用 `list` 而不是 `set` { #using-lists-instead-of-sets }

如果你忘记使用 `set` 而是使用了 `list` 或 `tuple`，FastAPI 仍会将其转换为 `set` 并正常工作：

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## 总结 { #recap }

使用*路径操作装饰器*的 `response_model` 参数来定义响应模型，尤其是确保私有数据被过滤掉。

使用 `response_model_exclude_unset` 来仅返回显式设置的值。



---

# Source: docs/tutorial/response-status-code.md


# 响应状态码 { #response-status-code }

与指定响应模型的方式相同，在以下任意*路径操作*中，可以使用 `status_code` 参数声明用于响应的 HTTP 状态码：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等。

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | 注意

注意，`status_code` 是（`get`、`post` 等）**装饰器**方法中的参数。与之前的参数和请求体不同，不是*路径操作函数*的参数。

///

`status_code` 参数接收表示 HTTP 状态码的数字。

/// note | 注意

`status_code` 还能接收 `IntEnum` 类型，比如 Python 的 [`http.HTTPStatus`](https://docs.python.org/3/library/http.html#http.HTTPStatus)。

///

它可以：

* 在响应中返回状态码
* 在 OpenAPI schema（以及用户界面）中将其记录为该状态码：

<img src="/img/tutorial/response-status-code/image01.png">

/// note | 注意

某些响应状态码表示响应没有响应体（参阅下一节）。

FastAPI 可以进行识别，并生成表明无响应体的 OpenAPI 文档。

///

## 关于 HTTP 状态码 { #about-http-status-codes }

/// note | 注意

如果已经了解 HTTP 状态码，请跳到下一节。

///

在 HTTP 协议中，发送 3 位数的数字状态码是响应的一部分。

这些状态码都具有便于识别的关联名称，但是重要的还是数字。

简言之：

* `100 - 199` 用于返回“信息”。这类状态码很少直接使用。具有这些状态码的响应不能包含响应体
* **`200 - 299`** 用于表示“成功”。这些状态码是最常用的
    * `200` 是默认状态码，表示一切“OK”
    * `201` 表示“已创建”，通常在数据库中创建新记录后使用
    * `204` 是一种特殊的例子，表示“无内容”。该响应在没有为客户端返回内容时使用，因此，该响应不能包含响应体
* **`300 - 399`** 用于“重定向”。具有这些状态码的响应不一定包含响应体，但 `304`“未修改”是个例外，该响应不得包含响应体
* **`400 - 499`** 用于表示“客户端错误”。这些可能是第二常用的类型
    * `404`，用于“未找到”响应
    * 对于来自客户端的一般错误，可以只使用 `400`
* `500 - 599` 用于表示服务器端错误。几乎永远不会直接使用这些状态码。应用代码或服务器出现问题时，会自动返回这些状态码

/// tip | 提示

想了解每个状态码的更多信息以及适用场景，请参阅 [<abbr title="Mozilla Developer Network - Mozilla 开发者网络">MDN</abbr> 的 HTTP 状态码文档](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)。

///

## 状态码名称快捷方式 { #shortcut-to-remember-the-names }

再看下之前的例子：

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` 表示“已创建”的状态码。

但我们没有必要记住所有代码的含义。

可以使用 `fastapi.status` 中的快捷变量。

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

这只是一种快捷方式，具有相同的数字代码，但它可以使用编辑器的自动补全功能：

<img src="/img/tutorial/response-status-code/image02.png">

/// note | 技术细节

也可以使用 `from starlette import status`。

为了让开发者更方便，**FastAPI** 提供了与 `starlette.status` 完全相同的 `fastapi.status`。但它直接来自于 Starlette。

///

## 更改默认状态码 { #changing-the-default }

稍后在[高级用户指南](../advanced/response-change-status-code.md)中，你将看到如何返回与此处声明的默认状态码不同的状态码。



---

# Source: docs/tutorial/schema-extra-example.md


# 声明请求示例数据 { #declare-request-example-data }

你可以为你的应用将接收的数据声明示例。

这里有几种实现方式。

## Pydantic 模型中的额外 JSON Schema 数据 { #extra-json-schema-data-in-pydantic-models }

你可以为一个 Pydantic 模型声明 `examples`，它们会被添加到生成的 JSON Schema 中。

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

这些额外信息会原样添加到该模型输出的 **JSON Schema** 中，并会在 API 文档中使用。

你可以使用属性 `model_config`，它接收一个 `dict`，详见 [Pydantic 文档：配置](https://docs.pydantic.dev/latest/api/config/)。

你可以设置 `"json_schema_extra"`，其值为一个 `dict`，包含你希望出现在生成 JSON Schema 中的任意附加数据，包括 `examples`。

/// tip | 提示

你也可以用同样的技巧扩展 JSON Schema，添加你自己的自定义额外信息。

例如，你可以用它为前端用户界面添加元数据等。

///

/// note | 注意

OpenAPI 3.1.0（自 FastAPI 0.99.0 起使用）增加了对 `examples` 的支持，它是 **JSON Schema** 标准的一部分。

在此之前，只支持使用单个示例的关键字 `example`。OpenAPI 3.1.0 仍然支持它，但它已被弃用，并不属于 JSON Schema 标准。因此，建议你把 `example` 迁移到 `examples`。🤓

你可以在本页末尾阅读更多内容。

///

## `Field` 的附加参数 { #field-additional-arguments }

在 Pydantic 模型中使用 `Field()` 时，你也可以声明额外的 `examples`：

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## JSON Schema 中的 `examples` - OpenAPI { #examples-in-json-schema-openapi }

在以下任意场景中使用：

- `Path()`
- `Query()`
- `Header()`
- `Cookie()`
- `Body()`
- `Form()`
- `File()`

你也可以声明一组 `examples`，这些带有附加信息的示例将被添加到它们在 **OpenAPI** 中的 **JSON Schema** 里。

### 带有 `examples` 的 `Body` { #body-with-examples }

这里我们向 `Body()` 传入 `examples`，其中包含一个期望的数据示例：

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### 文档 UI 中的示例 { #example-in-the-docs-ui }

使用上述任一方法，在 `/docs` 中看起来会是这样：

<img src="/img/tutorial/body-fields/image01.png">

### 带有多个 `examples` 的 `Body` { #body-with-multiple-examples }

当然，你也可以传入多个 `examples`：

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

这样做时，这些示例会成为该请求体数据内部 **JSON Schema** 的一部分。

不过，在<dfn title="2023-08-26">撰写本文时</dfn>，用于展示文档 UI 的 Swagger UI 并不支持显示 **JSON Schema** 中数据的多个示例。但请继续阅读，下面有一种变通方法。

### OpenAPI 特定的 `examples` { #openapi-specific-examples }

在 **JSON Schema** 支持 `examples` 之前，OpenAPI 就已支持一个同名但不同的字段 `examples`。

这个 **OpenAPI 特定的** `examples` 位于 OpenAPI 规范的另一处。它放在**每个*路径操作*的详细信息**中，而不是每个 JSON Schema 里。

而 Swagger UI 早就支持这个特定的 `examples` 字段。因此，你可以用它在文档 UI 中**展示**不同的**示例**。

这个 OpenAPI 特定字段 `examples` 的结构是一个包含**多个示例**的 `dict`（而不是一个 `list`），每个示例都包含会被添加到 **OpenAPI** 的额外信息。

这不放在 OpenAPI 内部包含的各个 JSON Schema 里，而是直接放在*路径操作*上。

### 使用 `openapi_examples` 参数 { #using-the-openapi-examples-parameter }

你可以在 FastAPI 中通过参数 `openapi_examples` 来声明这个 OpenAPI 特定的 `examples`，适用于：

- `Path()`
- `Query()`
- `Header()`
- `Cookie()`
- `Body()`
- `Form()`
- `File()`

这个 `dict` 的键用于标识每个示例，每个值是另一个 `dict`。

`examples` 中每个具体示例的 `dict` 可以包含：

- `summary`：该示例的简短描述。
- `description`：较长描述，可以包含 Markdown 文本。
- `value`：实际展示的示例，例如一个 `dict`。
- `externalValue`：`value` 的替代项，指向该示例的 URL。不过它的工具支持度可能不如 `value`。

你可以这样使用：

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### 文档 UI 中的 OpenAPI 示例 { #openapi-examples-in-the-docs-ui }

当把 `openapi_examples` 添加到 `Body()` 后，`/docs` 会如下所示：

<img src="/img/tutorial/body-fields/image02.png">

## 技术细节 { #technical-details }

/// tip | 提示

如果你已经在使用 **FastAPI** 版本 **0.99.0 或更高版本**，你大概率可以**跳过**这些细节。

它们对更早版本（OpenAPI 3.1.0 尚不可用之前）更相关。

你可以把这当作一堂简短的 OpenAPI 和 JSON Schema **历史课**。🤓

///

/// warning | 警告

以下是关于 **JSON Schema** 和 **OpenAPI** 标准的非常技术性的细节。

如果上面的思路对你已经足够可用，你可能不需要这些细节，可以直接跳过。

///

在 OpenAPI 3.1.0 之前，OpenAPI 使用的是一个更旧且经过修改的 **JSON Schema** 版本。

当时 JSON Schema 没有 `examples`，所以 OpenAPI 在它修改过的版本中添加了自己的 `example` 字段。

OpenAPI 还在规范的其他部分添加了 `example` 和 `examples` 字段：

- [`Parameter Object`（规范中）](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object)，被 FastAPI 的以下内容使用：
    - `Path()`
    - `Query()`
    - `Header()`
    - `Cookie()`
- [`Request Body Object` 中的 `content` 字段里的 `Media Type Object`（规范中）](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object)，被 FastAPI 的以下内容使用：
    - `Body()`
    - `File()`
    - `Form()`

/// note | 注意

这个旧的、OpenAPI 特定的 `examples` 参数，自 FastAPI `0.103.0` 起改名为 `openapi_examples`。

///

### JSON Schema 的 `examples` 字段 { #json-schemas-examples-field }

后来，JSON Schema 在新版本的规范中添加了 [`examples`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5) 字段。

随后新的 OpenAPI 3.1.0 基于最新版本（JSON Schema 2020-12），其中包含了这个新的 `examples` 字段。

现在，这个新的 `examples` 字段优先于旧的单个（且自定义的）`example` 字段，后者已被弃用。

在 JSON Schema 中，这个新的 `examples` 字段**只是一个由示例组成的 `list`**，而不是像上面提到的 OpenAPI 其他位置那样带有额外元数据的 `dict`。

/// note | 注意

即使在 OpenAPI 3.1.0 发布、并与 JSON Schema 有了这种更简单的集成之后，有一段时间里，提供自动文档的 Swagger UI 并不支持 OpenAPI 3.1.0（它自 5.0.0 版本起已支持 🎉）。

因此，FastAPI 0.99.0 之前的版本仍然使用低于 3.1.0 的 OpenAPI 版本。

///

### Pydantic 与 FastAPI 的 `examples` { #pydantic-and-fastapi-examples }

当你在 Pydantic 模型中添加 `examples`，通过 `schema_extra` 或 `Field(examples=["something"])`，这些示例会被添加到该 Pydantic 模型的 **JSON Schema** 中。

这个 Pydantic 模型的 **JSON Schema** 会被包含到你的 API 的 **OpenAPI** 中，然后在文档 UI 中使用。

在 FastAPI 0.99.0 之前的版本（0.99.0 及以上使用更新的 OpenAPI 3.1.0），当你在其他工具（`Query()`、`Body()` 等）中使用 `example` 或 `examples` 时，这些示例不会被添加到描述该数据的 JSON Schema 中（甚至不会添加到 OpenAPI 自己的 JSON Schema 版本中），而是会直接添加到 OpenAPI 的*路径操作*声明中（在 OpenAPI 使用 JSON Schema 的部分之外）。

但现在 FastAPI 0.99.0 及以上使用 OpenAPI 3.1.0（其使用 JSON Schema 2020-12）以及 Swagger UI 5.0.0 及以上后，一切更加一致，示例会包含在 JSON Schema 中。

### Swagger UI 与 OpenAPI 特定的 `examples` { #swagger-ui-and-openapi-specific-examples }

由于截至 2023-08-26，Swagger UI 不支持多个 JSON Schema 示例，用户无法在文档中展示多个示例。

为了解决这个问题，FastAPI `0.103.0` **增加了支持**，可以通过新参数 `openapi_examples` 声明同样的旧式 **OpenAPI 特定的** `examples` 字段。🤓

### 总结 { #summary }

我曾经说我不太喜欢历史... 结果现在在这儿上“技术史”课。😅

简而言之，**升级到 FastAPI 0.99.0 或更高版本**，一切会更**简单、一致、直观**，你也不必了解这些历史细节。😎



---

# Source: docs/tutorial/security/first-steps.md


# 安全 - 第一步 { #security-first-steps }


假设你的**后端** API 位于某个域名下。

而**前端**在另一个域名，或同一域名的不同路径（或在移动应用中）。

你希望前端能通过**username** 和 **password** 与后端进行身份验证。

我们可以用 **OAuth2** 在 **FastAPI** 中实现它。

但为了节省你的时间，不必为获取少量信息而通读冗长的规范。

我们直接使用 **FastAPI** 提供的安全工具。

## 效果预览 { #how-it-looks }

先直接运行代码看看效果，之后再回过头理解其背后的原理。

## 创建 `main.py` { #create-main-py }

把下面的示例代码复制到 `main.py`：

{* ../../docs_src/security/tutorial001_an_py310.py *}

## 运行 { #run-it }

/// note | 注意

当你使用命令 `pip install "fastapi[standard]"` 安装 **FastAPI** 时，[`python-multipart`](https://github.com/Kludex/python-multipart) 包会自动安装。

但是，如果你使用 `pip install fastapi`，默认不会包含 `python-multipart` 包。

如需手动安装，请先创建[虚拟环境](../../virtual-environments.md)、激活它，然后执行：

```console
$ pip install python-multipart
```

这是因为 **OAuth2** 使用“表单数据”来发送 `username` 和 `password`。

///

用下面的命令运行示例：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 查看 { #check-it }

打开交互式文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到类似这样的界面：

<img src="/img/tutorial/security/image01.png">

/// tip | Authorize 按钮！

页面右上角已经有一个崭新的“Authorize”按钮。

你的*路径操作*右上角还有一个可点击的小锁图标。

///

点击它，会弹出一个授权表单，可输入 `username` 和 `password`（以及其它可选字段）：

<img src="/img/tutorial/security/image02.png">

/// note | 注意

目前无论在表单中输入什么都不会生效，我们稍后就会实现它。

///

这当然不是面向最终用户的前端，但它是一个很棒的自动化工具，可交互式地为整个 API 提供文档。

前端团队（也可能就是你自己）可以使用它。

第三方应用和系统也可以使用它。

你也可以用它来调试、检查和测试同一个应用。

## `password` 流 { #the-password-flow }

现在回过头来理解这些内容。

`password` “流”（flow）是 OAuth2 定义的处理安全与身份验证的一种方式。

OAuth2 的设计目标是让后端或 API 与负责用户认证的服务器解耦。

但在这个例子中，**FastAPI** 应用同时处理 API 和认证。

从这个简化的角度来看看流程：

* 用户在前端输入 `username` 和 `password`，然后按下 `Enter`。
* 前端（运行在用户浏览器中）把 `username` 和 `password` 发送到我们 API 中的特定 URL（使用 `tokenUrl="token"` 声明）。
* API 校验 `username` 和 `password`，并返回一个“令牌”（这些我们尚未实现）。
    * “令牌”只是一个字符串，包含一些内容，之后可用来验证该用户。
    * 通常，令牌会在一段时间后过期。
        * 因此，用户过一段时间需要重新登录。
        * 如果令牌被窃取，风险也更小。它不像一把永久有效的钥匙（在大多数情况下）。
* 前端会把令牌临时存储在某处。
* 用户在前端中点击跳转到前端应用的其他部分。
* 前端需要从 API 获取更多数据。
    * 但该端点需要身份验证。
    * 因此，为了与我们的 API 进行身份验证，它会发送一个 `Authorization` 请求头，值为 `Bearer ` 加上令牌。
    * 如果令牌内容是 `foobar`，`Authorization` 请求头的内容就是：`Bearer foobar`。

## **FastAPI** 的 `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI** 在不同抽象层级提供了多种安全工具。

本示例将使用 **OAuth2** 的 **Password** 流程并配合 **Bearer** 令牌，通过 `OAuth2PasswordBearer` 类来实现。

/// note | 注意

“Bearer” 令牌并非唯一选项。

但它非常适合我们的用例。

对于大多数用例，它也可能是最佳选择，除非你是 OAuth2 专家，并明确知道为何其他方案更适合你的需求。

在那种情况下，**FastAPI** 同样提供了相应的构建工具。

///

创建 `OAuth2PasswordBearer` 类实例时，需要传入 `tokenUrl` 参数。该参数包含客户端（运行在用户浏览器中的前端）用来发送 `username` 和 `password` 以获取令牌的 URL。

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip | 提示

这里的 `tokenUrl="token"` 指向的是尚未创建的相对 URL `token`，等价于 `./token`。

因为使用的是相对 URL，若你的 API 位于 `https://example.com/`，它将指向 `https://example.com/token`；若你的 API 位于 `https://example.com/api/v1/`，它将指向 `https://example.com/api/v1/token`。

使用相对 URL 很重要，这能确保你的应用在诸如[使用代理](../../advanced/behind-a-proxy.md)等高级用例中依然正常工作。

///

这个参数不会创建该端点/*路径操作*，而是声明客户端应使用 `/token` 这个 URL 来获取令牌。这些信息会用于 OpenAPI，进而用于交互式 API 文档系统。

我们很快也会创建对应的实际路径操作。

/// note | 注意

如果你是非常严格的 “Pythonista”，可能不喜欢使用参数名 `tokenUrl` 而不是 `token_url`。

这是因为它使用了与 OpenAPI 规范中相同的名称。这样当你需要深入了解这些安全方案时，可以直接复制粘贴去查找更多信息。

///

`oauth2_scheme` 变量是 `OAuth2PasswordBearer` 的一个实例，同时它也是“可调用”的。

可以像这样调用：

```Python
oauth2_scheme(some, parameters)
```

因此，它可以与 `Depends` 一起使用。

### 使用 { #use-it }

现在你可以通过 `Depends` 将 `oauth2_scheme` 作为依赖传入。

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

该依赖会提供一个 `str`，赋值给*路径操作函数*的参数 `token`。

**FastAPI** 会据此在 OpenAPI 架构（以及自动生成的 API 文档）中定义一个“安全方案”。

/// note | 技术细节

**FastAPI** 之所以知道可以使用（在依赖中声明的）`OAuth2PasswordBearer` 在 OpenAPI 中定义安全方案，是因为它继承自 `fastapi.security.oauth2.OAuth2`，而后者又继承自 `fastapi.security.base.SecurityBase`。

所有与 OpenAPI（以及自动 API 文档）集成的安全工具都继承自 `SecurityBase`，这就是 **FastAPI** 能将它们集成到 OpenAPI 的方式。

///

## 它做了什么 { #what-it-does }

它会在请求中查找 `Authorization` 请求头，检查其值是否为 `Bearer ` 加上一些令牌，并将该令牌作为 `str` 返回。

如果没有 `Authorization` 请求头，或者其值不包含 `Bearer ` 令牌，它会直接返回 401 状态码错误（`UNAUTHORIZED`）。

你甚至无需检查令牌是否存在即可返回错误；只要你的函数被执行，就可以确定会拿到一个 `str` 类型的令牌。

你已经可以在交互式文档中试试了：

<img src="/img/tutorial/security/image03.png">

我们还没有验证令牌是否有效，但这已经是一个良好的开端。

## 小结 { #recap }

只需增加三四行代码，你就已经拥有了一种初步的安全机制。



---

# Source: docs/tutorial/security/get-current-user.md


# 获取当前用户 { #get-current-user }

上一章中，（基于依赖注入系统的）安全系统向*路径操作函数*传递了 `str` 类型的 `token`：

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

但这并不实用。

接下来，我们学习如何返回当前用户。

## 创建用户模型 { #create-a-user-model }

首先，创建 Pydantic 用户模型。

与使用 Pydantic 声明请求体相同，并且可在任何位置使用：

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:16] *}

## 创建 `get_current_user` 依赖项 { #create-a-get-current-user-dependency }

创建 `get_current_user` 依赖项。

还记得依赖项支持子依赖项吗？

`get_current_user` 使用 `oauth2_scheme` 作为依赖项。

与之前直接在路径操作中的做法相同，新的 `get_current_user` 依赖项从子依赖项 `oauth2_scheme` 中接收 `str` 类型的 `token`：

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## 获取用户 { #get-the-user }

`get_current_user` 使用创建的（伪）工具函数，该函数接收 `str` 类型的令牌，并返回 Pydantic 的 `User` 模型：

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## 注入当前用户 { #inject-the-current-user }

在*路径操作* 的 `Depends` 中使用 `get_current_user`：

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

注意，此处把 `current_user` 的类型声明为 Pydantic 的 `User` 模型。

这有助于在函数内部使用代码补全和类型检查。

/// tip | 提示

还记得请求体也是使用 Pydantic 模型声明的吧。

放心，因为使用了 `Depends`，**FastAPI** 不会搞混。

///

/// tip | 提示

依赖系统的这种设计方式可以支持不同的依赖项（不同的“可依赖项”）返回同一个 `User` 模型。

而不是局限于只能有一个返回该类型数据的依赖项。

///

## 其它模型 { #other-models }

接下来，直接在*路径操作函数*中获取当前用户，并用 `Depends` 在**依赖注入**系统中处理安全机制。

开发者可以使用任何模型或数据满足安全需求（本例中是 Pydantic 的 `User` 模型）。

而且，不局限于只能使用特定的数据模型、类或类型。

不想在模型中使用 `username`，而是使用 `id` 和 `email`？当然可以。这些工具也支持。

只想使用字符串？或字典？甚至是数据库类模型的实例？工作方式都一样。

实际上，就算登录应用的不是用户，而是只拥有访问令牌的机器人、程序或其它系统？工作方式也一样。

尽管使用应用所需的任何模型、类、数据库。**FastAPI** 通过依赖注入系统都能帮您搞定。

## 代码大小 { #code-size }

这个示例看起来有些冗长。毕竟这个文件同时包含了安全、数据模型的工具函数，以及路径操作等代码。

但，关键是：

**安全和依赖注入的代码只需要写一次。**

就算写得再复杂，也只是在一个位置写一次就够了。所以，要多复杂就可以写多复杂。

但是，就算有数千个端点（*路径操作*），它们都可以使用同一个安全系统。

而且，所有端点（或它们的任何部件）都可以利用这些依赖项或任何其它依赖项。

所有*路径操作*只需 3 行代码就可以了：

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## 小结 { #recap }

现在，我们可以直接在*路径操作函数*中获取当前用户。

至此，安全的内容已经讲了一半。

只要再为用户或客户端的*路径操作*添加真正发送 `username` 和 `password` 的功能就可以了。

下一章见。



---

# Source: docs/tutorial/security/index.md


# 安全性 { #security }

有许多方法可以处理安全性、身份认证和授权等问题。

而且这通常是一个复杂而「困难」的话题。

在许多框架和系统中，仅处理安全性和身份认证就会花费大量的精力和代码（在许多情况下，可能占编写的所有代码的 50％ 或更多）。

**FastAPI** 提供了多种工具，可帮助你以标准的方式轻松、快速地处理**安全性**，而无需研究和学习所有的安全规范。

但首先，让我们来看一些小的概念。

## 赶时间 { #in-a-hurry }

如果你不关心这些术语，而只需要*立即*通过基于用户名和密码的身份认证来增加安全性，请跳转到接下来的章节。

## OAuth2 { #oauth2 }

OAuth2是一个规范，它定义了几种处理身份认证和授权的方法。

它是一个相当广泛的规范，涵盖了一些复杂的使用场景。

它包括了使用「第三方」进行身份认证的方法。

这就是所有带有「使用 Facebook，Google，X (Twitter)，GitHub 登录」的系统背后所使用的机制。

### OAuth 1 { #oauth-1 }

有一个 OAuth 1，它与 OAuth2 完全不同，并且更为复杂，因为它直接包含了有关如何加密通信的规范。

如今它已经不是很流行，没有被广泛使用了。

OAuth2 没有指定如何加密通信，它期望你为应用程序使用 HTTPS 进行通信。

/// tip | 提示

在有关**部署**的章节中，你将了解如何使用 Traefik 和 Let's Encrypt 免费设置 HTTPS。

///

## OpenID Connect { #openid-connect }

OpenID Connect 是另一个基于 **OAuth2** 的规范。

它只是扩展了 OAuth2，并明确了一些在 OAuth2 中相对模糊的内容，以尝试使其更具互操作性。

例如，Google 登录使用 OpenID Connect（底层使用OAuth2）。

但是 Facebook 登录不支持 OpenID Connect。它具有自己的 OAuth2 风格。

### OpenID（非「OpenID Connect」） { #openid-not-openid-connect }

还有一个「OpenID」规范。它试图解决与 **OpenID Connect** 相同的问题，但它不是基于 OAuth2。

因此，它是一个完整的附加系统。

如今它已经不是很流行，没有被广泛使用了。

## OpenAPI { #openapi }

OpenAPI（以前称为 Swagger）是用于构建 API 的开放规范（现已成为 Linux Foundation 的一部分）。

**FastAPI** 基于 **OpenAPI**。

这就是使多个自动交互式文档界面，代码生成等成为可能的原因。

OpenAPI 有一种定义多个安全「方案」的方法。

通过使用它们，你可以利用所有这些基于标准的工具，包括这些交互式文档系统。

OpenAPI 定义了以下安全方案：

* `apiKey`：一个特定于应用程序的密钥，可以来自：
    * 查询参数。
    * 请求头。
    * cookie。
* `http`：标准的 HTTP 身份认证系统，包括：
    * `bearer`: 一个值为 `Bearer ` 加令牌字符串的 `Authorization` 请求头。这是从 OAuth2 继承的。
    * HTTP Basic 认证方式。
    * HTTP Digest，等等。
* `oauth2`：所有的 OAuth2 处理安全性的方式（称为「流程」）。
    *以下几种流程适合构建 OAuth 2.0 身份认证的提供者（例如 Google，Facebook，X (Twitter)，GitHub 等）：
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * 但是有一个特定的「流程」可以完美地用于直接在同一应用程序中处理身份认证：
        * `password`：接下来的几章将介绍它的示例。
* `openIdConnect`：提供了一种定义如何自动发现 OAuth2 身份认证数据的方法。
    * 此自动发现机制是 OpenID Connect 规范中定义的内容。


/// tip | 提示

集成其他身份认证/授权提供者（例如Google，Facebook，X (Twitter)，GitHub等）也是可能的，而且较为容易。

最复杂的问题是创建一个像这样的身份认证/授权提供程序，但是 **FastAPI** 为你提供了轻松完成任务的工具，同时为你解决了重活。

///

## **FastAPI** 实用工具 { #fastapi-utilities }

FastAPI 在 `fastapi.security` 模块中为每个安全方案提供了几种工具，这些工具简化了这些安全机制的使用方法。

在接下来的章节中，你将看到如何使用 **FastAPI** 所提供的这些工具为你的 API 增加安全性。

而且你还将看到它如何自动地被集成到交互式文档系统中。



---

# Source: docs/tutorial/security/oauth2-jwt.md


# 使用密码（及哈希）的 OAuth2，基于 JWT 的 Bearer 令牌 { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

现在我们已经有了完整的安全流程，接下来用 <abbr title="JSON Web Tokens - JSON Web 令牌">JWT</abbr> 令牌和安全的密码哈希，让应用真正安全起来。

这些代码可以直接用于你的应用，你可以把密码哈希保存到数据库中，等等。

我们将从上一章结束的地方继续，逐步完善。

## 关于 JWT { #about-jwt }

JWT 意为 “JSON Web Tokens”。

它是一种标准，把一个 JSON 对象编码成没有空格、很密集的一长串字符串。看起来像这样：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

它不是加密的，所以任何人都可以从内容中恢复信息。

但它是“签名”的。因此，当你收到一个自己签发的令牌时，你可以验证它确实是你签发的。

这样你就可以创建一个例如有效期为 1 周的令牌。然后当用户第二天带着这个令牌回来时，你能知道该用户仍然处于登录状态。

一周后令牌过期，用户将不再被授权，需要重新登录以获取新令牌。而如果用户（或第三方）尝试修改令牌来更改过期时间，你也能发现，因为签名将不匹配。

如果你想动手体验 JWT 令牌并了解它的工作方式，请访问 [https://jwt.io](https://jwt.io/)。

## 安装 `PyJWT` { #install-pyjwt }

我们需要安装 `PyJWT`，以便在 Python 中生成和校验 JWT 令牌。

请确保创建并激活一个[虚拟环境](../../virtual-environments.md)，然后安装 `pyjwt`：

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// note | 注意

如果你计划使用类似 RSA 或 ECDSA 的数字签名算法，你应该安装加密库依赖项 `pyjwt[crypto]`。

可以在 [PyJWT 安装文档](https://pyjwt.readthedocs.io/en/latest/installation.html)中了解更多。

///

## 密码哈希 { #password-hashing }

“哈希”是指把一些内容（这里是密码）转换成看起来像乱码的一串字节（其实就是字符串）。

当你每次传入完全相同的内容（完全相同的密码）时，都会得到完全相同的“乱码”。

但你无法从这个“乱码”反向还原出密码。

### 为什么使用密码哈希 { #why-use-password-hashing }

如果你的数据库被盗，窃贼拿到的不会是用户的明文密码，而只是哈希值。

因此，窃贼无法把该密码拿去尝试登录另一个系统（很多用户在各处都用相同的密码，这将非常危险）。

## 安装 `pwdlib` { #install-pwdlib }

pwdlib 是一个用于处理密码哈希的优秀 Python 包。

它支持多种安全的哈希算法以及相关工具。

推荐的算法是 “Argon2”。

请确保创建并激活一个[虚拟环境](../../virtual-environments.md)，然后安装带 Argon2 的 pwdlib：

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | 提示

使用 `pwdlib`，你甚至可以把它配置为能够读取由 **Django**、**Flask** 安全插件或其他许多工具创建的密码。

例如，你可以在数据库中让一个 Django 应用和一个 FastAPI 应用共享同一份数据。或者在使用同一个数据库的前提下，逐步迁移一个 Django 应用到 FastAPI。

同时，你的用户既可以从 Django 应用登录，也可以从 **FastAPI** 应用登录。

///

## 哈希并校验密码 { #hash-and-verify-the-passwords }

从 `pwdlib` 导入所需工具。

用推荐设置创建一个 PasswordHash 实例——它将用于哈希与校验密码。

/// tip | 提示

pwdlib 也支持 bcrypt 哈希算法，但不包含遗留算法——如果需要处理过时的哈希，建议使用 passlib 库。

例如，你可以用它读取并校验其他系统（如 Django）生成的密码，但对任何新密码使用不同的算法（如 Argon2 或 Bcrypt）进行哈希。

并且能够同时与它们全部兼容。

///

创建一个工具函数来哈希用户传入的密码。

再创建一个工具函数来校验接收的密码是否匹配已存储的哈希。

再创建一个工具函数来进行身份验证并返回用户。

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

当使用一个在数据库中不存在的用户名调用 `authenticate_user` 时，我们仍然会针对一个虚拟哈希运行 `verify_password`。

这可以确保无论用户名是否有效，端点的响应时间大致相同，从而防止可用于枚举已存在用户名的**时序攻击**。

/// note | 注意

如果你查看新的（伪）数据库 `fake_users_db`，现在你会看到哈希后的密码类似这样：`"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`。

///

## 处理 JWT 令牌 { #handle-jwt-tokens }

导入已安装的模块。

创建一个用于对 JWT 令牌进行签名的随机密钥。

使用下列命令生成一个安全的随机密钥：

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

把输出复制到变量 `SECRET_KEY`（不要使用示例中的那个）。

创建变量 `ALGORITHM`，设置用于签名 JWT 令牌的算法，这里设为 `"HS256"`。

创建一个变量用于设置令牌的过期时间。

定义一个用于令牌端点响应的 Pydantic 模型。

创建一个生成新访问令牌的工具函数。

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## 更新依赖项 { #update-the-dependencies }

更新 `get_current_user` 以接收与之前相同的令牌，但这次使用的是 JWT 令牌。

解码接收到的令牌，进行校验，并返回当前用户。

如果令牌无效，立即返回一个 HTTP 错误。

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## 更新 `/token` *路径操作* { #update-the-token-path-operation }

用令牌的过期时间创建一个 `timedelta`。

创建一个真正的 JWT 访问令牌并返回它。

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### 关于 JWT “主题” `sub` 的技术细节 { #technical-details-about-the-jwt-subject-sub }

JWT 规范中有一个 `sub` 键，表示令牌的“主题”（subject）。

使用它是可选的，但通常会把用户的标识放在这里，所以本例中我们使用它。

JWT 除了用于识别用户并允许其直接在你的 API 上执行操作之外，还可能用于其他场景。

例如，你可以用它来标识一辆“车”或一篇“博客文章”。

然后你可以为该实体添加权限，比如“drive”（用于车）或“edit”（用于博客）。

接着，你可以把这个 JWT 令牌交给一个用户（或机器人），他们就可以在没有账户的前提下，仅凭你的 API 生成的 JWT 令牌来执行这些操作（开车、编辑文章）。

基于这些想法，JWT 可以用于更复杂的场景。

在这些情况下，多个实体可能会有相同的 ID，比如都叫 `foo`（用户 `foo`、车 `foo`、博客文章 `foo`）。

因此，为了避免 ID 冲突，在为用户创建 JWT 令牌时，你可以给 `sub` 键的值加一个前缀，例如 `username:`。所以在这个例子中，`sub` 的值可以是：`username:johndoe`。

需要牢记的一点是，`sub` 键在整个应用中应该是一个唯一标识符，并且它应该是字符串。

## 检查 { #check-it }

运行服务器并打开文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到这样的用户界面：

<img src="/img/tutorial/security/image07.png">

像之前一样进行授权。

使用以下凭证：

用户名: `johndoe`
密码: `secret`

/// tip | 提示

注意，代码中的任何地方都没有明文密码 “`secret`”，我们只有它的哈希版本。

///

<img src="/img/tutorial/security/image08.png">

调用 `/users/me/` 端点，你将得到如下响应：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

如果你打开开发者工具，你会看到发送的数据只包含令牌。密码只会在第一个请求中用于认证用户并获取访问令牌，之后就不会再发送密码了：

<img src="/img/tutorial/security/image10.png">

/// note | 注意

注意 `Authorization` 请求头，其值以 `Bearer ` 开头。

///

## 使用 `scopes` 的高级用法 { #advanced-usage-with-scopes }

OAuth2 支持 “scopes”（作用域）。

你可以用它们为 JWT 令牌添加一组特定的权限。

然后你可以把这个令牌直接交给用户或第三方，在一组限制条件下与 API 交互。

在**高级用户指南**中你将学习如何使用它们，以及它们如何集成进 **FastAPI**。

## 小结 { #recap }

通过目前所学内容，你可以使用 OAuth2 和 JWT 等标准来搭建一个安全的 **FastAPI** 应用。

在几乎任何框架中，处理安全问题都会很快变得相当复杂。

许多把安全流程大幅简化的包，往往要在数据模型、数据库和可用特性上做出大量妥协。而有些过度简化的包实际上在底层存在安全隐患。

---

**FastAPI** 不会在任何数据库、数据模型或工具上做妥协。

它给予你完全的灵活性，选择最适合你项目的方案。

而且你可以直接使用许多维护良好、广泛使用的包，比如 `pwdlib` 和 `PyJWT`，因为 **FastAPI** 不需要复杂机制来集成外部包。

同时它也为你提供尽可能简化流程的工具，而不牺牲灵活性、健壮性或安全性。

你可以以相对简单的方式使用和实现像 OAuth2 这样的安全、标准协议。

在**高级用户指南**中，你可以进一步了解如何使用 OAuth2 的 “scopes”，以遵循相同标准实现更细粒度的权限系统。带作用域的 OAuth2 是许多大型身份认证提供商（如 Facebook、Google、GitHub、Microsoft、X（Twitter）等）用来授权第三方应用代表其用户与其 API 交互的机制。



---

# Source: docs/tutorial/security/simple-oauth2.md


# OAuth2 实现简单的 Password 和 Bearer 验证 { #simple-oauth2-with-password-and-bearer }

本章添加上一章示例中欠缺的部分，实现完整的安全流。

## 获取 `username` 和 `password` { #get-the-username-and-password }

首先，使用 **FastAPI** 安全工具获取 `username` 和 `password`。

OAuth2 规范要求使用“密码流”（也就是我们正在使用的流程）时，客户端或用户必须以表单数据形式发送 `username` 和 `password` 字段。

并且，这两个字段必须命名为 `username` 和 `password`，不能使用 `user-name` 或 `email` 等其它名称。

不过也不用担心，前端仍可以显示终端用户所需的名称。

数据库模型也可以使用所需的名称。

但对于登录*路径操作*，则要使用兼容规范的 `username` 和 `password`，（例如，实现与 API 文档集成）。

该规范要求必须以表单数据形式发送 `username` 和 `password`，因此，不能使用 JSON 对象。

### `scope` { #scope }

OAuth2 还支持客户端发送**`scope`**表单字段。

虽然表单字段的名称是 `scope`（单数），但实际上，它是以空格分隔的，由多个**scope**组成的长字符串。

**作用域**只是不带空格的字符串。

常用于声明指定安全权限，例如：

* 常见用例为，`users:read` 或 `users:write`
* 脸书和 Instagram 使用 `instagram_basic`
* 谷歌使用 `https://www.googleapis.com/auth/drive`

/// note | 注意

OAuth2 中，**作用域**只是声明指定权限的字符串。

是否使用冒号 `:` 等符号，或是不是 URL 并不重要。

这些细节只是特定的实现方式。

对 OAuth2 来说，都只是字符串而已。

///

## 获取 `username` 和 `password` 的代码 { #code-to-get-the-username-and-password }

接下来，使用 **FastAPI** 工具获取用户名与密码。

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

首先，导入 `OAuth2PasswordRequestForm`，然后，在 `/token` *路径操作* 中，用 `Depends` 把该类作为依赖项。

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` 是用以下几项内容声明表单请求体的类依赖项：

* `username`
* `password`
* 可选的 `scope` 字段，由多个空格分隔的字符串组成的长字符串
* 可选的 `grant_type`

/// tip | 提示

实际上，OAuth2 规范*要求* `grant_type` 字段使用固定值 `password`，但 `OAuth2PasswordRequestForm` 没有作强制约束。

如需强制使用固定值 `password`，则不要用 `OAuth2PasswordRequestForm`，而是用 `OAuth2PasswordRequestFormStrict`。

///

* 可选的 `client_id`（本例未使用）
* 可选的 `client_secret`（本例未使用）

/// note | 注意

`OAuth2PasswordRequestForm` 并不像 `OAuth2PasswordBearer` 那样是 **FastAPI** 的特殊类。

**FastAPI** 把 `OAuth2PasswordBearer` 识别为安全方案。因此，可以通过这种方式把它添加至 OpenAPI。

但 `OAuth2PasswordRequestForm` 只是可以自行编写的类依赖项，也可以直接声明 `Form` 参数。

但由于这种用例很常见，**FastAPI** 为了简便，就直接提供了对它的支持。

///

### 使用表单数据 { #use-the-form-data }

/// tip | 提示

`OAuth2PasswordRequestForm` 类依赖项的实例没有以空格分隔的长字符串属性 `scope`，但它支持 `scopes` 属性，由已发送的 scope 字符串列表组成。

本例没有使用 `scopes`，但开发者也可以根据需要使用该属性。

///

现在，即可使用表单字段 `username`，从（伪）数据库中获取用户数据。

如果不存在指定用户，则返回错误消息，提示**用户名或密码错误**。

本例使用 `HTTPException` 异常显示此错误：

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### 校验密码 { #check-the-password }

至此，我们已经从数据库中获取了用户数据，但尚未校验密码。

接下来，首先将数据放入 Pydantic 的 `UserInDB` 模型。

注意：永远不要保存明文密码，本例暂时先使用（伪）哈希密码系统。

如果密码不匹配，则返回与上面相同的错误。

#### 密码哈希 { #password-hashing }

**哈希**是指，将指定内容（本例中为密码）转换为形似乱码的字节序列（其实就是字符串）。

每次传入完全相同的内容（比如，完全相同的密码）时，得到的都是完全相同的乱码。

但这个乱码无法转换回传入的密码。

##### 为什么使用密码哈希 { #why-use-password-hashing }

原因很简单，假如数据库被盗，窃贼无法获取用户的明文密码，得到的只是哈希值。

这样一来，窃贼就无法在其它应用中使用窃取的密码，要知道，很多用户在所有系统中都使用相同的密码，风险超大。

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### 关于 `**user_dict` { #about-user-dict }

`UserInDB(**user_dict)` 是指：

*直接把 `user_dict` 的键与值当作关键字参数传递，等效于：*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// note | 注意

关于 `**user_dict` 的更完整说明，详见[**更多模型**文档](../extra-models.md#about-user-in-model-dump)。

///

## 返回 Token { #return-the-token }

`token` 端点的响应必须是 JSON 对象。

响应返回的内容应该包含 `token_type`。本例中用的是**Bearer**Token，因此， Token 类型应为**`bearer`**。

返回内容还应包含 `access_token` 字段，它是包含权限 Token 的字符串。

本例只是简单的演示，返回的 Token 就是 `username`，但这种方式极不安全。

/// tip | 提示

下一章介绍使用哈希密码和 <abbr title="JSON Web Tokens - JSON Web 令牌">JWT</abbr> Token 的真正安全机制。

但现在，仅关注所需的特定细节。

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | 提示

按规范的要求，应像本示例一样，返回带有 `access_token` 和 `token_type` 的 JSON 对象。

这是开发者必须在代码中自行完成的工作，并且要确保使用这些 JSON 的键。

这几乎是唯一需要开发者牢记在心，并按规范要求正确执行的事。

**FastAPI** 则负责处理其它的工作。

///

## 更新依赖项 { #update-the-dependencies }

接下来，更新依赖项。

使之仅在当前用户为激活状态时，才能获取 `current_user`。

为此，要再创建一个依赖项 `get_current_active_user`，此依赖项以 `get_current_user` 依赖项为基础。

如果用户不存在，或状态为未激活，这两个依赖项都会返回 HTTP 错误。

因此，在端点中，只有当用户存在、通过身份验证、且状态为激活时，才能获得该用户：

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// note | 注意

此处返回值为 `Bearer` 的响应头 `WWW-Authenticate` 也是规范的一部分。

任何 401“UNAUTHORIZED”HTTP（错误）状态码都应返回 `WWW-Authenticate` 响应头。

本例中，因为使用的是 Bearer Token，该响应头的值应为 `Bearer`。

实际上，忽略这个附加响应头，也不会有什么问题。

之所以在此提供这个附加响应头，是为了符合规范的要求。

此外，现在或将来，可能会有工具期望并使用它，而且现在或将来这也可能对你或你的用户有用。

这就是遵循标准的好处...

///

## 实际效果 { #see-it-in-action }

打开交互式文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

### 身份验证 { #authenticate }

点击“Authorize”按钮。

使用以下凭证：

用户名：`johndoe`

密码：`secret`

<img src="/img/tutorial/security/image04.png">

通过身份验证后，显示下图所示的内容：

<img src="/img/tutorial/security/image05.png">

### 获取当前用户数据 { #get-your-own-user-data }

使用 `/users/me` 路径的 `GET` 操作。

可以提取如下当前用户数据：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

点击小锁图标，注销后，再执行同样的操作，则会得到 HTTP 401 错误：

```JSON
{
  "detail": "Not authenticated"
}
```

### 未激活用户 { #inactive-user }

测试未激活用户，输入以下信息，进行身份验证：

用户名：`alice`

密码：`secret2`

然后，执行 `/users/me` 路径的 `GET` 操作。

显示下列**未激活用户**错误信息：

```JSON
{
  "detail": "Inactive user"
}
```

## 小结 { #recap }

使用本章的工具实现基于 `username` 和 `password` 的完整 API 安全系统。

这些工具让安全系统兼容任何数据库、用户及数据模型。

唯一欠缺的是，它仍然不是真的**安全**。

下一章你将看到如何使用安全的密码哈希库和 <abbr title="JSON Web Tokens - JSON Web 令牌">JWT</abbr> 令牌。



---

# Source: docs/tutorial/server-sent-events.md


# 服务器发送事件（SSE） { #server-sent-events-sse }

你可以使用**服务器发送事件**（SSE）向客户端流式发送数据。

这类似于[流式传输 JSON Lines](stream-json-lines.md)，但使用 `text/event-stream` 格式，浏览器原生通过 [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 支持。

/// note | 注意

新增于 FastAPI 0.135.0。

///

## 什么是服务器发送事件？ { #what-are-server-sent-events }

SSE 是一种通过 HTTP 从服务器向客户端流式传输数据的标准。

每个事件是一个带有 `data`、`event`、`id` 和 `retry` 等“字段”的小文本块，以空行分隔。

看起来像这样：

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE 常用于 AI 聊天流式输出、实时通知、日志与可观测性，以及其他服务器向客户端推送更新的场景。

/// tip | 提示

如果你想流式传输二进制数据（例如视频或音频），请查看高级指南：[流式传输数据](../advanced/stream-data.md)。

///

## 使用 FastAPI 流式传输 SSE { #stream-sse-with-fastapi }

要在 FastAPI 中流式传输 SSE，在你的*路径操作函数*中使用 `yield`，并设置 `response_class=EventSourceResponse`。

从 `fastapi.sse` 导入 `EventSourceResponse`：

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

每个被 yield 的项会被编码为 JSON，并放入 SSE 事件的 `data:` 字段发送。

如果你将返回类型声明为 `AsyncIterable[Item]`，FastAPI 将使用它通过 Pydantic对数据进行**校验**、**文档化**和**序列化**。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | 提示

由于 Pydantic 会在**Rust** 端序列化它，相比未声明返回类型，你将获得更高的**性能**。

///

### 非 async 的*路径操作函数* { #non-async-path-operation-functions }

你也可以使用常规的 `def` 函数（没有 `async`），并以同样的方式使用 `yield`。

FastAPI 会确保其正确运行，从而不阻塞事件循环。

由于此时函数不是 async，正确的返回类型应为 `Iterable[Item]`：

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### 无返回类型 { #no-return-type }

你也可以省略返回类型。FastAPI 将使用 [`jsonable_encoder`](./encoder.md) 转换数据并发送。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

如果你需要设置 `event`、`id`、`retry` 或 `comment` 等 SSE 字段，你可以 yield `ServerSentEvent` 对象，而不是直接返回数据。

从 `fastapi.sse` 导入 `ServerSentEvent`：

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` 字段始终会被编码为 JSON。你可以传入任何可被序列化为 JSON 的值，包括 Pydantic 模型。

## 原始数据 { #raw-data }

如果你需要发送**不**进行 JSON 编码的数据，请使用 `raw_data` 而不是 `data`。

这对于发送预格式化文本、日志行或特殊的 <dfn title="用于指示特殊条件或状态的值">"哨兵"</dfn> 值（例如 `[DONE]`）很有用。

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | 注意

`data` 和 `raw_data` 是互斥的。每个 `ServerSentEvent` 上只能设置其中一个。

///

## 使用 `Last-Event-ID` 恢复 { #resuming-with-last-event-id }

当连接中断后浏览器重新连接时，会在 `Last-Event-ID` 头中发送上次收到的 `id`。

你可以将其读取为一个请求头参数，并据此从客户端离开的地方恢复流：

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## 使用 POST 的 SSE { #sse-with-post }

SSE 适用于**任意 HTTP 方法**，不仅仅是 `GET`。

这对像 [MCP](https://modelcontextprotocol.io) 这样通过 `POST` 传输 SSE 的协议很有用：

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## 技术细节 { #technical-details }

FastAPI 开箱即用地实现了一些 SSE 的最佳实践。

- 当 15 秒内没有任何消息时，发送一个**保活 `ping` 注释**，以防某些代理关闭连接，正如 [HTML 规范：Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) 中建议的那样。
- 设置 `Cache-Control: no-cache` 响应头，**防止缓存**流。
- 设置特殊响应头 `X-Accel-Buffering: no`，以**防止**某些代理（如 Nginx）**缓冲**。

你无需做任何事，它开箱即用。🤓



---

# Source: docs/tutorial/sql-databases.md


# SQL（关系型）数据库 { #sql-relational-databases }

**FastAPI** 并不要求你使用 SQL（关系型）数据库。你可以使用你想用的**任何数据库**。

这里，我们来看一个使用 [SQLModel](https://sqlmodel.tiangolo.com/) 的示例。

**SQLModel** 基于 [SQLAlchemy](https://www.sqlalchemy.org/) 和 Pydantic 构建。它由 **FastAPI** 的同一作者制作，旨在完美匹配需要使用**SQL 数据库**的 FastAPI 应用程序。

/// tip | 提示

你可以使用任意其他你想要的 SQL 或 NoSQL 数据库类库（在某些情况下称为 <abbr title="Object Relational Mapper - 对象关系映射器: 一个花哨的术语，指一种库，其中某些类表示 SQL 表，而实例表示这些表中的行">"ORMs"</abbr>），FastAPI 不会强迫你使用任何东西。😎

///

由于 SQLModel 基于 SQLAlchemy，因此你可以轻松使用任何由 SQLAlchemy **支持的数据库**（这也让它们被 SQLModel 支持），例如：

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server 等

在这个示例中，我们将使用 **SQLite**，因为它使用单个文件，并且 Python 对其有集成支持。因此，你可以直接复制这个示例并运行。

之后，对于你的生产应用程序，你可能会想要使用像 **PostgreSQL** 这样的数据库服务器。

/// tip | 提示

有一个使用 **FastAPI** 和 **PostgreSQL** 的官方项目生成器，其中包括了前端和更多工具： [https://github.com/fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

///

这是一个非常简单和简短的教程。如果你想了解一般的数据库、SQL 或更高级的功能，请查看 [SQLModel 文档](https://sqlmodel.tiangolo.com/)。

## 安装 `SQLModel` { #install-sqlmodel }

首先，确保你创建并激活了[虚拟环境](../virtual-environments.md)，然后安装 `sqlmodel`：

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 创建含有单一模型的应用 { #create-the-app-with-a-single-model }

我们先创建应用的最简单的第一个版本，只有一个 **SQLModel** 模型。

稍后我们将通过下面的**多个模型**提高其安全性和多功能性。🤓

### 创建模型 { #create-models }

导入 `SQLModel` 并创建一个数据库模型：

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` 类与 Pydantic 模型非常相似（实际上，从底层来看，它*确实就是一个 Pydantic 模型*）。

有一些区别：

* `table=True` 会告诉 SQLModel 这是一个*表模型*，它应该表示 SQL 数据库中的一个**表**，而不仅仅是一个*数据模型*（就像其他常规的 Pydantic 类一样）。

* `Field(primary_key=True)` 会告诉 SQLModel `id` 是 SQL 数据库中的**主键**（你可以在 SQLModel 文档中了解更多关于 SQL 主键的信息）。

    **注意：** 我们为主键字段使用 `int | None`，这样在 Python 代码中我们可以*在没有 `id` 的情况下创建对象*（`id=None`），并假定数据库会*在保存时生成它*。SQLModel 会理解数据库会提供 `id`，并在数据库模式中*将该列定义为非空的 `INTEGER`*。详见 [SQLModel 关于主键的文档](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id)。

* `Field(index=True)` 会告诉 SQLModel 应该为此列创建一个 **SQL 索引**，这样在读取按此列过滤的数据时，程序能在数据库中进行更快的查找。

    SQLModel 会知道声明为 `str` 的内容将是类型为 `TEXT`（或 `VARCHAR`，具体取决于数据库）的 SQL 列。

### 创建引擎（Engine） { #create-an-engine }

SQLModel 的 `engine`（实际上它是一个 SQLAlchemy 的 `engine`）是用来与数据库**保持连接**的。

你只需构建**一个 `engine` 对象**，让你的所有代码连接到同一个数据库。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

使用 `check_same_thread=False` 可以让 FastAPI 在不同线程中使用同一个 SQLite 数据库。这很有必要，因为**单个请求**可能会使用**多个线程**（例如在依赖项中）。

不用担心，我们会按照代码结构确保**每个请求使用一个单独的 SQLModel 会话（session）**，这实际上就是 `check_same_thread` 想要实现的。

### 创建表 { #create-the-tables }

然后，我们来添加一个函数，使用 `SQLModel.metadata.create_all(engine)` 为所有*表模型***创建表**。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### 创建会话（Session）依赖项 { #create-a-session-dependency }

**`Session`** 会存储**内存中的对象**并跟踪数据中所需更改的内容，然后它**使用 `engine`** 与数据库进行通信。

我们会使用 `yield` 创建一个 FastAPI **依赖项**，为每个请求提供一个新的 `Session`。这确保我们每个请求使用一个单独的会话。🤓

然后我们创建一个 `Annotated` 的依赖项 `SessionDep` 来简化其他也会用到此依赖的代码。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 在启动时创建数据库表 { #create-database-tables-on-startup }

我们会在应用程序启动时创建数据库表。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

此处，在应用程序启动事件中，我们创建了表。

在生产环境中，你可能会使用一个在启动应用程序之前运行的迁移脚本。🤓

/// tip | 提示

SQLModel 将会拥有封装 Alembic 的迁移工具，但目前你可以直接使用 [Alembic](https://alembic.sqlalchemy.org/en/latest/)。

///

### 创建 Hero { #create-a-hero }

因为每个 SQLModel 模型同时也是一个 Pydantic 模型，所以你可以在与 Pydantic 模型相同的**类型注解**中使用它。

例如，如果你声明一个类型为 `Hero` 的参数，它将从 **JSON 主体**中读取数据。

同样，你可以将其声明为函数的**返回类型**，然后数据的结构就会显示在自动生成的 API 文档界面中。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

这里，我们使用 `SessionDep` 依赖项（一个 `Session`）将新的 `Hero` 添加到 `Session` 实例中，提交更改到数据库，刷新 `hero` 中的数据，并返回它。

### 读取 Hero { #read-heroes }

我们可以使用 `select()` 从数据库中**读取** `Hero`，并利用 `limit` 和 `offset` 来对结果进行分页。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 读取单个 Hero { #read-one-hero }

我们可以**读取**单个 `Hero`。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### 删除单个 Hero { #delete-a-hero }

我们也可以**删除**一个 `Hero`。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### 运行应用 { #run-the-app }

你可以运行这个应用：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后在 `/docs` UI 中，你能够看到 **FastAPI** 会用这些**模型**来**记录** API，并且还会用它们来**序列化**和**验证**数据。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 使用多个模型更新应用 { #update-the-app-with-multiple-models }

现在让我们稍微**重构**一下这个应用，以提高**安全性**和**多功能性**。

如果你查看之前的应用程序，你可以在 UI 界面中看到，到目前为止，它允许客户端决定要创建的 `Hero` 的 `id`。😱

我们不应该允许这样做，因为他们可能会覆盖我们在数据库中已经分配的 `id`。决定 `id` 的行为应该由**后端**或**数据库**来完成，**而非客户端**。

此外，我们为 hero 创建了一个 `secret_name`，但到目前为止，我们在各处都返回了它，这就不太**秘密**了……😅

我们将通过添加一些**额外的模型**来解决这些问题，而 SQLModel 将在这里大放异彩。✨

### 创建多个模型 { #create-multiple-models }

在 **SQLModel** 中，任何含有 `table=True` 属性的模型类都是一个**表模型**。

任何不含有 `table=True` 属性的模型类都是**数据模型**，这些实际上只是 Pydantic 模型（附带一些小的额外功能）。🤓

有了 SQLModel，我们就可以利用**继承**来在所有情况下**避免重复**所有字段。

#### `HeroBase` - 基类 { #herobase-the-base-class }

我们从一个 `HeroBase` 模型开始，该模型具有所有模型**共享的字段**：

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *表模型* { #hero-the-table-model }

接下来，我们创建 `Hero`，实际的*表模型*，并添加那些不总是在其他模型中的**额外字段**：

* `id`
* `secret_name`

因为 `Hero` 继承自 `HeroBase`，所以它**也**包含了在 `HeroBase` 中声明过的**字段**。因此 `Hero` 的所有字段为：

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 公共*数据模型* { #heropublic-the-public-data-model }

接下来，我们创建一个 `HeroPublic` 模型，这是将**返回**给 API 客户端的模型。

它包含与 `HeroBase` 相同的字段，因此不会包括 `secret_name`。

终于，我们英雄的身份得到了保护！🥷

它还重新声明了 `id: int`。这样我们便与 API 客户端建立了一种**约定**，使他们始终可以期待 `id` 存在并且是一个整数 `int`（永远不会是 `None`）。

/// tip | 提示

确保返回模型始终提供一个值并且始终是 `int`（而不是 `None`）对 API 客户端非常有用，他们可以在这种确定性下编写更简单的代码。

此外，**自动生成的客户端**将拥有更简洁的接口，这样与你的 API 交互的开发者就能更轻松地使用你的 API。😎

///

`HeroPublic` 中的所有字段都与 `HeroBase` 中的相同，其中 `id` 声明为 `int`（不是 `None`）：

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - 用于创建 hero 的*数据模型* { #herocreate-the-data-model-to-create-a-hero }

现在我们创建一个 `HeroCreate` 模型，这是用于**验证**客户端数据的模型。

它不仅拥有与 `HeroBase` 相同的字段，还有 `secret_name`。

现在，当客户端**创建一个新的 hero** 时，他们会发送 `secret_name`，它会被存储到数据库中，但这些 `secret_name` 不会通过 API 返回给客户端。

/// tip | 提示

这应当是**密码**被处理的方式：接收密码，但不要通过 API 返回它们。

在存储密码之前，你还应该对密码的值进行**哈希**处理，**绝不要以明文形式存储它们**。

///

`HeroCreate` 的字段包括：

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - 用于更新 hero 的*数据模型* { #heroupdate-the-data-model-to-update-a-hero }

在之前的应用程序中，我们没有办法**更新 hero**，但现在有了**多个模型**，我们便能做到这一点了。🎉

`HeroUpdate` *数据模型*有些特殊，它包含创建新 hero 所需的**所有相同字段**，但所有字段都是**可选的**（它们都有默认值）。这样，当你更新一个 hero 时，你可以只发送你想要更新的字段。

因为所有**字段实际上**都发生了**变化**（类型现在包括 `None`，并且它们现在有一个默认值 `None`），我们需要**重新声明**它们。

我们并不真的需要从 `HeroBase` 继承，因为我们会重新声明所有字段。我会让它继承只是为了保持一致，但这并不必要。这更多是个人喜好的问题。🤷

`HeroUpdate` 的字段包括：

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### 使用 `HeroCreate` 创建并返回 `HeroPublic` { #create-with-herocreate-and-return-a-heropublic }

既然我们有了**多个模型**，我们就可以对使用它们的应用程序部分进行更新。

我们在请求中接收到一个 `HeroCreate` *数据模型*，然后从中创建一个 `Hero` *表模型*。

这个新的*表模型* `Hero` 会包含客户端发送的字段，以及一个由数据库生成的 `id`。

然后我们将与函数中相同的*表模型* `Hero` 原样返回。但是由于我们使用 `HeroPublic` *数据模型*声明了 `response_model`，**FastAPI** 会使用 `HeroPublic` 来验证和序列化数据。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 提示

现在我们使用 `response_model=HeroPublic` 来代替**返回类型注解** `-> HeroPublic`，因为我们返回的值实际上*并不是* `HeroPublic`。

如果我们声明了 `-> HeroPublic`，你的编辑器和代码检查工具会（理所应当地）抱怨你返回了一个 `Hero` 而不是一个 `HeroPublic`。

通过 `response_model` 的声明，我们让 **FastAPI** 按照它自己的方式处理，而不会干扰类型注解以及编辑器和其他工具提供的帮助。

///

### 使用 `HeroPublic` 读取 Hero { #read-heroes-with-heropublic }

我们可以像之前一样**读取** `Hero`，同样，使用 `response_model=list[HeroPublic]` 确保正确地验证和序列化数据。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### 使用 `HeroPublic` 读取单个 Hero { #read-one-hero-with-heropublic }

我们可以**读取**单个 hero：

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### 使用 `HeroUpdate` 更新单个 Hero { #update-a-hero-with-heroupdate }

我们可以**更新**单个 hero。为此，我们会使用 HTTP 的 `PATCH` 操作。

在代码中，我们会得到一个 `dict`，其中包含客户端发送的所有数据，**只有客户端发送的数据**，并排除了任何一个仅仅作为默认值存在的值。为此，我们使用 `exclude_unset=True`。这是最主要的技巧。🪄

然后我们会使用 `hero_db.sqlmodel_update(hero_data)`，来利用 `hero_data` 的数据更新 `hero_db`。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### （再次）删除单个 Hero { #delete-a-hero-again }

**删除**一个 hero 基本保持不变。

我们不会满足在这一部分中重构一切的愿望。😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### （再次）运行应用 { #run-the-app-again }

你可以再运行一次应用程序：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果你进入 `/docs` API UI，你会看到它现在已经更新，并且在创建 hero 时，它不会再期望从客户端接收 `id` 数据等。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## 总结 { #recap }

你可以使用 [**SQLModel**](https://sqlmodel.tiangolo.com/) 与 SQL 数据库进行交互，并通过*数据模型*和*表模型*简化代码。

你可以在 **SQLModel** 文档中学习到更多内容，其中有一个更详细的[将 SQLModel 与 **FastAPI** 一起使用的迷你教程](https://sqlmodel.tiangolo.com/tutorial/fastapi/)。🚀



---

# Source: docs/tutorial/static-files.md


# 静态文件 { #static-files }

你可以使用 `StaticFiles` 从目录中自动提供静态文件。

/// tip | 提示

如果你需要托管前端，请改用 `app.frontend()`，可在[前端](frontend.md)中阅读相关内容。

`app.frontend()` 底层使用 `StaticFiles`，并为前端提供了几个额外优势，例如处理客户端路由。

///

## 使用 `StaticFiles` { #use-staticfiles }

* 导入 `StaticFiles`。
* 将一个 `StaticFiles()` 实例“挂载”（Mount）到指定路径。

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | 技术细节

你也可以用 `from starlette.staticfiles import StaticFiles`。

**FastAPI** 提供了和 `starlette.staticfiles` 相同的 `fastapi.staticfiles`，只是为了方便你这个开发者。但它确实直接来自 Starlette。

///

### 什么是“挂载”（Mounting） { #what-is-mounting }

“挂载”表示在特定路径添加一个完全“独立”的应用，然后负责处理所有子路径。

这与使用 `APIRouter` 不同，因为挂载的应用是完全独立的。主应用的 OpenAPI 和文档不会包含已挂载应用的任何内容，等等。

你可以在[高级用户指南](../advanced/index.md)中了解更多。

## 细节 { #details }

第一个 `"/static"` 指的是这个“子应用”将被“挂载”到的子路径。因此，任何以 `"/static"` 开头的路径都会由它处理。

`directory="static"` 指的是包含你的静态文件的目录名称。

`name="static"` 为它提供了一个可被 **FastAPI** 内部使用的名称。

这些参数都可以不是“`static`”，请根据你的应用需求和具体细节进行调整。

## 更多信息 { #more-info }

更多细节和选项请查阅 [Starlette 的静态文件文档](https://www.starlette.dev/staticfiles/)。



---

# Source: docs/tutorial/stream-json-lines.md


# 流式传输 JSON Lines { #stream-json-lines }

当你想以“流”的方式发送一系列数据时，可以使用 JSON Lines。

/// note | 注意

新增于 FastAPI 0.134.0。

///

## 什么是流 { #what-is-a-stream }

“流式传输”数据意味着你的应用会在整段数据全部准备好之前，就开始把每个数据项发送给客户端。

也就是说，它会先发送第一个数据项，客户端会接收并开始处理它，而此时你的应用可能还在生成下一个数据项。

```mermaid
sequenceDiagram
    participant App
    participant Client

    App->>App: Produce Item 1
    App->>Client: Send Item 1
    App->>App: Produce Item 2
    Client->>Client: Process Item 1
    App->>Client: Send Item 2
    App->>App: Produce Item 3
    Client->>Client: Process Item 2
    App->>Client: Send Item 3
    Client->>Client: Process Item 3
    Note over App: Keeps producing...
    Note over Client: Keeps consuming...
```

它甚至可以是一个无限流，你可以一直持续发送数据。

## JSON Lines { #json-lines }

在这些场景中，常见的做法是发送 “JSON Lines”，这是一种每行发送一个 JSON 对象的格式。

响应的内容类型是 `application/jsonl`（而不是 `application/json`），响应体类似这样：

```json
{"name": "Plumbus", "description": "A multi-purpose household device."}
{"name": "Portal Gun", "description": "A portal opening device."}
{"name": "Meeseeks Box", "description": "A box that summons a Meeseeks."}
```

它与 JSON 数组（相当于 Python 的 list）非常相似，但不是用 `[]` 包裹、并在各项之间使用 `,` 分隔，而是每行一个 JSON 对象，彼此以换行符分隔。

/// note | 注意

关键在于你的应用可以逐行生成数据，而客户端在消费前面的行。

///

/// note | 技术细节

由于每个 JSON 对象将以换行分隔，它们的内容中不能包含字面量换行符，但可以包含转义换行符（`\n`），这属于 JSON 标准的一部分。

不过通常你无需操心，这些都会自动完成，继续阅读即可。🤓

///

## 使用场景 { #use-cases }

你可以用它来从 AI LLM 服务、日志或遥测中流式传输数据，或其他可以用 JSON 项目来结构化的数据。

/// tip | 提示

如果你想流式传输二进制数据，例如视频或音频，请查看进阶指南：[流式传输数据](../advanced/stream-data.md)。

///

## 使用 FastAPI 流式传输 JSON Lines { #stream-json-lines-with-fastapi }

要在 FastAPI 中流式传输 JSON Lines，可以在路径操作函数中不用 `return`，而是用 `yield` 逐个产生每个数据项。

{* ../../docs_src/stream_json_lines/tutorial001_py310.py ln[1:24] hl[24] *}

如果你要返回的每个 JSON 项是类型 `Item`（一个 Pydantic 模型），并且这是一个异步函数，你可以将返回类型声明为 `AsyncIterable[Item]`：

{* ../../docs_src/stream_json_lines/tutorial001_py310.py ln[1:24] hl[9:11,22] *}

如果你声明了返回类型，FastAPI 会用它来验证数据、在 OpenAPI 中生成文档、进行过滤，并使用 Pydantic 进行序列化。

/// tip | 提示

由于 Pydantic 会在 Rust 侧进行序列化，如果你声明了返回类型，将获得更高的性能。

///

### 非异步的*路径操作函数* { #non-async-path-operation-functions }

你也可以使用常规的 `def` 函数（不带 `async`），并以同样的方式使用 `yield`。

FastAPI 会确保其正确运行，不会阻塞事件循环。

因为这个函数不是异步的，合适的返回类型是 `Iterable[Item]`：

{* ../../docs_src/stream_json_lines/tutorial001_py310.py ln[27:30] hl[28] *}

### 无返回类型 { #no-return-type }

你也可以省略返回类型。此时 FastAPI 会使用 [`jsonable_encoder`](./encoder.md) 将数据转换为可序列化为 JSON 的形式，然后以 JSON Lines 发送。

{* ../../docs_src/stream_json_lines/tutorial001_py310.py ln[33:36] hl[34] *}

## 服务器发送事件（SSE） { #server-sent-events-sse }

FastAPI 还对 Server-Sent Events（SSE）提供一等支持，它们与此非常相似，但有一些额外细节。你可以在下一章了解更多：[服务器发送事件（SSE）](server-sent-events.md)。🤓



---

# Source: docs/tutorial/testing.md


# 测试 { #testing }

感谢 [Starlette](https://www.starlette.dev/testclient/)，测试**FastAPI** 应用轻松又愉快。

它基于 [HTTPX](https://www.python-httpx.org)，而HTTPX又是基于Requests设计的，所以很相似且易懂。

有了它，你可以直接与**FastAPI**一起使用 [pytest](https://docs.pytest.org/)。

## 使用 `TestClient` { #using-testclient }

/// note | 注意

要使用 `TestClient`，先要安装 [`httpx`](https://www.python-httpx.org)。

确保你创建并激活一个[虚拟环境](../virtual-environments.md)，然后再安装，例如：

```console
$ pip install httpx
```

///

导入 `TestClient`。

通过传入你的**FastAPI**应用创建一个 `TestClient` 。

创建名字以 `test_` 开头的函数（这是标准的 `pytest` 约定）。

像使用 `httpx` 那样使用 `TestClient` 对象。

为你需要检查的地方用标准的Python表达式写个简单的 `assert` 语句（重申，标准的`pytest`）。

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip | 提示

注意测试函数是普通的 `def`，不是 `async def`。

还有client的调用也是普通的调用，不是用 `await`。

这让你可以直接使用 `pytest` 而不会遇到麻烦。

///

/// note | 技术细节

你也可以用 `from starlette.testclient import TestClient`。

**FastAPI** 提供了和 `starlette.testclient` 一样的 `fastapi.testclient`，只是为了方便开发者。但它直接来自Starlette。

///

/// tip | 提示

除了发送请求之外，如果你还想测试时在FastAPI应用中调用 `async` 函数（例如异步数据库函数）， 可以在高级教程中看下[异步测试](../advanced/async-tests.md)。

///

## 分离测试 { #separating-tests }

在实际应用中，你可能会把你的测试放在另一个文件里。

你的**FastAPI**应用程序也可能由一些文件/模块组成等等。

### **FastAPI** app 文件 { #fastapi-app-file }

假设你有一个像[更大的应用](bigger-applications.md)中所描述的文件结构:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

在 `main.py` 文件中你有一个 **FastAPI** app:


{* ../../docs_src/app_testing/app_a_py310/main.py *}

### 测试文件 { #testing-file }

然后你会有一个包含测试的文件 `test_main.py` 。它可以位于同一个 Python 包中（一样是目录，但有个 `__init__.py` 文件）：

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

因为这文件在同一个包中，所以你可以通过相对导入从 `main` 模块（`main.py`）导入`app`对象：

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}


...然后测试代码和之前一样的。

## 测试：扩展示例 { #testing-extended-example }

现在让我们扩展这个例子，并添加更多细节，看下如何测试不同部分。

### 扩展后的 **FastAPI** app 文件 { #extended-fastapi-app-file }

让我们继续之前的文件结构：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

假设现在包含**FastAPI** app的文件 `main.py` 有些其他**路径操作**。

有个 `GET` 操作可能返回一个错误。

有个 `POST` 操作可能返回多个错误。

两个*路径操作* 都需要一个`X-Token` 头。

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### 扩展后的测试文件 { #extended-testing-file }

然后你可以使用扩展后的测试更新`test_main.py`：

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


每当你需要客户端在请求中传递信息，但你不知道如何传递时，你可以通过搜索（谷歌）如何用 `httpx` 做，或者是用 `requests` 做，毕竟HTTPX的设计是基于Requests的设计的。

接着只需在测试中同样操作。

示例：

* 传一个*路径* 或*查询* 参数，添加到URL上。
* 传一个JSON体，传一个Python对象(例如一个`dict`)到参数 `json`。
* 如果你需要发送 *Form Data* 而不是 JSON，使用 `data` 参数。
* 要发送 *headers*，传 `dict` 给 `headers` 参数。
* 对于 *cookies*，传 `dict` 给 `cookies` 参数。

关于如何传数据给后端的更多信息（使用 `httpx` 或 `TestClient`），请查阅 [HTTPX 文档](https://www.python-httpx.org)。

/// note | 注意

注意 `TestClient` 接收可以被转化为JSON的数据，而不是Pydantic模型。

如果你在测试中有一个Pydantic模型，并且你想在测试时发送它的数据给应用，你可以使用在[JSON 兼容编码器](encoder.md)介绍的`jsonable_encoder` 。

///

## 运行起来 { #run-it }

之后，你只需要安装 `pytest`。

确保你创建并激活一个[虚拟环境](../virtual-environments.md)，然后再安装，例如：

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

它会自动检测文件和测试，执行测试，然后向你报告结果。

执行测试：

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>



---

# Source: docs/virtual-environments.md


# 虚拟环境 { #virtual-environments }

当你在 Python 工程中工作时，你可能会有必要用到一个**虚拟环境**（或类似的机制）来隔离你为每个工程安装的包。

/// note | 注意

如果你已经了解虚拟环境，知道如何创建和使用它们，你可以考虑跳过这一部分。🤓

///

/// tip | 提示

**虚拟环境**和**环境变量**是不同的。

**环境变量**是系统中的一个变量，可以被程序使用。

**虚拟环境**是一个包含一些文件的目录。

///

/// note | 注意

这个页面将教你如何使用**虚拟环境**以及了解它们的工作原理。

如果你计划使用一个**可以为你管理一切的工具**（包括安装 Python），试试 [uv](https://github.com/astral-sh/uv)。

///

## 创建一个工程 { #create-a-project }

首先，为你的工程创建一个目录。

我通常会在我的主目录下创建一个名为 `code` 的目录。

在这个目录下，我再为每个工程创建一个目录。

<div class="termy">

```console
// 进入主目录
$ cd
// 创建一个用于存放所有代码工程的目录
$ mkdir code
// 进入 code 目录
$ cd code
// 创建一个用于存放这个工程的目录
$ mkdir awesome-project
// 进入这个工程的目录
$ cd awesome-project
```

</div>

## 创建一个虚拟环境 { #create-a-virtual-environment }

在开始一个 Python 工程的**第一时间**，**<dfn title="还有其他做法，此处仅作一个简单的指南">在你的工程内部</dfn>**创建一个虚拟环境。

/// tip | 提示

你只需要 **在每个工程中操作一次**，而不是每次工作时都操作。

///

//// tab | `venv`

你可以使用 Python 自带的 `venv` 模块来创建一个虚拟环境。

<div class="termy">

```console
$ python -m venv .venv
```

</div>

/// details | 上述命令的含义

* `python`: 使用名为 `python` 的程序
* `-m`: 以脚本的方式调用一个模块，我们将告诉它接下来使用哪个模块
* `venv`: 使用名为 `venv` 的模块，这个模块通常随 Python 一起安装
* `.venv`: 在新目录 `.venv` 中创建虚拟环境

///

////

//// tab | `uv`

如果你安装了 [`uv`](https://github.com/astral-sh/uv)，你也可以使用它来创建一个虚拟环境。

<div class="termy">

```console
$ uv venv
```

</div>

/// tip | 提示

默认情况下，`uv` 会在一个名为 `.venv` 的目录中创建一个虚拟环境。

但你可以通过传递一个额外的参数来自定义它，指定目录的名称。

///

////

这个命令会在一个名为 `.venv` 的目录中创建一个新的虚拟环境。

/// details | `.venv`，或是其他名称

你可以在不同的目录下创建虚拟环境，但通常我们会把它命名为 `.venv`。

///

## 激活虚拟环境 { #activate-the-virtual-environment }

激活新的虚拟环境来确保你运行的任何 Python 命令或安装的包都能使用到它。

/// tip | 提示

**每次**开始一个 **新的终端会话** 来工作在这个工程时，你都需要执行这个操作。

///

//// tab | Linux, macOS

<div class="termy">

```console
$ source .venv/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .venv\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

或者，如果你在 Windows 上使用 Bash（例如 [Git Bash](https://gitforwindows.org/)）：

<div class="termy">

```console
$ source .venv/Scripts/activate
```

</div>

////

/// tip | 提示

每次你在这个环境中安装一个 **新的包** 时，都需要 **重新激活** 这个环境。

这么做确保了当你使用一个由这个包安装的 **终端（<abbr title="command line interface - 命令行界面">CLI</abbr>）程序** 时，你使用的是你的虚拟环境中的程序，而不是全局安装、可能版本不同的程序。

///

## 检查虚拟环境是否激活 { #check-the-virtual-environment-is-active }

检查虚拟环境是否激活 (前面的命令是否生效)。

/// tip | 提示

这是 **可选的**，但这是一个很好的方法，可以 **检查** 一切是否按预期工作，以及你是否使用了你打算使用的虚拟环境。

///

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which python

/home/user/code/awesome-project/.venv/bin/python
```

</div>

如果它显示了在你工程 (在这个例子中是 `awesome-project`) 的 `.venv/bin/python` 中的 `python` 二进制文件，那么它就生效了。🎉

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command python

C:\Users\user\code\awesome-project\.venv\Scripts\python
```

</div>

如果它显示了在你工程 (在这个例子中是 `awesome-project`) 的 `.venv\Scripts\python` 中的 `python` 二进制文件，那么它就生效了。🎉

////

## 升级 `pip` { #upgrade-pip }

/// tip | 提示

如果你使用 [`uv`](https://github.com/astral-sh/uv) 来安装内容，而不是 `pip`，那么你就不需要升级 `pip`。😎

///

如果你使用 `pip` 来安装包（它是 Python 的默认组件），你应该将它 **升级** 到最新版本。

在安装包时出现的许多奇怪的错误都可以通过先升级 `pip` 来解决。

/// tip | 提示

通常你只需要在创建虚拟环境后 **执行一次** 这个操作。

///

确保虚拟环境是激活的 (使用上面的命令)，然后运行：

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

/// tip | 提示

有时在尝试升级 pip 时，你可能会遇到 **`No module named pip`** 错误。

如果发生这种情况，使用下面的命令来安装并升级 pip：

<div class="termy">

```console
$ python -m ensurepip --upgrade

---> 100%
```

</div>

该命令会在尚未安装 pip 时进行安装，并确保安装的 pip 版本不早于 `ensurepip` 提供的版本。

///

## 添加 `.gitignore` { #add-gitignore }

如果你使用 **Git** (这是你应该使用的)，添加一个 `.gitignore` 文件来排除你的 `.venv` 中的所有内容。

/// tip | 提示

如果你使用 [`uv`](https://github.com/astral-sh/uv) 来创建虚拟环境，它会自动为你完成这个操作，你可以跳过这一步。😎

///

/// tip | 提示

通常你只需要在创建虚拟环境后 **执行一次** 这个操作。

///

<div class="termy">

```console
$ echo "*" > .venv/.gitignore
```

</div>

/// details | 上述命令的含义

* `echo "*"`: 将在终端中 "打印" 文本 `*`（接下来的部分会对这个操作进行一些修改）
* `>`: 使左边的命令打印到终端的任何内容实际上都不会被打印，而是会被写入到右边的文件中
* `.gitignore`: 被写入文本的文件的名称

而 `*` 对于 Git 来说意味着 "所有内容"。所以，它会忽略 `.venv` 目录中的所有内容。

该命令会创建一个名为 `.gitignore` 的文件，内容如下：

```gitignore
*
```

///

## 安装软件包 { #install-packages }

在激活虚拟环境后，你可以在其中安装软件包。

/// tip | 提示

当你需要安装或升级软件包时，执行本操作**一次**；

如果你需要再升级版本或添加新软件包，你可以**再次执行此操作**。

///

### 直接安装包 { #install-packages-directly }

如果你急于安装，不想使用文件来声明工程的软件包依赖，你可以直接安装它们。

/// tip | 提示

将程序所需的软件包及其版本放在文件中（例如 `requirements.txt` 或 `pyproject.toml`）是个好（并且非常好）的主意。

///

//// tab | `pip`

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

////

//// tab | `uv`

如果你有 [`uv`](https://github.com/astral-sh/uv):

<div class="termy">

```console
$ uv pip install "fastapi[standard]"
---> 100%
```

</div>

////

### 从 `requirements.txt` 安装 { #install-from-requirements-txt }

如果你有一个 `requirements.txt` 文件，你可以使用它来安装其中的软件包。

//// tab | `pip`

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
```

</div>

////

//// tab | `uv`

如果你有 [`uv`](https://github.com/astral-sh/uv):

<div class="termy">

```console
$ uv pip install -r requirements.txt
---> 100%
```

</div>

////

/// details | 关于 `requirements.txt`

一个包含一些软件包的 `requirements.txt` 文件看起来应该是这样的：

```requirements.txt
fastapi[standard]==0.113.0
pydantic==2.8.0
```

///

## 运行程序 { #run-your-program }

在你激活虚拟环境后，你可以运行你的程序，它将使用虚拟环境中的 Python 和你在其中安装的软件包。

<div class="termy">

```console
$ python main.py

Hello World
```

</div>

## 配置编辑器 { #configure-your-editor }

你可能会用到编辑器，请确保配置它使用与你创建的相同的虚拟环境（它可能会自动检测到），以便你可以获得自动补全和内联错误提示。

例如：

* [VS Code](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment)
* [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

/// tip | 提示

通常你只需要在创建虚拟环境时执行此操作**一次**。

///

## 退出虚拟环境 { #deactivate-the-virtual-environment }

当你完成工作后，你可以**退出**虚拟环境。

<div class="termy">

```console
$ deactivate
```

</div>

这样，当你运行 `python` 时，它不会尝试从那个虚拟环境及其已安装的软件包中运行。

## 开始工作 { #ready-to-work }

现在你已经准备好开始你的工作了。



/// tip | 提示

你想要理解上面的所有内容吗？

继续阅读。👇🤓

///

## 为什么要使用虚拟环境 { #why-virtual-environments }

你需要安装 [Python](https://www.python.org/) 才能使用 FastAPI。

之后，你需要**安装** FastAPI 和你想要使用的任何其他**软件包**。

要安装软件包，你通常会使用随 Python 一起提供的 `pip` 命令（或类似的替代方案）。

然而，如果你直接使用 `pip`，软件包将被安装在你的**全局 Python 环境**中（即 Python 的全局安装）。

### 存在的问题 { #the-problem }

那么，在全局 Python 环境中安装软件包有什么问题呢？

有些时候，你可能会编写许多不同的程序，这些程序依赖于**不同的软件包**；你所做的一些工程也会依赖于**同一软件包的不同版本**。😱

例如，你可能会创建一个名为 `philosophers-stone` 的工程，这个程序依赖于另一个名为 **`harry` 的软件包，使用版本 `1`**。因此，你需要安装 `harry`。

```mermaid
flowchart LR
    stone(philosophers-stone) -->|需要| harry-1[harry v1]
```

然而在此之后，你又创建了另一个名为 `prisoner-of-azkaban` 的工程，这个工程也依赖于 `harry`，但是这个工程需要 **`harry` 版本 `3`**。

```mermaid
flowchart LR
    azkaban(prisoner-of-azkaban) --> |需要| harry-3[harry v3]
```

那么现在的问题是，如果你将软件包安装在全局环境中而不是在本地**虚拟环境**中，你将不得不面临选择安装哪个版本的 `harry` 的问题。

如果你想运行 `philosophers-stone`，你需要首先安装 `harry` 版本 `1`，例如：

<div class="termy">

```console
$ pip install "harry==1"
```

</div>

然后你将在全局 Python 环境中安装 `harry` 版本 `1`。

```mermaid
flowchart LR
    subgraph global[全局环境]
        harry-1[harry v1]
    end
    subgraph stone-project[工程 philosophers-stone]
        stone(philosophers-stone) -->|需要| harry-1
    end
```

但是如果你想运行 `prisoner-of-azkaban`，你需要卸载 `harry` 版本 `1` 并安装 `harry` 版本 `3`（或者说，只要你安装版本 `3` ，版本 `1` 就会自动卸载）。

<div class="termy">

```console
$ pip install "harry==3"
```

</div>

于是，你在你的全局 Python 环境中安装了 `harry` 版本 `3`。

如果你再次尝试运行 `philosophers-stone`，有可能它**无法正常工作**，因为它需要 `harry` 版本 `1`。

```mermaid
flowchart LR
    subgraph global[全局环境]
        harry-1[<strike>harry v1</strike>]
        style harry-1 fill:#ccc,stroke-dasharray: 5 5
        harry-3[harry v3]
    end
    subgraph stone-project[工程 philosophers-stone]
        stone(philosophers-stone) -.-x|⛔️| harry-1
    end
    subgraph azkaban-project[工程 prisoner-of-azkaban]
        azkaban(prisoner-of-azkaban) --> |需要| harry-3
    end
```

/// tip | 提示

Python 包在推出**新版本**时通常会尽量**避免破坏性更改**，但最好还是要小心，要想清楚再安装新版本，而且在运行测试以确保一切能正常工作时再安装。

///

现在，想象一下，如果有**许多**其他**软件包**，它们都是你的**工程所依赖的**。这是非常难以管理的。你可能会发现，有些工程使用了一些**不兼容的软件包版本**，而不知道为什么某些东西无法正常工作。

此外，取决于你的操作系统（例如 Linux、Windows、macOS），它可能已经预先安装了 Python。在这种情况下，它可能已经预先安装了一些软件包，这些软件包的特定版本是**系统所需的**。如果你在全局 Python 环境中安装软件包，你可能会**破坏**一些随操作系统一起安装的程序。

## 软件包安装在哪里 { #where-are-packages-installed }

当你安装 Python 时，它会在你的计算机上创建一些目录，并在这些目录中放一些文件。

其中一些目录负责存放你安装的所有软件包。

当你运行：

<div class="termy">

```console
// 先别去运行这个命令，这只是一个示例 🤓
$ pip install "fastapi[standard]"
---> 100%
```

</div>

这将会从 [PyPI](https://pypi.org/project/fastapi/) 下载一个压缩文件，其中包含 FastAPI 代码。

它还会**下载** FastAPI 依赖的其他软件包的文件。

然后它会**解压**所有这些文件，并将它们放在你的计算机上的一个目录中。

默认情况下，它会将下载并解压的这些文件放在随 Python 安装的目录中，这就是**全局环境**。

## 什么是虚拟环境 { #what-are-virtual-environments }

解决软件包都安装在全局环境中的问题的方法是为你所做的每个工程使用一个**虚拟环境**。

虚拟环境是一个**目录**，与全局环境非常相似，你可以在其中专为某个工程安装软件包。

这样，每个工程都会有自己的虚拟环境（`.venv` 目录），其中包含自己的软件包。

```mermaid
flowchart TB
    subgraph stone-project[工程 philosophers-stone]
        stone(philosophers-stone) --->|需要| harry-1
        subgraph venv1[.venv]
            harry-1[harry v1]
        end
    end
    subgraph azkaban-project[工程 prisoner-of-azkaban]
        azkaban(prisoner-of-azkaban) --->|需要| harry-3
        subgraph venv2[.venv]
            harry-3[harry v3]
        end
    end
    stone-project ~~~ azkaban-project
```

## 激活虚拟环境意味着什么 { #what-does-activating-a-virtual-environment-mean }

当你激活了一个虚拟环境，例如：

//// tab | Linux, macOS

<div class="termy">

```console
$ source .venv/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .venv\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

或者如果你在 Windows 上使用 Bash（例如 [Git Bash](https://gitforwindows.org/)）：

<div class="termy">

```console
$ source .venv/Scripts/activate
```

</div>

////

这个命令会创建或修改一些[环境变量](environment-variables.md)，这些环境变量将在接下来的命令中可用。

其中之一是 `PATH` 变量。

/// tip | 提示

你可以在 [环境变量](environment-variables.md#path-environment-variable) 部分了解更多关于 `PATH` 环境变量的内容。

///

激活虚拟环境会将其路径 `.venv/bin`（在 Linux 和 macOS 上）或 `.venv\Scripts`（在 Windows 上）添加到 `PATH` 环境变量中。

假设在激活环境之前，`PATH` 变量看起来像这样：

//// tab | Linux, macOS

```plaintext
/usr/bin:/bin:/usr/sbin:/sbin
```

这意味着系统会在以下目录中查找程序：

* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Windows\System32
```

这意味着系统会在以下目录中查找程序：

* `C:\Windows\System32`

////

激活虚拟环境后，`PATH` 变量会变成这样：

//// tab | Linux, macOS

```plaintext
/home/user/code/awesome-project/.venv/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

这意味着系统现在会首先在以下目录中查找程序：

```plaintext
/home/user/code/awesome-project/.venv/bin
```

然后再在其他目录中查找。

因此，当你在终端中输入 `python` 时，系统会在以下目录中找到 Python 程序：

```plaintext
/home/user/code/awesome-project/.venv/bin/python
```

并使用这个。

////

//// tab | Windows

```plaintext
C:\Users\user\code\awesome-project\.venv\Scripts;C:\Windows\System32
```

这意味着系统现在会首先在以下目录中查找程序：

```plaintext
C:\Users\user\code\awesome-project\.venv\Scripts
```

然后再在其他目录中查找。

因此，当你在终端中输入 `python` 时，系统会在以下目录中找到 Python 程序：

```plaintext
C:\Users\user\code\awesome-project\.venv\Scripts\python
```

并使用这个。

////

一个重要的细节是，虚拟环境路径会被放在 `PATH` 变量的**开头**。系统会在找到任何其他可用的 Python **之前**找到它。这样，当你运行 `python` 时，它会使用**虚拟环境中**的 Python，而不是任何其他 `python`（例如，全局环境中的 `python`）。

激活虚拟环境还会改变其他一些东西，但这是它所做的最重要的事情之一。

## 检查虚拟环境 { #checking-a-virtual-environment }

当你检查虚拟环境是否激活时，例如：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which python

/home/user/code/awesome-project/.venv/bin/python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command python

C:\Users\user\code\awesome-project\.venv\Scripts\python
```

</div>

////

这意味着将使用的 `python` 程序是**在虚拟环境中**的那个。

在 Linux 和 macOS 中使用 `which`，在 Windows PowerShell 中使用 `Get-Command`。

这个命令的工作方式是，它会在 `PATH` 环境变量中查找，按顺序**逐个路径**查找名为 `python` 的程序。一旦找到，它会**显示该程序的路径**。

最重要的部分是，当你调用 `python` 时，将执行的就是这个确切的 "`python`"。

因此，你可以确认你是否在正确的虚拟环境中。

/// tip | 提示

激活一个虚拟环境，获取一个 Python，然后**转到另一个工程**是一件很容易的事情；

但如果第二个工程**无法工作**，那是因为你使用了来自另一个工程的虚拟环境的、**不正确的 Python**。

因此，会检查正在使用的 `python` 是很有用的。🤓

///

## 为什么要停用虚拟环境 { #why-deactivate-a-virtual-environment }

例如，你可能正在一个工程 `philosophers-stone` 上工作，**激活了该虚拟环境**，安装了包并使用了该环境，

然后你想要在**另一个工程** `prisoner-of-azkaban` 上工作，

你进入那个工程：

<div class="termy">

```console
$ cd ~/code/prisoner-of-azkaban
```

</div>

如果你不去停用 `philosophers-stone` 的虚拟环境，当你在终端中运行 `python` 时，它会尝试使用 `philosophers-stone` 中的 Python。

<div class="termy">

```console
$ cd ~/code/prisoner-of-azkaban

$ python main.py

// 导入 sirius 报错，它没有安装 😱
Traceback (most recent call last):
    File "main.py", line 1, in <module>
        import sirius
```

</div>

但是如果你停用虚拟环境并激活 `prisoner-of-azkaban` 的新虚拟环境，那么当你运行 `python` 时，它会使用 `prisoner-of-azkaban` 中的虚拟环境中的 Python。

<div class="termy">

```console
$ cd ~/code/prisoner-of-azkaban

// 你不需要在旧目录中操作停用，你可以在任何地方操作停用，甚至在转到另一个工程之后 😎
$ deactivate

// 激活 prisoner-of-azkaban/.venv 中的虚拟环境 🚀
$ source .venv/bin/activate

// 现在当你运行 python 时，它会在这个虚拟环境中找到安装的 sirius 包 ✨
$ python main.py

I solemnly swear 🐺
```

</div>

## 替代方案 { #alternatives }

这是一个简单的指南，可以帮助你入门并教会你如何理解一切**底层**的东西。

有许多**替代方案**来管理虚拟环境、包依赖（requirements）、工程。

一旦你准备好并想要使用一个工具来**管理整个工程**、包依赖、虚拟环境等，建议你尝试 [uv](https://github.com/astral-sh/uv)。

`uv` 可以做很多事情，它可以：

* 为你**安装 Python**，包括不同的版本
* 为你的工程管理**虚拟环境**
* 安装**软件包**
* 为你的工程管理软件包的**依赖和版本**
* 确保你有一个**确切**的软件包和版本集合来安装，包括它们的依赖项，这样你就可以确保在生产中运行你的工程与在开发时在你的计算机上运行的工程完全相同，这被称为**锁定**
* 还有很多其他功能

## 结论 { #conclusion }

如果你读过并理解了所有这些，现在**你对虚拟环境的了解比很多开发者都要多**。🤓

在未来当你调试看起来复杂的东西时，了解这些细节很可能会有用，你会知道**它是如何在底层工作的**。😎



---

# Source: llm-prompt.md


### Target language

Translate to Simplified Chinese (简体中文).

Language code: zh.

### Grammar and tone

- Use clear, concise technical Chinese consistent with existing docs.
- Address the reader naturally (commonly using “你/你的”).

### Headings

- Follow existing Simplified Chinese heading style (short and descriptive).
- Do not add trailing punctuation to headings.
- If a heading contains only the name of a FastAPI feature, do not translate it.

### Quotes and punctuation

- Keep punctuation style consistent with existing Simplified Chinese docs (they often mix English terms like “FastAPI” with Chinese text).
- Never change punctuation inside inline code, code blocks, URLs, or file paths.

### Ellipsis

- Keep ellipsis style consistent within each document, prefer `...` over  `……`.
- Never change ellipsis in code, URLs, or CLI examples.

### Preferred translations / glossary

Use the following preferred translations when they apply in documentation prose:

- request (HTTP): 请求
- response (HTTP): 响应
- path operation: 路径操作
- path operation function: 路径操作函数

### `///` admonitions

- Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
- If a title is present, prefer these canonical titles:

- `/// tip | 提示`
- `/// note | 注意`
- `/// warning | 警告`
- `/// info | 信息`
- `/// danger | 危险`

