import math

from helpers.setup import *
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def plot_poly(ax, p, color):
    pts = p.points
    if len(pts) == 0:
        return

    xss = []
    yss = []
    arcs = []
    xs = [pts[0].x.value]
    ys = [pts[0].y.value]

    i = 1
    while i < len(pts):
        if pts[i].is_arc:
            if len(xs) > 1:
                # flush current line segment
                xss.append(xs)
                yss.append(ys)
            xs = []
            ys = []

            start = pts[i - 1]
            end = pts[(i + 1) % len(pts)]
            arc = ArcData(start, end, height=pts[i].arc_height.value)
            center = arc.center
            center_pt = [center.x.value, center.y.value]
            theta1 = math.atan2((start - center).y.value, (start - center).x.value)
            theta2 = math.atan2((end - center).y.value, (end - center).x.value)
            diameter = arc.radius * 2
            arcs.append(
                mpatches.Arc(
                    center_pt,
                    height=diameter,
                    width=diameter,
                    theta1=math.degrees(theta1),
                    theta2=math.degrees(theta2),
                    color=color,
                    lw=1.5,
                )
            )
        else:
            xs.append(pts[i].x.value)
            ys.append(pts[i].y.value)
        i += 1

    if not pts[-1].is_arc:
        # close the loop
        xs.append(pts[0].x.value)
        ys.append(pts[0].y.value)

    if len(xs) > 0:
        xss.append(xs)
        yss.append(ys)

    for a in arcs:
        ax.add_patch(a)

    for i in range(0, len(xss)):
        ax.plot(xss[i], yss[i], color=color)


def plot_polys(ax, ps, title):
    try:
        if len(ps) == 0:
            return
    except TypeError:
        ps = [p]

    ax.set_title(title)

    # plot contours
    for p in ps:
        plot_poly(ax, p, color="tab:blue")

    # plot holes
    holes = [h for p in ps for h in p.holes]
    for h in holes:
        plot_poly(ax, h, color="tab:orange")
