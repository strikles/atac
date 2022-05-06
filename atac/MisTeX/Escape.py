import re

# Pattern for escaping to raw latex
# We match for any text between ^^^, lazily
PATTERN = re.compile(
    r"\^\^\^([\s\S]*?)\^\^\^"
)

# define how to parse matc
def parse(md_block, match, state):
    # Extract content from match
    text = match.group(1)
    # Tell mistune this is raw text and doesn't need
    # to be processed further.
    return {'type': 'escape', 'raw': text}

# Rendered output is just the input
def render(text):
    return text

def escape(md):
    # Register as a block rule 
    md.block.register_rule('escape', PATTERN, parse)

    # Add to active rules
    md.block.rules.append('escape')
    
    # Tell our renderer how to render it
    md.renderer.register('escape', render)