# Manimを使用して三平方の定理を説明するアニメーションを作成してください。
# 作成したコードを実行しただけでアニメーションが作られる形式である必要があります。
# アニメーションには以下の要素を含めてください：
# 1. 直角三角形の描画
# 2. 各辺の長さの表示
# 3. 各辺の二乗を表す正方形の描画
# 4. a^2 + b^2 = c^2 の数式の表示

from manim import *

if __name__ == "__main__":

    class ThreeSquareTheorem(Scene):
        def construct(self):
            # 直角三角形の描画
            triangle = Polygon(np.array([-3, 0, 0]), np.array([3, 0, 0]), np.array([0, 3, 0]))
            self.play(Create(triangle))

            # 各辺の長さの表示
            a = Line(np.array([-3, 0, 0]), np.array([3, 0, 0]))
            b = Line(np.array([3, 0, 0]), np.array([0, 3, 0]))
            c = Line(np.array([0, 3, 0]), np.array([-3, 0, 0]))
            self.play(Create(a), Create(b), Create(c))

            # 各辺の二乗を表す正方形の描画
            a_square = Square(np.array([-3, 0, 0]), np.array([3, 0, 0]))
            b_square = Square(np.array([3, 0, 0]), np.array([0, 3, 0]))
            c_square = Square(np.array([0, 3, 0]), np.array([-3, 0, 0]))
            self.play(Create(a_square), Create(b_square), Create(c_square))

            # a^2 + b^2 = c^2 の数式の表示
            equation = MathTex(r"a^2 + b^2 = c^2")
            equation.scale(2)
            equation.shift(UP)
            self.play(Write(equation))
