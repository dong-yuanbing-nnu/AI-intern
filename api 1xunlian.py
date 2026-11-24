api_response = {
    "status": "success",
    "data": {
        "model": "gpt-4",
        "tokens_used": 150,
        "messages": [
            {"role": "user", "content": "帮我写个排序算法"},
            {"role": "assistant", "content": "好的，以下是 Python 的排序代码..."}
        ]
    }
}
print(f"{api_response['status']}")
print(f"{api_response['data']['model']}")
print(f"{api_response['data']['messages'][0]['content']}")