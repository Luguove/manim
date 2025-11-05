"""@file example_scenes.py
@brief Manim 示例场景合集。
@details 本文件展示了多个典型的 Manim 动画场景，帮助快速了解常用接口。
"""

from dataclasses import dataclass

from manimlib import *
import numpy as np

# To watch one of these scenes, run the following: 要观看这些示例场景，请运行：
# manimgl example_scenes.py OpeningManimExample （示例命令）
# Use -s to skip to the end and just save the final frame（使用 -s 参数可跳到结尾并只保存最终帧）
# Use -w to write the animation to a file（使用 -w 参数将动画写入文件）
# Use -o to write it to a file and open it once done（使用 -o 参数输出文件并在结束后自动打开）
# Use -n <number> to skip ahead to the n'th animation of a scene.（使用 -n <number> 参数跳转到第 n 个子动画）


class OpeningManimExample(Scene):
    """@brief 开场 Manim 示例场景，展示线性变换与复平面映射。"""

    def construct(self):
        """@brief 构建演示动画的各个步骤。"""
        intro_words = Text("""
            The original motivation for manim was to
            better illustrate mathematical functions
            as transformations.
        """)
        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)

        # Linear transform
        # 线性变换
        grid = NumberPlane((-10, 10), (-5, 5))
        matrix = [[1, 1], [0, 1]]
        linear_transform_words = VGroup(
            Text("This is what the matrix"),
            IntegerMatrix(matrix),
            Text("looks like")
        )
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_backstroke(width=5)

        self.play(
            ShowCreation(grid),
            FadeTransform(intro_words, linear_transform_words)
        )
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        # Complex map
        # 复映射
        c_grid = ComplexPlane()
        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        complex_map_words = TexText("""
            Or thinking of the plane as $\\mathds{C}$,\\\\
            this is the map $z \\rightarrow z^2$
        """)
        complex_map_words.to_corner(UR)
        complex_map_words.set_backstroke(width=5)

        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeTransform(linear_transform_words, complex_map_words),
        )
        self.wait()
        self.play(
            moving_c_grid.animate.apply_complex_function(lambda z: z**2),
            run_time=6,
        )
        self.wait(2)


class AnimatingMethods(Scene):
    """@brief 演示通过 animate 语法调用 Mobject 方法的场景。"""

    def construct(self):
        """@brief 展示多个通过 animate 调用实现的动画效果。"""
        grid = Tex(R"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # You can animate the application of mobject methods with the ".animate" syntax.
        # 你可以使用 ".animate" 语法将 Mobject 方法的调用制作成动画效果。
        self.play(grid.animate.shift(LEFT))

        # Both animations interpolate from the mobject's initial state to the post-method state; calling grid.shift(LEFT) shifts the grid left by one unit, and self.play animates that motion.
        # 以上动画都会在物体的初始状态与方法调用后的状态之间插值，直接调用 grid.shift(LEFT) 会让网格左移一个单位，而 self.play 则把它变成动画。

        # The same applies for any method, including those setting colors.
        # 这一结论对其他方法同样适用，包括设置颜色的方法。
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary complex functions by treating defining points as complex numbers.
        # Mobject.apply_complex_function 允许将任意复函数作用于对象，并把物体上的点视作复数。
        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # More generally, Mobject.apply_function lets you apply functions from R^3 to R^3.
        # 更一般地，可以使用 Mobject.apply_function，将 R^3 到 R^3 的函数作用于对象。
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()


class TextExample(Scene):
    """@brief 展示 Text 与字体配置差异的示例场景。"""

    def construct(self):
        """@brief 对比 Text 配置并说明字体控制。"""
        # To run this scene properly, ensure the \"Consolas\" font is installed; see https://github.com/3b1b/manim/pull/680 for details.
        # 若要正确播放本场景，请确保系统安装了 \"Consolas\" 字体；更多信息参见 https://github.com/3b1b/manim/pull/680。
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c is a dict that you can choose color for different text
            # t2c 是一个字典，可为不同文本选择颜色。
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


class TexTransformExample(Scene):
    """@brief 演示 Tex 变换与字符串匹配的场景。"""

    def construct(self):
        """@brief 展示不同 Tex 变换组合的效果。"""
        # Tex to color map
        # Tex 字符到颜色的映射表
        t2c = {
            "A": BLUE,
            "B": TEAL,
            "C": GREEN,
        }
        # Configuration to pass along to each Tex mobject
        # 需要传给每个 Tex 对象的统一配置
        kw = dict(font_size=72, t2c=t2c)
        lines = VGroup(
            Tex("A^2 + B^2 = C^2", **kw),
            Tex("A^2 = C^2 - B^2", **kw),
            Tex("A^2 = (C + B)(C - B)", **kw),
            Tex(R"A = \sqrt{(C + B)(C - B)}", **kw),
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)

        self.add(lines[0])
        # The animation TransformMatchingStrings lines up matching substrings, and a small path_arc lets pieces rotate into their final positions—great for equation rearrangements.
        # TransformMatchingStrings 会对齐源和目标中匹配的子串，设置轻微的 path_arc 可让部件旋转到位，表现等式重排。
        self.play(
            TransformMatchingStrings(
                lines[0].copy(), lines[1],
                # matched_keys specifies which substrings should align; otherwise the longest match like "^2 = C^2" would be used.
                # matched_keys 指定需要对齐的子串，避免自动匹配时出现歧义，此例可防止把 "^2 = C^2" 视为最长匹配字符串。
                matched_keys=["A^2", "B^2", "C^2"],
                # When mapping to a different substring on the target, use key_map.
                # 当需要将源字符串中的片段映射到不同目标片段时，可使用 key_map。
                key_map={"+": "-"},
                path_arc=90 * DEG,
            ),
        )
        self.wait()
        self.play(TransformMatchingStrings(
            lines[1].copy(), lines[2],
            matched_keys=["A^2"]
        ))
        self.wait()
        self.play(
            TransformMatchingStrings(
                lines[2].copy(), lines[3],
                key_map={"2": R"\sqrt"},
                path_arc=-30 * DEG,
            ),
        )
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, lines, shift=2 * RIGHT))

        # TransformMatchingShapes matches all submobjects between source and target regardless of their types.
        # TransformMatchingShapes 会尝试匹配源与目标中的所有子对象，并不关心两者的 Mobject 类型是否一致。
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)
        saved_source = source.copy()

        self.play(Write(source))
        self.wait()
        kw = dict(run_time=3, path_arc=PI / 2)
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, saved_source, **kw))
        self.wait()


