import os
import yaml
from glob import glob

POSTS_DIR = '_posts'
TAGS_DIR = 'tags'
LAYOUT = 'tag'

# Collect all tags from posts
def get_all_tags():
    tags = set()
    for post_file in glob(os.path.join(POSTS_DIR, '*')):
        with open(post_file, 'r', encoding='utf-8') as f:
            lines = f.read().split('---')
            if len(lines) > 2:
                front_matter = yaml.safe_load(lines[1])
                if front_matter and 'tags' in front_matter:
                    tags.update(front_matter['tags'])
    return sorted(tags)

def slugify(tag):
    return tag.lower().replace(' ', '-')

def ensure_tags_dir():
    if not os.path.exists(TAGS_DIR):
        os.makedirs(TAGS_DIR)

def write_tag_page(tag):
    slug = slugify(tag)
    tag_dir = os.path.join(TAGS_DIR, slug)
    os.makedirs(tag_dir, exist_ok=True)
    page_path = os.path.join(tag_dir, 'index.md')
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(f"""---
layout: {LAYOUT}
tag: {tag}
permalink: /tags/{slug}/
---
""")

def main():
    ensure_tags_dir()
    tags = get_all_tags()
    for tag in tags:
        write_tag_page(tag)
    print(f"Generated {len(tags)} tag pages in '{TAGS_DIR}/'.")

if __name__ == '__main__':
    main()
