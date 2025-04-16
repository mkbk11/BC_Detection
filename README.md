# 血细胞检测系统

## 项目介绍
本项目是一个基于YOLOv8的血细胞检测系统，使用Streamlit构建Web界面，实现了实时血细胞检测、图片检测、视频检测等功能。系统具有用户管理、检测历史记录查询等功能，为医学诊断提供了有效的技术支持。

## 技术栈
- **前端**: Streamlit
- **后端**: Python
- **数据库**: MySQL
- **模型**: YOLOv8
- **其他库**: OpenCV, Pandas, Matplotlib, Seaborn, Altair

## 安装说明
1. 克隆项目到本地
```bash
git clone [项目地址]
cd BC_detection
```

2. 安装依赖
```bash
pip install -r streamlit/requirements.txt
```

## 使用方法
1. 启动应用
```bash
streamlit run streamlit/login.py
```

2. 在浏览器中访问应用（默认地址：http://localhost:8501）

3. 使用系统功能：
   - 登录/注册
   - 实时血细胞检测
   - 图片血细胞检测
   - 视频血细胞检测
   - 检测历史查询
   - 系统设置

## 项目结构
```
BC_detection/
├── streamlit/                # 主项目目录
│   ├── config.yaml          # 配置文件
│   ├── login.py            # 登录入口
│   ├── func_pages/         # 功能页面
│   │   ├── 1_About.py      # 关于页面
│   │   ├── 2_object_detection.py  # 目标检测页面
│   │   ├── 3_Setting.py    # 设置页面
│   │   ├── Setting_administer.py  # 管理员设置
│   │   └── history.py      # 历史记录页面
│   ├── images/             # 图片资源
│   ├── weight/             # 模型权重文件
│   └── ultralytics/        # YOLOv8相关文件
├── .gitignore              # Git忽略文件
├── LICENSE                 # 许可证文件
└── README.md              # 项目说明文档
```

## 主要功能
1. **实时检测**：通过摄像头实时检测血细胞
2. **图片检测**：上传图片进行血细胞检测
3. **视频检测**：上传视频进行血细胞检测
4. **历史记录**：查询和管理检测历史
5. **用户管理**：用户注册、登录和权限管理
6. **系统设置**：检测参数配置和系统设置

## 注意事项
1. 确保系统已安装Python 3.8或更高版本
2. 使用前请确认已安装所有依赖包
3. 模型文件较大，请确保有足够的存储空间
4. 实时检测功能需要摄像头支持

## 许可证
本项目采用MIT许可证，详见LICENSE文件。

## 联系方式
如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件至[您的邮箱]

## 致谢
感谢所有为本项目做出贡献的开发者和用户。