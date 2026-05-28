from app.kb.tokenizer import count_tokens


sample_text = """
Agreement in restraint of trade is void.
"""

# count tokens
tokens = count_tokens(sample_text)

# print token count
print("Number of Tokens:", tokens)