class TexIndexing(Scene):
    """@brief 演示 Tex 对象的索引与正则匹配。"""

    def construct(self):
        """@brief 展示多种基于索引的 Tex 部分操作。"""
        # You can index into Tex mobject (or other StringMobjects) by substrings
        # 可以通过子串来索引 Tex 对象（或其他字符串对象）。
        equation = Tex(R"e^{\pi i} = -1", font_size=144)

        self.add(equation)
        self.play(FlashAround(equation["e"]))
        self.wait()
        self.play(Indicate(equation[R"\pi"]))
        self.wait()
        self.play(TransformFromCopy(
            equation[R"e^{\pi i}"].copy().set_opacity(0.5),
            equation["-1"],
            path_arc=-PI / 2,
            run_time=3
        ))
        self.play(FadeOut(equation))

        # Or regular expressions
        # 也可以使用正则表达式来索引。
        equation = Tex("A^2 + B^2 = C^2", font_size=144)

        self.play(Write(equation))
        for part in equation[re.compile(r"\w\^2")]:
            self.play(FlashAround(part))
        self.wait()
        self.play(FadeOut(equation))
        
        # Indexing by substrings can fail when LaTeX draws symbols in a different order than they appear; here infinity is drawn before sigma, so the match is missed.
        # 当 LaTeX 绘制符号的顺序与字符串中出现的顺序不一致时，基于子串的索引可能会失败，例如此处无穷符号比西格玛先绘制。
        equation = Tex(R"\sum_{n = 1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}", font_size=72)
        self.play(FadeIn(equation))
        self.play(equation[R"\infty"].animate.set_color(RED))  # Doesn't hit the infinity
        self.wait()
        self.play(FadeOut(equation))

        # Explicitly passing substrings to isolate—and using \over instead of \frac—prevents the issue.
        # 通过在创建时显式传入需要分离的子串，同时对分数使用 \\over 代替 \\frac，可以避免该问题。
        equation = Tex(
            R"\sum_{n = 1}^\infty {1 \over n^2} = {\pi^2 \over 6}",
            # Explicitly mark "\infty" as a substring you might want to access
            # 显式标记可能需要访问的子串 \"\\infty\"
            isolate=[R"\infty"],
            font_size=72
        )
        self.play(FadeIn(equation))
        self.play(equation[R"\infty"].animate.set_color(RED))  # Got it!
        self.wait()
        self.play(FadeOut(equation))


