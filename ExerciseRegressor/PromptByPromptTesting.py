import sys
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained("ActivityIntensityRegressor")
tokz = AutoTokenizer.from_pretrained("ActivityIntensityRegressor")

def predict(text):
    inputs = tokz(text, return_tensors="pt", padding=True, truncation=True)
    print(inputs)
    with torch.no_grad():
        output = model(**inputs)
        print(output)
        return output.logits.squeeze().item()

while 1 != 0:
    text = input("Prompt: ")
    print(predict(text))
