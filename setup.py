import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leaguepedia_validation",
    version="0.0.1",
    author="RheingoldRiver",
    author_email="river.esports@gmail.com",
    description="Validating templates for Leaguepedia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RheingoldRiver/leaguepedia_validation",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    # install_requires=['mwclient', 'mwparserfromhell'],
    dependency_links=['https://github.com/RheingoldRiver/river_mwclient#egg=0.1']
)