class UpdatersExample(Scene):
    """@brief 演示 updaters 与 always_* 工具的场景。"""

    def construct(self):
        """@brief 展示多种基于更新器的动态更新技巧。"""
        square = Square()
        square.set_fill(BLUE_E, 1)

        # On every frame Brace(square, UP) is rebuilt so the brace stays aligned with the square.
        # 每一帧都会重新调用 Brace(square, UP)，保证括号与方块保持同步。
        brace = always_redraw(Brace, square, UP)

        label = TexText("Width = 0.00")
        number = label.make_number_changeable("0.00")

        # This ensures decimal.next_to(square) is called on every frame.
        # 这样可以确保每一帧都会调用 decimal.next_to(square)。
        label.always.next_to(brace, UP)
        # You could also write the following equivalent line（也可以使用 add_updater 编写等价逻辑）
        # label.add_updater(lambda m: m.next_to(brace, UP))  # 与 add_updater 等价写法

        # When arguments may change, use f_always with callables returning the updated parameters so decimal.set_value runs every frame.
        # 当方法参数本身会变化时，可使用 f_always，并提供返回参数的函数；这样能保证每帧都调用 decimal.set_value(square.get_width)。
        number.f_always.set_value(square.get_width)
        # You could also write the following equivalent line（也可以通过 add_updater 实现相同的效果）
        # number.add_updater(lambda m: m.set_value(square.get_width()))  # 与 add_updater 等价写法

        self.add(square, brace, label)

        # Notice that the brace and label track with the square.
        # 括号和标签会持续跟随方块的尺寸变化。
        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(
            square.animate.set_width(2),
            run_time=3
        )
        self.wait()

        # In general, Mobject.add_updater lets you register a function per frame, receiving the mobject (and optionally elapsed time) each call.
        # 总的来说，可以调用 Mobject.add_updater，并传入每帧执行的函数；函数参数可以是 Mobject 自身，或额外包含上一帧到现在的时间。
        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.sin(self.time - now) + w0)
        )
        self.wait(4 * PI)


class CoordinateSystemExample(Scene):
    """@brief 演示坐标系及坐标转换的场景。"""

    def construct(self):
        """@brief 展示在坐标系中定位、移动点以及辅助线。"""
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1（x 轴范围为 -1 到 10，默认步长为 1）
            x_range=(-1, 10),
            # y-axis ranges from -2 to 2 with a step size of 0.5（y 轴范围为 -2 到 2，步长 0.5）
            y_range=(-2, 2, 0.5),
            # The axes stretch to match the specified height and width.（坐标轴会被缩放以匹配指定的高度和宽度）
            height=6,
            width=10,
            # Axes is made of two NumberLine mobjects; configure them with axis_config.（Axes 由两条 NumberLine 组成，可通过 axis_config 配置细节）
            axis_config=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                numbers_to_exclude=[0],
            ),
            # Alternatively, configure just one axis as shown.（也可以像下面这样仅配置其中一条坐标轴。）
            y_axis_config=dict(
                big_tick_numbers=[-2, 2],
            )
        )
        # Keyword arguments of add_coordinate_labels configure the DecimalNumber mobjects it creates.（add_coordinate_labels 的关键字参数可用于配置生成的 DecimalNumber。）
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        # Axes descends from CoordinateSystem, so axes.coords_to_point（axes.c2p） maps coordinates to points.（Axes 继承自 CoordinateSystem，可通过 coords_to_point（c2p）将坐标映射到平面点。）
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        # Similarly, axes.point_to_coords（axes.p2c）recovers coordinates from a point。print(axes.p2c(dot.get_center()))
        # 同理可调用 point_to_coords（p2c）将点还原为坐标。

        # Draw helper lines from the axes to mark coordinates; always_redraw redraws them each frame.（可以从坐标轴作出辅助线标记点的位置，always_redraw 会在每帧重绘这些线条。）
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        # If the dot is tied to fixed coordinates, moving the axes keeps the dot consistent with that system.（如果将点绑定到特定坐标，移动坐标轴时它会保持与坐标系的相对关系。）
        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(
            axes.animate.scale(0.75).to_corner(UL),
            run_time=2,
        )
        self.wait()
        self.play(FadeOut(VGroup(axes, dot, h_line, v_line)))

        # Other coordinate systems to explore include ThreeDAxes, NumberPlane, and ComplexPlane.（还可以尝试 ThreeDAxes、NumberPlane、ComplexPlane 等其他坐标系。）


