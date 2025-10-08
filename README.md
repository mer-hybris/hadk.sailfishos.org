# Sailfish OS Hardware Adaptation Development Kit

## Building the documentation

The documentation is built with [MkDocs](https://www.mkdocs.org/) and
[Material for mkDocs](https://squidfunk.github.io/mkdocs-material/)

Build environment is easiest to setup with [uv](https://docs.astral.sh/uv/).
After installing uv just run:

    uv run mkdocs serve

That will setup Python virtual env, instal all the dependencies, and start the
MkDocs built-in dev server, which allows you to view the documentation in
browser and does live reloads as you edit the source markdown.
