#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import math
import random
#
# ***** Modified on 06/13/2020 *****
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# ***** Modified on 06/13/2020 *****
#
class Inverted_Pendulum(): # 台車と振り子の動作
    def __init__(self, x, theta, noisy=True): # 初期値
        self.x = x
        self.x_dot = 0
        self.theta = theta
        self.theta_dot = 0
        self.u = 0
        self.noisy = noisy
        self.t_one = t / t_num

    def do_action(self, action): # 台車の行動
        if action == 'left':
            self.u = -25
        elif action == 'right':
            self.u = 25
        else:
            self.u = 0
        if self.noisy: # 真の場合
            self.u = np.random.uniform(-5, 5) # ランダム方向へ微動する
        self.update_state()
        
#
# ***** Modified on 06/13/2020 *****
        print("{:.7f} {:.7f}".format(self.theta, self.theta_dot))
# ***** Modified on 06/13/2020 *****
#
        return (self.theta, self.theta_dot), self.calc_reward()

    def update_state(self): # 状態を更新
        for i in range(t_num):
            cos_theta = np.cos(self.theta)
            sin_theta = np.sin(self.theta)
            temp = (self.u + m * l * self.theta_dot**2 * sin_theta) / total_mass
            theta_acc = ((g * sin_theta - cos_theta * temp) /
                        (l * (4/3 - m * cos_theta**2 / total_mass)))
            x_acc = temp - m * l * theta_acc * cos_theta / total_mass

            self.x += self.t_one * self.x_dot
            self.x_dot += self.t_one * x_acc
            self.theta += self.t_one * self.theta_dot
            self.theta_dot += self.t_one * theta_acc

    def calc_reward(self): # 報酬
        if -math.pi/2 <= self.theta <= math.pi/2:
            return 0
        else:
            return 1

    def get_car_x(self):
        return self.x

#
# ***** Modified on 06/13/2020 *****
# def movie(x_history, angle_history, l, t, my_action): # 座標リストから動画を描画
#   range_width = l * 2.5
#   fig = plt.figure()
#   ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
#                        xlim=(-range_width, range_width), ylim=(-range_width, range_width))
#   ax.grid()
#   line, = ax.plot([], [], 'ro--', lw=2, markersize=8)
#   time_text = ax.text(0.02, 0.95, '', transform = ax.transAxes)
# ***** Modified on 06/13/2020 *****
#
    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text

    def animate(i):
        line.set_data([x_history[i], x_history[i]+2*l*np.sin(angle_history[i])],
                      [0, 2*l*np.cos(angle_history[i])])
        time_text.set_text('time = {0:.1f}'.format(i*t))
        return line, time_text

#
# ***** Modified on 06/13/2020 *****
#   ani = FuncAnimation(fig, animate, frames=range(len(x_history)),
#                       interval=t*1000, blit=True, init_func=init, repeat=False)
#   ani.save("pendulum.gif", writer="imagemagick")
#   plt.show()
#   #plt.close()
# ***** Modified on 06/13/2020 *****
#
def main():
    x_history_list = [0.] # x座標を格納するリスト。初期座標にゼロ設定
    angle_history_list = [initial_angle] # 角度を格納するリスト

    # インスタンスの生成           (x座標,              角度,                  ノイズ)
    my_instance = Inverted_Pendulum(x_history_list[0], angle_history_list[0], noise_flag)
    for i in range(100):
        #my_action = random.choice(my_action_list)
        my_action = my_action_list[2]
        next_s, reward = my_instance.do_action(my_action)
        x_history_list.append(my_instance.get_car_x()) # 振り子のx座標の履歴のリスト
        angle_history_list.append(next_s[0]) # 角度の履歴のリスト

    # 取得した座標リストを元に動画再生
#
# ***** Modified on 06/13/2020 *****
#   movie(x_history_list, angle_history_list, l, t, my_action)
# ***** Modified on 06/13/2020 *****
#
if __name__ == '__main__':
    M = 10 # 台車の重さ[kg]。値を大きく例えば100にすると単振り子に近くなる。
    m = 2 # 振り子の重さ[kg]
    total_mass = M + m
    l = 0.5 # 振り子の長さ[m](実質は重心位置。2l=1 が棒の長さ)
    g = 9.8 # 重力加速度[m/s2]
    
    initial_angle = 5 * (math.pi/180) # 初期角度[rad]
    t = 0.1 # 時間刻み幅
    t_num = 1000

    noise_flag = False # ノイズの微小動作設定の有無
    my_action_list = ['left', 'right', 'zero'] # 台車の行動
    
    main()
