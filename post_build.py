#!/usr/bin/env python3
"""Post-build fixups for OntarioPoker.com"""

import os, re, glob

OUT = os.path.join(os.path.dirname(__file__), "OntarioPoker.com")
BASE_URL = "https://ontariopoker.com"

def process_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Strip .html from internal href links (but not from canonical, sitemap references, etc.)
    # Only strip from href attributes that are relative links
    content = re.sub(r'href="([^"]*?)\.html"', lambda m: f'href="{m.group(1)}"' if not m.group(1).startswith('http') and not m.group(1).startswith('//') else m.group(0), content)

    # 2. Add rel="noopener noreferrer" to external links missing it
    def add_rel(match):
        tag = match.group(0)
        if 'rel=' not in tag and ('target="_blank"' in tag or 'target=_blank' in tag):
            tag = tag.replace('target="_blank"', 'target="_blank" rel="noopener noreferrer"')
        return tag
    content = re.sub(r'<a [^>]*?>', add_rel, content)

    # 3. Add rel="sponsored" to affiliate exit links
    content = re.sub(r'rel="noopener noreferrer"([^>]*>Visit)', r'rel="sponsored noopener noreferrer"\1', content)

    # 4. Replace em dashes with hyphens
    content = content.replace('\u2014', ' - ')
    content = content.replace('\u2013', '-')

    # 5. Add decoding="async" to images that don't have it
    def add_decoding(match):
        tag = match.group(0)
        if 'decoding=' not in tag and 'fetchpriority' not in tag:
            tag = tag.replace('<img ', '<img decoding="async" ')
        return tag
    content = re.sub(r'<img [^>]*?>', add_decoding, content)

    # 6. Add loading="lazy" to images below the fold (skip first image)
    img_count = [0]
    def add_lazy(match):
        img_count[0] += 1
        tag = match.group(0)
        if img_count[0] > 2 and 'loading=' not in tag:
            tag = tag.replace('<img ', '<img loading="lazy" ')
        return tag
    content = re.sub(r'<img [^>]*?>', add_lazy, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
count = 0
for filepath in glob.glob(os.path.join(OUT, '**', '*.html'), recursive=True):
    if process_html(filepath):
        count += 1

print(f"Post-build: processed {count} files")

# Verify no broken internal links
print("\nChecking internal links...")
all_files = set()
for filepath in glob.glob(os.path.join(OUT, '**', '*.html'), recursive=True):
    rel = os.path.relpath(filepath, OUT)
    all_files.add(rel)
    # Also add without .html
    all_files.add(rel.replace('.html', ''))

broken = []
for filepath in glob.glob(os.path.join(OUT, '**', '*.html'), recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()
    rel_dir = os.path.dirname(os.path.relpath(filepath, OUT))
    for match in re.finditer(r'href="([^"]*)"', content):
        href = match.group(1)
        if href.startswith('http') or href.startswith('//') or href.startswith('#') or href.startswith('mailto:'):
            continue
        if href.endswith('.xml') or href.endswith('.json') or href.endswith('.css') or href.endswith('.js') or href.endswith('.svg') or href.endswith('.png') or href.endswith('.webp'):
            continue
        # Resolve relative path
        if href.startswith('../'):
            resolved = os.path.normpath(os.path.join(rel_dir, href))
        elif href.startswith('./'):
            resolved = os.path.normpath(os.path.join(rel_dir, href[2:]))
        else:
            resolved = os.path.normpath(os.path.join(rel_dir, href))

        # Check if file exists (with or without .html)
        if resolved not in all_files and resolved + '.html' not in all_files and resolved + '/index.html' not in all_files:
            # It's OK - the post-build strips .html, so check the actual file
            if not os.path.exists(os.path.join(OUT, resolved)) and not os.path.exists(os.path.join(OUT, resolved + '.html')):
                broken.append((os.path.relpath(filepath, OUT), href))

if broken:
    print(f"Found {len(broken)} potentially broken links:")
    for src, href in broken[:10]:
        print(f"  {src} -> {href}")
else:
    print("No broken internal links found")
