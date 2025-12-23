import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd



load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# Load dataset of software requirements
df = pd.read_csv("/Users/karishmakarabi/Downloads/ResearchProject/Binary Classification/promise_dataset.csv")
for trial in range(1,6):
    print(f"\n TRIAL {trial}")
    sampled = df.sample(n=50, random_state=None)
    requirements = "\n".join([f"{i+1}. {req}" for i, req in enumerate(sampled["Requirement"].tolist())])
    print(sampled[['Requirement', 'Type']])
    model = genai.GenerativeModel(
        model_name='gemini-2.5-pro',
        generation_config={
       # "temperature": 1.0,
        }
)
    response = model.generate_content(f""" Act as a requirements engineering domain expert and classify the given list of requirements into functional (labelled as F) and non-functional requirements (labelled as NF){requirements}""")
    print(response.text)