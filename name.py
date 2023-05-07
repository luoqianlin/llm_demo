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
    chat = ChatOpenAI(temperature=0.3)
    messages = [
        SystemMessage(content="你很擅长给人取名字,根据提供的信息，给出10个候选名字，要求名字结合八字，有寓意，出自古诗"),
        HumanMessage(content="小朋友是2023年5月6日14点出生，性别为男，姓罗")
    ]
    print("===msg===")
    result = chat(messages)
    print(result.content)


if __name__ == '__main__':
    print('===')
    main()
