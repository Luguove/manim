<p align="center">
    <a href="https://github.com/3b1b/manim">
        <img src="https://raw.githubusercontent.com/3b1b/manim/master/logo/cropped.png">
    </a>
</p>

[English README](README.en.md)

[![pypi version](https://img.shields.io/pypi/v/manimgl?logo=pypi)](https://pypi.org/project/manimgl/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
[![Manim Subreddit](https://img.shields.io/reddit/subreddit-subscribers/manim.svg?color=ff4301&label=reddit&logo=reddit)](https://www.reddit.com/r/manim/)
[![Manim Discord](https://img.shields.io/discord/581738731934056449.svg?label=discord&logo=discord)](https://discord.com/invite/bYCyhM9Kz2)
[![docs](https://github.com/3b1b/manim/workflows/docs/badge.svg)](https://3b1b.github.io/manim/)

Manim 是一个用于精确编程动画的引擎，专为制作数学讲解类视频设计。

请注意，Manim 目前存在两个主要版本。该仓库始于 [3Blue1Brown](https://www.3blue1brown.com/) 作者的个人项目，用于制作上述频道的视频，对应的视频示例代码在 [这里](https://github.com/3b1b/videos)。2020 年，一群开发者创建了一个新的 [社区版](https://github.com/ManimCommunity/manim/)，目标是更加稳定、测试完善、快速响应社区贡献，并且更加易于上手。更多差异细节可参考 [此页面](https://docs.manim.community/en/stable/faq/installation.html#different-versions)。

## 安装
> [!Warning]
> **警告：** 以下仅适用于 ManimGL。若尝试使用这些步骤安装 [Manim Community/manim](https://github.com/ManimCommunity/manim) 或使用那边的指引安装本仓库版本，都会导致问题。请先决定要安装的版本，再严格遵循对应版本的说明。

> [!Note]
> **提示：** 通过 pip 安装时请留意包名。本仓库是 3b1b 维护的 ManimGL，对应的包名为 `manimgl`，不是 `manim` 或 `manimlib`。请使用 `pip install manimgl` 安装本仓库版本。

Manim 需要 Python 3.7 及以上版本。

系统依赖包括 [FFmpeg](https://ffmpeg.org/)、[OpenGL](https://www.opengl.org/) 以及（可选）[LaTeX](https://www.latex-project.org) —— 如果你希望使用 LaTeX 排版。对于 Linux，还需要安装 [Pango](https://pango.org) 及其开发头文件，可参考 [此处说明](https://github.com/ManimCommunity/ManimPango#building)。

### 直接安装

```sh
# 安装 manimgl
pip install manimgl

# 试运行
manimgl
```

更多运行选项可参考下方的「使用 Manim」章节。

如果你希望直接修改 manimlib 的源码，可以先克隆本仓库，并在仓库根目录执行：

```sh
# 安装 manimgl
pip install -e .

# 试运行
manimgl example_scenes.py OpeningManimExample
# 或者
manim-render example_scenes.py OpeningManimExample
```

### 直接安装（Windows）

1. [安装 FFmpeg](https://www.wikihow.com/Install-FFmpeg-on-Windows)。
2. 安装一套 LaTeX 发行版，推荐 [MiKTeX](https://miktex.org/download)。
3. 安装剩余的 Python 依赖。
   ```sh
   git clone https://github.com/3b1b/manim.git
   cd manim
   pip install -e .
   manimgl example_scenes.py OpeningManimExample
   ```

### Mac OSX

1. 使用 Homebrew 安装 FFmpeg 和 LaTeX。
   ```sh
   brew install ffmpeg mactex
   ```

2. 如果你使用的是 ARM 架构的处理器，请安装 Cairo。
   ```sh
   arch -arm64 brew install pkg-config cairo
   ```

3. 按以下命令安装最新版 Manim。
   ```sh
   git clone https://github.com/3b1b/manim.git
   cd manim
   pip install -e .
   manimgl example_scenes.py OpeningManimExample # 请先将 manimgl 加入 path
   ```

## Anaconda 安装

1. 按前述说明安装 LaTeX。
2. 使用 `conda create -n manim python=3.8` 创建环境。
3. 使用 `conda activate manim` 激活环境。
4. 通过 `pip install -e .` 安装 manimgl。

## 使用 Manim

试着运行以下命令：

```sh
manimgl example_scenes.py OpeningManimExample
```

这会打开一个播放简单场景的窗口。

你可以阅读[示例场景](https://3b1b.github.io/manim/getting_started/example_scenes.html)，了解库的语法、动画类型与对象类型。在 [3b1b/videos](https://github.com/3b1b/videos) 仓库中，可以找到频道视频对应的全部代码，不过较早视频的代码可能无法与最新版本兼容。该仓库的 README 也介绍了如何搭建更具交互性的工作流，如 [这个演示视频](https://www.youtube.com/watch?v=rbu7Zu5X1zI) 中所示。

在命令行运行时，一些常用参数包括：
* `-w`：将场景写入文件
* `-o`：写入文件并自动打开
* `-s`：跳到末尾，只展示最终帧
    * `-so`：保存最终帧为图片并打开
* `-n <number>`：跳到场景的第 `n` 个动画
* `-f`：播放窗口全屏

更多配置可查看根目录下的 `custom_config.yml`。你可以直接编辑该文件，或在任意运行 Manim 的目录下新建一个同名文件，以覆盖默认配置。例如 [3b1b/videos 仓库的配置文件](https://github.com/3b1b/videos/blob/master/custom_config.yml) 展示了视频输出目录、资源路径，以及其他风格与视频质量相关的默认值。

### 文档
官方文档正在 [3b1b.github.io/manim](https://3b1b.github.io/manim/) 撰写中。此外，[**@manim-kindergarten**](https://manim.org.cn) 维护了中文文档，可在 [docs.manim.org.cn](https://docs.manim.org.cn/) 查阅。

[manim-kindergarten](https://github.com/manim-kindergarten/) 还编写和收集了一些额外的实用类和视频示例代码，集中在 [manim_sandbox 仓库](https://github.com/manim-kindergarten/manim_sandbox)。

## 贡献
欢迎提交贡献。正如前文所述，[社区版](https://github.com/ManimCommunity/manim) 拥有更活跃的生态、完善的测试与 CI，但我们也欢迎针对本仓库的 PR。请在提交时说明变更动机并提供效果示例。

## 许可证
本项目基于 MIT 许可证发布。
