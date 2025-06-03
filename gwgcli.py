#!/usr/bin/env python3

import os
import re
from datetime import date

import click

from bin.data_helpers import read_json_as_dict
from bin.file_helpers import get_json_files
from bin.terminal_helpers import execute_commands


@click.group()
def cli():
    pass


@cli.command(name="extract-image-paths")
@click.option(
    "--guide",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="Path to the guide file",
)
@click.option(
    "--dry-run", is_flag=True, help="If set, performs a dry run without copying files"
)
def extract_image_paths(guide, dry_run):
    guide_data = read_json_as_dict(guide, raw=False)

    image_paths = [gift.image.url for gift in guide_data.gifts]

    print(f"Extracting image paths for {len(image_paths)} gifts")

    commands = []
    for i in image_paths:
        command = ["rsync"]
        if dry_run:
            command.append("--dry-run")
        filename = os.path.basename(i)
        gwg_flask_path = "~/code/projects/gwg_projects/gwg_flask/app/static/images/"
        gwg_flask_img_path = f"{gwg_flask_path}{filename}"
        dest_path = "src/images/gifts/"
        print(f"cp {gwg_flask_path}{filename} {dest_path}")
        command.extend([os.path.expanduser(gwg_flask_img_path), dest_path])
        commands.append(command)

    execute_commands(commands)


def print_guide_view(guide):
    print(f'Name: {guide["name"]}')
    print(f'Tagline: {guide["tagline"]}')
    print("\nGifts\n===\n")
    for gift in guide["gifts"]:
        print(f"{gift['name']} from {gift['shop']}")
        print(gift["description"])
        print("---")


@cli.command(name="guide-view")
@click.option(
    "--name",
    type=str,
    help="Name of guide",
)
def guide_view(name):
    guides = get_json_files("data/guides")
    if name:
        guides = [guide for guide in guides if name in guide]

    if len(guides):
        guide_data = read_json_as_dict(guides[0])
        print_guide_view(guide_data)
    else:
        print(f"Not guide called: {name}")


def slugify(title):
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    slug = slug.strip("-")
    return slug


@cli.command(name="blog")
@click.option(
    "--name",
    required=True,
    type=str,
    help="Title of the blog post",
)
def blog(name):
    """Set up files for a new blog post."""
    slug = slugify(name)
    blog_dir = os.path.join("content", "blog", slug)
    os.makedirs(blog_dir, exist_ok=True)
    md_path = os.path.join(blog_dir, "index.md")
    today = date.today().strftime("%Y-%m-%d")
    frontmatter = f"""---\nlayout: article\ntitle: {name}\ncreated_date: \"{today}\"\nsummary: \n---\n\n"""
    if not os.path.exists(md_path):
        with open(md_path, "w") as f:
            f.write(frontmatter)
        print(f"Created {md_path}")
    else:
        print(f"{md_path} already exists")


if __name__ == "__main__":
    cli()