class GraphExample(Scene):
    """@brief 演示绘制函数图像与处理不连续点的场景。"""

    def construct(self):
        """@brief 展示多种函数曲线绘制与组合的效果。"""
        axes = Axes((-3, 10), (-1, 8), height=6)
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        # Axes.get_graph 会返回给定函数的曲线。
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        # By default the curve smoothly interpolates sampled points; set use_smoothing=False if you need sharp corners.（默认情况下会平滑连接采样点；若需要出现拐角，可将 use_smoothing 设为 False。）
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        # For discontinuous functions specify the discontinuities so the graph avoids bridging gaps.（对于不连续函数，可以指定间断点以避免跨越间隙绘制。）
        step_graph = axes.get_graph(
            lambda x: 2.0 if x > 3 else 1.0,
            discontinuities=[3],
            color=GREEN,
        )

        # Axes.get_graph_label accepts a string (interpreted as LaTeX) or mobject, places it near the right side, and matches the graph color.（Axes.get_graph_label 接受字符串或 Mobject，字符串按 LaTeX 解析，默认把标签放在右侧并匹配曲线颜色。）
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"), x=4)

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label),
        )
        self.wait()

        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(
            FadeOut(step_graph),
            FadeOut(step_label),
            ShowCreation(parabola)
        )
        self.wait()

        # Use axes.input_to_graph_point（axes.i2gp） to locate points on the graph.（可以使用 axes.input_to_graph_point（i2gp）定位曲线上的点。）
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A ValueTracker animates a parameter so other mobjects can react to it.（ValueTracker 可以驱动参数动画，从而联动其他对象发生更新。）
        x_tracker = ValueTracker(2)
        dot.add_updater(lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), parabola)))

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()


class TexAndNumbersExample(Scene):
    """@brief 演示 Tex 对象与数字的动态联动效果。"""

    def construct(self):
        """@brief 展示圆半径与公式参数绑定的动画流程。"""
        axes = Axes((-3, 3), (-3, 3), unit_size=1)
        axes.to_edge(DOWN)
        axes.add_coordinate_labels(font_size=16)
        circle = Circle(radius=2)
        circle.set_stroke(YELLOW, 3)
        circle.move_to(axes.get_origin())
        self.add(axes, circle)

        # Numbers within Tex can be replaced by DecimalMobjects to enable get_value/set_value and animations like ChangeDecimalToValue.（Tex 中的数字可以替换为 DecimalMobject，以便调用 get_value / set_value 等方法并配合数值动画。）
        tex = Tex("x^2 + y^2 = 4.00")
        tex.next_to(axes, UP, buff=0.5)
        value = tex.make_number_changeable("4.00")


        # This ties the equation's right-hand side to the square of the circle radius.（这样就能把等式右端与圆半径的平方绑定起来。）
        value.add_updater(lambda v: v.set_value(circle.get_radius()**2))
        self.add(tex)

        text = Text("""
            You can manipulate numbers
            in Tex mobjects
        """, font_size=30)
        text.next_to(tex, RIGHT, buff=1.5)
        arrow = Arrow(text, tex)
        self.add(text, arrow)

        self.play(
            circle.animate.set_height(2.0),
            run_time=4,
            rate_func=there_and_back,
        )

        # By default tex.make_number_changeable replaces the first match; replace_all=True updates all matches and returns the group.（默认只替换第一个匹配数字，传入 replace_all=True 可替换全部并返回结果组。）
        exponents = tex.make_number_changeable("2", replace_all=True)
        self.play(
            LaggedStartMap(
                FlashAround, exponents,
                lag_ratio=0.2, buff=0.1, color=RED
            ),
            exponents.animate.set_color(RED)
        )

        def func(x, y):
            # Switch from manim coords to axes coords
            # 将 manim 坐标转换到坐标轴坐标系
            xa, ya = axes.point_to_coords(np.array([x, y, 0]))
            return xa**4 + ya**4 - 4

        new_curve = ImplicitFunction(func)
        new_curve.match_style(circle)
        circle.rotate(angle_of_vector(new_curve.get_start()))  # Align
        value.clear_updaters()

        self.play(
            *(ChangeDecimalToValue(exp, 4) for exp in exponents),
            ReplacementTransform(circle.copy(), new_curve),
            circle.animate.set_stroke(width=1, opacity=0.5),
        )


