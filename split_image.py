import cv2
import numpy as np
# 日時でディレクトリを作成
import os
import datetime

# 画像を読み込む
image_path = input('画像ファイルのパスを入力してください: ')
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

image_filename = os.path.basename(image_path).split('.')[0]

now = datetime.datetime.now()
dir_name = now.strftime(f'{image_filename}_%Y%m%d_%H%M%S')
os.makedirs(dir_name, exist_ok=True)


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
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# 各領域を処理する
for i, contour in enumerate(contours):
    # contourからマスク領域を作成
    mask = np.zeros_like(alpha_channel)
    cv2.drawContours(mask, contours, i, 255, -1)

    # マスク領域とアルファチャンネルをAND演算
    transparent_img = image.copy()
    transparent_img[:, :, 3] = cv2.bitwise_and(alpha_channel, mask)
    
    # 修正された画像を透過PNGとして保存する
    part_filename = f'{dir_name}/part_{i}.png'
    cv2.imwrite(part_filename, transparent_img)
    print(f'パーツ{i}が {part_filename} として保存されました。')

print('全てのパーツの保存が完了しました。')
