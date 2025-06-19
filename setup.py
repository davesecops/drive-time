from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="drivetime",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Get live driving ETAs with traffic information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davesecops/drive-time",
    packages=find_packages(),
    py_modules=["drive_time"],
    entry_points={
        "console_scripts": [
            "drivetime=drive_time:main",
        ],
    },
    install_requires=[
        "googlemaps==4.10.0",
        "python-dotenv==1.1.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
