from bin.jinja_setup import setup_jinja, render


env = setup_jinja()


def generate_pages():
    test_template = env.get_template("test.html")
    # render the full backlog
    render(
        "./docs/index.html",
        test_template,
        name="GWG"
    )



if __name__ == "__main__":
    generate_pages()