class SurfaceExample(ThreeDScene):
    """@brief 演示三维曲面、贴图与光照的场景。"""

    def construct(self):
        """@brief 展示三维曲面转换与光源调整的步骤。"""
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)
        # You can texture a surface with up to two images for the light-facing and shadow sides, using URLs or image-directory paths from custom_config.yml.（曲面最多可使用两张贴图，分别代表向光面和背光面，可使用 URL 或自定义图像目录下的本地路径。）

        # day_texture = "EarthTextureMap"  # 示例白天纹理
        # night_texture = "NightEarthTextureMap"  # 示例夜间纹理
        day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            Transform(surface, surfaces[2]),
            # Move camera frame during the transition
            # 在转场过程中移动相机
            self.frame.animate.increment_phi(-10 * DEG),
            self.frame.animate.increment_theta(-20 * DEG),
            run_time=3
        )
        # Add ambient rotation
        # 为相机添加缓慢旋转
        self.frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # Play around with where the light is
        # 试着移动光源位置
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        light_dot = GlowDot(color=WHITE, radius=0.5)
        light_dot.always.move_to(light)
        self.add(light, light_dot)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or f")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()


class InteractiveDevelopment(Scene):
    """@brief 演示交互式开发与 embed 调试流程的场景。"""

    def construct(self):
        """@brief 展示 embed 终端交互与鼠标绑定示例。"""
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()

        # This opens an iPython terminal so you can keep writing lines as if inside construct; 'square', 'circle', and 'self' remain in scope.（这会打开一个 iPython 终端，可像编写 construct 方法一样继续输入，其中 square、circle 与 self 都会在作用域中。）
        self.embed()

        # Try copying and pasting some lines below into the interactive shell.（可以尝试将下面的代码复制到交互式终端执行。）
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate.stretch(4, 0))
        self.play(Rotate(circle, 90 * DEG))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

        text = Text("""
            In general, using the interactive shell
            is very helpful when developing new scenes
        """)
        self.play(Write(text))

        # In the interactive shell, call play/add/remove/clear/wait/save_state/restore without prefixing self.（在交互式终端中，可直接调用 play、add、remove、clear、wait、save_state、restore 等方法。）

        # Type touch() to interact with the window: scroll to pan, hold 'z' to zoom, hold 'd' to adjust perspective, press 'r' to reset, and 'q' to exit back to the shell.（输入 touch() 可与窗口交互：滚轮滚动浏览，按住 z 滚动实现缩放，按住 d 移动鼠标改变视角，按 r 重置视角，按 q 退出交互回到终端。）

        # You can customize scenes to respond to mouse and keyboard interactions.（理论上可以自定义场景以响应鼠标和键盘事件。）
        always(circle.move_to, self.mouse_point)


class ControlsExample(Scene):
    """@brief 演示控件交互与实时文本更新的场景。"""

    drag_to_pan = False

    def setup(self):
        """@brief 初始化文本框、复选框及颜色选择控件。"""
        self.textbox = Textbox()
        self.checkbox = Checkbox()
        self.color_picker = ColorSliders()
        self.panel = ControlPanel(
            Text("Text", font_size=24), self.textbox, Line(),
            Text("Show/Hide Text", font_size=24), self.checkbox, Line(),
            Text("Color of Text", font_size=24), self.color_picker
        )
        self.add(self.panel)

    def construct(self):
        """@brief 通过控件数值驱动文本内容与样式的更新。"""
        text = Text("text", font_size=96)

        def text_updater(old_text):
            assert(isinstance(old_text, Text))
            new_text = Text(self.textbox.get_value(), font_size=old_text.font_size)
            # new_text.align_data_and_family(old_text)  # 若需保持结构一致可取消注释
            new_text.move_to(old_text)
            if self.checkbox.get_value():
                new_text.set_fill(
                    color=self.color_picker.get_picked_color(),
                    opacity=self.color_picker.get_picked_opacity()
                )
            else:
                new_text.set_opacity(0)
            old_text.become(new_text)

        text.add_updater(text_updater)

        self.add(MotionMobject(text))

        self.textbox.set_value("Manim")
        # self.wait(60)  # 保持场景暂停以观察控件
        # self.embed()  # 进入交互式终端


