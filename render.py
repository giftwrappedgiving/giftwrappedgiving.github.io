import os
from datetime import datetime

import frontmatter
from markdown import markdown

from bin.data_helpers import read_json_as_dict
from bin.file_helpers import get_json_files, strip_extension
from bin.jinja_setup import render, setup_jinja
from bin.markdown_files import get_front_matter

env = setup_jinja()
env.globals["current_year"] = datetime.now().year
blog_template = env.get_template("blog.html")


def set_layouts():
    return {
        "base": env.get_template("layouts/base.html"),
        "article": env.get_template("layouts/article.html"),
        "list": env.get_template("layouts/list.html"),
    }


layouts = set_layouts()
blog = {"posts": {}}


def generate_posts_idx(posts, base_path="content/blog"):
    """Updates the dictionary with metadata from markdown files."""
    for key in posts.keys():
        file_path = os.path.join(base_path, key, "index.md")
        if os.path.exists(file_path):
            metadata = get_front_matter(file_path)
            # Extract the desired fields
            title = metadata.get("title", "No Title")
            created_date = metadata.get("created_date", "No Date")
            summary = metadata.get("summary", "No Summary")
            # Update the dictionary
            posts[key].update(
                {
                    "title": title,
                    "created_date": created_date,
                    "summary": summary,
                    "slug": key,
                }
            )
        else:
            print(f"File {file_path} does not exist.")
    return dict(sorted(posts.items(), key=lambda x: x[1]["created_date"], reverse=True))


def generate_blog_posts(path_to_post):
    page_content = frontmatter.load(f"{path_to_post}/index.md")
    html = markdown(page_content.content)
    content = {"main": html}

    # strip 'content/'
    output_dir = path_to_post.replace("content/", "docs/")

    layout = layouts[page_content.metadata.get("layout", "article")]
    render(
        f"{output_dir}/index.html",
        layout,
        content=content,
        fm=page_content.metadata,
    )


def render_blog_idx(idx):
    render("docs/blog/index.html", blog_template, posts=idx)


def loop_over_directory(target_dir):
    for root, dir_names, file_names in os.walk(target_dir):
        for d in dir_names:
            # will need to do the same again
            child_dir = f"{root}/{d}"
            loop_over_directory(child_dir)

        # look for the main markdown file and render
        for f in file_names:
            if f == "index.md":
                generate_blog_posts(root)
                if os.path.basename(root) not in blog["posts"]:
                    blog["posts"].setdefault(os.path.basename(root), {})

        # assets = [a for a in file_names if not a.endswith(".md")]
        # publish_assets(root, assets)


def generate_blog():
    loop_over_directory("content/blog")
    # to do: make blog index page
    posts_idx = generate_posts_idx(blog["posts"])
    render_blog_idx(posts_idx)

    print(posts_idx)


def create_html_path(filename):
    slug = strip_extension(filename)
    return f"./docs/{slug.replace('data/', '')}/index.html"


def generate_guides():
    guide_template = env.get_template("guide-layout.html")
    guides_template = env.get_template("guides.html")
    guides = []

    json_files = get_json_files("data/guides/")

    for guide_filename in json_files:

        guide = read_json_as_dict(guide_filename, raw=False)
        html_path = create_html_path(guide_filename)
        guide_slug = html_path.replace("./docs", "", 1).replace("index.html", "")
        render(html_path, guide_template, guide=guide)
        guides.append((guide.name, guide_slug, getattr(guide, "homepage-order", 0)))
        print(f"Created guide: {html_path}")

    # To do: order by something other than alphabetical
    # render the list of guides
    render("./docs/guides.html", guides_template, guides=guides)
    print("Generate guide list page")
    return guides


def generate_homepage(guides):
    home_template = env.get_template("home.html")
    editorspicks = read_json_as_dict("data/guides/editors-picks.json", raw=False)
    # gifts for homepage
    gifts = [gift for gift in editorspicks.gifts if hasattr(gift, "homepage")]
    # render the homepage
    render("./docs/index.html", home_template, name="GWG", gifts=gifts, guides=guides)


def generate_pages():
    all_guides = generate_guides()
    homepage_guides = sorted(
        [guide for guide in all_guides if guide[2]], key=lambda x: x[2]
    )
    generate_homepage(guides=homepage_guides)
    guide_template = env.get_template("guide.html")
    about_template = env.get_template("about.html")
    styleguide_template = env.get_template("styleguide.html")
    typography_template = env.get_template("typography.html")

    # render the styleguide
    render("./docs/styleguide.html", styleguide_template)
    render("./docs/typography.html", typography_template)
    # render a guide page
    render("./docs/guide.html", guide_template)
    # render a about page
    render("./docs/about.html", about_template)
    generate_blog()


if __name__ == "__main__":
    generate_pages()
