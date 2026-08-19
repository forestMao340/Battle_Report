# 1. 基础镜像：使用轻量级 Python 3.10 官方镜像
FROM python:3.10-slim

# 2. 设置工作目录（容器内的目录）
WORKDIR /app

# 3. 复制依赖清单（先复制这一份，利用 Docker 缓存机制）
COPY requirements.txt .

# 4. 安装 Python 依赖（使用国内镜像源加速，避免超时）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 复制项目源代码（app 文件夹）
COPY ./app ./app

# 6. 声明容器运行时监听的端口（仅文档作用，实际映射需在 run 时指定）
EXPOSE 8000

# 7. 启动命令：使用 uvicorn 运行 FastAPI 应用
# 注意：必须使用 JSON 数组形式（Exec 形式），以确保信号处理正确
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]