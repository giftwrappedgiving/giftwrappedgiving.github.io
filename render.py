from bin.jinja_setup import render, setup_jinja

env = setup_jinja()


def generate_pages():
    home_template = env.get_template("home.html")
    styleguide_template = env.get_template("styleguide.html")
    # render the homepage
    render("./docs/index.html", home_template, name="GWG")
    # render the styleguide
    render("./docs/styleguide.html", styleguide_template)


if __name__ == "__main__":
    generate_pages()
