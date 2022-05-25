from distutils.core import setup

setup(
    # How you named your package folder (MyLib)
    name="atac",
    # Chose the same as "name"
    packages=["atac", "MarkdownPP", "MarkdownPP/modules"],
    entry_points={
        "console_scripts": [
            "atac = atac.main:main",
            "markdown-pp = MarkdownPP.main:main",
        ],
    },
    # Start with a small number and increase it with every change you make
    version="0.1",
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license="MIT",
    # Give a short description about your library
    description="activism tools",
    # Type in your name
    author="strikles",
    # Type in your E-Mail
    author_email="strikles@gmail.com",
    # Provide either the link to your github or to your website
    url="https://github.com/strikles/atac",
    # I explain this later on
    download_url="https://github.com/strikles/atac/archive/v_01.tar.gz",
    # Keywords that define your package best
    keywords=["activism", "scrape", "cybertorture"],
    # I get to this in a second
    install_requires=[
        "ascii-magic",
        "beautifulsoup4",
        "boto3",
        "bs4",
        "pycairo",
        "colorama",
        "coloredlogs",
        "coverage",
        "cryptography",
        "envelope",
        "facebook-sdk",
        "Faker",
        "fake-useragent",
        "lxml",
        "markovify",
        "mistune",
        "numpy",
        "phonenumbers",
        "Pillow",
        "py3-validate-email",
        "pyaxmlparser",
        "python-frontmatter",
        "python-gnupg",
        "pywhatkit",
        "PyYAML",
        "qrcode",
        "random-word",
        "regex",
        "requests",
        "samila",
        "scipy",
        "shadow-useragent",
        "spacy",
        "stdiomask",
        "syllapy",
        "tqdm",
        "tsp_solver2",
        "tweepy",
        "urllib3",
        "utils",
        "validators",
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Development Status :: 3 - Alpha",
        # Define that your audience are developers
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Set the license
        "License :: OSI Approved :: MIT License",
        # Specify the pyhton versions supported
        "Programming Language :: Python :: 3.8",
    ],
)
