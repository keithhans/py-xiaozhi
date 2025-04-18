import cv2
import base64
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import threading
from src.iot.thing import Thing
from src.iot.things.CameraVL import VL

logger = logging.getLogger("Camera")


class Camera(Thing):
    def __init__(self):
        super().__init__("Camera", "摄像头管理")
        """初始化摄像头管理器"""
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        # 加载配置
        self.cap = None
        self.is_running = False
        self.camera_thread = None
        self.result=""
        from src.utils.config_manager import ConfigManager
        self.config = ConfigManager.get_instance()
        # 摄像头控制器
        VL.ImageAnalyzer.get_instance().init(self.config.get_config('CAMERA.VLapi_key'), self.config.get_config('CAMERA.Loacl_VL_url'),self.config.get_config('CAMERA.models'))
        self.VL= VL.ImageAnalyzer.get_instance()
        print(f"[虚拟设备] 摄像头设备初始化完成")

        self.add_property_and_method()#定义设备方法与状态属性

    def add_property_and_method(self):
        # 定义属性
        self.add_property("result", "识别画面的内容", lambda: self.result )
        # 定义方法
        self.add_method("process", "识别画面", [],
                        lambda params: self.process())
    
    def process(self):
        """截取当前画面并转换为 Base64 编码"""
        if self.cap == None:
            camera_index = self.config.get_config('CAMERA.camera_index')
            self.cap = cv2.VideoCapture(camera_index)

            if not self.cap.isOpened():
                logger.error("无法打开摄像头")
                return

            # 设置摄像头参数
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get_config('CAMERA.frame_width'))
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get_config('CAMERA.frame_height'))
            self.cap.set(cv2.CAP_PROP_FPS, self.config.get_config('CAMERA.fps'))

        # 清空缓冲区
        for _ in range(5):  # 丢弃几帧，确保获取最新画面
            self.cap.grab()
            
        ret, frame = self.cap.read()
        if not ret:
            logger.error("无法读取画面")
            return None

        # 将帧转换为 JPEG 格式
        _, buffer = cv2.imencode('.jpg', frame)

        # 将 JPEG 图像转换为 Base64 编码
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        self.result = str(self.VL.analyze_image(frame_base64, "简单介绍一下你看到的内容"))
        logger.info("画面已经识别到啦")
        print(f"[虚拟设备] 画面已经识别完成")

        return {"status": 'success', "message": "识别成功", "result" : self.result}
    
    def __del__(self):
        """析构函数，确保释放摄像头资源"""
        if self.cap is not None:
            self.cap.release()
    
