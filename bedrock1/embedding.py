import os
from pathlib import Path


def load_documents_from_folder(path):
    # List to store loaded documents
    documents = []

    # Process all files in the folder
    for filename in os.listdir(path):
        filepath = Path(os.path.join(path, filename))
        # Only process files, not directories
        if filepath.is_file():
            try:
                # Open and read the file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                # Only add non-empty documents
                if content:
                    documents.append({
                        "key": filepath.stem,          # Use filename without extension as key
                        "content": content,             # File content
                        "metadata": {
                            "filename": filepath.name  # Store filename as metadata
                        }
                    })

            except Exception as e:
                print(f"Error loading {filepath.name}: {e}")

    return documents
