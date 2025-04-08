from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import vector_retriever

model = OllamaLLM(model="llama3.2")

template = """
    You are an AI model tasked with answering questions based on the provided content.

Here is some relevant content:
{content}

Here is the question to answer:
{question}
    """

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

while True:
    print("\n\n------------------------------------")
    question = input("Ask your question (q to quit):")
    print("\n\n")
    if question == "q":
        break
    
    content = vector_retriever.invoke(question)
    result = chain.invoke({"content":content, "question":question})

    print(result)

