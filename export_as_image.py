import PIL
from PIL import Image, ImageDraw, ImageFont

import html

import os
from os.path import join

import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters
import pygments.styles as styles

FONT_COLOR_INSTRUCTION = (200, 200, 200)


def main():
    code = """
public boolean containsSubstring(String word, String substring) {
    for (int i = 0; i < word.length(); i++) {
        for (int j = 0; j < substring.length(); j++) {
            if (i + j >= word.length())
                break;
            if (word.charAt(i + j) != substring.charAt(j)) {
                break;
            } else {
                if (j == substring.length() - 1) {
                    return true;
                }
            }
        }
    }

    return false;
}
"""
    getImage("test123", code)


def getImage(function_name, code, code_task):
    print("creating image for " + function_name)
    fullSizeX = 1280 #1920
    fullSizeY = 1024 #1080
    image = Image.new("RGBA", (fullSizeX, fullSizeY), (0,0,0))
    draw = ImageDraw.Draw(image)

    inconsolata = ImageFont.truetype("resources/Inconsolata-Regular.ttf", 32)

    # draw instructions for code task
    (instruction_width, instruction_height) = ImageDraw.ImageDraw(image).textsize(text=code_task, font=inconsolata)
    draw.text((fullSizeX/2 - instruction_width/2, (fullSizeY / 20)), code_task, FONT_COLOR_INSTRUCTION, font=inconsolata)

    # draw code
    code_in_html = create_syntax_highlighting_html(code)
    code_in_html = html.unescape(code_in_html)
    code_in_html = code_in_html.replace('\t', '    ')
    code_in_html = code_in_html.replace("<span></span>", "")

    (allTextSizeX, allTextSizeY) = ImageDraw.ImageDraw(image).multiline_textsize(text=code, font=inconsolata)
    allTextSizeY *= 1.4 #for additional vertical padding, otherwise the text is too hard to read

    xPosStart = (fullSizeX/2) - (allTextSizeX/2)
    yPos = (fullSizeY/2) - (allTextSizeY/2)
    (nil, verticalPadding) = ImageDraw.ImageDraw(image).textsize(text="blubb", font=inconsolata)

    code_in_html_lines = code_in_html.split("\n")

    for code_line in code_in_html_lines:
        if code_line == "</pre></div>":
            break

        # remove four first characters from each line to offset the incorrect indentation
        if code_line.startswith('    '):
            code_line = code_line[4:]

        code_elements = code_line.split("<span")

        xPos = xPosStart
        yPos += (verticalPadding * 1.4)

        for element in code_elements:
            element = element.replace("</span>", "")
            endPos = element.find('>')

            span_class = ''

            if endPos != -1:
                span_class = element[8:endPos-1]
                element = element[endPos+1:]

            draw.text((xPos, yPos), element, get_color_for_span_class(span_class), font=inconsolata)
            (sizeX, sizeY) = ImageDraw.ImageDraw(image).textsize(text=element, font=inconsolata)
            xPos += sizeX

    write_image_to_file(function_name, image)


def write_image_to_file(file_name, image):
    subdirectory = 'output_images'
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass

    #image.thumbnail((1280, 1024), PIL.Image.ANTIALIAS)
    #image.save(join(subdirectory, file_name + '_resized.png'), "PNG")
    image.save(join(subdirectory, file_name + '.png'), "PNG")


def get_color_for_span_class(span_class):
    return {
        'kc': (0,128,0),
        'kd': (0,0,255),
        'k': (0,128,64),
        'kt': (67,168,237),
        'mi': (85,26,139),
        'nf': (102, 255, 255),
        'na': (125,144,41),
        'String': (125,144,41),
        'o': (102,102,102),
        's': (0,128,0),
        'sc': (0,128,0),
        'n': (255,255,255),
        'err': (255,255,255),
    }.get(span_class, (255,255,255))


def create_syntax_highlighting_html(code_function_string):
    # Create Pygments formatter (http://pygments.org/)
    formatter = formatters.get_formatter_by_name("html")
    formatter.full = True
    formatter.style = styles.get_style_by_name("manni")
    lexer = lexers.get_lexer_by_name('Java')
    # Use pygments to create code with syntax highlighting in HTML
    code_in_html = pygments.highlight(code_function_string, lexer, formatter)
    # Convert syntax highlighting from HTML to the Presentation-format
    code_in_presentation = code_in_html
    pos = code_in_html.find("<pre>")
    code_in_presentation = code_in_presentation.replace(code_in_presentation[:pos + 5], '')
    return code_in_presentation
