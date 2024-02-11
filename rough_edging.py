import cv2
import numpy as np


def scale_contours(contours, scale_factor):
    """
    輪郭を拡大する関数
    :param contours: 拡大する輪郭のリスト
    :param scale_factor: 拡大係数
    :return: 拡大された輪郭のリスト
    """
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


# 画像の読み込みとアルファチャンネルの取得
image_path = input('画像ファイルのパスを入力してください: ')
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
alpha = image[:, :, 3]

# アルファチャンネルから二値画像を作成
thresh = 128  # 閾値
binary_image = np.array(alpha) > thresh
binary_image = binary_image.astype(np.uint8) * 255


# 輪郭の検出
contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭を拡大する係数を1.5に設定
scale_factor = 1.08

# 拡大する関数を呼び出し
scaled_contours = scale_contours(contours, scale_factor)

# 輪郭を低ポリゴンの多角形で近似
approx_polygons = [cv2.approxPolyDP(contour, 20, True) for contour in scaled_contours]

# 結果を描画する新しい画像
polygon_image = np.zeros_like(binary_image, dtype=np.uint8)
cv2.drawContours(polygon_image, approx_polygons, -1, (255), thickness=-1)  # thickness=-1で内部を塗りつぶす

# 画像の合成
foreground_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# 出力用の画像を作成
output_image = np.zeros_like(foreground_image)

# まずポリゴン画像のデータをコピー
output_image[:, :, 0] = polygon_image
output_image[:, :, 1] = polygon_image
output_image[:, :, 2] = polygon_image
output_image[:, :, 3] = polygon_image

# 元画像の透明度を使って合成
for y in range(foreground_image.shape[0]):
    for x in range(foreground_image.shape[1]):
        alpha = foreground_image[y, x, 3] / 255.0
        output_image[y, x, 0:3] = (1 - alpha) * output_image[y, x, 0:3] + alpha * foreground_image[y, x, 0:3]

# 結果の保存
cv2.imwrite(f'raugh_edging_{image_path}', output_image)
