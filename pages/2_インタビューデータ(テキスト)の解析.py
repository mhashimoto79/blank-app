import streamlit as st
from streamlit.components.v1 import html
from tempfile import NamedTemporaryFile
from pathlib import Path
from plantuml import PlantUML
import base64
#import openai
#import mermaid
import graphviz

from DataModels.DataModels import InterviewAnalyzeRequest, InterviewFullData, Language
from Utilities.StreamlitHelper import initialize_page, update_windows_size, get_windows_height
from Utilities.FileFolderHelper import clear_folder
#from Tools.tool_interview_analyze import analyze_interview

SESSION_KEY_INTERVIEW_ANALYZE_REQUEST = "InterviewAnalyzeRequest"
SESSION_KEY_INTERVIEW_FULL_DATA = "InterviewFullData"

@st.dialog("**インタビューデータ選定", width="large")
def show_file_selection(analyze_request: InterviewAnalyzeRequest):
    interview_data = st.file_uploader("インタビューデータを選択してください", type=["txt", "csv"])
    if interview_data is not None and st.button('**選定**', type="primary"):
        with NamedTemporaryFile(delete=False, dir="./tmp", prefix=Path(interview_data.name).name,
            suffix=Path(interview_data.name).suffix ) as tmpfile:
            tmpfile.write(interview_data.read())
            analyze_request.interviewTextFilePath = tmpfile.name
            st.rerun()


def show_analyze_settings():
    interview_full_data: InterviewFullData = st.session_state.get(SESSION_KEY_INTERVIEW_FULL_DATA, None)
    analyze_request: InterviewAnalyzeRequest = st.session_state.get(SESSION_KEY_INTERVIEW_ANALYZE_REQUEST, None)
    container_expanded = interview_full_data is None
    container_title = "🔧**設定**" if container_expanded else f"🔧**設定** ファイル:**{analyze_request.interviewTextFilePath}**、言語：**{analyze_request.language}**"
    with st.expander(container_title, expanded=container_expanded):
        if analyze_request is None:
            analyze_request = InterviewAnalyzeRequest()
            st.session_state[SESSION_KEY_INTERVIEW_ANALYZE_REQUEST] = analyze_request
        c1, c2 = st.columns([1,3])
        with c1:
            analyze_request.language = Language(st.selectbox("**言語：**", [lang.value for lang in Language]))
            analyze_request.theme = st.text_input("**インタビューのテーマ：**", value=analyze_request.theme)
        if c2.button("**インタビューデータUP**", type="primary"):
            show_file_selection(analyze_request)

def show_analyze_button():
    analyze_request: InterviewAnalyzeRequest = st.session_state.get(SESSION_KEY_INTERVIEW_ANALYZE_REQUEST, None)
    if analyze_request is not None and analyze_request.interviewTextFilePath is not None:
        c1, c2 = st.columns([10,1])
        with c1:
            if st.button('**インタビューデータ解析**', type="primary"):
                with st.spinner("解析中..."):
                    #interview_full_data:InterviewFullData = analyze_interview(analyze_request)
                    interview_full_data:InterviewFullData = "test"
                    st.session_state[SESSION_KEY_INTERVIEW_FULL_DATA] = interview_full_data
                    st.write("解析完了")
                    st.rerun()
        with c2:
            update_windows_size()

def create_flowchart1():
    dot = graphviz.Digraph(format="png", graph_attr={"rankdir": "LR"})
    
    # ノードとエッジの追加（図の内容に基づく）
    dot.node("start", "父親が新潟出身で毎年\nおいしい新米を食べていた", shape="circle")
    dot.node("health", "父母のためにも身体に\n良さそうなものを使いたい", shape="circle")
    dot.node("concern", "父母の\n機器の誤操作などの不安", shape="circle")
    
    # 枝分かれ部分
    dot.node("branch1", "炊飯器がほしい", shape="circle")
    dot.node("branch2", "お米が重い\n量が多いと使い切れない", shape="circle")
    
    # 左側のルート
    dot.node("error", "認知症の母が炊飯器を\n誤った使い方で壊してしまう", shape="circle")
    dot.node("pot", "鍋で炊けるけど\n予約できない", shape="circle")
    dot.node("panasonic", "どうせなら\n高性能器が良い", shape="circle")
    dot.node("panasonic_new", "パナソニックの\n新しい試みだな", shape="circle")
    
    # 右側のルート
    dot.node("small_pack", "少量のお米で\n置いておきたい", shape="circle")
    dot.node("foodable", "foodable申込", shape="circle")
    dot.node("pressure", "圧力などで美味しく炊けて\n銘柄炊き分け良さそう", shape="circle")
    
    # 必須通過点・分岐点
    dot.node("decide", "真空パックの少量の\nお米が届くところが決め手に", shape="circle")
    dot.node("delicious", "数ヶ月後、銘柄を\n選択するようになった", shape="circle")
    dot.node("hokkaido", "北海道銘柄が美味しいし\n安心感がある", shape="circle")
    dot.node("purchase", "等至点\n選択したために\nついでに購入", shape="circle")
    dot.node("rakuten", "楽天やスーパーで購入", shape="circle")
    
    # エッジの設定
    dot.edges([
        ("start", "health"),
        ("health", "concern"),
        ("concern", "branch1"),
        ("concern", "branch2"),
        ("branch1", "error"),
        ("branch1", "panasonic"),
        ("error", "pot"),
        ("panasonic", "panasonic_new"),
        ("branch2", "small_pack"),
        ("small_pack", "foodable"),
        ("foodable", "decide"),
        ("decide", "pressure"),
        ("decide", "delicious"),
        ("delicious", "hokkaido"),
        ("delicious", "purchase"),
        ("purchase", "rakuten")
    ])
    
    return dot

