# 🚀 GitHub上传完整指南

## 📋 准备工作

### 1. 安装Git
- **Windows**: 下载并安装 [Git for Windows](https://git-scm.com/download/win)
- **macOS**: 使用Homebrew安装 `brew install git`
- **Linux**: 使用包管理器安装 `sudo apt install git` (Ubuntu) 或 `sudo yum install git` (CentOS)

### 2. 创建GitHub账户
- 访问 [GitHub](https://github.com) 注册账户
- 验证邮箱地址

### 3. 配置Git用户信息
```bash
git config --global user.name "您的GitHub用户名"
git config --global user.email "您的邮箱"
```

## 🎯 自动上传方法（推荐）

### 方法1：使用批处理脚本（Windows）
```bash
# 双击运行
upload_to_github.bat
```

### 方法2：使用Python脚本
```bash
python upload_to_github.py
```

## 📝 手动上传步骤

### 步骤1：初始化Git仓库
```bash
git init
```

### 步骤2：添加文件
```bash
git add .
```

### 步骤3：提交更改
```bash
git commit -m "Initial commit: YouTube Ultra HD Downloader - Free Version"
```

### 步骤4：创建GitHub仓库
1. 访问 [GitHub New Repository](https://github.com/new)
2. 输入仓库名称（建议：`yt_zipper`）
3. 选择 Public 或 Private
4. **不要勾选** "Add a README file"
5. **不要勾选** "Add .gitignore"
6. **不要勾选** "Choose a license"
7. 点击 "Create repository"

### 步骤5：添加远程仓库
```bash
git remote add origin https://github.com/您的用户名/yt_zipper.git
```

### 步骤6：推送到GitHub
```bash
git branch -M main
git push -u origin main
```

## 🔐 身份验证

### 方法1：Personal Access Token（推荐）
1. 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo`（完整仓库访问权限）
4. 生成并复制token
5. 推送时使用token作为密码

### 方法2：SSH密钥
```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "您的邮箱"

# 添加到SSH代理
ssh-add ~/.ssh/id_ed25519

# 复制公钥到GitHub
cat ~/.ssh/id_ed25519.pub
```

## 📁 项目文件结构

上传前确认项目包含以下文件：
```
yt_zipper/
├── README.md                    # 项目说明
├── .gitignore                   # Git忽略配置
├── LICENSE                      # 开源许可证
├── requirements.txt             # Python依赖
├── cookies.txt                  # YouTube cookies（示例）
├── quick_start.py              # Python启动器
├── start_downloader.bat        # 批处理启动器
├── enhanced_downloader.py      # 增强版下载器
├── ultra_hd_download_fixed.py  # 超高清下载器
├── enhanced_downloader_pro.py  # 专业版下载器
├── upload_to_github.bat        # 自动上传脚本
├── upload_to_github.py         # Python上传脚本
└── youtube_ultra_hd_downloader/ # 独立模块
    ├── __init__.py
    ├── README.md
    ├── LICENSE
    ├── requirements.txt
    ├── ultra_hd_downloader.py
    ├── PAID_CONTENT_EXPLANATION.md
    └── VERSION_v1.0.md
```

## ⚠️ 注意事项

### 1. 隐私安全
- `cookies.txt` 包含登录信息，不要分享
- 建议在 `.gitignore` 中忽略 `cookies.txt`
- 用户需要自己提供cookies文件

### 2. 文件大小
- 确保没有大文件（>100MB）
- 视频文件不应上传到GitHub
- 使用 `.gitignore` 排除不必要的文件

### 3. 许可证
- 项目使用MIT许可证
- 确保 `LICENSE` 文件存在
- 在README中说明许可证信息

## 🔄 后续更新

### 日常更新流程
```bash
# 1. 修改代码后添加文件
git add .

# 2. 提交更改
git commit -m "更新说明：具体修改内容"

# 3. 推送到GitHub
git push
```

### 查看状态
```bash
# 查看文件状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v
```

## 🛠️ 故障排除

### 常见问题

**1. 推送失败**
```bash
# 检查网络连接
ping github.com

# 检查远程仓库URL
git remote -v

# 重新设置远程仓库
git remote set-url origin https://github.com/用户名/仓库名.git
```

**2. 身份验证失败**
- 检查Personal Access Token是否正确
- 确认token有足够的权限
- 尝试重新生成token

**3. 文件冲突**
```bash
# 拉取最新代码
git pull origin main

# 解决冲突后重新提交
git add .
git commit -m "解决冲突"
git push
```

## 📊 上传后检查

### 1. 访问仓库页面
- 确认所有文件都已上传
- 检查README.md显示正常
- 验证许可证信息

### 2. 测试克隆
```bash
# 测试仓库是否可以正常克隆
git clone https://github.com/您的用户名/yt_zipper.git test_clone
```

### 3. 检查文件完整性
- 确认所有Python文件完整
- 检查依赖文件存在
- 验证启动脚本正常

## 🎉 完成！

上传成功后，您的项目将可以在GitHub上访问：
- 仓库地址：`https://github.com/您的用户名/yt_zipper`
- 用户可以克隆、下载、贡献代码
- 支持Issues和Pull Requests

---

**💡 提示**：使用自动上传脚本可以大大简化上传过程！
