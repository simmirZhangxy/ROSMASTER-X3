# ROSMASTER X3 — ROS 2 工作空间

基于 [Yahboom ROSMASTER X3](https://www.yahboom.net/) 的 ROS 2 **Foxy** 功能包集合，包含底盘驱动、激光雷达、SLAM、导航、视觉与示例教程等。

> 个人学习与备份仓库，源码主要随 Yahboom 资料包提供。  
> GitHub: [simmirZhangxy/ROSMASTER-X3](https://github.com/simmirZhangxy/ROSMASTER-X3)

## 环境要求

- Ubuntu 20.04 + **ROS 2 Foxy**
- `colcon`、`rosdep`
- 实机：X3 主控、RPLidar（默认 A1）、串口权限（用户需在 `dialout` 组）

## 快速开始（本机编译）

```bash
git clone https://github.com/simmirZhangxy/ROSMASTER-X3.git yahboomcar_ws
cd yahboomcar_ws

# 见下方「仓库中未包含的文件」：大文件需从原厂资料复制到对应路径

source /opt/ros/foxy/setup.bash
rosdep install --from-paths src --ignore-src -r -y   # 可选，按依赖安装
colcon build
source install/setup.bash

export ROBOT_TYPE=x3
export RPLIDAR_TYPE=a1
```

启动项因功能而异，常见入口在 `yahboomcar_bringup` 等包下的 `launch/`，具体请参考 Yahboom 官方教程。

## Docker（可选）

仓库内提供 `Dockerfile` 与 `docker-compose.yaml`，便于在容器内使用已配置好的 Foxy 环境。

构建镜像前请注意：

| 文件/目录 | 说明 |
|-----------|------|
| `ros.key` | ROS 源 GPG 密钥，**未纳入 Git**，需自行放在工作空间根目录 |
| `py_install/Rosmaster_Lib/` | Dockerfile 会复制 `Rosmaster_Lib.py`，需从 Yahboom 资料包补齐 |
| 大文件（见下表） | 需在 `COPY src` 之前放入 `src` 对应路径，否则 SLAM/人脸等功能在镜像内不可用 |

```bash
docker compose build
docker compose run --rm yahboom_x3
```

`docker-compose` 使用 `network_mode: host`、`privileged: true` 并映射 `/dev`，便于访问雷达与底盘串口。

## 仓库中未包含的文件（体积限制）

以下文件在 `.gitignore` 中，**clone 后需从 Yahboom 配套资源或原环境拷贝**：

| 路径 | 用途 |
|------|------|
| `src/yahboomcar_slam/params/ORBvoc.txt` | ORB-SLAM 词典（约 140MB） |
| `src/yahboomcar_mediapipe/.../shape_predictor_68_face_landmarks.dat` | MediaPipe 人脸关键点模型（约 95MB） |
| `ros.key` | 仅 Docker 构建需要 |
| `build/`、`install/`、`log/` | 本地编译产物，请自行 `colcon build` |

请勿将程序崩溃产生的 `core` 文件提交到 Git。

## 主要功能包（`src/`）

| 包名 | 说明（简述） |
|------|----------------|
| `yahboomcar_bringup` / `yahboomcar_base_node` / `yahboomcar_ctrl` | 底盘与启动 |
| `yahboomcar_nav` | 导航 |
| `yahboomcar_slam` / `slam_gmapping` | 建图与 SLAM |
| `sllidar_ros2` | 激光雷达驱动 |
| `yahboomcar_description` | 机器人模型 |
| `pkg_*` | ROS 2 学习示例（话题、服务、动作等） |

## 许可证与致谢

各子包可能带有各自的许可证（见各包内 `package.xml`）。硬件与基础资料版权归 **Yahboom** 所有；使用与再分发请遵守原厂许可与 ROS 相关开源协议。
