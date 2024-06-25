from bin.jinja_setup import setup_jinja, render


env = setup_jinja()


def generate_pages():
    home_template = env.get_template("home.html")
    # render the full backlog
    render(
        "./docs/index.html",
        home_template,
        name="GWG"
    )


if __name__ == "__main__":
    generate_pages()
