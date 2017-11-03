import os
from os.path import isfile, join

import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters
import pygments.styles as styles

import export_as_image as code_image

def main():
    # TODO let this program be executable from the command line
    # TODO make config accessible from outside
    # config
    file_directory = "C:/Users/npeitek/Documents/fmri-td/CodeSnippets/src/com/fmri/topdown/original/words"
    limit_to_files_with_condition = True
    output_separated = False
    create_code_images = True
    output_single = {}
    output_single_name = 'AllFunctionsWords'
    snippet_time = '$TopDownTime'

    # read all files from a directory and loop through them
    only_files = [f for f in os.listdir(file_directory) if isfile(join(file_directory, f))]

    for file_name in only_files:
        if limit_to_files_with_condition:
            # only select files with a condition in their name
            conditions = ['LDBO', 'LDBS', 'LOBO', 'LOBS']
            if any(x in file_name for x in conditions):
                convert_file(file_directory, file_name, output_single, output_separated, snippet_time, create_code_images)
        else:
            convert_file(file_directory, file_name, output_single, output_separated, snippet_time, create_code_images)

    # if configured, write large output file with everything put together
    if not output_separated:
        all_functions = ''
        function_calls = ''

        for key, value in output_single.items():
            all_functions += value + '\n\n'
            function_calls += key + '.present();\n'

        write_presentation_string_to_file(all_functions, output_single_name)
        write_presentation_string_to_file(function_calls, output_single_name + "_pclfile")


def convert_file(file_directory, file_name, output, output_separated, snippet_time, create_code_images = False):
    with open(join(file_directory, file_name)) as text_file:
        code_file = text_file.read()

        # extract Java function from code file
        code_function_start, code_function_string = extract_function_from_file(code_file)

        # get name of the function to specify the Presentation code block
        # TODO figure out unscrambled function name
        function_name_string = code_function_string[len(code_function_start):]
        function_name_position_end = function_name_string.find("(")
        function_name = function_name_string[:function_name_position_end]

        # remove conditions (LDBO, ..) from function name
        # TODO limit it to the function name to prevent bugs
        code_function_string = code_function_string \
            .replace('LDBO', '') \
            .replace('LDBS', '') \
            .replace('LOBO', '') \
            .replace('LOBS', '')

        code_in_html = create_syntax_highlighting_html(code_function_string)

        code_in_presentation = convert_syntax_highlighting_to_presentation(code_in_html)

        if create_code_images:
            code_image.getImage(function_name, code_function_string)

        # Put the code with syntax highlighting in Presentation's variable framework
        full_presentation_string = "#" + function_name + """ 
picture {    
    text { 
        formatted_text = true;
        caption = \"<font color='200,200,200'>          equivalent?</font>
                        
                        
""" + code_in_presentation + """";}; x = $xf; y = $yf;}
code_""" + function_name + "; \n\n" + \
"""
trial {
    trial_duration = '""" + snippet_time + """';
    picture code_""" + function_name + """ ; 
    time = 0 ; 
    duration = '$TopDownTime'; 
    code = \"code_""" + function_name + """\"; 
} """ + function_name + """;"""

        # TODO move all files into an array

        # TODO write entire array into an output file
        if output_separated:
            write_presentation_string_to_file(full_presentation_string, function_name)
        else:
            output[function_name] = full_presentation_string


def extract_function_from_file(code_file):
    # TODO support multiple functions for each file
    code_function_start_lookups = ['public int ', 'public String ', 'public boolean ']

    code_function_start = next((x for x in code_function_start_lookups if x in code_file), False)

    if not code_function_start:
        raise Exception('no function found')

    code_function_position = code_file.find(code_function_start)
    code_function_string = code_file[code_function_position:]
    number_of_open_curly_brackets = 0
    code_function_end = -1
    for i, c in enumerate(code_function_string):
        if (c == "{"):
            number_of_open_curly_brackets += 1

        if (c == "}"):
            number_of_open_curly_brackets -= 1
            if (number_of_open_curly_brackets <= 0):
                code_function_end = i
                break
    code_function_string = code_function_string[:code_function_end + 1]
    return code_function_start, code_function_string


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


def convert_syntax_highlighting_to_presentation(code_in_presentation):
    # TODO handle all other <span> classes (ignore them?)
    # TODO move colors into separate configuration
    code_in_presentation = code_in_presentation.replace("<span></span>", "")
    code_in_presentation = code_in_presentation.replace('<span class="k">', "<font color='0,128,0'>")  # "for"
    code_in_presentation = code_in_presentation.replace('<span class="kc">', "<font color='0,128,0'>")
    code_in_presentation = code_in_presentation.replace('<span class="kd">',
                                                        "<font color='0,0,255'>")  # public, private...
    code_in_presentation = code_in_presentation.replace('<span class="kt">',
                                                        "<font color='67,168,237'>")  # function type (void, ..)
    code_in_presentation = code_in_presentation.replace('<span class="mi">',
                                                        "<font color='85,26,139'>")  # variable declaration value like = 1
    code_in_presentation = code_in_presentation.replace('<span class="n">', "<font color='255,255,255'>")  # neutral
    code_in_presentation = code_in_presentation.replace('<span class="err">', "<font color='255,255,255'>")  # neutral
    code_in_presentation = code_in_presentation.replace('<span class="nf">',
                                                        "<font color='102, 255, 255'>")  # function name
    code_in_presentation = code_in_presentation.replace('<span class="na">',
                                                        "<font color='125,144,41'>")  # variable type
    code_in_presentation = code_in_presentation.replace('String',
                                                        "<font color='125,144,41'>String</font>")  # variable type
    code_in_presentation = code_in_presentation.replace('<span class="o">',
                                                        "<font color='102,102,102'>")  # operator, brackets
    code_in_presentation = code_in_presentation.replace('<span class="s">', "<font color='0,128,0'>")
    code_in_presentation = code_in_presentation.replace('<span class="sc">', "<font color='0,128,0'>")  # literal: char
    code_in_presentation = code_in_presentation.replace('&quot;', '\\"')
    code_in_presentation = code_in_presentation.replace('&#39;', '\'')
    code_in_presentation = code_in_presentation.replace('</span>', '</font>')
    code_in_presentation = code_in_presentation[:-29]
    return code_in_presentation


def write_presentation_string_to_file(full_presentation_string, function_name):
    subdirectory = 'output'
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    with open(join(subdirectory, 'Output_' + function_name + '.txt'), 'w') as output_file:
        print(full_presentation_string, file=output_file)


# Just call main function at the moment
main()
