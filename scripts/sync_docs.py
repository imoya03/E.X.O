"""
Copies web/static/ into docs/ so GitHub Pages can serve the site.
Run this before pushing to GitHub whenever the site content changes.
"""

import shutil
import os

SOURCE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web", "static")
DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

if __name__ == "__main__":
    if os.path.exists(DEST):
        shutil.rmtree(DEST)
    shutil.copytree(SOURCE, DEST)
    print(f"Synced {SOURCE} -> {DEST}")