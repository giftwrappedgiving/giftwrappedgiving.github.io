import frontmatter


def get_front_matter(file_path):
    """Reads the front matter from a markdown file using python-frontmatter."""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        return post.metadata
