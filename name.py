import logging
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from name_prompt import PROMPT_CONTENT


class TokenUsageInfo:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0


class NameModel:
    def __init__(self):
        self.token_usage_info = TokenUsageInfo()

    def __call__(self, last_name: str, name_length: int, gender: str = None, date_birth: str = None):
        # return f"last_name:{last_name} name_length:{name_length} gender:{gender} date_birth:{date_birth}"
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.65)
        date_birth_text = f"{date_birth}出生"
        gender_text = f"性别{gender}"
        last_name_text = f"姓\"{last_name}\""
        name_length_text = f"取{name_length}个字的名字"
        text_blocks = []
        if date_birth is not None:
            text_blocks.append(date_birth_text)
        if gender is not None:
            text_blocks.append(gender_text)
        text_blocks.append(last_name_text)
        text_blocks.append(name_length_text)
        human_msg = '，'.join(text_blocks)
        messages = [
            SystemMessage(content=PROMPT_CONTENT),
            HumanMessage(content=human_msg)
        ]
        result = self.chat.generate([messages])
        logging.info(result.llm_output)
        # {'token_usage': {'prompt_tokens': 2157, 'completion_tokens': 732, 'total_tokens': 2889}, 'model_name': 'gpt-3.5-turbo'}
        token_usage = result.llm_output['token_usage']
        self.token_usage_info.total_tokens += token_usage['total_tokens']
        self.token_usage_info.prompt_tokens += token_usage['prompt_tokens']
        self.token_usage_info.completion_tokens += token_usage['completion_tokens']
        return result.generations[0][0].text


name_model = NameModel()


def predict(last_name, name_length, gender=None, date_birth=None) -> str:
    name_length = 2 if name_length.startswith("单字") else 3
    gender = None if gender == '未知' else gender
    return name_model(last_name, name_length, gender, date_birth)


def main():
    logger = logging.getLogger('openai')
    logger.setLevel(logging.DEBUG)

    with gr.Blocks(title="AI取名") as demo:
        last_name_input = gr.Textbox(label="姓氏")
        gender_raido = gr.Radio(["男", "女", "未知"], label="性别")
        name_length_radio = gr.Radio(["单字(如：朱茵)", "双字(如：刘德华)"], label="名字类型")
        submit_button = gr.Button("提交")
        text_area = gr.TextArea()
        submit_button.click(predict, inputs=[last_name_input, name_length_radio, gender_raido],
                            outputs=text_area)
    demo.launch(server_name="0.0.0.0")


if __name__ == '__main__':
    main()
