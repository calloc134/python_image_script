import cv2
import numpy as np


# 輪郭を拡大する関数
# 引数: 輪郭のリスト、拡大係数
# 戻り値: 拡大された輪郭のリスト
def scale_contours(contours, scale_factor):
    scaled_contours = []  # 拡大された輪郭を格納するリスト
    for contour in contours:
        # 輪郭の重心を計算
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            # 重心が計算できない場合はその輪郭はスキップ
            continue

        new_contour = []  # 新しい輪郭を格納するリスト
        for point in contour:
            x, y = point[0]
            rel_x, rel_y = x - cx, y - cy  # 重心からの相対位置を計算
            # 相対位置を拡大係数でスケーリング
            new_x = cx + rel_x * scale_factor
            new_y = cy + rel_y * scale_factor
            new_contour.append([[int(new_x), int(new_y)]])

        scaled_contours.append(np.array(new_contour, dtype=np.int32))
    return scaled_contours

# 二値画像を作成する関数
# 引数: 画像
# 戻り値: 二値画像
def create_binary_image(image):
    # アルファチャンネルの取得
    alpha = image[:, :, 3]

    # しきい値を設定
    thresh = 128

    # しきい値処理を適用して二値画像を作成
    binary_image = np.array(alpha) > thresh
    binary_image = binary_image.astype(np.uint8) * 255
    return binary_image

# 輪郭を低ポリゴンの多角形で近似する関数
# 引数: 輪郭のリスト、近似精度
# 戻り値: 近似された輪郭のリスト
def approximate_contours(contours, accuracy):
    approx_contours = [cv2.approxPolyDP(contour, accuracy, True) for contour in contours]
    return approx_contours

# アルファチャンネルのある画像を合成する関数
# 引数: 元画像、ポリゴン画像
# 戻り値: 合成された画像
def composite_images(foreground_image, polygon_image):
    # 出力用の画像を作成
    output_image = np.zeros_like(foreground_image)

    # ポリゴン画像をアルファチャンネルとして使う
    output_image[:, :, 0:3] = np.repeat(polygon_image[:, :, np.newaxis], 3, axis=2)
    output_image[:, :, 3] = polygon_image

    # 元画像の透明度を使って合成
    for y in range(foreground_image.shape[0]):
        for x in range(foreground_image.shape[1]):
            alpha = foreground_image[y, x, 3] / 255.0
            output_image[y, x, 0:3] = (1 - alpha) * output_image[y, x, 0:3] + alpha * foreground_image[y, x, 0:3]

    return output_image


# 画像の読み込みとアルファチャンネルの取得
image_path = input('画像ファイルのパスを入力してください: ')
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
alpha = image[:, :, 3]

# アルファチャンネルから二値画像を作成
binary_image = create_binary_image(image)

# 輪郭の検出
contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 拡大する関数を呼び出し
scaled_contours = scale_contours(contours, scale_factor=1.09)

# 輪郭を低ポリゴンの多角形で近似
approx_polygons = approximate_contours(scaled_contours, accuracy=20)

# 結果を描画する新しい画像
polygon_image = np.zeros_like(binary_image, dtype=np.uint8)
# 近似された輪郭を塗りつぶしアリで描画
cv2.drawContours(polygon_image, approx_polygons, -1, (255), thickness=-1)

# 画像の合成
foreground_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# 出力用の画像を作成
output_image = composite_images(foreground_image, polygon_image)

# 結果の保存
cv2.imwrite(f'raugh_edging_{image_path}', output_image)