def create_flowchart2():
    dot = graphviz.Digraph(format="png", graph_attr={"rankdir": "LR"})
    
    # 切片 (Initial Conditions)
    dot.node("IC1", "炊飯器の故障", shape="box")
    dot.node("IC2", "フーダブルに興味\n(少量米・銘柄炊き分け)", shape="box")
    dot.node("IC3", "他社製品・土鍋炊飯の検討", shape="box")
    dot.node("IC4", "週10回の自炊\n(時短重視・両親の健康配慮)", shape="box")
    dot.node("IC5", "家族の健康配慮と\n食品ロスの回避", shape="box")
    dot.node("IC6", "料理のモチベーション\n(キッチンリフォーム)", shape="box")

    # 等至点 (Equifinality Point: EFP) - double box
    dot.node("EFP", "等至点:\nフーダブルを選択して継続利用", shape="box", style="double")

    # 分岐点 (Bifurcation Point: BFP) - diamond
    dot.node("BFP1", "BFP1:\n購入 vs サブスクリプション", shape="diamond")
    dot.node("BFP2", "BFP2:\n他社製品との比較", shape="diamond")
    dot.node("BFP3", "BFP3:\n自動受け取り vs 銘柄選択", shape="diamond")

    # 必須通過点 (Obligatory Passage Point: OPP) - double box
    dot.node("OPP1", "OPP1:\n炊飯器の故障", shape="box", style="double")
    dot.node("OPP2", "OPP2:\n家族の食生活への配慮", shape="box", style="double")
    dot.node("OPP3", "OPP3:\n情報収集と比較検討", shape="box", style="double")

    # 社会的方向づけ (SD) - 四角 & 目立つ色
    dot.node("SD1", "SD1:\n高価格の抵抗感", shape="box", style="filled", color="#FF9999", fontcolor="white")
    dot.node("SD2", "SD2:\n高齢の両親の操作不安", shape="box", style="filled", color="#FF9999", fontcolor="white")
    dot.node("SD3", "SD3:\n食生活の制約", shape="box", style="filled", color="#FF9999", fontcolor="white")

    # 助勢 (SG) - 四角 & 目立つ色
    dot.node("SG1", "SG1:\n少量米の便利さ\n食品ロス削減", shape="box", style="filled", color="#90EE90", fontcolor="white")
    dot.node("SG2", "SG2:\n銘柄炊き分けの楽しさ", shape="box", style="filled", color="#90EE90", fontcolor="white")
    dot.node("SG3", "SG3:\nブランドの信頼感", shape="box", style="filled", color="#90EE90", fontcolor="white")
    dot.node("SG4", "SG4:\nリフォームによる\nモチベーションアップ", shape="box", style="filled", color="#90EE90", fontcolor="white")

    # エッジの設定 (因果関係、時系列)
    dot.edges([
        ("IC1", "OPP1"),
        ("IC2", "BFP2"),
        ("IC2", "SG1"),
        ("IC2", "SG2"),
        ("IC3", "BFP2"),
        ("IC4", "OPP2"),
        ("IC5", "SG1"),
        ("IC6", "SG4"),
        ("OPP1", "BFP1"),
        ("OPP2", "BFP2"),
        ("OPP3", "BFP3"),
        ("BFP1", "EFP"),
        ("BFP2", "EFP"),
        ("BFP3", "EFP"),
        ("SD1", "BFP2"),
        ("SD2", "BFP1"),
        ("SD3", "OPP2"),
        ("SG1", "EFP"),
        ("SG2", "EFP"),
        ("SG3", "BFP2"),
        ("SG4", "EFP")
    ])


    return dot

