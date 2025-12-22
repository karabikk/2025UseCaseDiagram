import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()
api_key = os.getenv("CHATGPT_API_KEY")
client = OpenAI(api_key = api_key)
df = pd.read_csv("bakery_requirements.csv")
functional_requirements = "\n".join(df["RequirementID"] + ": " + df["Requirement"])
#functional_requirements = "\n".join( df["Requirement"])

response = client.chat.completions.create(
    model = "gpt-5",
    messages = [
        {"role": "user", "content": f"You are a Software System Engineer using the IEEE 29148 SRS standard. Your task is to rewrite software functional requirements into a professional system requirement. {functional_requirements}"}
        ]
)
chain1 = response.choices[0].message.content
print(chain1)
#print(response.model)

response2 = client.chat.completions.create(
    model = "gpt-5",
    messages = [
        {"role": "user", "content":f"You are a Software Systems Engineer who is given the following task: please extract actors from the functional requirements and describe their goals. Then convert their goals into use cases. Output only the use cases.  {chain1}."}
    ]
)
chain2 = response2.choices[0].message.content
print(chain2)

response3 = client.chat.completions.create(
    model = "gpt-5",
    messages = [
        {"role": "user", "content":f"You are a Software Systems Engineer tasked with designing a UML use case diagram; given the following use cases, decide the appropriate relationships between them and then create a use case diagram using PlantUML notation.{chain2}"}
    ]
)
chain3 = response3.choices[0].message.content
print(chain3)

response4 = client.chat.completions.create(
    model = "gpt-5",
    messages=[  
                {"role": "user", "content":f"""You are a Software Systems Engineer who is assigned the following: remove any actor-to-use case associations where the use case is already connected through an <<extend>> or <<include>> relationship.
                  {chain3}. """}
    ]
)
chain4 =response4.choices[0].message.content
print(chain4)

response5 = client.chat.completions.create(
    model = "gpt-5",
    messages=[  
                {"role": "user", "content":f"""You are given three tasks. Your first task is to convert the actor use case association arrows into plain, non-directional lines.   Your second task is to find any <<extend>> relationship and rewrite it using a dotted arrow with UP directional modifier using this format: X .up.> Y : <<extend>>  Your third task is find any <<include>> relationship and rewrite it using a dotted arrow with DOWN directional modifier using this format: X .down.> Y :<<include>>
                  {chain4}. """}
    ]
)
chain5 =response5.choices[0].message.content
print(chain5)