from chatbot import review_chain

question = """O que é day trading?"""
print(review_chain.invoke({'question': question}))