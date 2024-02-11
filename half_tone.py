from PIL import Image
import math

# ハーフトーンを適用する関数
# 引数: 画像, 強度, グリッドサイズ, スケール, シフト, ドットの色, 背景色, ガンマ
# 強度: ハーフトーンの強度 (0.0 - 1.0)
# グリッドサイズ: ドットの間隔
# スケール: ドットの大きさ
# シフト: ドットのシフト
# ドットの色: ドットの色
# 背景色: 背景の色
# ガンマ: ガンマ補正
# 戻り値: 画像
def apply_halftone(image, strength=1.0, grid_size=4, scale=1.0, shift=0, dot_color=(0, 0, 0), bg_color=(255, 255, 255), gamma=1.0):
    # 画像データをロード   
    pixels = image.load()
    width, height = image.size

    # 画像のそれぞれのピクセルに対して処理を行う
    for y in range(height):
        for x in range(width):
            # 元の色とアルファ値を取得
            original_r, original_g, original_b, alpha = pixels[x, y]
            
            # 輝度を計算
            luminance = (0.298912 * original_r + 0.586611 * original_g + 0.114478 * original_b) / 255
            
            # 対応するグリッドの位置を計算
            grid_x = (x + shift) % grid_size
            grid_y = (y + shift) % grid_size
            
            # グリッドの中心までの距離を計算
            dist = math.sqrt(grid_x**2 + grid_y**2) * grid_size
            
            # ドットの大きさを計算
            dot_size = (1 - luminance**gamma) * scale * grid_size
            
            # 割合を計算
            ratio = min(1, max(0, strength * (1 - (dist - dot_size))))
            
            # 新しい色を計算
            new_r = ratio * dot_color[0] + (1 - ratio) * bg_color[0]
            new_g = ratio * dot_color[1] + (1 - ratio) * bg_color[1]
            new_b = ratio * dot_color[2] + (1 - ratio) * bg_color[2]
            
            # ピクセルの色を更新
            pixels[x, y] = (int(new_r), int(new_g), int(new_b), alpha)

    return image

file_path = input('画像ファイルのパスを入力してください: ')

# 画像を読み込む
input_image = Image.open(file_path)

# エフェクトの適用
output_image = apply_halftone(input_image, strength=1.0, grid_size=4, scale=100, shift=0, dot_color=(0,0,0), bg_color=(255,255,255), gamma=0.04)

# 画像を保存
output_image.save(f'halftone_{file_path}')
