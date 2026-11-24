import requests
import json

API_KEY = "在这里输入key" 
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. 建立一个“记忆列表”（Day 3 学的列表），一开始可以放个设定让它扮演角色
messages = [
    {"role": "system", "content": "你是一个专业的AI导师，回答要简洁有力。"}
]

print("=== 智谱AI 聊天机器人已启动（输入 'quit' 退出）===")

# 2. 开启死循环，一直聊天（Day 2 学的 while）
while True:
    # 3. 接收你的输入
    user_input = input("\n你: ")
    
    # 如果输入 quit 就退出循环
    if user_input.lower() == 'quit':
        print("退出聊天。")
        break
    if user_input.strip() =='':
             print("请不要输入空白哦")
             continue
    
    # 4. 把你的话加入记忆列表
    messages.append({"role": "user", "content": user_input})
    
    # 5. 准备数据发货（带上所有的聊天记录！）
    data = {
        "model": "glm-4-flash",
        "messages": messages  # 注意这里，把整个记忆列表发过去
    }
    
    print("AI 正在思考...")
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    try:
        # 正常情况：剥 choices 洋葱
        ai_reply = result['choices'][0]['message']['content']
        print(f"AI: {ai_reply}")
        messages.append({"role": "assistant", "content": ai_reply})
        
    except KeyError:
        # 报错情况：剥 error 洋葱
        try:
            error_message = result['error']['message']
            print(f"出错了！{error_message}")
        except KeyError:
            # 如果连 error 都没有，直接打印原形
            print(f"出错了！服务器返回了未知格式：{result}")