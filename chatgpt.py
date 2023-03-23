import logging
import sys
from datetime import datetime

import gradio as gr
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

import prompt

tools = [
    Tool(
        name="Clock",
        func=lambda *args: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        description="可以获取当前的年份/日期/时间",
    ),
    Tool(
        name="Dummy",
        func=lambda *args: "",
        description="一个没用的工具",
    ),
]

llm = OpenAI(temperature=0, model_name='text-davinci-003', request_timeout=10)
# from langchain.chat_models import ChatOpenAI
# llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(tools, llm,
                         agent="conversational-react-description",
                         verbose=True,
                         memory=memory,
                         agent_kwargs={'prefix': prompt.PREFIX,
                                       'format_instructions': prompt.FORMAT_INSTRUCTIONS,
                                       'suffix': prompt.SUFFIX,
                                       },
                         )

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG,
    #                     filename='output.log',
    #                     datefmt='%Y/%m/%d %H:%M:%S',
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
    logger = logging.getLogger('openai')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        # Logging to console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter('%(message)s'))


        class NoParsingFilter(logging.Filter):
            def filter(self, record):
                msg = record.getMessage()
                prefix = 'api_version=None data='
                if 'prompt' in msg and msg.startswith(prefix):
                    indx = msg.rindex('}\'')
                    prompt = msg[len(prefix):indx + 2]
                    json_data = eval(eval(prompt))
                    print('prompt=>', json_data['prompt'][0])
                    # print(json.dumps(json_data, indent=3))
                    return False
                return False


        logger.addFilter(NoParsingFilter())
        logger.addHandler(stream_handler)

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(label='ChatGPT')
        # state = gr.State([])
        msg = gr.Textbox()
        clear = gr.Button("Clear")


        def user(user_message, history):
            history = history + [[user_message, None]]
            return "", history


        def bot(history):
            output = agent.run(history[-1][0])
            history[-1][1] = output
            return history


        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
        demo.launch()
