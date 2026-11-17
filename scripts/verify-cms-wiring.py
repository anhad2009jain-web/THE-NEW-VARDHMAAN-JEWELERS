"""Verify every Pages CMS field is backed by a real content key and consumed by the frontend."""
import yaml, json, os, re, glob, sys

cfg = yaml.safe_load(open('.pages.yml', encoding='utf-8'))
errors, checked = [], 0

def flat_fields(fields, prefix=''):
    """Yield dotted field paths, descending into object fields."""
    for f in fields:
        p = f"{prefix}{f['name']}"
        yield p, f
        if f.get('type') == 'object' and 'fields' in f:
            yield from flat_fields(f['fields'], p + '.')

def get_nested(obj, dotted):
    cur = obj
    for part in dotted.split('.'):
        if isinstance(cur, list) and cur:
            cur = cur[0]  # object lists: check against the first item
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur

# ---- 1. JSON file sections: every CMS field must exist in the JSON ----
for section in cfg['content']:
    if section.get('type') != 'file':
        continue
    data = json.load(open(section['path'], encoding='utf-8'))
    for path, field in flat_fields(section['fields']):
        checked += 1
        if get_nested(data, path) is None:
            errors.append(f"[{section['label']}] field '{path}' missing in {section['path']}")

# ---- 2. Collection sections: required frontmatter keys present in every entry ----
for section in cfg['content']:
    if section.get('type') != 'collection':
        continue
    top_keys = [f['name'] for f in section['fields'] if f['name'] != 'body']
    files = glob.glob(os.path.join(section['path'], '*.md'))
    assert files, f"no entries in {section['path']}"
    for fp in files:
        text = open(fp, encoding='utf-8').read()
        fm = text.split('---')[1]
        data = yaml.safe_load(fm)
        for k in top_keys:
            checked += 1
            if k not in data:
                errors.append(f"[{section['label']}] '{k}' missing in {fp}")

# ---- 3. Reverse check: no "dead" CMS fields — each must be used in src ----
src_files = glob.glob('src/**/*.astro', recursive=True) + glob.glob('src/**/*.ts', recursive=True)
src = '\n'.join(open(f, encoding='utf-8').read() for f in src_files)

for section in cfg['content']:
    for path, field in flat_fields(section.get('fields', [])):
        leaf = path.split('.')[-1]
        checked += 1
        if leaf not in src:
            errors.append(f"[{section['label']}] field '{path}' never read by frontend code")

print(f"Checked {checked} field assertions.")
if errors:
    print("\nFAILURES:")
    for e in errors:
        print(" ✗", e)
    sys.exit(1)
print("PASS — every CMS field is backed by content and consumed by the frontend.")
