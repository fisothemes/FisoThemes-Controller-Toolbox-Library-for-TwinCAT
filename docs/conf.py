project   = "FsControllerToolbox"
author    = "FisoThemes"
copyright = "2026, FisoThemes"
version   = "0.3.0"
release   = "0.3.0"

extensions = ["sphinx.ext.autosectionlabel"]
autosectionlabel_prefix_document = True
suppress_warnings = ["autosectionlabel.*"]

html_theme = "sphinx_rtd_theme"
html_title = f"{project} v{release}"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary":  "#2563eb",
        "color-brand-content":  "#1d4ed8",
    },
    "dark_css_variables": {
        "color-brand-primary":  "#60a5fa",
        "color-brand-content":  "#93c5fd",
    },
    "footer_icons": [],
}
html_show_sourcelink = False
html_copy_source = False
highlight_language = "none"
