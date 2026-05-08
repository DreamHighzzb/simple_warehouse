import tkinter as tk
from tkinter import ttk
import dateshow
from datetime import datetime

class Combobox(ttk.Frame):
    def __init__(self, parent, values, inputSize, arrowSize, boxSize, showCombox = True, showDate = False, callBack = None, params = None, isFilterBtn = False, boxPos = None, **kwargs):
        """
        parent: 父控件
        values: 选项列表，如 ["选项1", "选项2", ...]
        callBack: 选中回调函数，接收选中值作为参数
        """
        super().__init__(parent, **kwargs)

        self.parent = parent
        self.original_values = values
         # 选项数据
        self.original_values = values or []
        self.filtered_values = self.original_values.copy()
        self.callBack = callBack
        self.is_open = False
        self.boxSize = boxSize
        self.params = params
        self.isFilterBtn = isFilterBtn
        self.inputValue = ""
        self.boxPos = boxPos
        fgColor = '#99ccff'
        if self.isFilterBtn:
            fgColor = '#ffffff'
        self.frame = tk.Frame(
            self,
            bg='#ffffff',
            highlightbackground=fgColor,
            highlightthickness=1
        )
        self.frame.grid(row=0, column=1, sticky=tk.W)
        self.entry_var = tk.StringVar()
        fgColor = '#003366'
        if self.isFilterBtn:
            fgColor = '#ffffff'
        self.entry = tk.Entry(self.frame, 
                    textvariable=self.entry_var,
                    width=inputSize[0], 
                    font=("微软雅黑", inputSize[1]),
                    bg='#ffffff',
                    fg=fgColor,
                    relief=tk.FLAT, 
                    bd=0,
                    highlightthickness=0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=False)

        self.showDate = showDate
        self.showCombox = showCombox
        if True == showCombox:
            self.button = tk.Button(self.frame, text="▼", width=arrowSize[0], height = arrowSize[1], command=self.toggle_dropdown)
            self.button.pack(side=tk.LEFT,fill=tk.X, expand=True)

        # 下拉列表窗口（顶层窗口，浮动）
        self.listbox_win = None
        self.listbox = None

        # 绑定全局点击事件（点击其他地方关闭下拉）
        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.entry.bind('<FocusIn>', self.on_entry_focus_in)

        self.entry.bind('<Button-1>', self.on_entry_click)
        self.frame.bind_all("<Button-1>", self.on_global_click, add="+")

    def toggle_dropdown(self):
        if self.is_open:
            self.close_dropdown()
        else:
            self.open_dropdown()

    def on_entry_click(self, event):
        """输入框点击事件"""
        if self.showDate:
            today = datetime.now()
            result_date = f"{today.year}-{today.month:02d}-{int(today.day):02d}"
            self.entry_var.set(result_date)
            dateEntry = dateshow.DateTimePickerDialog(self.frame, self, "300x350")

    def open_dropdown(self):
        if self.listbox_win is not None:
            return

        # 计算下拉窗口位置：位于 entry 正下方
        x = self.frame.winfo_rootx()
        y = self.frame.winfo_rooty() + self.frame.winfo_height()
        width = self.frame.winfo_width()
        if self.boxPos:
            x = x + self.boxPos[0]
            y = y + self.boxPos[1]

        self.listbox_win = tk.Toplevel(self.parent)
        self.listbox_win.wm_overrideredirect(True)  # 无边框
        # self.listbox_win.geometry(f"{width}x{min(150, len(self.values)*20)}+{x}+{y}")
        self.listbox_win.geometry("{0}x{1}+{2}+{3}".format(self.boxSize[0], self.boxSize[1], x, y))
        self.listbox_win.attributes('-topmost', True)

        # 创建 Listbox 和滚动条
        frame = tk.Frame(self.listbox_win)
        frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.filtered_values = self.original_values.copy()
        # 填充数据
        for val in self.filtered_values:
            self.listbox.insert(tk.END, val)

        # 绑定双击事件
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        # 可选：绑定键盘回车选择
        self.listbox.bind("<Return>", self.on_double_click)
        # 点击下拉窗口外关闭的功能由全局点击事件处理

        self.is_open = True

    def close_dropdown(self):
        if self.listbox_win:
            self.listbox_win.destroy()
            self.listbox_win = None
            self.listbox = None
            self.is_open = False

    def on_double_click(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            self.set(value)
            if self.callBack:
                self.callBack(value, self.params)
        self.close_dropdown()

    def filter_values(self, search_text):
        """筛选选项"""
        if not search_text:
            self.filtered_values = self.original_values.copy()
            return
        
        search_lower = search_text.lower()
        self.filtered_values = [
            value for value in self.original_values 
            if search_lower in str(value).lower()
        ]

    def on_global_click(self, event):
        """点击下拉列表之外的任何地方，关闭下拉"""
        if not self.is_open or self.listbox_win is None:
            return
        x = self.listbox_win.winfo_rootx()
        y = self.listbox_win.winfo_rooty()
        w = self.listbox_win.winfo_width()
        h = self.listbox_win.winfo_height()
        inside = (x <= event.x_root <= x + w) and (y <= event.y_root <= y + h)
        fx = self.frame.winfo_rootx()
        fy = self.frame.winfo_rooty()
        fw = self.frame.winfo_width()
        fh = self.frame.winfo_height()
        in_frame = (fx <= event.x_root <= fx + fw) and (fy <= event.y_root <= fy + fh)
        if not inside and not in_frame:
            self.close_dropdown()

    def on_entry_focus_in(self, event):
        # 显示下拉列表
        if not self.is_open:
            self.open_dropdown()
    
    def on_key_release(self, event):
        """输入框按键释放事件"""
        # 忽略方向键和功能键
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 
                           'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
        
        # 获取当前输入
        current_text = self.entry_var.get()
        
        # 筛选选项
        self.filter_values(current_text)
        
        if self.is_open:
            self.update_listbox()
        else:
            self.open_dropdown()
        
    def update_listbox(self):
        if False == self.showCombox:
            return
        """更新列表框内容"""
        # 清空列表框
        self.listbox.delete(0, tk.END)
        
        # 添加筛选后的选项
        for i, value in enumerate(self.filtered_values):
            self.listbox.insert(tk.END, str(value))
        
        # 如果有选项，选择第一个
        if self.filtered_values:
            self.listbox.selection_set(0)
            self.listbox.see(0)

    def _callBack(self, value):
        if self.showDate:
            self.entry_var.set(value)

    def clear(self):
        """清空"""
        self.close_dropdown()

    def get(self):
        return self.entry_var.get()

    def set(self, value):
        if self.isFilterBtn:
            self.inputValue = value
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(value))
            self.entry_var.set(str(value))
            self.filtered_values = self.original_values.copy()
            current_value = self.get()
            if current_value:
                self.filter_values(current_value)
                self.update_listbox()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
