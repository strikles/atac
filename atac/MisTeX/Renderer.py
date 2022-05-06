import mistune
from mistune.util import escape, escape_html

# A LaTeX renderer for mistune
class Renderer(mistune.renderers.HTMLRenderer):
    name = "LaTeX"

    '''
    Inline Level
    '''
    def image(self, src, alt="", title=None):
        return "\\includegraphics[" + alt + "]{" + src + "}\n"

    def codespan(self, text):
        return "\\mintinline{text}{" + text + "}"

    def newline(self):
        return ''
     
    def text(self, text):
        return text

    def emphasis(self, text):
        return '\\emph{' + text + '}'

    def strong(self, text):
        return '\\textbf{' + text + '}'

    '''
    # Looks for HTML tags specifically, not really
    # what we're looking for
    def inline_html(self, html):
        raise NotImplementedError()
    
    
    # What does a link even mean in the context of
    # a latex document.
    def link(self, link, text=None, title=None):
        raise NotImplementedError()
   
    def linebreak(self):
        raise NotImplementedError()
    '''
    
    '''
    Block Level
    '''
    def paragraph(self, text):
        return text + "\par\n"
   
    def block_code(self, code, info=None):
        return '\\begin{minted}{' + info + '}\n' + code + '\\end{minted}\n'

    def heading(self, text, level):
        heading_types = ['section', 'subsection', 'subsubsection']
        return "\\" + heading_types[level-1] + "{" + text + "}\n"
    
    def thematic_break(self):
        return "\\noindent\\rule{\\textwidth}{1pt}\n"

    def block_text(self, text):
        return text + "\n"
    
    def block_quote(self, text):
        return "\\begin{quote}\n" + text + "\\end{quote}\n"
    
    def list(self, text, ordered, level, start=None):
        if not ordered:
            return "\\begin{itemize}\n" + text + "\\end{itemize}\n"
        else: 
            return "\\begin{enumerate}\n" + text + "\\end{enumerate}\n"
    
    def list_item(self, text, level):
        return "\\item " + text

    '''
    # Again, we can't really make use of this
    def block_html(self, html):
        raise NotImplementedError()

    # This too
    def block_error(self, html):
        raise NotImplementedError()

    def finalize(self, data):
        raise NotImplementedError()
    '''