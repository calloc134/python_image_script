import cv2
import numpy as np
# 日時でディレクトリを作成
import os
import datetime

# 画像のパーツを分割するユーザ定義関数
# 引数: 画像ファイルのデータ
# 戻り値: 画像データのリスト
def split_image(image):
    # アルファチャンネルの有無を確認
    alpha_present = image.shape[2] == 4
    if alpha_present:
        # アルファチャンネルが存在する場合、それを取得
        alpha_channel = image[:, :, 3]
    else:
        # アルファチャンネルがない場合、終了する
        print('アルファチャンネルがありません。')
        exit()

    # しきい値を設定する
    threshold_value = 128

    # しきい値処理を適用して二値画像を作成する
    _, binary_image = cv2.threshold(alpha_channel, threshold_value, 255, cv2.THRESH_BINARY)

    # 二値画像から連続する領域（contours）を検出する
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 画像データのリストを初期化
    image_list = []

    # 各領域を処理する
    for i, _  in enumerate(contours):
        # contourからマスク領域を作成
        mask = np.zeros_like(alpha_channel)
        cv2.drawContours(mask, contours, i, 255, -1)

        # マスク領域とアルファチャンネルをAND演算
        transparent_img = image.copy()
        transparent_img[:, :, 3] = cv2.bitwise_and(alpha_channel, mask)

        # 修正された画像をリストに追加
        image_list.append(transparent_img)

    return image_list

# 画像を読み込む
image_path = input('画像ファイルのパスを入力してください: ')
# アルファチャンネル付きで画像を読み込む
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# ファイル名の部分を取得
image_filename = os.path.basename(image_path).split('.')[0]

# 本日の日付と時刻を使ってディレクトリを作成
now = datetime.datetime.now()
dir_name = now.strftime(f'{image_filename}_%Y%m%d_%H%M%S')
os.makedirs(dir_name, exist_ok=True)

# 画像を分割
split_images = split_image(image)

# 分割された画像を保存
for i, img in enumerate(split_images):
    cv2.imwrite(f'{dir_name}/part_{i}.png', img)

print(f'{len(split_images)}個の画像を保存しました。')


