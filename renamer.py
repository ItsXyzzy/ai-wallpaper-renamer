import os
from pathlib import Path
import re
import argparse
import ollama

def sanitize_filename(text):
    # Convert to lowercase
    text = text.lower().strip()
    # Remove everything except alphanumeric characters, spaces, and hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces and multiple hyphens with a single hyphen
    text = re.sub(r'[-\s]+', '-', text)
    # Strip leading/trailing hyphens
    return text.strip('-')

def rename_wallpapers(folder_path, model_name, dry_run=False):
    folder = Path(folder_path)
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}

    if not folder.exists() or not folder.is_dir():
        print(f"Error: Folder '{folder_path}' does not exist or is not a directory.")
        return

    print(f"\nScanning folder: {folder.resolve()}")
    print(f"Using Ollama model: {model_name}")
    if dry_run:
        print("--- DRY RUN MODE ENABLED (No files will be modified) ---\n")

    for img_path in folder.iterdir():
        if img_path.suffix.lower() in valid_extensions:
            print(f"Analyzing {img_path.name}...")
            try:
                # Use a clear prompt and limit output generation using num_predict
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are a filename generator. Output only 2 to 4 descriptive keywords separated by spaces. Do not write sentences or descriptions.'
                        },
                        {
                            'role': 'user',
                            'content': 'Provide 2 to 4 keywords for this image:',
                            'images': [str(img_path)]
                        }
                    ],
                    options={
                        'num_predict': 12,   # Stop generating early to force short responses
                        'temperature': 0.2,  # Reduce creative rambling
                    }
                )

                raw_description = response['message']['content']

                # Extract only the first 3 words to guarantee short names
                words = raw_description.strip().split()[:3]
                joined_words = ' '.join(words)
                
                slug = sanitize_filename(joined_words)

                # Fallback if the model returned something empty
                if not slug:
                    print(f"Skipping {img_path.name}: Generated name was empty.")
                    continue

                new_name = f"{slug}{img_path.suffix.lower()}"
                new_path = folder / new_name

                # Skip renaming if the filename is already correct
                if img_path == new_path:
                    print(f"Skipping {img_path.name}: Name already matches.\n")
                    continue

                # Prevent overwriting existing files with duplicate names
                counter = 1
                while new_path.exists():
                    new_name = f"{slug}-{counter}{img_path.suffix.lower()}"
                    new_path = folder / new_name
                    counter += 1

                if dry_run:
                    print(f"[DRY RUN] Would rename: {img_path.name} -> {new_name}\n")
                else:
                    print(f"Renaming: {img_path.name} -> {new_name}\n")
                    img_path.rename(new_path)

            except Exception as e:
                print(f"Error processing {img_path.name}: {e}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-rename wallpapers using local Ollama vision models.")
    parser.add_argument("-p", "--path", type=str, required=True, help="Path to the wallpaper folder")
    parser.add_argument("-m", "--model", type=str, default="llava-phi3", help="Ollama vision model name (default: llava-phi3)")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Preview changes without actually renaming files")

    args = parser.parse_args()
    rename_wallpapers(args.path, args.model, args.dry_run)