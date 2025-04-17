from src.iot.thing import Thing
import hiwonder.ActionGroupControl as AGC


class Robot(Thing):
    def __init__(self):
        super().__init__("Robot", "小幻机器人")
        # self.power = False

        print(f"[小幻机器人] 初始化完成")

        # 定义属性
        # self.add_property("power", "灯是否打开", lambda: self.power)

        # 定义方法
        self.add_method("Forward", "前进", [],
                        lambda params: self._forward())

        self.add_method("Backward", "后退", [],
                        lambda params: self._backward())

    def _forward(self):
        AGC.runActionGroup('go_forward')
        print(f"[小幻机器人] 已前进")
        return {"status": "success", "message": "前进"}

    def _backward(self):
        AGC.runActionGroup('back_fast')
        print(f"[小幻机器人] 已后退")
        return {"status": "success", "message": "后退"}