def show_analyze_results(): 
    interview_full_data: InterviewFullData = st.session_state.get(SESSION_KEY_INTERVIEW_FULL_DATA, None)
    analyze_request: InterviewAnalyzeRequest = st.session_state.get(SESSION_KEY_INTERVIEW_ANALYZE_REQUEST, None)

    if interview_full_data is not None:
        window_height = get_windows_height()
        with st.container(border=True, height=window_height - 150):
            analyze_tab, mindmap_tab, review_tab, tea_tab, tem_map_tab, summary, qa_tab, doc_generate_tab = st.tabs(
                ["**インタビュー解析**","**インタビューマインドマップ**","**インタビューレビュー**","**TEA解析**","**TEM図作成**","**インタビューイの特徴分析**","**インタビューQ&A**","**ダウンロード**"])
            with analyze_tab:
                if analyze_request.theme == "2nd":
                    st.write('''
                            ## Foodableサービスに関するインタビュー 2回目

                            ### 1. 購入・申し込みの経緯
                            * **炊飯器購入の動機**
                            * 故障をきっかけに新しい炊飯器が必要となった
                            * 量販店やネットでの比較検討
                            * 高性能炊飯器への憧れ
                            * **フーダブルの選択理由**
                            * パナソニックの新しい試みという印象
                            * 真空パックの少量米が決め手
                            * 銘柄ごとの炊き分け機能への関心
                            * **他の選択肢との比較**
                            * 土鍋炊飯や他社製品の検討
                            * 予約機能のない炊飯方法の不便さ

                            ### 2. 食生活・暮らし方
                            * **自炊の頻度と工夫**
                            * 週に約10回の自炊
                            * 昼は簡単な麺類や前日の残り物の活用
                            * 夜は炊飯器を事前セットして時短
                            * **献立の工夫と買い物の意識**
                            * 週末にまとめ買い、平日はアレンジの効く食材を選択
                            * 冷凍食品をストックして忙しい日の対策
                            * **土日と平日の違い**
                            * 土日は手の込んだ料理に挑戦
                            * 平日は時短重視で簡単に済ませる
                            * **外食の頻度と家族の影響**
                            * 月に1〜2回程度の外食
                            * 高齢の両親の嗜好に合わせたメニュー選択
                            * 若い頃の外食経験や料理教室の影響

                            ### 3. 価値観・心理的要因
                            * **健康意識と家族への配慮**
                            * 両親の健康を考えた食材選び
                            * 少量米を選ぶことでの食品ロスの軽減
                            * **料理に対するモチベーション**
                            * キッチンのリフォームでモチベーションアップ
                            * 料理自体は好きではないが、工夫して楽しもうとする姿勢
                            * **社会的・文化的影響**
                            * 親戚の訪問時に高評価だった銘柄選びの影響
                            * 昔通っていた料理教室の経験が現在の献立に影響

                            ### 4. 製品・サービスの評価
                            * **フーダブルの使用感**
                            * 銘柄炊き分けの良さ
                            * 少量パックの防災食としてのメリット
                            * **パナソニック製品の印象**
                            * 家族全体のブランド好感度
                            * リフォーム後の最新キッチン家電への満足度
                            * **改善点・要望**
                            * 銘柄選択の画面操作の改善点
                            * 追加購入のしやすさに対する要望

                    '''
                    )
                else:
                    st.write('''
                            ## Foodableサービスに関するインタビュー

                            ### 1. 契約時の動機
                            * **サブスクリプション契約の理由**
                            * 家電破損や利便性追求
                            * 母親の認知症による安全対策
                            * Foodableの2合パックの使いやすさ
                            * **他社製品との比較**
                            * Foodableの交換サービスと品質の高さ
                            * スーパー購入との比較での効率性

                            ### 2. 使用頻度と利用状況
                            * **使用頻度**
                            * 炊飯器: 2日に1回、2合
                            * 食材パック: 冷凍保存し計画的に使用
                            * **使用方法**
                            * 食材は定期的に届き、必要に応じて追加注文
                            * 2合パックの量が家族構成にちょうど良い

                            ### 3. 製品の満足点
                            * **サービスの魅力**
                            * 2合パックの便利さ
                            * Wi-Fi接続による遠隔管理
                            * 炊飯器の多機能性
                            * **製品機能**
                            * 安全性と便利さの両立
                            * サービスの手軽さ

                            ### 4. 製品の不満点
                            * **不便な点**
                            * 炊飯器の重量
                            * 注文画面の操作性
                            * **サービス利用時の困難**
                            * 配送タイミングの不明確さ
                            * 母親による誤操作

                            ### 5. サービスの選択基準
                            * **継続する理由**
                            * 定期配送の利便性
                            * 品質と安全性の信頼感
                            * **他社製品との違い**
                            * 食材や家電の計画的な管理

                            ### 6. 生活への影響
                            * **Foodable導入後の変化**
                            * 家事負担軽減
                            * 健康志向への貢献
                            * **他の家電製品への波及効果**
                            * 家庭の安全性向上
                            * 家電の使いやすさへの影響

                            ### 7. 追加購入と選択行動
                            * **追加購入の動機**
                            * 備蓄不足
                            * 新しい銘柄への興味
                            * **月初めの行動パターン**
                            * 月初めに必要なものを追加注文
                            * ポイント活用

                            ### 8. 顧客背景とコンテクスト
                            * **インタビュー対象者の背景**
                            * 健康志向
                            * 家族の健康状態
                            * **他の家電との関係**
                            * 安全性と利便性を重視

                            ### 9. 改善提案
                            * **サービスの改善点**
                            * 注文画面の簡素化
                            * 配送タイミングの透明性向上
                            * 操作性のシンプルな家電設計
                            * **新しい機能**
                            * 高齢者向けUI
                            * 個別ニーズに応じたパーソナライズ
                    '''
                    )

                    
            with mindmap_tab:
                if analyze_request.theme == "2nd":
                    plantuml_code = '''
                        @startmindmap
                        * Foodableサービスに関するインタビュー 2回目
                        ** 1. 購入・申し込みの経緯
                        *** 炊飯器購入の動機
                        **** 故障をきっかけに新しい炊飯器が必要となった
                        **** 量販店やネットでの比較検討
                        **** 高性能炊飯器への憧れ
                        *** フーダブルの選択理由
                        **** パナソニックの新しい試みという印象
                        **** 真空パックの少量米が決め手
                        **** 銘柄ごとの炊き分け機能への関心
                        *** 他の選択肢との比較
                        **** 土鍋炊飯や他社製品の検討
                        **** 予約機能のない炊飯方法の不便さ

                        ** 2. 食生活・暮らし方
                        *** 自炊の頻度と工夫
                        **** 週に約10回の自炊
                        **** 昼は簡単な麺類や前日の残り物の活用
                        **** 夜は炊飯器を事前セットして時短
                        *** 献立の工夫と買い物の意識
                        **** 週末にまとめ買い、平日はアレンジの効く食材を選択
                        **** 冷凍食品をストックして忙しい日の対策
                        *** 土日と平日の違い
                        **** 土日は手の込んだ料理に挑戦
                        **** 平日は時短重視で簡単に済ませる
                        *** 外食の頻度と家族の影響
                        **** 月に1〜2回程度の外食
                        **** 高齢の両親の嗜好に合わせたメニュー選択
                        **** 若い頃の外食経験や料理教室の影響

                        ** 3. 価値観・心理的要因
                        *** 健康意識と家族への配慮
                        **** 両親の健康を考えた食材選び
                        **** 少量米を選ぶことでの食品ロスの軽減
                        *** 料理に対するモチベーション
                        **** キッチンのリフォームでモチベーションアップ
                        **** 料理自体は好きではないが、工夫して楽しもうとする姿勢
                        *** 社会的・文化的影響
                        **** 親戚の訪問時に高評価だった銘柄選びの影響
                        **** 昔通っていた料理教室の経験が現在の献立に影響

                        ** 4. 製品・サービスの評価
                        *** フーダブルの使用感
                        **** 銘柄炊き分けの良さ
                        **** 少量パックの防災食としてのメリット
                        *** パナソニック製品の印象
                        **** 家族全体のブランド好感度
                        **** リフォーム後の最新キッチン家電への満足度
                        *** 改善点・要望
                        **** 銘柄選択の画面操作の改善点
                        **** 追加購入のしやすさに対する要望 
                        @endmindmap
                        '''
                else:
                    plantuml_code = '''
                        @startmindmap
                        * Foodableサービスに関するインタビュー
                        ** 1. 契約時の動機
                        *** サブスクリプション契約の理由
                        **** 家電破損や利便性追求
                        **** 母親の認知症による安全対策
                        **** Foodableの2合パックの使いやすさ
                        *** 他社製品との比較
                        **** Foodableの交換サービスと品質の高さ
                        **** スーパー購入との比較での効率性
                        ** 2. 使用頻度と利用状況
                        *** 使用頻度
                        **** 炊飯器: 2日に1回、2合
                        **** 食材パック: 冷凍保存し計画的に使用
                        *** 使用方法
                        **** 食材は定期的に届き、必要に応じて追加注文
                        **** 2合パックの量が家族構成にちょうど良い

                        ** 3. 製品の満足点
                        *** サービスの魅力
                        **** 2合パックの便利さ
                        **** Wi-Fi接続による遠隔管理
                        **** 炊飯器の多機能性
                        *** 製品機能
                        **** 安全性と便利さの両立
                        **** サービスの手軽さ

                        ** 4. 製品の不満点
                        *** 不便な点
                        **** 炊飯器の重量
                        **** 注文画面の操作性
                        *** サービス利用時の困難
                        **** 配送タイミングの不明確さ
                        **** 母親による誤操作

                        ** 5. サービスの選択基準
                        *** 継続する理由
                        **** 定期配送の利便性
                        **** 品質と安全性の信頼感
                        *** 他社製品との違い
                        **** 食材や家電の計画的な管理

                        ** 6. 生活への影響
                        *** Foodable導入後の変化
                        **** 家事負担軽減
                        **** 健康志向への貢献
                        *** 他の家電製品への波及効果
                        **** 家庭の安全性向上
                        **** 家電の使いやすさへの影響

                        ** 7. 追加購入と選択行動
                        *** 追加購入の動機
                        **** 備蓄不足
                        **** 新しい銘柄への興味
                        *** 月初めの行動パターン
                        **** 月初めに必要なものを追加注文
                        **** ポイント活用

                        ** 8. 顧客背景とコンテクスト
                        *** インタビュー対象者の背景
                        **** 健康志向
                        **** 家族の健康状態
                        *** 他の家電との関係
                        **** 安全性と利便性を重視

                        ** 9. 改善提案
                        *** サービスの改善点
                        **** 注文画面の簡素化
                        **** 配送タイミングの透明性向上
                        **** 操作性のシンプルな家電設計
                        *** 新しい機能
                        **** 高齢者向けUI
                        **** 個別ニーズに応じたパーソナライズ
                        @endmindmap
                        '''
                # PlantUMLサーバーのURL
                plantuml_server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
                # PlantUMLコードを画像に変換
                plantuml_image = plantuml_server.processes(plantuml_code)
                # 画像をBase64エンコード
                plantuml_image_base64 = base64.b64encode(plantuml_image).decode('utf-8')
                # 画像を表示
                st.image(f"data:image/png;base64,{plantuml_image_base64}")
            with qa_tab:
                # Accept user input
                if prompt := st.chat_input("What is up?"):
                    # Display user message in chat message container
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
            with summary:
                if analyze_request.theme == "2nd":
                    st.write('''
                        # インタビューイの分析

                        ---

                        ## 1. 背景・状況
                        - インタビューイは家庭内での食事準備を担当しており、家族（両親）と同居しています。
                        - 両親の健康状態を考慮しながらの食事準備が必要で、特に消化しやすい料理を心がけています。
                        - 過去に料理教室に通っていた経験があり、様々な料理を学んでいますが、現在はシンプルな料理を中心にしています。

                        ---

                        ## 2. 価値観・モチベーション
                        - **食事の価値観**: 食事を通じて家族との繋がりを重視。特に両親の健康を考慮した選択をしています。
                        - **料理に対するモチベーション**:
                        - 基本的には料理が「好き」というよりも「必要だからする」スタンス。
                        - ただし、キッチンのリフォームを通じてモチベーションを上げる工夫をしています。
                        - 土日には「楽しみ」の要素を取り入れ、少し手の込んだ料理に挑戦することも。

                        ---

                        ## 3. 行動パターン
                        - **平日の料理**:
                        - 仕事の合間に炊飯器をセットし、仕事が終わったら30分程度で料理を仕上げるスタイル。
                        - 忙しい日は簡単に作れるもの、または買い物で済ませることもある。
                        - **土日の料理**:
                        - 平日と比べて余裕があるため、手の込んだ料理に挑戦することが多い。
                        - 料理本やネットのレシピを参考にすることがあり、キッチンにデバイスを設置して効率よく調べながら調理している。

                        ---

                        ## 4. 課題・悩み
                        - 両親の嗜好に合わせた料理が求められ、自分が本当に作りたいものや食べたいものを作る機会が限られている。
                        - 特に両親が食べ慣れない料理（外国料理など）は避ける傾向にあり、レパートリーが狭まっている。
                        - 忙しい平日に効率よく料理をする必要があり、時短を意識した食材選びや家電の活用をしている。

                        ---

                        ## 5. インサイト・提案
                        - **食事キットや冷凍食品の利用**:
                        - 忙しい平日に役立つ半調理品や、時短レシピが充実した食事キットを活用すると、料理の負担が軽減される可能性がある。
                        - **レパートリー拡充のサポート**:
                        - 家族の嗜好に合わせつつ、インタビューイ自身の興味に合った新しいレシピの提案が有効。
                        - 特に和食のバリエーションを増やすことで、両親に受け入れられやすく、かつ本人のモチベーションアップにつながる可能性がある。
                        - **料理体験の共有**:
                        - コロナ禍で減少した料理の共有体験を、オンライン料理教室やレシピの共有プラットフォームなどを通じて補うことが、楽しみを増やす要因になるかもしれない。

                        ---

                        ## 6. 結論
                        - インタビューイは、家族を大切にしつつ、料理の負担を減らし、効率化と楽しみのバランスを追求している。
                        - 両親の健康を考慮した献立づくりが求められる中で、食事の準備におけるストレスを軽減する方法が望まれている。
                        - 料理そのものに対するモチベーションは低めだが、キッチンの環境改善や新しいレシピの導入を通じて、楽しみを見出そうとしている。

                        ---
                        ''')
                else:
                    st.write('''
                        ## インタビューイの分析

                        ### 1. **コミュニケーションスタイル**
                        - **応答の迅速さ**: 質問に対して即座に返答しており、コミュニケーションに対する抵抗感は低いと考えられます。
                        - **内容の簡潔さ**: 必要最低限の情報をシンプルに伝えているため、論理的かつ効率的なコミュニケーションを好む傾向があります。

                        ### 2. **感情・態度の傾向**
                        - **落ち着きと受容性**: 「特にない」「分からなければ」という表現から、リラックスしており、相手の主導に任せる姿勢が見られます。
                        - **慎重さと確認意識**: 「間違うんです 早知しました」という表現から、誤解を避けるための確認意識が高いと推察されます。

                        ### 3. **関心事・価値観**
                        - **事前準備の重要性**: 最初の会話で「気になることは特にない」と答えていますが、質問があった場合に備えていることから、柔軟性と適応力を重視していることが伺えます。
                        - **個人情報の取扱いに対する慎重さ**: 名前や家族構成に関する質問に対して、適度な情報開示を意識している様子が見られ、プライバシー保護への配慮が感じられます。

                        ### 4. **推奨されるコミュニケーション戦略**
                        - **シンプルで明確な質問**: 短くて明快な質問形式が、インタビューイのコミュニケーションスタイルにマッチします。
                        - **確認を促すフィードバック**: 誤解を避けるため、要点をまとめて確認するフィードバックを取り入れることで、より円滑な対話が可能です。
                            ''')
            with review_tab:
                if analyze_request.theme == "2nd":
                    st.write('''
                        ## インタビュアー評価

                        ### 1. 目的「footableの契約」に関する行動変異を広く聞き出せたか  
                        **評価: 3/5**  
                        **コメント:**  
                        契約に至るまでの過程や他の選択肢について一定の情報を引き出せています。しかし、情報がやや表面的で、より詳細な背景（例: 他の炊飯器との比較検討や契約を迷った要因など）を深掘りする余地がありました。選択肢の幅を広げるために、具体的な場面設定や選択のプロセスに焦点を当てた質問があるとさらに良かったです。

                        ---

                        ### 2. 行動の理由を深掘りできたか (感情面など)  
                        **評価: 3/5**  
                        **コメント:**  
                        炊飯器の選択理由やフーダブルを選んだ決定打について、感情面を含めある程度掘り下げていますが、さらに「なぜそう思ったのか」「その感情に影響を与えた要素は何か」といった深堀りが不足しています。回答者の価値観や動機の背景に迫るために、共感を示しながら感情の源泉にアプローチする質問があるとより効果的でした。

                        ---

                        ### 3. その他  
                        **評価: 4/5**  
                        **コメント:**  
                        全体的に和やかな雰囲気を作り、回答しやすい場を提供している点は評価できます。また、契約後の体験や食生活全般にまで話を広げ、契約に関連するライフスタイルの背景を理解しようとする姿勢は良かったです。ただし、契約決定に影響した外部要因（例: 家族の意見、経済的な要因）をもう少し探ることで、より包括的な理解が得られたと思われます。

                        ---

                        ## 総評  
                        聞き出しの幅はあるものの、深掘りがやや不足しており、行動変異の背景をもう一歩追求できる余地がありました。それでも、回答者がリラックスして話せる雰囲気作りや、幅広い情報を得ようとする姿勢は良好です。次回は、行動の背景にある動機や感情をさらに掘り下げるための質問設計に工夫が必要です。
                    ''')
                else:
                    st.write('''
                        ## インタビュアー評価

                        ### 1. 目的「footableの契約」に関する行動変異を広く聞き出せたか  
                        **評価: 3/5**  
                        **コメント:**  
                        基本的な質問から始めており、自然な流れで会話を進めていますが、「footableの契約」に関する行動変異を広く聞き出すためには、もう少し契約前後の具体的な状況や他の選択肢を検討した経緯に踏み込む必要がありました。例えば、「他に検討した製品はありましたか？」「その時どのように比較しましたか？」など、具体的な行動を掘り下げる質問があると、行動変異をより広く捉えられたでしょう。

                        ---

                        ### 2. 行動の理由を深掘りできたか (感情面など)  
                        **評価: 3/5**  
                        **コメント:**  
                        行動の背景にある感情面にある程度触れていますが、もう一歩踏み込んだ質問が少ない印象です。例えば、「その選択をしたとき、どのような気持ちになりましたか？」「その感情に影響を与えた要因は何ですか？」といった感情の源泉を探ることで、行動理由をより深く理解できたはずです。共感を示しながら感情面を引き出す工夫があると、さらに深掘りできたでしょう。

                        ---

                        ### 3. その他  
                        **評価: 4/5**  
                        **コメント:**  
                        会話の流れがスムーズで、回答者がリラックスして話せる雰囲気を作れていました。特に、会話の初めに「気になることはありますか？」と質問し、相手が質問しやすい状態を作った点は良かったです。ただ、インタビューの後半に向けて、少し深掘りが弱くなっているため、もう少し粘り強く聞く姿勢があると、より詳細な情報を引き出せたと思われます。

                        ---

                        ## 総評  
                        聞き出しの幅はあるものの、深掘りがやや不足しており、行動変異の背景をもう一歩追求できる余地がありました。特に、行動理由の感情面に関しては、もう少し踏み込んだ質問があると良かったです。それでも、回答者がリラックスして話せる雰囲気作りや、自然な流れでの質問は良好です。次回は、感情面の背景に迫るための質問設計に工夫が必要です。

                        ''')
            with tea_tab:
                if analyze_request.theme == "2nd":
                    st.write('''
                        # TEA 分析結果

                        ## 1. 切片化
                        ### 購入・申し込みの経緯
                        - 炊飯器が故障し、新しい炊飯器の必要性を感じた。
                        - フーダブルに興味を持ったきっかけは、パナソニックの新しい試みと真空パックの少量米。
                        - 銘柄ごとの炊き分け機能に魅力を感じた。
                        - 他の選択肢として土鍋炊飯や他社製品を検討していたが、使い勝手や安全性を考慮して断念。
                        - フーダブルを選択した決め手は、少量のお米が届く便利さと防災食としての有用性。

                        ### 食生活・暮らし方
                        - 週に約10回の自炊を行っている。
                        - 昼は麺類や前日の残り物で簡単に済ませ、夜は炊飯器を事前セットして時短を図っている。
                        - 平日は時短重視だが、土日は手の込んだ料理に挑戦している。
                        - 家族全員の食事を準備する必要があり、高齢の両親の嗜好や健康を考慮している。

                        ### 価値観・心理的要因
                        - 家族の健康を考慮して、体に良い食材を選ぶようにしている。
                        - 食品ロスを避けるため、少量米を選ぶ傾向がある。
                        - キッチンをリフォームして料理のモチベーションを上げる工夫をしている。
                        - 料理自体は好きではないが、家族のために工夫しながら楽しもうとしている。

                        ## 2. 等至点 (Equifinality Point: EFP)
                        - **EFP: フーダブルを選択して継続的に利用すること。**
                        - 少量米の便利さ、銘柄炊き分けの楽しみ、高齢の両親への配慮が等至点に向かう共通の動機。

                        ## 3. 分岐点 (Bifurcation Point: BFP)
                        - **BFP1: 家電を購入する vs サブスクリプションで借りる**
                        - 購入の方が長期的なコストパフォーマンスが良いが、フーダブルのサブスクリプションの利便性を選択。
                        - **BFP2: 他社製品との比較**
                        - 土鍋炊飯や他社の高級炊飯器を検討したが、機能性や使い勝手でフーダブルを選択。
                        - **BFP3: 銘柄選択の方法**
                        - 自動で届くものを受け取る vs 毎回銘柄を選択する
                        - 初期は自動受け取りを利用していたが、後にメール通知をきっかけに銘柄選択を始めた。

                        ## 4. 必須通過点 (Obligatory Passage Point: OPP)
                        - **OPP1: 炊飯器の故障**
                        - 新しい炊飯器の購入を検討するきっかけとなった重要な出来事。
                        - **OPP2: 家族の食生活への配慮**
                        - 高齢の両親の健康を考慮し、少量米や銘柄炊き分けに関心を持つ要因。
                        - **OPP3: 情報収集と比較検討**
                        - 量販店やネットでの情報収集を経てフーダブルを選択。

                        ## 5. 社会的方向づけ (Social Direction: SD) と助勢 (Social Guidance: SG)
                        ### SD (阻害要因)
                        - **SD1: 高価格の炊飯器に対する抵抗感**
                        - 高性能炊飯器の価格がネックになり、他社製品と比較検討を行った。
                        - **SD2: 高齢の両親の操作不安**
                        - 複雑な操作性に対する不安が、購入決断に影響を与えた。
                        - **SD3: 食生活の制約**
                        - 高齢の両親の嗜好や健康状態に合わせた献立を考える必要がある。

                        ### SG (助勢要因)
                        - **SG1: 少量米の便利さと食品ロスの削減**
                        - フーダブルの少量米パックが、食品ロスの軽減と防災食としてのメリットを提供。
                        - **SG2: 銘柄炊き分け機能の楽しさ**
                        - 銘柄ごとの炊き分けが、食事の楽しみを増幅させた。
                        - **SG3: パナソニックブランドの信頼感**
                        - 家族全体のブランド好感度が購入を後押し。
                        - **SG4: キッチンのリフォームによるモチベーションアップ**
                        - リフォーム後の最新キッチン家電が料理のモチベーションを向上。

                        ---

                        ## 総括
                        インタビュー対象者は、炊飯器の故障をきっかけに新しい炊飯器の必要性を感じ、パナソニックのフーダブルを選択した。少量米の便利さ、銘柄炊き分けの楽しさ、高齢の両親への配慮が等至点(EFP)に到達する主な動機であった。一方で、他社製品との比較や価格に対する抵抗感などが分岐点(BFP)となった。また、家族の健康への配慮や食品ロスの軽減を目指す行動が、社会的方向づけ(SD)と助勢(SG)の要因となっている。最終的に、これらの要因が絡み合いながら、フーダブルの継続利用という等至点に到達している。

                        ''')
                else:
                    st.write('''
                        ## Foodable契約と利用継続に関する分岐点分析

                        ### 分岐点と意思決定要因

                        #### 1. 契約動機における分岐点
                        * **家電故障と代替品選択:**
                        * 認知症の母親のために、安全で使いやすい炊飯器が必要だった。
                        * 定期的な買い替えが含まれるFoodableのサービスに魅力を感じた。
                        * **購入方法の選択:**
                        * スーパーでの大量購入による無駄をなくしたい。
                        * 必要な分だけ炊ける2合パックの便利さ。
                        * **他社製品との比較:**
                        * Foodableの機能性（Wi-Fi接続、銘柄ごとの炊き分け）が優れていた。
                        * 定期配送の利便性と、スーパー購入とのコスト比較。

                        #### 2. 生活スタイルとの適合性
                        * **生活の計画性:**
                        * 定期配送により、食事の準備が楽になった。
                        * 家族構成に合わせた2合パックが無駄をなくす。
                        * **特定機能へのニーズ:**
                        * Wi-Fi接続による遠隔操作の便利さ。
                        * 銘柄ごとの炊き分け機能の有用性。

                        ### 必須通過点
                        * 家電の故障や利用不能
                        * 便利で安全なサービスの必要性
                        * 他社製品との比較
                        * 継続利用を見据えた条件

                        ### 社会的助勢（SG）と社会的方向づけ（SD）
                        #### 社会的助勢（SG）
                        * **定期配送の利便性:** 食材の供給が途切れない、家事負担軽減
                        * **炊飯器の高機能性:** ニーズを満たし、生活の質向上
                        * **サイズ感と食品パックの利便性:** 過剰購入防止、コスト削減
                        * **契約更新やサポートの仕組み:** 安心感の提供、継続利用の促進
                        * **健康志向や家族の安全:** 健康や安全への配慮

                        #### 社会的方向づけ（SD）
                        * **コスト面の課題:** スーパー購入との比較でのコスト高
                        * **製品の重さや操作性:** 物理的な使いにくさ、誤操作
                        * **注文画面や管理の煩雑さ:** 操作性の悪さ
                        * **配送タイミングの不透明さ:** 配送の遅延や不確実性

                        ### 分析結果
                        * **主要な分岐点:** 家電故障、購入方法、他社製品との比較、生活スタイルとの適合性
                        * **契約を促進する要因:** 便利さ、機能性、安全性、健康志向、サポート体制
                        * **契約を阻害する要因:** コスト、使いにくさ、操作性、配送の遅延

                        ### まとめ
                        Foodableの契約は、家電の故障をきっかけに、便利さや機能性、健康志向といった多様な要因が複雑に絡み合って決定される。特に、定期配送の利便性や炊飯器の高機能性が大きな魅力として挙げられる。一方で、コストや操作性といった課題も存在し、今後の改善点となる。

                        **この分析結果を基に、以下の点が考えられます。**
                        * **マーケティング:**
                        * コストパフォーマンスの向上
                        * 操作性の改善
                        * 配送サービスの精度向上
                        * **製品開発:**
                        * より多様なユーザーに対応できる機能の追加
                        * デザインの改善
                        * **顧客サポート:**
                        * 操作に関する問い合わせへの迅速な対応
                        * 契約に関する不安解消

                        ### その他
                        * **可視化:** 上記の分析結果を図やグラフを用いて可視化することで、より分かりやすく伝わる。
                        * **深堀り:** 各分岐点について、さらに詳細な分析を行うことで、より深い洞察を得られる。
                        * **比較分析:** 他社の類似サービスとの比較分析を行うことで、Foodableの強みと弱みを明確にする。                
                    ''')
            with tem_map_tab:
                if analyze_request.theme == "2nd":
                    flowchart = create_flowchart2()
                    st.graphviz_chart(flowchart)
                else:
                    flowchart = create_flowchart1()
                    st.graphviz_chart(flowchart)

            with doc_generate_tab:
                # ダウンロードしたいファイルのパス
                file_path = "test.txt"

                # ダウンロードボタンの表示
                st.download_button(
                    label="解析ファイルを一括ダウンロード",
                    data=open(file_path, 'rb').read(),
                    file_name='sample_data.csv',
                    mime='text/csv'
                )

#

@st.cache_resource
def init_env():
    clear_folder("./tmp")

def main():
    initialize_page(page_title="テキストの解析", page_icon="📝")
    init_env()
    show_analyze_settings()
    show_analyze_button()
    show_analyze_results()


if __name__ == '__main__':
    main()