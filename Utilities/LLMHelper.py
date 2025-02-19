import os
from typing import Type, Any, Iterator
from operator import itemgetter
from pydantic_core._pydantic_core import ValidationError
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings.embeddings import Embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
# from Utilities.LLMCallbackHandler import get_global_llm_handler
#from Utilities.TracabilityHelper import get_observability_handler, update_llm_observation_name
from Utilities.EnvironmentHelper import EnvironmentKeys, env_setting
#from DataModels.DataModels import QAResponse, TraceType, LlmTaskType

LLM_LONG_CONTEXT_LIMIT = 110000

def get_chat_LLM() -> BaseChatModel:
    model = AzureChatOpenAI(
        azure_endpoint=env_setting(EnvironmentKeys.AZURE_OPENAI_GPT_4O_ENDPOINT),
        api_key=env_setting(EnvironmentKeys.AZURE_OPENAI_GPT_4O_API_KEY),
        openai_api_version=env_setting(EnvironmentKeys.AZURE_OPENAI_GPT_4O_API_VERSION),
        azure_deployment=env_setting(EnvironmentKeys.AZURE_OPENAI_GPT_4O_DEPLOYMENT_NAME),
        model=env_setting(EnvironmentKeys.AZURE_OPENAI_GPT_4O_MODEL_NAME),
        max_tokens=env_setting( EnvironmentKeys.AZURE_OPENAI_GPT_4O_MODEL_OUTPUT_MAX_TOKENS),)
    return model

# def get_long_context_chat_LLM() -> BaseChatModel:
#     model = ChatGoogleGenerativeAI(
#         model=env_setting(EnvironmentKeys.GOOGLE_GENERATIVE_AI_MODEL_NAME),
#         # temperature=0,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#         # other params...
#     )
#     return model

# def select_chat_LLM(query: str, system_prompt: str=None, chat_history: list[BaseMessage]=None
#             ) -> BaseChatModel:
#     temp_llm = get_chat_LLM()
#     userPromptCount = get_tokens_count(query, temp_llm)
#     systemPromptCount = get_tokens_count(system_prompt, temp_llm) if system_prompt is not None else 0
#     print(f"------- Prompts Count: (Total: {userPromptCount + systemPromptCount} => User: {userPromptCount}, System: {systemPromptCount})")
#     if userPromptCount + systemPromptCount > LLM_LONG_CONTEXT_LIMIT:
#         return get_long_context_chat_LLM()
#     else:
#         return temp_llm
    
# def get_embeddings_LLM() -> Embeddings:
#     embeddings = AzureOpenAIEmbeddings(
#         azure_endpoint=env_setting(EnvironmentKeys.AZURE_OPENAI_LARGE_EMBEDDING_ENDPOINT),
#         api_key=env_setting(EnvironmentKeys.AZURE_OPENAI_LARGE_EMBEDDING_API_KEY),
#         openai_api_version=env_setting(EnvironmentKeys.AZURE_OPENAI_LARGE_EMBEDDING_API_VERSION),
#         azure_deployment=env_setting(EnvironmentKeys.AZURE_OPENAI_LARGE_EMBEDDING_DEPLOYMENT_NAME),
#         model=env_setting(EnvironmentKeys.AZURE_OPENAI_LARGE_EMBEDDING_MODEL_NAME)
#         )
#     return embeddings

def get_prompt( prompt_template: str, **kwargs: Any ) -> str:
    prompt_template = PromptTemplate.from_template(prompt_template)
    return prompt_template.format(**kwargs)

def get_tokens_count(prompt: str, llm:BaseChatModel) -> int:
    """Returns the number of tokens in a text string."""
    return llm.get_num_tokens(prompt)

def invoke_query(query: str, return_type: Type=None, system_prompt: str=None,
                model: AzureChatOpenAI=None) -> Any:
    if model is None:
        #model = select_chat_LLM(query, system_prompt, chat_history)
        model = get_chat_LLM()
    output_parser = StrOutputParser()
    if return_type is not None and return_type is not str:
        output_parser = PydanticOutputParser(pydantic_object=return_type)
        query = f"{query}\n\n{output_parser.get_format_instructions()}"
    messages = []
    if system_prompt is not None:
        messages.append(SystemMessage(content=system_prompt))    
    messages.append(HumanMessage(content=query))
    configs = {}
    chain = model | output_parser
    result = chain.with_retry(retry_if_exception_type=(OutputParserException,), stop_after_attempt=5).invoke(
        messages, config=configs)
    return result

def invoke_query_stub(query: str, return_type: Type=None, system_prompt: str=None,
                model: AzureChatOpenAI=None) -> Any:
    print(f"query:{query}")
    print(f"return_type:{return_type}")
    print(f"system_prompt:{system_prompt}")
    print(f"model:{model}")

    result = "hogehoge"
    return result

# def invoke_query2(query: str, return_type: Type=None, system_prompt: str=None,
#                  chat_history: list[BaseMessage]=None, model: BaseChatModel=None,
#                  callback_handlers:list[BaseCallbackHandler]=[get_observability_handler()],
#                  trace_type:TraceType=None) -> Any:
#     if model is None:
#         model = select_chat_LLM(query, system_prompt, chat_history)
#     output_parser = StrOutputParser()
#     if return_type is not None and return_type is not str:
#         output_parser = PydanticOutputParser(pydantic_object=return_type)
#         query = f"{query}\n\n{output_parser.get_format_instructions()}"
#     messages = []
#     if system_prompt is not None:
#         messages.append(SystemMessage(content=system_prompt))
#     if chat_history is not None:
#         messages.extend(chat_history)
#     messages.append(HumanMessage(content=query))
#     configs = {}
#     if callback_handlers is not None:
#         configs["callbacks"] = callback_handlers
#         update_llm_observation_name(callback_handlers, trace_type, LlmTaskType.INVOKE_QUERY)
#     chain = model | output_parser
#     result = chain.with_retry(retry_if_exception_type=(OutputParserException,), stop_after_attempt=5).invoke(
#         messages, config=configs)
#     return result

