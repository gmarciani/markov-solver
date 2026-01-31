# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# Add src to path for autodoc
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# -- Project information
project = "Markov Solver"
copyright = "2021, Giacomo Marciani"
author = "Giacomo Marciani"

# Get version from package
from markov_solver.constants import __version__

release = __version__

# -- General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_click",
    "sphinx_new_tab_link",
    "sphinxcontrib.autodoc_pydantic",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
}

# html_favicon = "_static/favicon.ico"
# html_logo = "_static/logo.png"
# html_extra_path = ["_static/CNAME"]

# -- sphinx-click configuration
# This automatically documents Click commands

# -- sphinx_new_tab_link
new_tab_link_show_external_link_icon = True

# -- autodoc_pydantic
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_config_summary = True
