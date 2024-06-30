import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
from tkvideo import tkvideo
import pygame

# ダウンロード関連の関数
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(save_path, 'wb') as file:
        for data in response.iter_content(block_size):
            file.write(data)
    return total_size

# ダウンロードを開始する関数
def start_download():
    # ダウンロードするファイルのURL
    urls = [
        "https://github.com/yuzu-krs/YuzuClientLauncher/raw/main/3.0.0/YuzuClient.jar",
        "https://github.com/yuzu-krs/YuzuClientLauncher/raw/main/3.0.0/YuzuClient.json"
    ]

    # ダウンロード先のフォルダ名
    download_folder = "YuzuClient"
    save_folder_path = os.path.join(os.getcwd(), download_folder)

    # フォルダが存在しない場合は作成
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    progress_bar["maximum"] = len(urls)
    progress_bar["value"] = 0

    for i, url in enumerate(urls):
        filename = os.path.basename(url)
        file_path = os.path.join(save_folder_path, filename)
        label_status.config(text="", font=("Helvetica", 14, "bold"))  # テキストを空にしてフォントを太く
        root.update_idletasks()

        label_status.config(text=f"{filename} をダウンロード中...", font=("Helvetica", 14, "bold"))
        root.update_idletasks()

        download_file(url, file_path)

        label_status.config(text=f"{filename} のダウンロードが完了しました。", font=("Helvetica", 14, "bold"))
        root.update_idletasks()

        progress_bar["value"] = i + 1
        root.update_idletasks()

    # ユーザー名を取得
    user_name = os.getlogin()

    # マインクラフトのバージョンフォルダ
    minecraft_versions_folder = f"C:\\Users\\{user_name}\\AppData\\Roaming\\.minecraft\\versions"

    # 保存先のYuzuClientフォルダのパス
    minecraft_yuzu_folder = os.path.join(minecraft_versions_folder, download_folder)

    # フォルダが存在しない場合は作成
    if not os.path.exists(minecraft_yuzu_folder):
        os.makedirs(minecraft_yuzu_folder)

    for filename in os.listdir(save_folder_path):
        src_path = os.path.join(save_folder_path, filename)
        dst_path = os.path.join(minecraft_yuzu_folder, filename)
        with open(src_path, 'rb') as src_file:
            with open(dst_path, 'wb') as dst_file:
                dst_file.write(src_file.read())
        print(f"{filename} を {minecraft_yuzu_folder} にコピーしました。")

    label_status.config(text="すべてのダウンロードが完了しました。", font=("Helvetica", 14, "bold"))
    messagebox.showinfo("完了", "すべてのファイルがダウンロードされ、コピーされました。")

def play_background_music():
    # 音楽ファイルのパス
    music_path = "background.mp3"

    # Pygame の初期化
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # 無限ループ再生

# GUIの設定
root = tk.Tk()
root.title("YuzuClient - Installer")
root.resizable(0, 0)
lbl = tk.Label(root)
lbl.pack()

# ウィンドウサイズ設定
root.geometry("800x450")

# キャンバスを作成し、背景動画を表示する
canvas = tk.Canvas(root, width=800, height=450)
canvas.pack()

# フレームを作成し、ウィジェットを配置する
frame = tk.Frame(root, bg='#ffffff', bd=5)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# スタイル設定
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14, "bold"), padding=10)
style.configure("TLabel", background="white", font=("Helvetica", 14, "bold"))
style.configure("TProgressbar", thickness=20)

label_status = ttk.Label(frame, text="開始するには「ダウンロード」ボタンを押してください。", style="TLabel")
label_status.grid(row=0, column=0, pady=5)

progress_bar = ttk.Progressbar(frame, length=300, style="TProgressbar")
progress_bar.grid(row=1, column=0, pady=10)

download_button = ttk.Button(frame, text="ダウンロード", command=start_download, style="TButton")
download_button.grid(row=2, column=0, pady=20)

player = tkvideo("background.mp4", lbl, loop=1, size=(800, 450))
player.play()

# Function to limit FPS to 30
def update_gui():
    root.update_idletasks()
    root.update()
    root.after(33, update_gui)  # 1000ms / 30fps ≈ 33ms
play_background_music()

# Start the GUI update loop
root.after(33, update_gui)

root.mainloop()
