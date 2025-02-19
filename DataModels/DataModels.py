import dataclasses
from enum import StrEnum
from pydantic import BaseModel, Field, TypeAdapter
from typing import List, Optional

class Language(StrEnum):
    JAPANESE = 'Japanese'
    
@dataclasses.dataclass
class InterviewAnalyzeRequest:
    interviewTextFilePath: str = None
    language: Language = None
    theme: str = None

@dataclasses.dataclass
class InterviewFullData:
    interviewAnalyzeRequest: InterviewAnalyzeRequest = None
    analyze: str = None

class AnalyzeInfo(BaseModel):
    summary: str = Field(..., description="文章要約。markdown形式で800文字以内で日本語で記述する")
    segments: List[str] = Field(default_factory=list, description="文章の切片")
    efps: List[str] = Field(default_factory=list, description="等至点")
    bfps: List[str] = Field(default_factory=list, description="分岐点")
    opps: List[str] = Field(default_factory=list, description="必須通過点")
    sds: List[str] = Field(default_factory=list, description="社会的方向づけ")
    sgs: List[str] = Field(default_factory=list, description="助勢")