from setuptools import setup, find_packages

setup(
    name="music-visualization",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pygame>=2.5.0',
        'sounddevice>=0.4.6',
        'numpy>=1.24.0',
        'librosa>=0.10.0',
    ],
    author="lenliyy",
    author_email="",  # 如果您想添加邮箱可以告诉我
    description="A real-time music visualization tool with pulse effects",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lenliyy/Master-of-sound",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)