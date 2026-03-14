import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime

class DateTimePickerDialog:
    """日期时间选择弹窗 - 模仿图片样式"""
    
    def __init__(self, parent, call_back_entity, title="选择日期时间"):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("450x500")
        self.top.transient(parent)
        self.top.grab_set()  # 模态对话框
        
        # 存储选择结果
        self.result_date = None
        self.result_time = None
        self.result_datetime = None
        self.call_back_entity = call_back_entity
        
        # 设置窗口图标和样式
        self.top.resizable(False, False)
        
        # 创建界面
        self.create_widgets()
        
        # 设置窗口居中
        self.center_window()
    
    def create_widgets(self):
        """创建界面控件"""
        
        # 主框架
        main_frame = tk.Frame(self.top)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 1. 月份标题 - 模仿图片中的"2011年1月"
        self.year = 2026
        self.month = 2
        
        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.title_label = tk.Label(
            title_frame,
            text=f"{self.year}年{self.month}月",
            font=("微软雅黑", 14, "bold"),
            fg="#333333"
        )
        self.title_label.pack(side=tk.LEFT)
        
        # 月份切换按钮
        nav_frame = tk.Frame(title_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        tk.Button(
            nav_frame,
            text="<",
            width=3,
            command=self.prev_month,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            nav_frame,
            text=">",
            width=3,
            command=self.next_month,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=2)
        
        # 2. 日历表格 - 模仿图片中的表格
        calendar_frame = tk.Frame(main_frame, relief=tk.GROOVE, bd=1)
        calendar_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 创建星期标题行
        weekdays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        for i, day in enumerate(weekdays):
            day_label = tk.Label(
                calendar_frame,
                text=day,
                font=("微软雅黑", 10),
                width=8,
                height=2,
                relief=tk.RAISED,
                bg="#F0F0F0"
            )
            day_label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # 创建日期按钮网格
        self.date_buttons = []
        for row in range(6):  # 最多6行
            row_buttons = []
            for col in range(7):  # 7列（星期）
                btn = tk.Button(
                    calendar_frame,
                    text="",
                    width=6,
                    height=2,
                    font=("Arial", 10),
                    relief=tk.FLAT,
                    bg="white",
                    command=lambda r=row, c=col: self.select_date(r, c)
                )
                btn.grid(row=row+1, column=col, sticky="nsew", padx=1, pady=1)
                row_buttons.append(btn)
            self.date_buttons.append(row_buttons)
        
        # 配置网格权重
        for i in range(7):
            calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):  # 6行日期 + 1行星期标题
            calendar_frame.grid_rowconfigure(i, weight=1)
        
        # 3. 当前时间显示区域 - 模仿图片中的"今天: 2026-02-04"和"18:30:00"
        current_frame = tk.Frame(main_frame)
        current_frame.pack(fill=tk.X, pady=(0, 15))
        
        # "今天"标签
        today_label = tk.Label(
            current_frame,
            text="今天:",
            font=("微软雅黑", 11),
            fg="#333333"
        )
        today_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 当前日期显示
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_date_label = tk.Label(
            current_frame,
            text=current_date,
            font=("Arial", 11, "bold"),
            fg="#0066CC"
        )
        self.current_date_label.pack(side=tk.LEFT, padx=(0, 30))
        
        # 当前时间显示
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_time_label = tk.Label(
            current_frame,
            text=current_time,
            font=("Arial", 14, "bold"),
            fg="#FF6600"
        )
        self.current_time_label.pack(side=tk.RIGHT)
        
        # 4. 时间选择器
        time_frame = tk.LabelFrame(main_frame, text="选择时间", font=("微软雅黑", 10))
        time_frame.pack(fill=tk.X, pady=(0, 15))
        
        time_select_frame = tk.Frame(time_frame)
        time_select_frame.pack(pady=10)
        
        # 小时选择
        tk.Label(time_select_frame, text="时:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.hour_var = tk.StringVar(value="18")
        hour_spin = tk.Spinbox(
            time_select_frame,
            from_=0,
            to=23,
            textvariable=self.hour_var,
            width=4,
            format="%02.0f",
            state="readonly",
            wrap=True,
            font=("Arial", 10)
        )
        hour_spin.pack(side=tk.LEFT, padx=(0, 10))
        
        # 分钟选择
        tk.Label(time_select_frame, text="分:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.minute_var = tk.StringVar(value="30")
        minute_spin = tk.Spinbox(
            time_select_frame,
            from_=0,
            to=59,
            textvariable=self.minute_var,
            width=4,
            format="%02.0f",
            state="readonly",
            wrap=True,
            font=("Arial", 10)
        )
        minute_spin.pack(side=tk.LEFT, padx=(0, 10))
        
        # 秒选择
        tk.Label(time_select_frame, text="秒:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.second_var = tk.StringVar(value="00")
        second_spin = tk.Spinbox(
            time_select_frame,
            from_=0,
            to=59,
            textvariable=self.second_var,
            width=4,
            format="%02.0f",
            state="readonly",
            wrap=True,
            font=("Arial", 10)
        )
        second_spin.pack(side=tk.LEFT)
        
        # 5. 按钮区域
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # 确定按钮
        ok_button = ttk.Button(
            button_frame,
            text="确定",
            command=self.on_ok,
            width=10
        )
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 取消按钮
        cancel_button = ttk.Button(
            button_frame,
            text="取消",
            command=self.on_cancel,
            width=10
        )
        cancel_button.pack(side=tk.RIGHT)
        
        # 今天按钮
        today_button = ttk.Button(
            button_frame,
            text="今天",
            command=self.select_today,
            width=10
        )
        today_button.pack(side=tk.LEFT)
        
        # 初始化日历
        self.update_calendar()
        
        # 更新时间显示（动态）
        self.update_current_time()

    def update_calendar(self):
        """更新日历显示"""
        # 获取该月的日历
        cal = calendar.monthcalendar(self.year, self.month)
        
        # 清空所有按钮
        for row in range(6):
            for col in range(7):
                btn = self.date_buttons[row][col]
                btn.config(text="", bg="white", fg="black", state=tk.NORMAL)
        
        # 填充日期
        today = datetime.now()
        
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day != 0:
                    btn = self.date_buttons[week_idx][day_idx]
                    btn.config(text=str(day))
                    
                    # 判断是否为今天
                    if (self.year == today.year and 
                        self.month == today.month and 
                        day == today.day):
                        btn.config(bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
                    
                    # 判断是否为周末（周六或周日）
                    if day_idx == 0 or day_idx == 6:  # 0=周日, 6=周六
                        btn.config(fg="red")
        
        # 更新标题
        self.title_label.config(text=f"{self.year}年{self.month}月")
    
    def select_date(self, row, col):
        """选择日期"""
        # 获取按钮文本
        btn = self.date_buttons[row][col]
        day_text = btn.cget("text")
        
        if day_text == "":
            return
        
        # 重置所有按钮样式
        for r in range(6):
            for c in range(7):
                date_btn = self.date_buttons[r][c]
                day = date_btn.cget("text")
                if day != "":
                    # 恢复默认样式，但保留特殊日期的颜色
                    today = datetime.now()
                    
                    # 检查是否为今天
                    if (self.year == today.year and 
                        self.month == today.month and 
                        int(day) == today.day):
                        date_btn.config(bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
                    # 检查是否为周末
                    elif c == 0 or c == 6:
                        date_btn.config(bg="white", fg="red", font=("Arial", 10))
                    else:
                        date_btn.config(bg="white", fg="black", font=("Arial", 10))
        
        # 高亮选中的日期
        btn.config(bg="#0066CC", fg="white", font=("Arial", 10, "bold"))
        
        # 存储选择的日期
        self.result_date = f"{self.year}-{self.month:02d}-{int(day_text):02d}"
        
        # 更新当前日期显示
        self.current_date_label.config(text=self.result_date)
        self.call_back_entity._call_back(self.result_date)

    def prev_month(self):
        """切换到上一个月"""
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        
        self.update_calendar()
    
    def next_month(self):
        """切换到下一个月"""
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        
        self.update_calendar()
    
    def select_today(self):
        """选择今天"""
        today = datetime.now()
        self.year = today.year
        self.month = today.month
        
        self.update_calendar()
        
        # 找到并选中今天的按钮
        for row in range(6):
            for col in range(7):
                btn = self.date_buttons[row][col]
                day_text = btn.cget("text")
                if day_text == str(today.day):
                    self.select_date(row, col)
                    break
        
        # 设置时间为当前时间
        self.hour_var.set(today.strftime("%H"))
        self.minute_var.set(today.strftime("%M"))
        self.second_var.set(today.strftime("%S"))
        # 更新当前时间显示
        self.update_current_time()
    
    def update_current_time(self):
        """更新当前时间显示"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=current_time)

        # 每秒钟更新一次
        self.top.after(1000, self.update_current_time)
    
    def on_ok(self):
        """确定按钮点击事件"""
        # 获取选择的日期
        if self.result_date is None:
            today = datetime.now()
            self.result_date = today.strftime("%Y-%m-%d")
        
        # 获取选择的时间
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        second = self.second_var.get()
        
        self.result_time = f"{hour}:{minute}:{second}"
        self.result_datetime = f"{self.result_date} {self.result_time}"
        
        print(f"选择的日期时间: {self.result_datetime}")
        
        # 关闭窗口
        self.top.destroy()
    
    def on_cancel(self):
        """取消按钮点击事件"""
        self.result_datetime = None
        self.top.destroy()
    
    def center_window(self):
        """窗口居中显示"""
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
    
    def get_result(self):
        """获取选择的结果"""
        return self.result_datetime
