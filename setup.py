import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="color-theme-analyse",
    version="0.0.4",
    author="Soltus",
    author_email="694357845@qq.com",
    description="SCSD-PY001 info: This is a simple demo of pictures color theme batch analysis use MMCQ with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/hi-windom/color-theme-analyse",
    project_urls={
        "Bug Tracker": "https://gitee.com/hi-windom/color-theme-analyse/issues",
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    package_data={
        
    }, # 数据文件包含在包的子目录中
    data_files=[
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/index.html']),
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/gitee.svg']),
        ('lib/site-packages/MMCQsc/src/_css',['src/MMCQsc/src/_css/animate.css']),
        ('lib/site-packages/MMCQsc/src/_css',['src/MMCQsc/src/_css/base.css']),
        ('lib/site-packages/MMCQsc/src/_css',['src/MMCQsc/src/_css/sweet-alert.css']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/babel.min_5.8.23.js']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/base.js']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/react-dom.development.js']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/react.development.js']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/sweet-alert.js']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/wow.min.js']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/wow.min2.js']),
    ], # 不在包内的数据文件，(安装目录，文件目录)
    include_package_data=False, # !important
    entry_points={
        "distutils.commands": [
            "mmcqsc = MMCQsc:hello_soltus",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        'easygui',
        'opencv-python',
        'numpy',
        'pillow',
        'rich',
    ],
)