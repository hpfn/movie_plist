from setuptools import setup, find_packages

setup(
    name='movie_plist',
    version='20161225',
    packages=['conf', 'data', 'pyqt_gui', 'html_file', 'info_in_db'],
    #packages=find_packages(),
    scripts=['movie_plist.py'],
    setup_requires=['setuptools >= 28.7.1'],
    install_requires=['PyQt5 >= 5.7', 'beautifulsoup4 >= 4.5'],
    url='https://github.com/hpfn/movie_plist',
    license='GPLv3+',
    author='Herbert Parentes Fortes Neto',
    author_email='hpfn@users.noreply.github.com',
    description='list your movies',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPL-3+)',
        'Operating System :: Linux',
        'Intended Audience :: End Users/Desktop',
        'Environment :: X11 Applications :: Qt',
        'Topic :: Multimedia :: Graphics',
    ],
)
