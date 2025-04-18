import time
import random

from src.iot.thing import Thing, Parameter, ValueType

import hiwonder.ActionGroupControl as AGC

class Robot(Thing):
    def __init__(self, audio_codec):
        super().__init__("Robot", "小幻机器人")
        self.audio_codec = audio_codec

        print(f"[小幻机器人] 初始化完成")

        # 定义属性
        # self.add_property("power", "灯是否打开", lambda: self.power)

        # 定义方法
        self.add_method("Forward", "前进", 
                        [Parameter("steps", "1到100之间的整数", ValueType.NUMBER, False, 1)],
                        lambda params: self._forward(params["steps"].get_value()))

        self.add_method("Backward", "后退", [],
                        lambda params: self._backward())

        self.add_method("Stand", "立正", [],
                        lambda params: self._stand())

        self.add_method("TurnLeft", "左转", [],
                        lambda params: self._turn_left())

        self.add_method("TurnRight", "右转", [],
                        lambda params: self._turn_right())

        self.add_method("MoveLeft", "向左走", [],
                        lambda params: self._move_left())

        self.add_method("MoveRight", "向右走", [],
                        lambda params: self._move_right())

        self.add_method("Bow", "鞠躬", [],
                        lambda params: self._bow())
        
        self.add_method("Wave", "挥手", [],
                        lambda params: self._wave())
        
        self.add_method("Hug", "拥抱", [],
                        lambda params: self._hug())

        self.add_method("SitUp", "仰卧起坐", [],
                        lambda params: self._sit_up())

        self.add_method("Stepping", "跺脚", [],
                        lambda params: self._stepping())

        self.add_method("Squat", "深蹲", [],
                        lambda params: self._squat())

        self.add_method("Dance", "跳舞", [],
                        lambda params: self._dance())

        self.add_method("LieDown", "躺下", [],
                        lambda params: self._lie_down())

        self.add_method("StandUp", "爬起来", [],
                        lambda params: self._stand_up())

        self.add_method("WingChun", "咏春", [],
                        lambda params: self._wing_chun())

    def _wing_chun(self):
        AGC.runActionGroup('wing_chun')
        print(f"[小幻机器人] 已咏春")
        return {"status": "success", "message": "咏春"}

    def _stand_up(self):
        AGC.runActionGroup('stand_up_back')
        print(f"[小幻机器人] 已爬起来")
        return {"status": "success", "message": "爬起来"}

    def _lie_down(self):
        AGC.runActionGroup('lie_down')
        print(f"[小幻机器人] 已躺下")
        return {"status": "success", "message": "躺下"}

    def _dance(self):
        # 随机选择动作组 '16' 或 '24'
        dance_action = random.choice(['16', '24'])
        audio_file = "/home/pi/TonyPi/audio/{}.wav".format(dance_action)
        self.audio_codec.play_audio_file(audio_file)
        AGC.runActionGroup(dance_action)
        print(f"[小幻机器人] 已跳舞 (动作组: {dance_action})")
        return {"status": "success", "message": "跳舞"}

    def _squat(self):
        AGC.runActionGroup('squat')
        time.sleep(3)
        AGC.runActionGroup('squat_up')
        print(f"[小幻机器人] 已深蹲")
        return {"status": "success", "message": "深蹲"}

    def _stepping(self):
        AGC.runActionGroup('stepping')
        print(f"[小幻机器人] 已跺脚")
        return {"status": "success", "message": "跺脚"}

    def _sit_up(self):
        AGC.runActionGroup('sit_ups')
        print(f"[小幻机器人] 已仰卧起坐")
        return {"status": "success", "message": "仰卧起坐"}
    
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
        AGC.runActionGroup('turn_right')
        print(f"[小幻机器人] 已右转")
        return {"status": "success", "message": "右转"}

    def _move_left(self):
        AGC.runActionGroup('left_move_fast')
        print(f"[小幻机器人] 已向左走")
        return {"status": "success", "message": "向左走"}
    
    def _move_right(self):
        AGC.runActionGroup('right_move_fast')
        print(f"[小幻机器人] 已向右走")

    def _forward(self, steps):
        for i in range(steps):
            AGC.runActionGroup('go_forward')
            # time.sleep(0.5)
        AGC.runActionGroup('stand')
        print(f"[小幻机器人] 已前进{steps}步")
        return {"status": "success", "message": f"前进{steps}步"}

    def _backward(self):
        AGC.runActionGroup('back_fast')
        print(f"[小幻机器人] 已后退")
        return {"status": "success", "message": "后退"}