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

        self.add_method("Stand", "立正", [],
                        lambda params: self._stand())

        self.add_method("TurnLeft", "左转", [],
                        lambda params: self._turn_left())

        self.add_method("TurnRight", "右转", [],
                        lambda params: self._turn_right())

        self.add_method("Bow", "鞠躬", [],
                        lambda params: self._bow())
        
        self.add_method("Wave", "挥手", [],
                        lambda params: self._wave())
        
        self.add_method("Hug", "拥抱", [],
                        lambda params: self._hug())

    def _bow(self):
        AGC.runActionGroup('bow')
        print(f"[小幻机器人] 已鞠躬")
        return {"status": "success", "message": "鞠躬"}
    
    def _wave(self):
        AGC.runActionGroup('wave')
        print(f"[小幻机器人] 已挥手")
        return {"status": "success", "message": "挥手"}
    
    def _hug(self):
        AGC.runActionGroup('hug')
        print(f"[小幻机器人] 已拥抱")
        return {"status": "success", "message": "拥抱"}
    
    def _stand(self):
        AGC.runActionGroup('stand')
        print(f"[小幻机器人] 已立正")
        return {"status": "success", "message": "立正"}

    def _turn_left(self):
        AGC.runActionGroup('turn_left')
        print(f"[小幻机器人] 已左转")
        return {"status": "success", "message": "左转"}

    def _turn_right(self):
        AGC.runActionGroup('stand')
        print(f"[小幻机器人] 已右转")
        return {"status": "success", "message": "右转"}

    def _forward(self):
        AGC.runActionGroup('go_forward')
        print(f"[小幻机器人] 已前进")
        return {"status": "success", "message": "前进"}

    def _backward(self):
        AGC.runActionGroup('back_fast')
        print(f"[小幻机器人] 已后退")
        return {"status": "success", "message": "后退"}