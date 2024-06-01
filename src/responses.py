# Util functions to deal with LLM responses

def completion_to_dict(chat_completion):
    """
    Extracts relevant fields from a chat completion response from OpenAI and converts to a dict.
    """

    # Extracting fields into a dictionary
    response = {
        'id': chat_completion.id,
        'finish_reason': chat_completion.choices[0].finish_reason, 
        'index': chat_completion.choices[0].index,
        'logprobs': chat_completion.choices[0].logprobs,
        'content': chat_completion.choices[0].message.content,
        'role': chat_completion.choices[0].message.role,
        'function_call': chat_completion.choices[0].message.function_call,
        'tool_calls': chat_completion.choices[0].message.tool_calls,
        'created': chat_completion.created,
        'model': chat_completion.model,
        'object': chat_completion.object,
        'system_fingerprint': chat_completion.system_fingerprint,
        'completion_tokens': chat_completion.usage.completion_tokens,
        'prompt_tokens': chat_completion.usage.prompt_tokens,
        'total_tokens': chat_completion.usage.total_tokens
    }
    return response