@dataclass
class SpringState:
    """@brief 简单弹簧质点状态容器。"""

    positionM: float
    velocityMps: float

    def integrate(
        self,
        step_s: float,
        spring_stiffness_npm: float,
        damping_ns_per_m: float,
        mass_kg: float,
        position_limit_m: float,
    ) -> None:
        """@brief 使用半显式欧拉法推进弹簧质点。"""
        acceleration_mps2 = (
            -spring_stiffness_npm / mass_kg * self.positionM
            - damping_ns_per_m / mass_kg * self.velocityMps
        )
        self.velocityMps += acceleration_mps2 * step_s
        self.positionM += self.velocityMps * step_s
        self.positionM = np.clip(self.positionM, -position_limit_m, position_limit_m)


class SpringMass(VGroup):
    """@brief 负责将物理状态映射成可视化元素的质点模型。"""

    def __init__(
        self,
        indicator_offset_m: float,
        velocity_scale: float,
        velocity_clip_m: float,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.indicator_offset_m = indicator_offset_m
        self.velocity_scale = velocity_scale
        self.velocity_clip_m = velocity_clip_m

        self.body = Dot(radius=0.12, color=YELLOW)
        self.velocity_indicator = Arrow(
            ORIGIN,
            RIGHT * velocity_clip_m,
            buff=0,
            color=YELLOW,
            stroke_width=6,
        )
        self.add(self.body, self.velocity_indicator)

    def update_from_state(self, axis: NumberLine, state: SpringState) -> None:
        center = axis.n2p(state.positionM)
        self.body.move_to(center)

        arrow_start = center + UP * self.indicator_offset_m
        velocity_length_m = np.clip(
            state.velocityMps * self.velocity_scale,
            -self.velocity_clip_m,
            self.velocity_clip_m,
        )
        arrow_end = arrow_start + RIGHT * velocity_length_m
        self.velocity_indicator.put_start_and_end_on(arrow_start, arrow_end)


class PhysicsDrivenSpring(Scene):
    """@brief 展示如何将外部物理状态驱动 Manim 动画。"""

    SpringStiffnessNpm: float = 3.0
    DampingNsPerM: float = 0.8
    MassKg: float = 1.0
    InitialDisplacementM: float = 2.0
    InitialVelocityMps: float = 0.0
    PositionLimitM: float = 3.5
    VelocityIndicatorOffsetM: float = 0.6
    VelocityScale: float = 0.4
    VelocityClipM: float = 1.5
    TimeStepClampS: float = 1 / 60
    SimulationDurationS: float = 8.0

    def construct(self) -> None:
        """@brief 构建最小可运行的物理驱动画面。"""
        axis = NumberLine(x_range=(-4, 4, 1), length=8)
        axis.shift(DOWN * 1.5)

        state = SpringState(
            positionM=self.InitialDisplacementM,
            velocityMps=self.InitialVelocityMps,
        )

        spring = Line(axis.n2p(0.0), axis.n2p(state.positionM), color=BLUE)
        mass = SpringMass(
            indicator_offset_m=self.VelocityIndicatorOffsetM,
            velocity_scale=self.VelocityScale,
            velocity_clip_m=self.VelocityClipM,
        )
        mass.update_from_state(axis, state)

        position_label = Text("Position (m)", font_size=28)
        position_value = DecimalNumber(state.positionM, num_decimal_places=2)
        velocity_label = Text("Velocity (m/s)", font_size=28)
        velocity_value = DecimalNumber(state.velocityMps, num_decimal_places=2)
        panel = VGroup(
            VGroup(position_label, position_value).arrange(RIGHT, buff=0.3),
            VGroup(velocity_label, velocity_value).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.to_corner(UR).set_backstroke(width=4)

        def advance_state(dt: float) -> None:
            remaining = max(dt, 0)
            while remaining > 1e-6:
                step = min(self.TimeStepClampS, remaining)
                state.integrate(
                    step,
                    self.SpringStiffnessNpm,
                    self.DampingNsPerM,
                    self.MassKg,
                    self.PositionLimitM,
                )
                remaining -= step

        def update_spring(_: Mobject, dt: float) -> None:
            if dt > 0:
                advance_state(dt)
            spring.put_start_and_end_on(axis.n2p(0.0), axis.n2p(state.positionM))
            mass.update_from_state(axis, state)
            position_value.set_value(state.positionM)
            velocity_value.set_value(state.velocityMps)

        spring.add_updater(update_spring)

        self.add(axis, spring, mass, panel)
        self.wait(self.SimulationDurationS)
        spring.clear_updaters()


# See https://github.com/3b1b/videos for many, many more（更多示例参见此仓库）
