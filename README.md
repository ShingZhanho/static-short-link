# Static Short Link

This is a GitHub Pages-hosted static short link service for my domain `j-shi.ng`.
Link redirections are implemented using HTML's `<meta http-equiv="refresh">` tag.
All links are defined in the `links.txt` file, handled by `generate_links.py`, and
deployed via GitHub Actions.

## Format of `links.txt`

Every two lines define a short link:

```
/short-path
    :=https://target-url/
```

- The first line is the short path (must start with a `/`).
- The second line starts with a **tab** character (must not be spaces), followed by `:=`, and then the target URL.
- Comments are allowed **at the start** of a line using `;`.
- Blank lines are ignored.
- If a short path is not immediately followed by a target URL line, it will be ignored;
    similarly, a target URL line without a preceding short path will be ignored.
- Duplicate short paths will cause the later one to override the earlier one.

## `generate_links.py`

This script reads `links.txt` and generates the corresponding HTML files in the `out/`
directory using the `template.html` file.