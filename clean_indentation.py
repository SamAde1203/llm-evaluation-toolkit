import os

def clean_file_indentation(filepath):
    """Replace tabs with 4 spaces in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace tabs with 4 spaces
    cleaned = content.replace('\t', '    ')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"Cleaned: {filepath}")

# Clean the evaluator.py file
clean_file_indentation('src/datasets.py')