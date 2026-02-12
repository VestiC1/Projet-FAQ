from transformers import pipeline, QuestionAnsweringPipeline
from config import qna_model_name
from .abstract import Model

class QnAExtractor(Model):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        self.model = pipeline(task="question-answering", model=model_name)


    def predict(self, question, context):

        return self.model(question=question, context=context), context

