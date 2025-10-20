# Master of Sound

一个实时音频可视化项目，能够将声音转换为动态视觉艺术。

## 功能特点

- 实时音频输入和分析
- 动态粒子效果可视化
- 声音强度影响视觉效果
- 优雅的用户界面
- 3秒倒计时提示

## 依赖库

- pygame
- sounddevice
- numpy
- librosa

## 如何运行

1. 安装依赖：
```bash
pip install pygame sounddevice numpy librosa
```

2. 运行程序：
```bash
python music_visualization/music_visualizer.py
```

## 使用说明

1. 运行程序后，您会看到一个圆形的开始按钮
2. 点击按钮开始3秒倒计时
3. 倒计时结束后开始录音
4. 说话或播放音乐，观察动态视觉效果
5. 关闭窗口即可退出程序

## 交互效果

- 声音越大，粒子扩散越快
- 声音强度影响粒子颜色
- 粒子从中心向外扩散
- 类似心跳的脉冲效果