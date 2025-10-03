# AI人工智能视频监控平台

这是一个旨在构建AI人工智能视频监控平台的项目，支持联网部署，并兼容中国市场上主流摄像头品牌协议和GB28181协议。

## 项目目标

*   实现多协议（GB28181, ONVIF, RTSP等）视频流接入。
*   集成AI视频分析能力，如目标检测、人脸识别、行为分析等。
*   提供友好的Web管理界面，实现设备管理、视频预览、告警处理和数据可视化。
*   支持分布式部署，具备高可用性和可扩展性。

## 技术栈（初步设想）

*   **后端**：Python (FastAPI/Flask), Go
*   **流媒体**：FFmpeg, SRS (Simple Realtime Server)
*   **数据库**：PostgreSQL, MongoDB/Elasticsearch
*   **AI框架**：TensorFlow, PyTorch
*   **前端**：React/Vue, ECharts/AntV
*   **消息队列**：Kafka/RabbitMQ

## 模块划分（初步设想）

*   **`backend/`**：后端服务代码，包括设备接入、视频流处理、AI分析接口等。
*   **`frontend/`**：前端Web管理界面代码。
*   **`docs/`**：项目文档，包括架构设计、API文档、部署指南等。
*   **`ai_models/`**：AI模型文件和相关配置。
*   **`deploy/`**：部署相关脚本和配置文件（Docker, Kubernetes等）。

## 快速开始

（待补充）

## 贡献

欢迎社区贡献！请查阅 `CONTRIBUTING.md` 获取更多信息。

## 许可证

本项目采用 MIT 许可证。详情请查阅 `LICENSE` 文件。
