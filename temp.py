from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
import requests,openai,os
from dotenv.main import load_dotenv
from langchain_community.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from groq import Groq

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = Groq(
    api_key="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" #os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "How are you?",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)

print("API KEY : ")
print(OPENAI_API_KEY)

llm = OpenAI(
    
)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    print("API KEY : ")
    print(OPENAI_API_KEY)
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    text=data.get('data')
    user_input = text
    print(user_input)
    try:
        print("Function started : ")
        conversation = ConversationChain(llm=llm,memory=memory,verbose=True)
        var1 = conversation.predict(input=user_input)
        memory.save_context({"input": user_input}, {"output": var1})
        return jsonify({"response":True,"message":var1})
    except Exception as e:
        print(e)
        error_message = f'Error: {str(e)}'
        return jsonify({"message":error_message,"response":False})
    
if __name__ == '__main__':
    print(chat_completion.choices[0].message.content)
    app.run()
