import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def parse_markdown(markdown):
    """
    Converts markdown to HTML, supporting:
    ...headings, boldface text, unordered lists, links, and paragraphs. 
    """
    if markdown == None:
        return None

    # print('TOdo')
    # print(f"{markdown}")
    # # if ('\n' in markdown):
    # #     print(f"{markdown}")
    markdown_array = markdown.splitlines()
    # print(markdown_array)
    html = []
    h1 = re.compile('^#{1}')
    h2 = re.compile('^#{2}')
    h3 = re.compile('^#{3}')
    # match headings and paragraphs
    for string in markdown_array:
        if (string != ''):
            new_string = ''
            # html.append('<h1>' + string[1:] + '</h1>')
            if len(re.findall(h2, string)) > 0:     
                new_string = h2.sub('<h2>', string, count=1) + '</h2>'
                html.append(new_string)
            elif len(re.findall(h1, string)) > 0:
                new_string = h1.sub('<h1>', string, count=1) + '</h1>'
                html.append(new_string)
            else:
                html.append('<p>' + string + '</p>')
    print(html)
    # match boldface
    bold = re.compile('(\\*{2}[^-\s].*[^-\s]\\*{2}){1}')
    # bold = re.compile('.\\*{2}[^.](.*)[^.]\\*{2}')
    mysplit = re.compile('\\*{2}')
    for item in html:
        print(item)
        result = bold.findall(item)
        result2 = mysplit.sub('bold', item)
        print(result)
        print(result2)
    

    # print(html)
    # re.findall("^#")
    # x = re.findall("#", markdown)
    # print(x)
    # p = re.compile('^[**].[**]$')
    # print(p)

    # h1 = re.compile('^#{1}')
    # h2 = re.compile('^#{2}')
    # h3 = re.compile('^#{3}')

    # markdown = h1.sub('<h1>', markdown, count=1)
    # markdown = h2.sub('<h2>', markdown, count=1)
    # print('xx')
    # print(markdown)


