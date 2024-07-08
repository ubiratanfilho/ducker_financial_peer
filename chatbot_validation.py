from chatbot_api.chatbot_openai import review_chain

question = """O que é o Bitcoin pizza day?"""
print(review_chain.invoke({'question': question}))