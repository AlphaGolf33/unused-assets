# unused-assets

A tool for finding unused assets in your project

## Requirements

`python > 3.6`

## Usage

```
unused_assets.py [-h] [-p PATH] [-s SRC_DIR] [-a ASSETS_DIR] [-e EXTENSIONS [EXTENSIONS ...]]

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the project. Default to current directory
  -s SRC_DIR, --src-dir SRC_DIR
                        Source directory. Default to "<root-dir>/src"
  -a ASSETS_DIR, --assets-dir ASSETS_DIR
                        Assets directory. Default to "<root-dir>/assets"
  -e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        Extensions to analyse. Default is js, jsx, ts, tsx
```