# def stream_query(query: str, system_prompt: str=None,
#         chat_history: list[BaseMessage]=None, model: BaseChatModel=None,
#         callback_handlers:list[BaseCallbackHandler]=[get_observability_handler()],
#         trace_type:TraceType=None) -> Iterator[str]:
#     if model is None:
#         model = get_chat_LLM()
#     output_parser = StrOutputParser()
#     messages = []
#     if system_prompt is not None:
#         messages.append(SystemMessage(content=system_prompt))
#     if chat_history is not None:
#         messages.extend(chat_history)
#     messages.append(HumanMessage(content=query))
#     configs = {}
#     if callback_handlers is not None:
#         configs["callbacks"] = callback_handlers
#         update_llm_observation_name(callback_handlers, trace_type, LlmTaskType.STREAM_QUERY)
#     chain = model | output_parser
#     result = chain.with_retry(retry_if_exception_type=(OutputParserException,), stop_after_attempt=5).stream(
#         messages, config=configs)
#     return result

# def batch_queries(batch_queries: list[str], return_type: Type=None, system_prompt: str=None,
#         model: BaseChatModel=None, max_concurrency: int=10,
#         callback_handlers:list[BaseCallbackHandler]=[get_observability_handler()],
#         trace_type:TraceType=None)-> list[Any]:
#     if model is None:
#         model = get_chat_LLM()
#     if return_type is not None and return_type is not str:
#         model = model.with_structured_output(return_type)
#         chain = model
#     else:
#         chain = model | StrOutputParser()
#     batch_messages:list[list[BaseMessage]] = []
#     for idx, query in enumerate(batch_queries):
#         task_messages: list[BaseMessage] = []
#         if system_prompt is not None:
#             task_messages.append(SystemMessage(content=system_prompt))
#         task_messages.append(HumanMessage(content=query))
#         batch_messages.append(task_messages)
#     configs:dict[str,Any] = {"max_concurrency": max_concurrency}
#     if callback_handlers is not None:
#         configs["callbacks"] = callback_handlers
#         update_llm_observation_name(callback_handlers, trace_type, LlmTaskType.BATCH_QUERY)
#     results:list = chain.with_retry(retry_if_exception_type=(OutputParserException,ValidationError),
#         stop_after_attempt=5).batch( batch_messages, config=configs)
#     return results

# def invoke_query_retriever(question: str, context_search_prompt:str, retriever:BaseRetriever, return_type: Type=None,
#     system_prompt: str=None, chat_history: list[BaseMessage]=None, model: AzureChatOpenAI=None,
#     callback_handlers:list[BaseCallbackHandler]=[get_observability_handler()],
#     trace_type:TraceType=None) -> QAResponse:
#     print("==== 1. Invoke Query Retriever ====")
#     if model is None:
#         model = get_chat_LLM()
#     print("==== 2. Get Output Parser ====")
#     output_parser = StrOutputParser()
#     print("==== 3. Get Prompt ====")
#     if return_type is not None:
#         output_parser = PydanticOutputParser(pydantic_object=return_type)
#         context_search_prompt = f"{context_search_prompt}\n\n{output_parser.get_format_instructions()}"
#     print("==== 4. Get Messages ====")
#     messages = []
#     if system_prompt is not None:
#             messages.append(SystemMessagePromptTemplate.from_template(system_prompt))
#     print("==== 5. Append Chat History ====")
#     if chat_history is not None:
#         messages.extend(chat_history)
#     print("==== 6. Append Human Message ====")
#     messages.append(HumanMessagePromptTemplate.from_template(context_search_prompt))
#     print("==== 7. Get Chat Prompt ====")
#     prompts = ChatPromptTemplate.from_messages(messages)
#     configs = {}
#     print("==== 8. Update Callback Handlers ====")
#     if callback_handlers is not None:
#         configs["callbacks"] = callback_handlers
#         update_llm_observation_name(callback_handlers, trace_type, LlmTaskType.INVOKE_QUERY_RETRIEVER)
#     print("==== 9. Create Chain ====")
#     retriever_chain = RunnablePassthrough() | {"context": (itemgetter("question") | retriever) , "question": itemgetter("question") }
#     print("==== 10. Invoke Chain ====")
#     print(f"---- Question: {question}")
#     retriever_chain_results = retriever_chain.invoke( {"question":question}, config=configs)
#     print("==== 11. Create LLM Chain ====")
#     llm_chain = (prompts | model | output_parser)
#     llm_chain_results = llm_chain.with_retry(retry_if_exception_type=(OutputParserException,),
#         stop_after_attempt=5).invoke(retriever_chain_results, config=configs)
#     print("==== 12. Create Response ====")
#     response = QAResponse(question=question, sourceDocuments=retriever_chain_results["context"],
#         answer=llm_chain_results)
#     print("==== 13. Return Response ====")
#     return response

