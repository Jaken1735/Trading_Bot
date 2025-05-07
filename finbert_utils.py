from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')
model.to(device)
labels = ['positive', 'negative', 'neutral']

def calculate_sentiment(news):
    """
    Calculate the sentiment of a text using FinBERT
    """
    if news:
        tokens = tokenizer(news, return_tensors='pt', padding=True).to(device)
        result = model(tokens['input_ids'], attention_mask=tokens['attention_mask'])['logits']
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return sentiment, probability
    else:
        return 0, labels[-1]


if __name__ == '__main__':
    tensor, sentiment = calculate_sentiment(['The stock market is looking bad for the next couple of days', 'The analysts seem really worried about this stock'])
    print(tensor, sentiment)
    print(torch.cuda.is_available())
    


