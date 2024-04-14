import psutil
import time
import tkinter as tk

def optimize_memory():
    try:
        # 终止不必要的服务
        for service in psutil.win_service_iter():
            if service.name() not in ['wuauserv', 'SysMain', 'BITS']:
                try:
                    service.stop()
                except psutil.NoSuchProcess:
                    pass

        # 清除缓存
        psutil.swap().cached = 0

        # 压缩内存
        psutil.virtual_memory().compress()

        # 调整虚拟内存设置
        psutil.virtual_memory().set_pagefile(0)

        # 等待系统稳定
        time.sleep(1)

        # 再次压缩内存
        psutil.virtual_memory().compress()
    except Exception as e:
        print(f"内存优化失败：{e}")

def optimize_cpu():
    try:
        # 设置 CPU 优先级
        for proc in psutil.process_iter():
            if proc.info['name'] not in ['System', 'Idle']:
                try:
                    proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                except psutil.NoSuchProcess:
                    pass
    except Exception as e:
        print(f"CPU 优化失败：{e}")

def main():
    try:
        optimize_memory()
        optimize_cpu()
    except Exception as e:
        print(f"优化失败：{e}")

# 创建图形化界面
window = tk.Tk()
window.title("内存和 CPU 优化器")

# 创建按钮
memory_optimize_button = tk.Button(window, text="优化内存", command=optimize_memory)
cpu_optimize_button = tk.Button(window, text="优化 CPU", command=optimize_cpu)

# 布局按钮
memory_optimize_button.pack()
cpu_optimize_button.pack()

# 运行主循环
window.mainloop()

if __name__ == "__main__":
    main()