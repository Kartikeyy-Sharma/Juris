import tiktoken


# tokenizer used by OpenAI models
encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    
    # Count number of tokens in text.
    # Used for: adaptive chunking, context control, embedding limits
    

    return len(encoding.encode(text))