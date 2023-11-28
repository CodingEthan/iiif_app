import openai


def completion(prompt):
    # 输入你的 api_key
    chat_gpt_key = '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'
    # 将 Key 进行传入
    openai.api_key = chat_gpt_key
    response = openai.Completion.create(
        # text-davinci-003 是指它的模型
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None
    )
    message = response.choices[0].text
    return message
