from distutils.core import setup

setup(
    # How you named your package folder (MyLib)
    name='atac',
    # Chose the same as "name"
    packages=['atac'],
    # Start with a small number and increase it with every change you make
    version='0.1',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='activism tools',
    # Type in your name
    author='strikles',
    # Type in your E-Mail
    author_email='strikles@gmail.com',
    # Provide either the link to your github or to your website
    url='https://github.com/strikles/atac',
    # I explain this later on
    download_url='https://github.com/strikles/atac/archive/v_01.tar.gz',
    # Keywords that define your package best
    keywords=['activism', 'scrape', 'cybertorture'],
    # I get to this in a second
    install_requires=[
        'ascii-magic',
        'beautifulsoup4',
        'boto3',
        'bs4',
        'colorama',
        'coloredlogs',
        'coverage',
        'cryptography',
        'facebook-sdk',
        'Faker',
        'fake-useragent'
        'lxml',
        'markovify',
        'mistune',
        'phonenumbers',
        'Pillow',
        'py3-validate-email',
        'py5',
        'pyaxmlparser',
        'python-frontmatter',
        'python-gnupg',
        'pywhatkit',
        'pywhatsapp',
        'PyYAML',
        'qrcode',
        'random-word',
        'regex',
        'requests',
        'samila',
        'scipy',
        'shadow-useragent',
        'spacy',
        'stdiomask',
        'syllapy',
        'tqdm',
        'tweepy',
        'twilio',
        'urllib3',
        'utils',
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
