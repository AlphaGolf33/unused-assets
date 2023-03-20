#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
import sys
from glob import glob


def flatten(t):
    return [item for sublist in t for item in sublist]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="Path to the project. Default to current directory")
    parser.add_argument("-s", "--src-dir",
                        help="Source directory. Default to \"<root-dir>/src\"")
    parser.add_argument(
        "-a", "--assets-dir", help="Assets directory. Default to \"<root-dir>/assets\"")
    parser.add_argument("-e", "--extensions", nargs="+",
                        help="Extensions to analyse. Default is js, jsx, ts, tsx")
    args = parser.parse_args()

    current_dir = os.getcwd()
    project_path = os.path.join(
        current_dir, args.path) if args.path else current_dir
    src_dir = os.path.join(
        project_path, args.src_dir if args.src_dir else "src")
    if not os.path.exists(src_dir):
        print(
            f"ERROR: {src_dir} directory does not exist. Please check your arguments\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        return 1
    assets_dir = os.path.join(
        project_path, args.assets_dir if args.assets_dir else "assets")
    if not os.path.exists(assets_dir):
        print(
            f"ERROR: {assets_dir} directory does not exist. Please check your arguments\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        return 1
    extensions = args.extensions if args.extensions else [
        "js", "jsx", "ts", "tsx"]

    # Parse all assets files
    asset_files = {}
    for a in glob(os.path.join(assets_dir, "**/*"), recursive=True):
        name, ext = os.path.splitext(os.path.relpath(a, project_path))
        splits = name.split("@")
        base = splits.pop(0)
        if (base in asset_files):
            asset_files[base]["suffixes"].extend(splits)
        else:
            asset_files[base] = {
                "path": base + ext,
                "ext": ext,
                "suffixes": splits,
                "found": False
            }

    # Parse all source code and note the used assets
    code_files = flatten(
        [glob(os.path.join(src_dir, f"**/*.{ext}"), recursive=True) for ext in extensions])

    for code_file in code_files:

        with open(code_file, "r") as f:
            content = f.read()
            for a in asset_files:
                if asset_files[a]["found"] is False:
                    asset_files[a]["found"] = asset_files[a]["path"] in content

    # Print the unused assets
    count = 0
    for key, value in asset_files.items():
        if value["found"] is False:
            count += len(value["suffixes"]) + 1
            print(value["path"])
            for s in value["suffixes"]:
                print(key + "@" + s + value["ext"])
    print(f"{count} unused assets detected")

    return 0


if __name__ == "__main__":
    exit(main())
