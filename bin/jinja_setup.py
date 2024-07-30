import os

import jinja2

from bin.jinja_filters import render_markdown_filter


def setup_jinja():
    # register templates
    multi_loader = jinja2.ChoiceLoader(
        [
            jinja2.FileSystemLoader(searchpath=["./templates"]),
        ]
    )
    env = jinja2.Environment(loader=multi_loader)
    return register_filters(env)


def register_filters(env):
    env.filters["render_markdown"] = render_markdown_filter
    return env


def render(path, template, **kwargs):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(template.render(**kwargs))
