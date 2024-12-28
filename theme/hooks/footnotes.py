from mkdocs.structure.pages import Page

def on_page_markdown(markdown, page, **kwargs):
    """
    Replace footnotes marker with actual footnotes in blog posts
    """
    # Check if template exists in meta and if it's a blog post
    if page.meta and page.meta.get("template") == "blog-post.html":
        marker = "<!-- Footnotes -->"
        if marker in markdown:
            parts = markdown.split(marker)
            if len(parts) > 1:
                # Move footnotes to marker position
                return parts[0] + parts[1]
    return markdown