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
    chat = ChatOpenAI(temperature=0.65)
    system_msg_content = '''
名字由"姓"和"名"组成,"姓"在前，"名"在后,"姓"长度为1到2个字，2个字的"姓"为"复姓","名"长度为1到2个字。
你很擅长给人取名字,根据提供的信息，给出10个候选名字，要求名字结合八字，有寓意，出自古诗，若不知性别则分别提供适用男和女的名字各10个'''
    human_msg='''姓"罗"，取三个字的名字，中间字固定为"乾"
    '''
    messages = [
        SystemMessage(content=system_msg_content),
        HumanMessage(content=human_msg)
    ]
    result = chat(messages)
    print(result.content)


if __name__ == '__main__':
    main()
