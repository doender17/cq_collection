import cadquery as cq


def two_holes(obj, distance, circle_dia):
    return obj.pushPoints([(distance / 2, 0.0), (-distance / 2, 0.0)]).circle(circle_dia/2).cutThruAll()


def spring_cutout(obj, distance, width, circle_dia):
    obj = obj.faces(">Z").rect(distance, width).cutThruAll()
    obj = two_holes(obj, distance, circle_dia)
    return obj


def slider(length,
           width,
           total_height,
           step_height,
           step_tolerance,
           cutout_length,
           cutout_width,
           cutout_circle_dia,
           mount_holes_length,
           mount_holes_dia,
           adjust_hole_dia,
           adjust_hole_depth):
    bottom = cq.Workplane("XY").box(length, width, total_height - step_height - step_tolerance)
    top = bottom.faces(">Z").box(length, 8.5, step_height + step_tolerance, centered=(True, True, False))
    top = spring_cutout(top, cutout_length, cutout_width, cutout_circle_dia)
    top = two_holes(top, mount_holes_length, mount_holes_dia)
    top = top.faces("<Y").workplane().hole(adjust_hole_dia, adjust_hole_depth)

    spline_points = [
        (-length/2, 5.0),
        (-length/4, 6.0),
        (0.0, 5.5),
        (length/4, 6.0),
        (length/2, 5.0)
    ]

    cut_spline = ((cq.Workplane("XY").
                   moveTo(length/2, 20 + width/2).
                   lineTo(-length/2, 20 + width/2).
                   lineTo(-length/2, 5.0)).
                  spline(spline_points).close().mirrorX().extrude(100, both=True))

    top = top.cut(cut_spline, clean=True)
    top = top.edges("|Z or |Y").fillet(0.5)
    return top


def get_params_for_cs50():
    total_length = 100
    (adjust_hole_dia, adjust_hole_depth) = get_ruthex_h_d_m3()
    (mount_holes_dia, mount_holes_depth) =get_ruthex_h_d_m3()
    p = {
        "length": total_length,
        "width": 12,
        "total_height": 9,
        "step_height": 2,
        "step_tolerance": 0.25,
        "cutout_length": total_length * 0.6,
        "cutout_width": 2,
        "cutout_circle_dia": 4,
        "mount_holes_length": total_length * 0.8,
        "mount_holes_dia": mount_holes_dia,
        "adjust_hole_dia": adjust_hole_dia,
        "adjust_hole_depth": adjust_hole_depth
        }
    return p

def get_params_for_cs50_kumiko():
    total_length = 130
    (adjust_hole_dia, adjust_hole_depth) = get_ruthex_h_d_m3()
    (mount_holes_dia, mount_holes_depth) =get_ruthex_h_d_m5()
    p = {
        "length": total_length,
        "width": 12,
        "total_height": 9,
        "step_height": 2,
        "step_tolerance": 0.25,
        "cutout_length": total_length * 0.5,
        "cutout_width": 2,
        "cutout_circle_dia": 4,
        "mount_holes_length": 90,
        "mount_holes_dia": mount_holes_dia,
        "adjust_hole_dia": adjust_hole_dia,
        "adjust_hole_depth": adjust_hole_depth
        }
    return p

def get_ruthex_h_d_m3():
    height = 5.7
    dia = 4.0
    return dia, height

def get_ruthex_h_d_m5():
    height = 9.5
    dia = 6.4
    return dia, height

def get_ruthex_h_d_m6():
    height = 12.7
    dia = 8
    return dia, height

params = get_params_for_cs50_kumiko()
slider = slider(**params)
# debug(slider)
