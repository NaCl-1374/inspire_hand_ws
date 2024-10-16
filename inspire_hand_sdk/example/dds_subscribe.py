from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize

from inspire_sdkpy import inspire_hand_defaut,inspire_dds

import numpy as np
from scipy.interpolate import griddata
import colorcet  
import time

import threading


class DDSHandler():
   
    def __init__(self,network=None):
        super().__init__()  # 调用父类的 __init__ 方法
        if network ==None:
            ChannelFactoryInitialize(0)
        else:
            ChannelFactoryInitialize(0, network)
        self.data=inspire_hand_defaut.data_sheet
        self.sub_touch = ChannelSubscriber("rt/inspire_hand/touch/r", inspire_dds.inspire_hand_touch)
        self.sub_touch.Init(self.update_data_touch, 10)
        
        self.sub_states = ChannelSubscriber("rt/inspire_hand/state/r", inspire_dds.inspire_hand_state)
        self.sub_states.Init(self.update_data_state, 10)
        self.touch={}
        self.states={}
        self.data_touch_lock = threading.Lock()
        self.data_state_lock = threading.Lock()
    def interpolate_data(self,matrix, size):
        y = np.arange(size[1])
        x = np.arange(size[0])
        xi = np.linspace(0, size[1] - 1, size[1]*2)
        yi = np.linspace(0, size[0] - 1, size[0]*2)
        yi, xi = np.meshgrid(xi, yi)
        points = np.array(np.meshgrid(x, y)).T.reshape(-1, 2)
        values = matrix.flatten()
        return griddata(points, values, (xi, yi), method='linear')

    # 更新图形的函数
    def update_data_touch(self,msg:inspire_dds.inspire_hand_touch):
        with self.data_touch_lock:
            start_time = time.time()  # 记录开始时间
            for i, (name, addr, length, size,var) in enumerate(self.data):
                value=getattr(msg,var)
                if value is not None:
                    matrix = np.array(value).reshape(size)
                    Z_interp=self.interpolate_data(matrix,size)
                    self.touch[var]=Z_interp
            end_time = time.time()  # 记录结束时间
            elapsed_time = end_time - start_time  # 计算耗时
            # print(f"Data update time: {elapsed_time:.6f} seconds")  # 打印耗时
            
    def update_data_state(self,states_msg:inspire_dds.inspire_hand_state):
        with self.data_state_lock:
            self.states= {
                'POS_ACT': states_msg.pos_act,
                'ANGLE_ACT': states_msg.angle_act,
                'FORCE_ACT': states_msg.force_act,
                'CURRENT': states_msg.current,
                'ERROR': states_msg.err,
                'STATUS': states_msg.status,
                'TEMP': states_msg.temperature
            }
    def read(self):
        with self.data_state_lock and self.data_touch_lock:
            return   {'states':self.states,'touch':self.touch}



# from inspire_dds import inspire_hand_touch,inspire_hand_ctrl,inspire_hand_state
import sys
from inspire_sdkpy import qt_tabs,inspire_sdk,inspire_hand_defaut
# import inspire_sdkpy
if __name__ == "__main__":
    ddsHandler = DDSHandler()
    app = qt_tabs.QApplication(sys.argv)
    window = qt_tabs.MainWindow(data_handler=ddsHandler,dt=50,name="DDS Subscribe") # Update every 50 ms
    window.reflash()
    window.show()
    sys.exit(app.exec_())