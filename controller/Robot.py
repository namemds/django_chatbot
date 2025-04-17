import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from utils.MysqlUtil import get_conn
import requests
from django.http import StreamingHttpResponse


def query_ollama_chat(messages):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "deepseek-r1:8b",  # 模型名称
            "messages": messages,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            yield data.get("message", {}).get("content", "")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return JsonResponse({"error": "用户名或密码不能为空"}, status=400)

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            return JsonResponse({"error": "用户名已存在"}, status=409)

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
        conn.commit()
        conn.close()
        return JsonResponse({"message": "注册成功"})
    return JsonResponse({"error": "无效请求"}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        if user:
            return JsonResponse({"message": "登录成功", "user_id": user["id"]})
        else:
            return JsonResponse({"error": "用户名或密码错误"}, status=401)
    return JsonResponse({"error": "无效请求"}, status=405)


def get_conversations(request):
    user_id = request.GET.get('user_id')
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM conversations WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    data = [{"id": row["id"], "username": "user"} for row in cursor.fetchall()]
    conn.close()
    return JsonResponse({"conversations": data})


def get_messages(request):
    conv_id = request.GET.get("conversation_id")
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, text FROM messages WHERE conversation_id = %s ORDER BY created_at ASC", (conv_id,))
    messages = cursor.fetchall()
    conn.close()
    return JsonResponse({"messages": messages})


@csrf_exempt
def send_message(request):
    if request.method == "POST":
        body = json.loads(request.body)
        conversation_id = body["conversation_id"]
        user_text = body["text"]

        conn = get_conn()
        cursor = conn.cursor()

        # 保存用户消息
        cursor.execute(
            "INSERT INTO messages (conversation_id, sender, text) VALUES (%s, %s, %s)",
            (conversation_id, "user", user_text)
        )
        conn.commit()

        # 构建 message list
        cursor.execute(
            "SELECT sender, text FROM messages WHERE conversation_id = %s ORDER BY created_at ASC",
            (conversation_id,)
        )
        raw_msgs = cursor.fetchall()
        conn.close()

        message_list = []
        for m in raw_msgs:
            role = "user" if m["sender"] == "user" else "assistant"
            message_list.append({"role": role, "content": m["text"]})
        # optional: you can prepend system message if needed
        # message_list.insert(0, {"role": "system", "content": "You are a helpful assistant."})

        def stream_response():
            full_reply = ""
            for chunk in query_ollama_chat(message_list):
                full_reply += chunk
                yield chunk

            # 保存 AI 回复
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (conversation_id, sender, text) VALUES (%s, %s, %s)",
                (conversation_id, "bot", full_reply)
            )
            conn.commit()
            conn.close()

        return StreamingHttpResponse(stream_response(), content_type='text/plain')

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def create_conversation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (user_id) VALUES (%s)", (user_id,))
        conv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return JsonResponse({"conversation_id": conv_id})
    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def delete_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")

        conn = get_conn()
        cursor = conn.cursor()

        # 删除消息
        cursor.execute("""
            DELETE FROM messages WHERE conversation_id IN (
                SELECT id FROM conversations WHERE user_id = %s
            )
        """, (user_id,))

        # 删除会话
        cursor.execute("DELETE FROM conversations WHERE user_id = %s", (user_id,))

        # 删除用户
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

        conn.commit()
        conn.close()

        return JsonResponse({"message": "用户已删除"})

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def delete_conversation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        conv_id = data.get("conversation_id")

        if not conv_id:
            return JsonResponse({"error": "缺少 conversation_id"}, status=400)

        conn = get_conn()
        cursor = conn.cursor()

        # 删除该会话的所有消息
        cursor.execute("DELETE FROM messages WHERE conversation_id = %s", (conv_id,))

        # 删除会话本身
        cursor.execute("DELETE FROM conversations WHERE id = %s", (conv_id,))

        conn.commit()
        conn.close()

        return JsonResponse({"message": "会话已删除"})

    return JsonResponse({"error": "Invalid method"}, status=405)
