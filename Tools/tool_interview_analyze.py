import copy
from DataModels.DataModels import InterviewAnalyzeRequest, InterviewFullData, AnalyzeInfo
from Prompts.prompts import analyze_interview_system_prompt, analyze_interview_user_prompt
from Utilities.LLMHelper import get_chat_LLM, invoke_query, get_prompt, invoke_query_stub

def analyze_interview(request: InterviewAnalyzeRequest) -> InterviewFullData:
    system_prompt = analyze_interview_system_prompt()
    user_prompt = analyze_interview_user_prompt(request)
    result = invoke_query_stub(query=user_prompt,
        system_prompt=system_prompt, return_type=AnalyzeInfo
        )
    
    interviewFullData = InterviewFullData()
    interviewFullData.interviewAnalyzeRequest = copy.deepcopy(request)
    interviewFullData.analyze = result
    return interviewFullData