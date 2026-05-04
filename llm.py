from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def get_model():
    print(f"---- Loading Model ----")
    try:
        model = ChatNVIDIA(model="nvidia/nemotron-3-super-120b-a12b")
        print("---- Model Loaded ----")
        return model
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_answer(context, question):
    model = get_model()
    if model == None:
        return "Model not Loaded!!!"
    
    prompt = PromptTemplate(
        template = """Answer the following question in a detailed, informative, and professional way using the provided research paper context. Don't go beyond the information provided in the context.
        
        Context: {context}

        Question: {question}

        Detailed Answer:""",
        input_variables = ["context", "question"]
    )

    parser = StrOutputParser()
    chain = prompt | model | parser
    result = chain.invoke({"context": context, "question": question})
    print(result)
    return result

# generate_answer("LLM stands for Large Language Models", "What is LLM?")
