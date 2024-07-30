

## Quick start

Make python virtualenv then:

    make init

## Key commands

Build the pages

    make gwg

Build assets

    make build

## Adding content

### How to add blog posts

Add a new dir to `content/blog`. This should be the slug part of the url.
Then create a `index.md` file for the blog content.

The frontmatter should look like this
```
---
layout: article
title: Welcome to Gift Wrapped Giving
created_date: "2024-07-30"
summary: Discover thoughtfully curated gift guides that make every occasion special at Gift Wrapped Giving.
---
```
