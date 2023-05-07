import logging
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


def main():
    logger = logging.getLogger('openai')
    logger.setLevel(logging.DEBUG)
    chat = ChatOpenAI(temperature=0.99)
    messages = [
        SystemMessage(content="你是一位给小孩取名的专家"),
        HumanMessage(content="小朋友是2023年5月6日14点出生，性别为男，请为他取一个名字，要求名字结合八字，有寓意，出自古诗")
    ]
    print("===msg===")
    result = chat(messages)
    print(result)


if __name__ == '__main__':
    print('===')
    main()
