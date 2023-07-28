from manim import *
import numpy as np


def getCirclesAndLines(c, idx, t, stroke, scale):
    n = int((len(c) - 1) / 2)
    start_stroke = stroke[0]
    end_stroke = stroke[1]

    c = c * np.exp(idx * 2 * np.pi * t * 1j)

    lines = [
        Line(
            start=ORIGIN,
            end=[c[n].real * scale, c[n].imag * scale, 0],
            stroke_width=start_stroke * 0.75,
            stroke_opacity=0.75,
            stroke_color=RED,
        )
    ]

    c_now = c[n].copy()

    circles = [
        Circle(
            np.abs(c[n]),
            arc_center=ORIGIN,
            stroke_width=start_stroke * 0.75,
            stroke_opacity=0.75,
            stroke_color=YELLOW,
        )
    ]

    for i in range(1, n + 1):
        st_ = np.array([c_now.real * scale, c_now.imag * scale, 0])
        en_ = np.array(
            [
                c_now.real * scale + c[n + i].real * scale,
                c_now.imag * scale + c[n + i].imag * scale,
                0,
            ]
        )

        lines.append(
            Line(
                start=st_,
                end=en_,
                stroke_width=max(start_stroke * 2 / (i + 1), end_stroke),
                stroke_opacity=0.75,
                stroke_color=RED,
            )
        )

        circles.append(
            Circle(
                np.linalg.norm(en_ - st_),
                arc_center=st_,
                stroke_width=max(start_stroke / (i + 1), end_stroke),
                stroke_opacity=0.75,
                stroke_color=YELLOW,
            )
        )

        c_now += c[n + i]

        # print(c_now)

        st_ = np.array([c_now.real * scale, c_now.imag * scale, 0])
        en_ = np.array(
            [
                c_now.real * scale + c[n - i].real * scale,
                c_now.imag * scale + c[n - i].imag * scale,
                0,
            ]
        )

        lines.append(
            Line(
                start=st_,
                end=en_,
                stroke_width=max(start_stroke * 2 / (i + 1), end_stroke),
                stroke_opacity=0.75,
                stroke_color=RED,
            )
        )

        circles.append(
            Circle(
                np.linalg.norm(en_ - st_),
                arc_center=st_,
                stroke_width=max(start_stroke / (i + 1), end_stroke),
                stroke_opacity=0.75,
                stroke_color=YELLOW,
            )
        )

        c_now += c[n - i]

    return lines, circles


class FourierCircles(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.1,
            zoomed_display_height=5,
            zoomed_display_width=4,
            image_frame_stroke_width=5,
            zoomed_camera_config={
                "default_frame_stroke_width": 1,
            },
            **kwargs
        )

    def construct(self):
        data = np.loadtxt("fourierCoefficients.txt")

        data[0, :] = data[0, :]
        data[1, :] = data[1, :]

        c_ = data[0, :] + 1j * data[1, :]
        c = data[0, :] + 1j * data[1, :]

        scale = 1.0

        n = int((len(c) - 1) / 2)

        arrows = []

        idx = np.array(range(-n, n + 1))

        t = Variable(0.0, label="t")

        end_time = 1.0
        run_time = 180

        start_stroke = DEFAULT_STROKE_WIDTH / 2
        end_stroke = DEFAULT_STROKE_WIDTH / 50

        prev_time = t.tracker.get_value()

        def linesAndCirclesUpdater(l):
            c = data[0, :] + 1j * data[1, :]

            lines, circles = getCirclesAndLines(
                c, idx, t.tracker.get_value(), [start_stroke, end_stroke], scale
            )

            l.become(VGroup(*lines) + VGroup(*circles))

            # print(c_now)

        lines, circles = getCirclesAndLines(
            c, idx, t.tracker.get_value(), [start_stroke, end_stroke], scale
        )

        val = 0.0
        for id in idx:
            val += c_[id + n] * np.exp(id * 2 * np.pi * t.tracker.get_value() * 1j)

        path_stroke = DEFAULT_STROKE_WIDTH / 3

        def pathsUpdater(p):
            nonlocal prev_time

            c = data[0, :] + 1j * data[1, :]
            c = c * np.exp(idx * 2 * np.pi * prev_time * 1j)

            prevval = sum(c)

            c = data[0, :] + 1j * data[1, :]
            c = c * np.exp(idx * 2 * np.pi * t.tracker.get_value() * 1j)

            nextval = sum(c)

            prev_time = t.tracker.get_value()

            p.become(
                p
                + VGroup(
                    Line(
                        [prevval.real, prevval.imag, 0],
                        [nextval.real, nextval.imag, 0],
                        stroke_width=path_stroke,
                    )
                )
            )

        path = Line(
            [val.real, val.imag, 0],
            [val.real, val.imag, 0],
            stroke_width=path_stroke,
        )

        paths = VGroup(path)
        linesGroup = VGroup(*lines)
        circleGroup = VGroup(*circles)

        linesAndCirclesGroup = linesGroup + circleGroup

        linesAndCirclesGroup.add_updater(linesAndCirclesUpdater)
        paths.add_updater(pathsUpdater)

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(circles[-1])
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(
            zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF
        )
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(
            zd_rect, lambda rect: rect.replace(zoomed_display)
        )

        def frameUpdater(f):
            c = data[0, :] + 1j * data[1, :]
            c = c * np.exp(idx * 2 * np.pi * t.tracker.get_value() * 1j)

            nextval = sum(c)

            f.move_to([nextval.real, nextval.imag, 0])

        frame.add_updater(frameUpdater)

        # self.play(t.tracker.animate.set_value(0.0))

        # dotDebug = Dot([-0.9693065420728197, 0.0, 0.0])

        self.play(Create(frame))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)

        self.play(
            Create(linesGroup),
            run_time=7.5,
            # rate_func=rate_functions.ease_in_expo,
        )

        self.play(
            Create(circleGroup),
            run_time=7.5,
            # rate_func=rate_functions.ease_in_expo,
        )

        self.add(linesAndCirclesGroup)

        self.play(Create(paths))

        self.wait(2)

        self.play(t.tracker.animate.set_value(end_time), run_time=run_time)

        self.wait(10)
