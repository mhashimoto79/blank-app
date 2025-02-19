from DataModels.DataModels import InterviewAnalyzeRequest, InterviewFullData

def analyze_interview_system_prompt() -> str:
    return f"""
    あなたはテキストデータを解析するエージェントです。
    ユーザの入力したテキストデータに対して、TEA(Trajectory Equifinality Approach)の観点で分析し回答してください。
    分析結果はmarkdown形式で出力してください。

    分析手順
    1.切片化
    インタビュー内容を意味のあるセグメント(切片)に分けます。

    2. 等至点(Equifinality Point: EFP)の特定
    インタビュー対象者が到達した共通の目標や結論を特定します。

    3. 分岐点(Bifurcation Point: BFP)の抽出
    等至点に向かう途中で、選択や行動が分かれる重要なポイントを特定します。

    4.必須通過点(Obligatory Passage Point:OPP)の特定
    ユーザー全員が通過する重要なポイントを特定します。

    5.社会的方向づけ(Social Direction: SD) と助勢(Social Guidance: SG)
    各分岐点や必須通過点に対して、どのような阻害要因(SD)や助けとなる要因(SG)が働いているかを明確にします。

    例
    · 等至点(EFP): Foodableを選択して継続的に利用する。
    · 分岐点(BFP):家電を購入する vs サプスクリプションで借りる。他社製品との比較。
    · 必須通過点(OPP):家電の破損または使用困難な状況。
    · SD(社会的方向づけ):高価格や利用の不便さ。
    · SG(社会的助勢):提供される便利なサービスや製品の特性(例:2合パックの利便性)。
    """

def analyze_interview_user_prompt(request:InterviewAnalyzeRequest) -> str:
    # ファイルを開いて読み込む
    with open(request.interviewTextFilePath, 'r', encoding='utf-8') as f:
        contents = f.read()

    return f"""
    以下のテキストはインタビューの内容を文字起こししたテキストデータです。
    このテキストデータをTEA(Trajectory Equifinality Approach)の観点で分析してください。
    対象言語： {request.language}
    インタビューテーマ： {request.theme}
    インタビュー内容： {contents}
    """

def analyze_interview_user_prompt2(request:InterviewAnalyzeRequest) -> str:
    # ファイルを開いて読み込む
    with open(request.interviewTextFilePath, 'r', encoding='utf-8') as f:
        contents = f.read()

    return f"""
    以下のテキストはインタビューの内容を文字起こししたテキストデータです。
    このテキストデータをTEA(Trajectory Equifinality Approach)の観点で分析してください。
    まずは、インタビューデータから切片化ができるテーマをすべて出力してください。
    対象言語： {request.language}
    インタビューテーマ： {request.theme}
    インタビュー内容： {contents}
    """