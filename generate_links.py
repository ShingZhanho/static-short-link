from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List
import shutil


def parse_links_file(path: Path) -> Dict[str, str]:
	"""Parse the links file according to README.md rules.

	Returns a dict mapping short path (as written, e.g. '/foo') -> target URL.
	Later entries override earlier ones.
	"""
	if not path.exists():
		raise FileNotFoundError(f"links file not found: {path}")

	lines = path.read_text(encoding="utf-8").splitlines()
	mapping: Dict[str, str] = {}

	i = 0
	n = len(lines)
	while i < n:
		raw = lines[i]
		# Ignore comment lines that start with ';'
		if raw.startswith(';') or raw.strip() == '':
			i += 1
			continue

		# A short path must start with '/'
		if raw.startswith('/'):
			short_path = raw.rstrip('\n')
			# a short path must not be the root path alone
			if short_path == '/':
				print(f"Warning: ignoring root path '/' entry at line {i+1}. Root path redirects are not allowed.")
				i += 1
				continue
            
			# find next non-blank, non-comment line
			j = i + 1
			while j < n and (lines[j].strip() == '' or lines[j].lstrip().startswith(';')):
				j += 1

			if j < n and lines[j].startswith('\t:='):
				target = lines[j][3:].strip()
				if target:
					# store/override
					mapping[short_path] = target
					print(f"Mapping: {short_path} -> {target}")
				# advance past the pair
				i = j + 1
				continue
			else:
				# no valid target line immediately after; ignore this short path
				print(f"Warning: ignoring short path '{short_path}' at line {i+1} without valid target line.")
				i += 1
				continue

		# If line is a target line without preceding path, ignore
		print(f"Warning: ignoring target line without preceding path at line {i+1}.")
		i += 1

	return mapping


def render_template(template_text: str, target_url: str) -> str:
	return template_text.replace('{% TARGET_URL %}', target_url)


def write_redirects(mapping: Dict[str, str], template_path: Path, out_dir: Path) -> List[Path]:
	if not template_path.exists():
		raise FileNotFoundError(f"Template file not found: {template_path}")

	template_text = template_path.read_text(encoding='utf-8')
	written: List[Path] = []

	for short_path, target in mapping.items():
		# remove leading and trailing slashes to form path segments
		seg = short_path.strip('/')
		# validate no path traversal
		if '..' in seg.split('/'):
			# skip unsafe entry
			continue

		dest_dir = out_dir / seg
		dest_dir.mkdir(parents=True, exist_ok=True)
		dest = dest_dir / 'index.html'
		content = render_template(template_text, target)
		print(f"Writing to {dest}")
		dest.write_text(content, encoding='utf-8')
		written.append(dest)

	return written


def main(argv=None) -> int:
	parser = argparse.ArgumentParser(description='Generate static redirect pages from links.txt')
	parser.add_argument('--links', '-l', type=Path, default=Path('links.txt'), help='path to links.txt')
	parser.add_argument('--template', '-t', type=Path, default=Path('template.html'), help='path to template.html')
	parser.add_argument('--out', '-o', type=Path, default=Path('out'), help='output directory')

	args = parser.parse_args(argv)

	try:
		mapping = parse_links_file(args.links)
	except FileNotFoundError as e:
		print(e)
		return 2

	if not mapping:
		print('Warning: no valid links found in', args.links)
		return 0
	
	# Clear the output directory if it exists and is non-empty
	if args.out.exists() and any(args.out.iterdir()):
		print(f'Clearing existing output directory: {args.out}')
		shutil.rmtree(args.out)
		args.out.mkdir(parents=True, exist_ok=True)

	try:
		written = write_redirects(mapping, args.template, args.out)
	except FileNotFoundError as e:
		print(e)
		return 3

	print(f'Wrote {len(written)} redirect pages to {args.out!s}')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
