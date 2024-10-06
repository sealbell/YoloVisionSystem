# YoloVisionSystem

## 简介

**YoloVisionSystem** 是一个基于YOLOv5构建的实时目标检测系统，能够检测火、汽车、电动车和人。该系统支持多种输入形式，包括视频文件、实时摄像头影像和静态图片。系统集成了MySQL数据库进行数据管理，并使用PyQt5进行前后端的数据交互，为用户提供直观的操作界面。

## 功能特性

- 检测目标：火、汽车、电动车和人。
- 支持多种输入格式：
  - 视频文件
  - 实时摄像头影像
  - 静态图片
- 集成MySQL数据库，用于存储检测结果。
- 基于PyQt5的图形用户界面，实现前后端无缝交互。
- 实时检测，基于YOLOv5的高精度检测算法。

## 系统要求

运行该项目需要以下依赖：

- Python 3.x
- YOLOv5
- PyQt5
- MySQL
- OpenCV
- PyTorch
- 其他依赖项请参考 `requirements.txt`

## 安装步骤

1. 克隆此仓库：

   ```bash
   git clone https://github.com/sealbell/YoloVisionSystem.git
   cd YoloVisionSystem
   ```

2. 安装所需依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 设置MySQL数据库，并在 `config.py` 文件中配置数据库连接。

## 使用方法

1. 启动程序，运行以下命令：

   ```bash
   python main.py
   ```

2. 使用图形界面选择视频文件、实时摄像头影像或图片进行检测，检测结果将存储在MySQL数据库中。

## 截图

（这里可以添加系统界面和检测效果的截图展示。）

## 许可证

此项目使用MIT许可证，详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如果有任何问题或建议，请在GitHub上提交issue，或通过电子邮件与我们联系：sealbel66@gmail.com。
