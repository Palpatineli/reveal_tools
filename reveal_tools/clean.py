## pylint: disable=C0103
"""for a revealjs slide show, remove figures from figure folder that is not included in the markdown file"""
from os import chdir, remove, listdir
from os.path import join, split, splitext, isdir, isfile
import subprocess
from html.parser import HTMLParser
import json
from uifunc import FolderSelector

def swap_ext(in_data: str, ext: str) -> str:
    return splitext(in_data)[0] + '.' + ext


class HTMLImageParser(HTMLParser):
    figs = list()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.figs.extend([splitext(split(value)[-1])[0] for key, value in attrs if key == 'src'])

    def reset(self):
        self.figs.clear()
        return super(HTMLImageParser, self).reset()


parser = HTMLImageParser()


def html_figure(content):
    parser.reset()
    parser.feed(content)
    return parser.figs

def find_figure_walk(root):
    """find reference to figures in pandoc ast file"""
    fig_list = list()
    for item in root:
        if isinstance(item, dict) and 't'in item:
            if item['t'] == 'Image':
                fig_list.append(splitext(split(item['c'][-1][0])[-1])[0])
            elif 'c' in item:
                content = item['c']
                if isinstance(content, list):
                    if content[0] == 'html':
                        fig_list.extend(html_figure(content[1]))
                    else:
                        fig_list.extend(find_figure_walk(content))
        elif isinstance(item, list):
            fig_list.extend(find_figure_walk(item))
    return fig_list

def delete_unreferenced_figs(project_folder: str):
    """delete unreferenced figures in, assuming they are in 'img' or 'fig' folders and the markdown file is 'text.txt'
    under root"""
    txt_file = join(project_folder, 'text.txt')
    temp_file = swap_ext(txt_file, 'ast')
    subprocess.run(['pandoc', '-t', 'json', txt_file, '-o', temp_file])
    ast = json.load(open(temp_file))
    fig_list = find_figure_walk(ast['blocks'])
    chdir(project_folder)
    for fig_folder_name in ('fig', 'img'):
        if isdir(join(project_folder, fig_folder_name)):
            existing_fig_list = [x for x in listdir(join(project_folder, fig_folder_name))
                                 if isfile(join(fig_folder_name, x))]
            for fig_file in existing_fig_list:
                if not splitext(fig_file)[0] in fig_list:
                    print('removing {0}'.format(fig_file))
                    remove(join(project_folder, fig_folder_name, fig_file))
    remove(temp_file)
    print('removed')

##
def clean():
    FolderSelector(delete_unreferenced_figs)()
##
