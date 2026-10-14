# AI Wallpaper Renamer

A local, privacy-focused command-line tool that uses local Ollama vision models (like `llava-phi3`) to automatically scan, analyze, and rename your wallpapers into clean, descriptive slugs.

## Features

- **100% Local & Private:** Runs entirely on your machine via Ollama. No images are sent to the cloud.
- **Customizable Vision Models:** Choose any vision-capable model you have installed.
- **Smart Formatting:** Sanitizes descriptions into short, lowercase, hyphen-separated filenames.
- **Dry-Run Support:** Preview your new filenames safely before applying any changes to disk.
- **Collision Handling:** Automatically appends counters if two wallpapers generate the same name.

---

## Prerequisites

Make sure Ollama is installed and running on your system
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Then download a lightweight vision model (I used llava):
    
```bash
ollama pull llava-phi3
```

Clone this repository or save the script, then install the official Ollama Python package:
```bash
pip install ollama
```

---

## Usage

Run the script from your terminal by providing the path to your wallpaper folder using the `-p` flag.

### 1. Preview Changes (Dry-Run Mode)
It is recommended to test your folder first without modifying any files:

```bash
python rename_wallpapers.py -p ~/Pictures/Wallpapers --dry-run
```

### 2. Run the Renamer
Execute the batch-rename operation across your wallpaper directory:

```bash
python rename_wallpapers.py -p ~/Pictures/Wallpapers
```

### 3. Use a Different Vision Model
You can specify a different Ollama vision model using the `-m` flag:
```bash
python rename_wallpapers.py -p ~/Pictures/Wallpapers -m llama3.2-vision
```

---

## Command-Line Options

| Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-p` | `--path` | Path to the wallpaper directory (**Required**) | `None` |
| `-m` | `--model` | Ollama vision model name | `llava-phi3` |
| `-d` | `--dry-run` | Preview changes without renaming files | `False` |
| `-h` | `--help` | Show the help message and exit | `None` |
