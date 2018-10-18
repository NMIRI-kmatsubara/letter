#coding: utf-8
import numpy as np
import cv2

#画像の保存名
dir_path = "kmletter2.jpg"

#前処理
img = cv2.imread(dir_path)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,img_binary = cv2.threshold(img_gray,135,255,cv2.THRESH_BINARY)
img_binary_wise = cv2.bitwise_not(img_binary)

#ノイズ除去
_,img_contours,hierarchy = cv2.findContours(img_binary_wise,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
min_img_area = 140
large_contours =[cnt for cnt in img_contours if cv2.contourArea(cnt) > min_img_area]

bounding_img = np.copy(img)
#短形描画
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(bounding_img, (x,y), (x+w,y+h), (0,255,0), 3)
cv2.imwrite("select.jpg", bounding_img)

#切り抜き
#https://qiita.com/ShirataHikaru/items/a1dab6c6b5ba088123e0
i = 0
offset = 30
if len(large_contours) > 0:
    for rect in large_contours:
        x, y, w, h = cv2.boundingRect(rect)
        dst = img_binary_wise[y + offset:y+ h - offset, x + offset :x + w - offset]
        save_path = './' + 'sample/' + str(i) + '.jpg'
        dst2 = cv2.resize(dst,(int(h/3),int(w/3)))     #リサイズ
        cv2.imwrite(save_path, dst)                     #画像保存
        print("save")
        i += 1
print("finish")
