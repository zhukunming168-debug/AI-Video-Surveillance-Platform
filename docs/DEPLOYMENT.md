# 部署指南

本文档将指导您如何部署AI人工智能视频监控平台。

## 1. 环境准备

在部署之前，请确保您的系统已安装以下软件：

*   **Docker**: 版本 20.10.0 或更高。
*   **Docker Compose**: 版本 1.29.0 或更高。
*   **Git**: 用于克隆项目仓库。

## 2. 克隆项目

首先，将项目仓库克隆到您的本地机器：

```bash
git clone https://github.com/zhukunming168-debug/AI-Video-Surveillance-Platform.git
cd AI-Video-Surveillance-Platform
```

## 3. 构建和运行

项目使用Docker Compose进行多服务部署。进入项目根目录后，执行以下命令构建并启动服务：

```bash
docker-compose up --build -d
```

*   `--build`：强制重新构建镜像，确保使用最新的代码。
*   `-d`：在后台运行服务。

首次构建可能需要一些时间，因为它会下载所需的镜像并安装依赖。

## 4. 访问平台

服务启动后，您可以通过浏览器访问前端界面：

*   **前端界面**: `http://localhost:80`
*   **后端API**: `http://localhost:5000/api`

## 5. 停止和清理

要停止所有运行中的服务，请在项目根目录执行：

```bash
docker-compose down
```

要停止并删除所有容器、网络和卷，请执行：

```bash
docker-compose down -v
```

## 6. 后端服务说明

后端服务基于Flask开发，主要提供以下API接口：

*   `/api/devices`: 设备管理（增删改查）
*   `/api/stream/start/<device_id>`: 启动视频流
*   `/api/stream/stop/<device_id>`: 停止视频流
*   `/api/stream/play/<device_id>`: 播放视频流 (HLS/MJPEG)
*   `/api/ai/start/<device_id>`: 启动AI分析
*   `/api/ai/stop/<device_id>`: 停止AI分析
*   `/api/events`: AI事件查询

## 7. 前端服务说明

前端服务基于React开发，提供直观的用户界面，用于：

*   仪表板：概览设备状态和事件统计。
*   设备管理：添加、编辑、删除和查看摄像头设备。
*   视频监控：实时预览视频流，并进行截图操作。
*   事件管理：查看AI分析产生的事件列表。

## 8. 故障排除

*   **端口冲突**: 如果80或5000端口已被占用，您可以在`docker-compose.yml`文件中修改端口映射。
*   **FFmpeg/OpenCV**: 后端镜像已包含FFmpeg和OpenCV的依赖，如果遇到相关问题，请检查Docker日志。
*   **日志查看**: 使用 `docker-compose logs -f [service_name]` 命令查看特定服务的日志，例如 `docker-compose logs -f backend`。

