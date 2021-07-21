import setuptools
'''
官方推荐使用静态的 setup.cfg 但动态的 setup.py 对我们来说更熟悉，学习成本低，两个文件也可以共存
MANIFEST.in 需要放在和 setup.py 同级的顶级目录下，setuptools 会自动读取该文件
建议 MANIFEST.in 只用于构建 tar.gz 而不用于 whl ，即 setup.py 设置 [include_package_data=False]，至少在熟练掌握构建前应当这样做
'''
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="color-theme-analyse",
    setup_requires=['setuptools_scm'],
    use_scm_version=True, # .gitignore 应与 setup.py 在同一文件夹 更多信息参考 https://pypi.org/project/setuptools-scm/
    # version="0.0.5", # 默认的手动指定版本
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
        # 这一部分的编写指南可以参考 https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3.9", # 目标 Python 版本
        "Topic :: Multimedia :: Graphics"
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    exclude_package_data={},
    package_data={
        '':['*.json'],
    }, # 数据文件包含在包的子目录中,也就是有__init__.py 的文件夹中
    data_files=[
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/index.html']),
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/gitee.svg']),
        ('lib/site-packages/MMCQsc/src/_css',['src/MMCQsc/src/_css/base.css','src/MMCQsc/src/_css/animate.css','src/MMCQsc/src/_css/sweet-alert.css']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/base.js','src/MMCQsc/src/_js/babel.min_5.8.23.js','src/MMCQsc/src/_js/react-dom.development.js','src/MMCQsc/src/_js/react.development.js','src/MMCQsc/src/_js/sweet-alert.js','src/MMCQsc/src/_js/wow.min.js','src/MMCQsc/src/_js/wow.min2.js']),
    ], # 不在包内的数据文件，格式为(安装目录，文件目录)，注意都是相对路径
    include_package_data=False, # !important
    entry_points={
        "console_scripts": [
            "mmcqsc = MMCQsc.scp.main:mainFun",
        ],
    },
    # 将脚本添加到系统 PATH 中
    scripts=['src/MMCQsc/color_theme_analyse.py'],
    python_requires=">=3.8",
    # 关于 install_requires， 有以下五种常用的表示方法：(指定包名是必须的，而版本控制与可选依赖，则是高级形式。 这不仅仅是install_requires的形式，而是对setup.py的所有require都适用)
    # 'argparse'，只包含包名。 这种形式只检查包的存在性，不检查版本。 方便，但不利于控制风险。
    # 'setuptools==38.2.4' 指定版本。确保了开发、测试与部署的版本一致，不会出现意外。 缺点是不利于更新，每次更新都需要改动代码。
    # 'docutils >= 0.3'，这是比较常用的形式。 当对某个库比较信任时，这种形式可以自动保持版本为最新。
    # 'Django >= 1.11, != 1.11.1, <= 2'，这是比较复杂的形式。保证了Django的大版本在1.11和2之间，也即1.11.x；并且，排除了已知有问题的版本1.11.1（仅举例）。 对于一些大型、复杂的库，这种形式是最合适的。
    # 'requests[security, socks] >= 2.18.4'，这是包含了额外的可选依赖的形式。 正常安装requests会自动安装它的install_requires中指定的依赖，而不会安装security和socks这两组依赖（这两组依赖是定义在它的extras_require中）。
    install_requires=[
        'easygui',
        'opencv-python',
        'numpy',
        'pillow',
        'rich',
    ],
    # install_requires 在安装模块时会自动安装依赖包
    # extras_require 仅表示该模块依赖这些包，但不是必须的，需要用户手动安装
    extras_require={
        'PDF':  ["ReportLab>=1.2", "RXP"],
        'reST': ["docutils>=0.3"],
    },
    # 如果其中某些依赖，在官方的PyPI中不存在，则需要指定dependency_links (貌似已被弃用，但写上也不影响)
    dependency_links=[
        'http://pypi.douban.com/simple',
        'https://pypi.org/simple',
    ],
)