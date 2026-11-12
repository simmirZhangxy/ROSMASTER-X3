FROM yahboomtechnology/ros2-base:2.0.2

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# ============================================================
# 1. 使用本地下载好的 ROS GPG Key
# ============================================================

COPY ros.key /tmp/ros.key

RUN gpg --dearmor \
    -o /usr/share/keyrings/ros-archive-keyring.gpg \
    /tmp/ros.key \
    && rm -f /tmp/ros.key

# 配置 ROS 2 Foxy 软件源
RUN echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu focal main" \
    > /etc/apt/sources.list.d/ros2-latest.list


# ============================================================
# 2. 安装基础工具和 ROS 依赖
# ============================================================

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    python3-serial \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    usbutils \
    ros-foxy-robot-localization \
    ros-foxy-tf-transformations \
    && rm -rf /var/lib/apt/lists/*


# ============================================================
# 3. 工作空间
# ============================================================

WORKDIR /root/yahboomcar_ws


# ============================================================
# 4. 拷贝 Yahboom X3 源码
# ============================================================

COPY src ./src


# ============================================================
# 5. Rosmaster Python 驱动
# ============================================================

COPY py_install/Rosmaster_Lib/Rosmaster_Lib.py \
     /opt/rosmaster/Rosmaster_Lib.py

ENV PYTHONPATH="/opt/rosmaster:${PYTHONPATH}"


# ============================================================
# 6. 安装 ROS package 依赖
# ============================================================

RUN source /opt/ros/foxy/setup.bash && \
    rosdep install \
    --from-paths src \
    --ignore-src \
    -r -y


# ============================================================
# 7. 编译 Yahboom 工作空间
# ============================================================

RUN source /opt/ros/foxy/setup.bash && \
    MAKEFLAGS="-j1" colcon build --executor sequential --parallel-workers 1


# ============================================================
# 8. 启动脚本
# ============================================================
# 添加 ROS 环境变量到 bashrc
RUN echo 'source /opt/ros/foxy/setup.bash' >> /root/.bashrc && \
    echo 'source /root/yahboomcar_ws/install/setup.bash' >> /root/.bashrc && \
    echo 'export ROBOT_TYPE=x3' >> /root/.bashrc && \
    echo 'export RPLIDAR_TYPE=a1' >> /root/.bashrc && \
    echo 'ln -sfn /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 /dev/myserial' >> /root/.bashrc && \
    echo 'ln -sfn /dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 /dev/rplidar' >> /root/.bashrc

CMD ["bash"]
