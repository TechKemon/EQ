import json 
with open('data/sc_json.json', 'r') as f:
  data = json.load(f)
# print(data)

import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv(dotenv_path="ops/.env")

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# to store the optimised eligibility questions in a dictionary
os = {}

def oq(ques):
  system_message = (
      '''You are given a list of eligibility criteria for a scheme in form of logical statements separated by delimited semicolon ';'. 
      Optimise these questions by combining similar questions and removing redundant ones so that minimum questions need to be asked.
      output your list of optimised questions in form of logical conditions like 'Present Occupational Status = Student or Student and Working'

      EXAMPLE 1:
      given is a list of eligibility questions for scheme 'AICTE PRAGATI Scholarship for Girls (Technical Diploma) (Central)':
      Gender = Female;Family Annual Income <= 800000;Present Occupational Status = Student;Present Occupational Status = Student and Working;Which class/course are you studying at present? = ITI;Which class/course are you studying at present? = Diploma/ITI;Which class/course are you studying at present? = Vocational course;Which year of graduation you are studying in? = First Year;Which year of graduation you are studying in? = Second year

      EXPECTED OUTPUT:
      
      1. `Gender = Female`
      2. `Family Annual Income <= 800000`
      3. `Present Occupational Status = Student or Student and Working`
      4. `Which class/course are you studying at present? = ITI, Diploma/ITI, or Vocational course`
      5. `Which year of graduation you are studying in? = First Year or Second year`
      '''
  )
  
  user_message = "List of eligibility criteria separated by semicolon ';' are " + ques
  
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
      {"role": "system", "content": system_message},
      {"role": "user", "content": user_message},
    ]
  )
  print(response.choices[0].message.content, "/n")
  return response.choices[0].message.content

for k, v in data.items():
  ques = ';'.join(v)
  try:
      os[k] = oq(ques)
  except Exception as e:
      print(f"Error processing {k}: {str(e)}")
      os[k] = ques

# Save the dictionary to a JSON file
with open('optimized_scheme_questions.json', 'w') as json_file:
    json.dump(os, json_file, indent=4)
