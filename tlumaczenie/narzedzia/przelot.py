#!/usr/bin/env python3
"""Przelotowy preprocesor mdBook (fallback R2 zamiast mdbook-quiz)."""
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        sys.exit(0)
    context, book = json.load(sys.stdin)
    json.dump(book, sys.stdout)
