from utils.MysqlUtil import get_conn as gc
import time

conn = gc()
cur = conn.cursor()

# 模拟用户
users = ['admin', 'guest', 'dev']

# 模拟消息内容
user_inputs = [
    '你好，我想了解下AI的基础。',
    '你可以推荐几本书吗？',
    'Python 怎么入门？',
    '谢谢你的建议！'
]
bot_replies = [
    '当然可以，AI 是人工智能的简称，主要分为弱AI和强AI。',
    '推荐：《人工智能：一种现代的方法》，还有《深度学习》。',
    '可以从基础语法开始，建议配合项目实战。',
    '不客气，祝你学习顺利！'
]

# 插入模拟数据
for user in users:
    for _ in range(2):  # 每个用户 2 个对话
        # 插入一条对话
        cur.execute(
            "INSERT INTO history_conversation (username) VALUES (%s)",
            (user,)
        )
        conversation_id = cur.lastrowid

        # 插入消息（4条：2问 + 2答）
        for i in range(8):
            sender = 'user' if i % 2 == 0 else 'bot'
            text = user_inputs[i // 2] if sender == 'user' else bot_replies[i // 2]
            cur.execute(
                "INSERT INTO history_message (conversation_id, sender, text) VALUES (%s, %s, %s)",
                (conversation_id, sender, text)
            )
            time.sleep(0.05)

# 提交并关闭
conn.commit()
cur.close()
conn.close()

print("✅ 模拟聊天记录插入完成！")
