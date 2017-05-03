import setuptools

setuptools.setup(
    name="nbrefineproxy",
    version='0.1.0',
    url="",
    author=["Ryan Lovett", "Félix-Antoine Fortin"]
    description="Jupyter extension to proxy OpenRefine session",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[ 'tornado', 'notebook', 'nbserverproxy' ],
    package_data={'nbrsessionproxy': ['static/*']},
)
