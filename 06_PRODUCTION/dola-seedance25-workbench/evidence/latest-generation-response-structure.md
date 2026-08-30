# 最新 Dola1 生成响应结构（脱敏摘录）

本文件不是原始抓包，只保留事件类型、字段存在性和不含账号/签名的语义摘要。

## `/chat/completion`

```text
HTTP 200
Content-Type: text/event-stream

SSE_ACK
  query_list: present
  conversation_id: present but redacted
  task_id: absent/empty

FULL_MSG_NOTIFY
  user image attachment: present
  attachment progress: 100
  prompt: present

STREAM_CHUNK
  assistant text: present
  chat_ability: video capability present
  ratio: 9:16
  model: seedance_v2.5
  duration: 5
  has_video_gen: 1
  disable_regen: 1

STREAM_CHUNK
  assistant acknowledgement: present
  credit cost message: 2
  displayed remaining daily credits: 2

STREAM_CHUNK
  ai_creation_duration_info: present
  error_code: 0
  task_id: empty string
  creation_full_content: assistant acknowledgement/loading only

SSE_REPLY_END
  assistant reply ended
```

## 后续页面响应

```text
/im/conversation/batch_get       HTTP 200 observed, no media identity
/im/conversation/info             HTTP 200 observed, no media identity
/im/chain/single                  HTTP 200 observed, no media identity
/im/message/mark_conv_read        observed, no media identity
```

## 未观察到的关键字段

```text
vid
node_id
key / media_key
fallback_api
key_seed
video_list
original_media_info
media_info
main_url / download_url
provider task id
```

## 需要外部 AI 验证的推断

当前最值得验证的是：

1. `chat/completion` 的 assistant reply 结束并不代表视频任务结束；
2. 后端可能需要在同一 conversation 上继续轮询或等待另一条 completion/message；
3. `task_id` 为空可能表示 task ID 没有在 agent 层返回，而不是底层任务绝对没有创建；
4. 本地 180 秒 timeout 可能早于 provider 的最终消息，但这需要新一轮受控测试验证。
