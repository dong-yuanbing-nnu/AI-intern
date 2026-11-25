import os

import requests
import streamlit as st


API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4-flash"
SYSTEM_PROMPT = (
    "你是一位耐心、专业的 AI 导师，说话直接、爱举例子。"
    "你的学生是南京师范大学自动化专业的大三学生，正在从零转向 AI 应用方向。"
)


def get_api_key() -> str:
    """优先读 Streamlit 的 secrets（线上），其次读环境变量（本地）。"""
    try:
        return st.secrets["API_KEY"]
    except Exception:
        return os.getenv("API_KEY", "")


API_KEY = get_api_key()


st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")
st.title("🤖 自动化董元兵的专属 AI 助手")

if not API_KEY:
    st.warning(
        "没读到 API Key。本地运行请在 `.streamlit/secrets.toml` 里写 "
        'API_KEY = "你的key"；线上部署请在 Advanced settings → Secrets 里填。'
    )
    st.stop()

# 网页每次交互都会从头重跑这个脚本，所以对话历史必须存在 session_state 里
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 把历史消息画出来
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("你想问什么？")

if user_input:
    text = user_input.strip()

    # 空输入直接忽略
    if not text:
        st.stop()

    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)

    # 简单的退出指令：本地化处理
    if text.lower() in {"quit", "exit", "q", "退出", "再见"}:
        farewell = "好的，如果你需要帮助，随时回来。再见！"
        st.session_state.messages.append({"role": "assistant", "content": farewell})
        with st.chat_message("assistant"):
            st.markdown(farewell)
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("AI 正在疯狂思考中..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            }
            data = {"model": MODEL, "messages": st.session_state.messages}

            try:
                response = requests.post(API_URL, headers=headers, json=data, timeout=60)
                result = response.json()

                # 正常返回：choices[0].message.content
                if "choices" in result:
                    reply = result["choices"][0]["message"]["content"]
                else:
                    # 出错时智谱会返回 {"error": {"message": "..."}}
                    err = result.get("error", {})
                    reply = "出错了：%s" % err.get("message", result)

                st.markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error(f"请求失败了：{e}")
                with st.expander("想看细节的话，点这里"):
                    st.write(repr(e))