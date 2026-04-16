import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# ===================== 固定关键点 =====================
# 左区域4点：左上 → 右上 → 右下 → 左下
LEFT_POINTS = [(445, 486), (2104, 128), (2201, 2749), (650, 3261)]
# 右区域4点：左上 → 右上 → 右下 → 左下
RIGHT_POINTS = [(2129, 138), (4034, 92), (3635, 3399), (2216,2759)]
# ======================================================
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# ===================== 固定关键点 =====================
# 左区域4点：左上 → 右上 → 右下 → 左下
LEFT_POINTS = [(445, 486), (2104, 128), (2201, 2749), (650, 3261)]
# 右区域4点：左上 → 右上 → 右下 → 左下
RIGHT_POINTS = [(2129, 138), (4034, 92), (3635, 3399), (2216,2759)]
# ======================================================

class CorrectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片平整处理算法")
        self.root.geometry("900x700")

        self.img = None
        self.canvas_w = 880
        self.canvas_h = 600

        # 画布
        self.canvas = tk.Canvas(root, width=self.canvas_w, height=self.canvas_h, bg="#f0f0f0")
        self.canvas.pack(pady=5)

        # 按钮栏
        frame = ttk.Frame(root)
        frame.pack(pady=8)

        ttk.Button(frame, text="打开图片", command=self.open_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="定位关键点", command=self.show_points).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="校正并显示", command=self.correct_and_show).pack(side=tk.LEFT, padx=5)

        self.tk_img = None

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("图片", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not path:
            return
        self.img = cv2.imread(path)
        self.show_img(self.img)

    def show_img(self, img):
        if img is None:
            return
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]
        scale = min(self.canvas_w / w, self.canvas_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img_rgb = cv2.resize(img_rgb, (new_w, new_h))

        self.tk_img = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, image=self.tk_img)

    def show_points(self):
        if self.img is None:
            return
        tmp = self.img.copy()
        # 左点红色
        for pt in LEFT_POINTS:
            cv2.circle(tmp, pt, 20, (0, 0, 255), -1)
        # 右点绿色
        for pt in RIGHT_POINTS:
            cv2.circle(tmp, pt, 20, (0, 255, 0), -1)
        self.show_img(tmp)

    def warp_perspective(self, img, pts):
        pts = np.array(pts, dtype=np.float32)
        tl, tr, br, bl = pts
        w = int(max(np.linalg.norm(tr-tl), np.linalg.norm(br-bl)))
        h = int(max(np.linalg.norm(tr-br), np.linalg.norm(tl-bl)))
        dst = np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype=np.float32)
        M = cv2.getPerspectiveTransform(pts, dst)
        return cv2.warpPerspective(img, M, (w, h))

    def correct_and_show(self):
        if self.img is None:
            return
        # 分别校正
        left_correct = self.warp_perspective(self.img, LEFT_POINTS)
        right_correct = self.warp_perspective(self.img, RIGHT_POINTS)

        # 统一高度
        h1, w1 = left_correct.shape[:2]
        h2, w2 = right_correct.shape[:2]
        target_h = max(h1, h2)
        left_correct = cv2.resize(left_correct, (w1, target_h))
        right_correct = cv2.resize(right_correct, (w2, target_h))

        # 左右拼接
        merged = np.hstack([left_correct, right_correct])
        self.show_img(merged)
        cv2.imwrite("correct_result.jpg", merged)
        print("已保存校正结果：correct_result.jpg")

if __name__ == "__main__":
    root = tk.Tk()
    CorrectApp(root)
    root.mainloop()

class CorrectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片平整处理算法")
        self.root.geometry("900x700")

        self.img = None
        self.canvas_w = 880
        self.canvas_h = 600

        # 画布
        self.canvas = tk.Canvas(root, width=self.canvas_w, height=self.canvas_h, bg="#f0f0f0")
        self.canvas.pack(pady=5)

        # 按钮栏
        frame = ttk.Frame(root)
        frame.pack(pady=8)

        ttk.Button(frame, text="打开图片", command=self.open_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="定位关键点", command=self.show_points).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="校正并显示", command=self.correct_and_show).pack(side=tk.LEFT, padx=5)

        self.tk_img = None

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("图片", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not path:
            return
        self.img = cv2.imread(path)
        self.show_img(self.img)

    def show_img(self, img):
        if img is None:
            return
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]
        scale = min(self.canvas_w / w, self.canvas_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img_rgb = cv2.resize(img_rgb, (new_w, new_h))

        self.tk_img = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, image=self.tk_img)

    def show_points(self):
        if self.img is None:
            return
        tmp = self.img.copy()
        # 左点红色
        for pt in LEFT_POINTS:
            cv2.circle(tmp, pt, 5, (0, 0, 255), -1)
        # 右点绿色
        for pt in RIGHT_POINTS:
            cv2.circle(tmp, pt, 5, (0, 255, 0), -1)
        self.show_img(tmp)

    def warp_perspective(self, img, pts):
        pts = np.array(pts, dtype=np.float32)
        tl, tr, br, bl = pts
        w = int(max(np.linalg.norm(tr-tl), np.linalg.norm(br-bl)))
        h = int(max(np.linalg.norm(tr-br), np.linalg.norm(tl-bl)))
        dst = np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype=np.float32)
        M = cv2.getPerspectiveTransform(pts, dst)
        return cv2.warpPerspective(img, M, (w, h))

    def correct_and_show(self):
        if self.img is None:
            return
        # 分别校正
        left_correct = self.warp_perspective(self.img, LEFT_POINTS)
        right_correct = self.warp_perspective(self.img, RIGHT_POINTS)

        # 统一高度
        h1, w1 = left_correct.shape[:2]
        h2, w2 = right_correct.shape[:2]
        target_h = max(h1, h2)
        left_correct = cv2.resize(left_correct, (w1, target_h))
        right_correct = cv2.resize(right_correct, (w2, target_h))

        # 左右拼接
        merged = np.hstack([left_correct, right_correct])
        self.show_img(merged)
        cv2.imwrite("correct_result.jpg", merged)
        print("已保存校正结果：correct_result.jpg")

if __name__ == "__main__":
    root = tk.Tk()
    CorrectApp(root)
    root.mainloop()

