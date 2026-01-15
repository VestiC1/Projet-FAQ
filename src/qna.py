from transformers import pipeline
from config import qna_model_name


class QnAExtractor:
    def __init__(self, model_name: str):

        self.model = pipeline(task="question-answering", model=model_name)


    def reply(self, question, context):

        return self.model(question=question, context=context)
