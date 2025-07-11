import re
import argparse
from pathlib import Path
import yaml
import markdown2
import frontmatter

def convert_quarto_to_substack(quarto_file):
    """Convert a Quarto markdown file to Substack-compatible HTML"""
    
    # Read the Quarto file
    post = frontmatter.load(quarto_file)
    
    # Extract YAML metadata
    metadata = post.metadata
    content = post.content
    
    # Convert Quarto-specific syntax to standard markdown
    # Replace ```{python} with ```python etc
    content = re.sub(r'```{(\w+)}', r'```\1', content)
    
    # Ensure attribution is present
    attribution = "\n\n---\n\n*First published on [finance-with-ai.org](https://finance-with-ai.org)*"
    if attribution not in content:
        content = content + attribution
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        content,
        extras=['fenced-code-blocks', 'tables', 'metadata']
    )
    
    # Add metadata as HTML comments for reference
    metadata_html = f"""
    <!--
    title: {metadata.get('title', '')}
    description: {metadata.get('description', '')}
    date: {metadata.get('date', '')}
    -->
    """
    
    return metadata_html + html_content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Path to Quarto .qmd file')
    parser.add_argument('--output', help='Output HTML file path')
    args = parser.parse_args()
    
    html_content = convert_quarto_to_substack(args.input_file)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(html_content)
    else:
        print(html_content)

if __name__ == '__main__':
    main() 