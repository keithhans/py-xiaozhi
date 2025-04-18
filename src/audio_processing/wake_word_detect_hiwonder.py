import logging
import threading
import time

from speech import speech

from src.utils.config_manager import ConfigManager

# 配置日志
logger = logging.getLogger("WakeWordDetector")

class WakeWordDetectorHiWonder:
    """唤醒词检测类"""

    def __init__(self):
        """
        初始化唤醒词检测器
        """
        # 初始化基本属性
        self.on_detected_callbacks = []
        self.running = False
        self.detection_thread = None
        self.paused = False

        # 获取配置
        config = ConfigManager.get_instance()
        if not config.get_config('WAKE_WORD_OPTIONS.USE_WAKE_WORD', False):
            logger.info("唤醒词功能已禁用")
            self.enabled = False
            return

        # 基本初始化
        self.enabled = True

        self.kws = speech.WonderEcho('/dev/ttyUSB0')

    def start(self, audio_stream=None):
        """启动唤醒词检测"""
        if not getattr(self, 'enabled', True):
            logger.info("唤醒词功能已禁用，无法启动")
            return False

        # 先停止现有的检测
        self.stop()

        try:
            # 启动检测线程
            self.running = True
            self.paused = False

            self.kws.start()

            self.detection_thread = threading.Thread(
                target=self._detection_loop,
                daemon=True
            )
            self.detection_thread.start()
            return True
        except Exception as e:
            error_msg = f"启动唤醒词检测失败: {e}"
            logger.error(error_msg)
            self._cleanup()
            return False

    def stop(self):
        """停止唤醒词检测"""
        if self.running:
            self.running = False
            self.paused = False

            if self.detection_thread and self.detection_thread.is_alive():
                self.detection_thread.join(timeout=1.0)
                self.detection_thread = None

            self.kws.stop()

    def pause(self):
        """暂停唤醒词检测"""
        if self.running and not self.paused:
            self.paused = True
            logger.info("唤醒词检测已暂停")

    def resume(self):
        """恢复唤醒词检测"""
        if self.running and self.paused:
            self.paused = False
            # 如果流已关闭，重新启动检测
            self.start()
            logger.info("唤醒词检测已恢复")

    def is_running(self):
        """检查唤醒词检测是否正在运行"""
        return self.running and not self.paused

    def on_detected(self, callback):
        """
        注册唤醒词检测回调

        回调函数格式: callback(wake_word, full_text)
        """
        self.on_detected_callbacks.append(callback)

    def _cleanup(self):
        """清理资源"""
        self.stop()

    def _detection_loop(self):
        """唤醒词检测主循环"""
        logger.info("唤醒词检测循环已启动")

        while self.running:
            try:
                if self.paused:
                    time.sleep(0.1)
                    continue

                if self.kws.detect():
                    logger.info("唤醒词检测成功")
                    # 触发回调
                    self._trigger_callbacks("小幻小幻", "小幻小幻")

            except Exception as e:
                logger.error(f"唤醒词检测循环出错: {e}")

            time.sleep(0.1)

    def _trigger_callbacks(self, wake_word, text):
        """触发唤醒词回调"""
        for callback in self.on_detected_callbacks:
            try:
                callback(wake_word, text)
            except Exception as e:
                logger.error(f"执行唤醒词检测回调时出错: {e}")
