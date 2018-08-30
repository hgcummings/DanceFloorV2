import json
import io
import os

font_height = 0
font_alpha = {}

def height():
    return font_height

def alpha():
    return font_alpha

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'seven-plus.json')) as data_file:
    font_data = json.load(data_file)
    for name, data in font_data['glyphs'].iteritems():
        pixels = []
        pixels.extend([[0 for i in range(0, len(data['pixels'][0]))] for j in range(0, data['offset'])])
        pixels.extend(data['pixels'])
        font_alpha[name] = pixels
        font_height = max(font_height, len(pixels))

    for glyph in font_alpha.itervalues():
        glyph.extend([[0 for i in range(0, len(glyph[0]))] for j in range(len(glyph), font_height)])