import os
import datetime
from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from langfuse.decorators import observe, langfuse_context
#from DataModels.DataModels import TraceType, LlmTaskType
#from Utilities.UserSessionHelper import get_user_name, get_session_id
from Utilities.EnvironmentHelper import env_setting, EnvironmentKeys

def get_observability_handler():
    langfuse_handler = CallbackHandler(
        public_key=env_setting(EnvironmentKeys.FFS_COPILOT_LANGFUSE_PUBLIC_KEY),
        secret_key=env_setting(EnvironmentKeys.FFS_COPILOT_LANGFUSE_SECRET_KEY),
        host=env_setting(EnvironmentKeys.FFS_COPILOT_LANGFUSE_HOST),
        user_id=get_user_name(),
        session_id=get_session_id()
    )
    return langfuse_handler
def initiate_observability():
    os.environ["LANGFUSE_PUBLIC_KEY"] = env_setting(EnvironmentKeys.FFS_COPILOT_LANGFUSE_PUBLIC_KEY)
    os.environ["LANGFUSE_SECRET_KEY"] = env_setting(EnvironmentKeys.FFS_COPILOT_LANGFUSE_SECRET_KEY)
    os.environ["LANGFUSE_HOST"] = env_setting(EnvironmentKeys.FFS_COPILOT_LANGFUSE_HOST)
initiate_observability()
langfuse = Langfuse()
def get_langfuse():
    global langfuse
    return langfuse
def update_llm_observation_name(callback_handlers:list = None, observation_type:TraceType = None,
        llm_task_type:LlmTaskType = None):
    if observation_type and llm_task_type and callback_handlers:
        for handler in callback_handlers:
            if isinstance(handler, CallbackHandler):
                handler.trace_name = f"{observation_type.value if observation_type else TraceType.UNKNOWN.value} - {llm_task_type.value}"
def observer(name:str=None):
    print("Inside Observe Decorator - Before")
    def inner(func):
        print("Inside Inner Function - Before")
        def wrapper(*args, **kwargs):
            print("Inside wrapper function - Before")
            langfuse_local = get_langfuse()
            trace_name = name if name else func.__name__
            trace = langfuse_local.trace(name=trace_name, user_id=get_user_name(),)
            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            trace.span(name=trace_name, start_time=start_time, end_time=end_time)
            langfuse_local.flush()
            print("Inside wrapper function - After")
            return result
        print("Inside Inner Function - After")
        return wrapper
    print("Inside Observe Decorator - After")
    return inner
def trace(type:TraceType=None, func=None):
    def inner(func):
        observation_name = type.value if type else func.__name__
        @observe(name=observation_name)
        def wrapper(*args, **kwargs):
            langfuse_context.update_current_trace(user_id=get_user_name(), session_id=get_session_id())
            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            langfuse_context.update_current_observation(start_time=start_time, end_time=end_time)
            langfuse_context.flush()
            return result
        return wrapper
    return inner