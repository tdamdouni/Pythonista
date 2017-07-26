# https://github.com/dyyybek/pythonista

from ui import Path
from pathsLists import l

def make_glyph(glyphs):
    tempPath = None
    for paths in glyphs:
        path = Path()
        for segment in paths:
            if len(segment) == 4:
                start_x = segment[0][0]
                start_y = segment[0][1]
                cp1_x = segment[1][0]
                cp1_y = segment[1][1]
                cp2_x = segment[2][0]
                cp2_y = segment[2][1]
                end_x = segment[3][0]
                end_y = segment[3][1]
                if path.bounds.height == 0 and path.bounds.width == 0:
                    path.move_to(start_x, start_y)
                    path.add_curve(end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y)
                else:
                    path.add_curve(end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y)
            elif len(segment) == 2:
                start_x = segment[0][0]
                start_y = segment[0][1]
                end_x = segment[1][0]
                end_y = segment[1][1]
                if path.bounds.height == 0 and path.bounds.width == 0:
                    path.move_to(start_x, start_y)
                    path.line_to(end_x, end_y)
                else:
                    path.line_to(end_x, end_y)
        if tempPath:
            tempPath.append_path(path)
        else:
            tempPath = path
    return tempPath


def glyphsListConstruct(list_of_glyphs=l):
    return [make_glyph(glyphs) for glyphs in list_of_glyphs]
