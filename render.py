from datetime import datetime

from bin.jinja_setup import render, setup_jinja

env = setup_jinja()
env.globals["current_year"] = datetime.now().year


def generate_pages():
    home_template = env.get_template("home.html")
    guides_template = env.get_template("guides.html")
    guide_template = env.get_template("guide.html")
    styleguide_template = env.get_template("styleguide.html")
    # render the homepage
    render("./docs/index.html", home_template, name="GWG")
    # render the styleguide
    render("./docs/styleguide.html", styleguide_template)
    # render the list of guides
    render("./docs/guides.html", guides_template)
    # render a guide page
    render("./docs/guide.html", guide_template)


if __name__ == "__main__":
    generate_pages()
