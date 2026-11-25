import streamlit as st
import requests

st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")
st.title("🤖 董元兵的专属 AI 助手")


API_KEY = "输入你的API" 
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 记忆管理
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "你是一个专业的AI导师。"}]

# 渲染历史记录
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 接收输入
if prompt := st.chat_input("你想问点什么？"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 发送请求
    data = {
        "model": "glm-4-flash",
        "messages": st.session_state.messages
    }
    
    with st.spinner("AI 正在疯狂思考中..."):
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

    try:
        ai_reply = result['choices'][0]['message']['content']
        with st.chat_message("assistant"):
            st.write(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    except KeyError:
        st.error(f"出错了！错误信息：{result}")