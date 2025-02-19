import streamlit as st
#import whisper
import pandas as pd
import os
import tempfile
from Utilities.StreamlitHelper import initialize_page, update_windows_size, get_windows_height
#from pydub import AudioSegment

def main():
    initialize_page(page_title="音声文字起こし", page_icon="🎤")
    st.write("音声ファイル（MP4）をアップロードし、逐語録をCSV形式でダウンロードします。")

    # ファイルアップロードウィジェット
    uploaded_file = st.file_uploader("音声ファイルをアップロードしてください (MP4形式)", type=["mp4"])

    if uploaded_file is not None:
        # アップロードされたファイルを一時ディレクトリに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # mp4ファイルを音声形式に変換
        st.write("音声ファイルを処理中...")
        #audio = AudioSegment.from_file(temp_file_path, format="mp4")
        #audio_path = temp_file_path.replace(".mp4", ".wav")
        #audio.export(audio_path, format="wav")

        # Whisperモデルの読み込み
        st.write("Whisperモデルを読み込んでいます...")
        #model = whisper.load_model("base")  # 必要に応じて他のモデルサイズ（tiny, small, medium, large）を選択

        # 音声をテキストに変換
        st.write("逐語録を生成しています...")
        #result = model.transcribe(audio_path)
        #result = model.transcribe(audio_path, language="ja")  # 日本語指定

        # 逐語録をDataFrameに変換
        #segments = result['segments']
        #transcript_data = []
        #for segment in segments:
        #    start_time = segment['start']
        #    end_time = segment['end']
        #    text = segment['text']
        #    transcript_data.append({
        #        "時間": f"{start_time:.2f} - {end_time:.2f}",
        #        "会話内容": text
        #    })

        #df = pd.DataFrame(transcript_data)

        # CSVファイルとしてダウンロード
        st.write("逐語録の生成が完了しました。以下のボタンからダウンロードできます。")
        #csv = df.to_csv(index=False)
        #st.download_button(
        #    label="逐語録をダウンロード (CSV)",
        #    data=csv,
        #    file_name="transcription.csv",
        #    mime="text/csv",
        #)

        # 一時ファイルを削除
        #os.remove(temp_file_path)
        #os.remove(audio_path)


if __name__ == '__main__':
    main()