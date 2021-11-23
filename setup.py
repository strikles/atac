from distutils.core import setup
setup(
    name='atac',        # How you named your package folder (MyLib)
    packages=['atac'],  # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    license='MIT',      # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='activism tools',   # Give a short description about your library
    author='strikles',                   # Type in your name
    author_email='strikles@gmail.com',      # Type in your E-Mail
    url='https://github.com/strikles/atac',   # Provide either the link to your github or to your website
    download_url='https://github.com/strikles/atac/archive/v_01.tar.gz',    # I explain this later on
    keywords=['activism', 'scrape', 'cybertorture'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'ascii-magic',
        'beautifulsoup4',
        'bs4',
        'colorama',
        'coloredlogs',
        'coverage',
        'cryptography',
        'envelope',
        'facebook-sdk',
        'fake-useragent'
        'lxml',
        'Markdown',
        'markovify',
        'phonenumbers',
        'Pillow',
        'py3-validate-email',
        'pyaxmlparser',
        'python-frontmatter',
        'python-gnupg',
        'pywhatkit',
        'pywhatsapp',
        'PyYAML',
        'qrcode',
        'regex',
        'requests',
        'shadow-useragent',
        'stdiomask',
        'tqdm',
        'tweepy',
        'twilio',
        'urllib3',
        'validators',
        'wikipedia',
        'yowsup2'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Set the license
        'License :: OSI Approved :: MIT License',
        # Specify the pyhton versions supported
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
