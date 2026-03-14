import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import scripts.dateshow
from datetime import datetime

class StyledFilteredCombobox(ttk.Frame):
    """
    美化样式的筛选下拉框
    提供更好的视觉效果和用户体验
    """
    
    def __init__(self, parent, values=None, width=25, height=8, 
                 placeholder="请选择...", label_text=None, theme='light',
                 show_search_icon=True, show_down_icon = True, show_clear_button=True, **kwargs):
        """
        初始化美化样式的筛选下拉框
        
        Args:
            parent: 父窗口
            values: 选项列表
            width: 宽度
            height: 下拉列表高度
            placeholder: 占位文本
            label_text: 标签文本
            theme: 主题 ('light', 'dark', 'blue')
            show_search_icon: 是否显示搜索图标
            show_clear_button: 是否显示清空按钮
        """
        super().__init__(parent, **kwargs)
        
        # 参数设置
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.theme = theme
        self.show_search_icon = show_search_icon
        self.show_down_icon = show_down_icon
        self.show_clear_button = show_clear_button
        self.is_date_lab = False
        
        # 选项数据
        self.original_values = values or []
        self.filtered_values = self.original_values.copy()
        
        # 状态标志
        self.is_dropdown_visible = False
        self.is_placeholder = True
        
        # 设置样式
        self._setup_styles()
        
        # 创建界面
        self._create_widgets(label_text)
        
        # 绑定事件
        self._bind_events()
        
        # 初始化显示
        self._update_display()
    
    def _setup_styles(self):
        """设置样式"""
        # 定义不同主题的颜色
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'entry_border': '#cccccc',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#000000',
                'listbox_select_bg': '#0078d7',
                'listbox_select_fg': '#ffffff',
                'placeholder_fg': '#666666',
                'button_bg': '#f0f0f0',
                'button_fg': '#000000',
                'button_hover_bg': '#e0e0e0'
            },
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'entry_bg': '#3c3c3c',
                'entry_fg': '#ffffff',
                'entry_border': '#555555',
                'listbox_bg': '#3c3c3c',
                'listbox_fg': '#ffffff',
                'listbox_select_bg': '#0078d7',
                'listbox_select_fg': '#ffffff',
                'placeholder_fg': '#888888',
                'button_bg': '#555555',
                'button_fg': '#ffffff',
                'button_hover_bg': '#666666'
            },
            'blue': {
                'bg': '#e6f2ff',
                'fg': '#003366',
                'entry_bg': '#ffffff',
                'entry_fg': '#003366',
                'entry_border': '#99ccff',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#003366',
                'listbox_select_bg': '#3399ff',
                'listbox_select_fg': '#ffffff',
                'placeholder_fg': '#6699cc',
                'button_bg': '#99ccff',
                'button_fg': '#003366',
                'button_hover_bg': '#66b3ff'
            }
        }
        
        # 获取当前主题颜色
        self.colors = self.themes.get(self.theme, self.themes['light'])
    
    def _create_widgets(self, label_text):
        """创建界面组件"""
        # 如果有标签文本，创建标签
        if label_text:
            self.label = tk.Label(
                self, 
                text=label_text,
                bg=self.colors['bg'],
                fg=self.colors['fg'],
                font=('微软雅黑', 9)
            )
            self.label.grid(row=0, column=0, sticky=tk.W, padx=(0, 8), pady=2)
        
        # 创建主框架
        main_col = 1 if label_text else 0
        self.main_frame = tk.Frame(
            self,
            bg=self.colors['entry_bg'],
            highlightbackground=self.colors['entry_border'],
            highlightthickness=1
        )
        self.main_frame.grid(row=0, column=main_col, sticky=tk.W)
        
        # 创建输入框
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self.main_frame,
            textvariable=self.entry_var,
            width=self.width,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            font=('微软雅黑', 9),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.entry.pack(side=tk.LEFT, padx=(8, 0), pady=2)

        # 创建按钮框架
        self.button_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['entry_bg']
        )
        self.button_frame.pack(side=tk.LEFT, padx=(0, 2))
        
        # 创建搜索图标按钮（可选）
        if self.show_search_icon:
            self.search_btn = tk.Label(
                self.button_frame,
                text="🔍",
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                font=('Arial', 10),
                width=2,
                cursor='hand2'
            )
            self.search_btn.pack(side=tk.LEFT, padx=(0, 2), pady=1)
            self.search_btn.bind('<Button-1>', self._on_search_click)
        
        # 创建下拉按钮
        if self.show_down_icon:
            self.dropdown_btn = tk.Label(
                self.button_frame,
                text="▼",
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                font=('Arial', 10),
                width=2,
                cursor='hand2'
            )
            self.dropdown_btn.pack(side=tk.LEFT, padx=(0, 2), pady=1)
            self.dropdown_btn.bind('<Button-1>', self._on_dropdown_click)
        
        # 创建清空按钮（可选）
        if self.show_clear_button:
            self.clear_btn = tk.Label(
                self.button_frame,
                text="×",
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                font=('Arial', 10, 'bold'),
                width=2,
                cursor='hand2'
            )
            self.clear_btn.pack(side=tk.LEFT, pady=1)
            self.clear_btn.bind('<Button-1>', self._on_clear_click)
        
        # 创建下拉列表框（初始隐藏）
        self.listbox_frame = tk.Frame(
            self,
            bg=self.colors['listbox_bg'],
            highlightbackground=self.colors['entry_border'],
            highlightthickness=1,
            relief=tk.SOLID
        )
        
        # 创建列表框
        self.listbox = tk.Listbox(
            self.listbox_frame,
            bg=self.colors['listbox_bg'],
            fg=self.colors['listbox_fg'],
            selectbackground=self.colors['listbox_select_bg'],
            selectforeground=self.colors['listbox_select_fg'],
            font=('微软雅黑', 9),
            height=6,
            width=self.width,
            activestyle='none',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # 创建滚动条
        self.listbox_scrollbar = ttk.Scrollbar(
            self.listbox_frame,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox.configure(yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 初始隐藏下拉列表
        self.listbox_frame.grid_remove()
        
        # 设置组件背景色
        # self.configure(bg=self.colors['bg'])

    def _cancel_bind_events(self):
        if self.is_date_lab:
            self.entry.bind('<Key>', self._on_disable_keyboard)
    
    def _bind_events(self):
        """绑定事件"""
        # 输入框事件
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.entry.bind('<FocusOut>', self._on_entry_focus_out)
        self.entry.bind('<Return>', self._on_listbox_return)
        self.entry.bind('<Up>', self._on_entry_up)
        self.entry.bind('<Down>', self._on_entry_down)
        
        # 列表框事件
        self.listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
        self.listbox.bind('<Double-Button-1>', self._on_listbox_double_click)
        # self.listbox.bind('<Escape>', self._on_listbox_escape)
        
        # 按钮悬停效果
        for btn_name in ['search_btn', 'dropdown_btn', 'clear_btn']:
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                btn.bind('<Enter>', lambda e, b=btn_name: self._on_button_enter(e, b))
                btn.bind('<Leave>', lambda e, b=btn_name: self._on_button_leave(e, b))
        
        # 全局点击事件
        self.entry.bind('<Button-1>', self._on_entry_click)
        self.listbox.bind('<Button-1>', self._on_listbox_click)
    
    def _on_button_enter(self, event, button_name):
        """按钮鼠标进入事件"""
        if hasattr(self, button_name):
            btn = getattr(self, button_name)
            btn.configure(bg=self.colors['button_hover_bg'])
    
    def _on_button_leave(self, event, button_name):
        """按钮鼠标离开事件"""
        if hasattr(self, button_name):
            btn = getattr(self, button_name)
            btn.configure(bg=self.colors['button_bg'])
    
    def _on_search_click(self, event):
        """搜索按钮点击事件"""
        # 显示下拉列表并聚焦到输入框
        self._show_dropdown()
        self.entry.focus_set()
    
    def _on_dropdown_click(self, event):
        """下拉按钮点击事件"""
        if self.is_dropdown_visible:
            self._hide_dropdown()
        else:
            self._show_dropdown()
            # 更新列表框
            self._update_listbox()
    
    def _on_clear_click(self, event):
        """清空按钮点击事件"""
        self.clear()

    def _on_disable_keyboard(self, event):
        # 阻止所有键盘输入
        return "break"
    
    def _on_key_release(self, event):
        """输入框按键释放事件"""
        # 忽略方向键和功能键
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 
                           'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
        
        # 获取当前输入
        current_text = self.entry_var.get()
        
        # 如果是占位文本状态，清空占位文本
        if self.is_placeholder and current_text == self.placeholder:
            self.entry_var.set('')
            self.is_placeholder = False
            current_text = ''
        
        # 筛选选项
        self._filter_values(current_text)
        
        # 更新列表框
        self._update_listbox()
        
        # 如果有输入且有筛选结果，显示下拉列表
        if current_text and self.filtered_values:
            self._show_dropdown()
        elif not current_text and self.is_dropdown_visible:
            # 如果没有输入但下拉列表显示中，更新为所有选项
            self.filtered_values = self.original_values.copy()
            self._update_listbox()
    
    def _on_entry_focus_in(self, event):
        """输入框获得焦点事件"""
        # 如果是占位文本，清空并改变颜色
        if self.is_placeholder:
            self.entry_var.set('')
            self.is_placeholder = False
            self.entry.configure(fg=self.colors['entry_fg'])
        
        # 高亮边框
        self.main_frame.configure(highlightbackground='#0078d7')
        
        # 显示下拉列表
        self._show_dropdown()
        # 更新列表框
        self._update_listbox()
    
    def _on_entry_focus_out(self, event):
        """输入框失去焦点事件"""
        # 恢复边框颜色
        self.main_frame.configure(highlightbackground=self.colors['entry_border'])
        
        # 如果输入为空，恢复占位文本
        if not self.entry_var.get():
            self._set_placeholder()
        
        # 延迟隐藏下拉列表
        self.after(100, self._check_and_hide_dropdown)
    
    def _on_entry_escape(self, event):
        """输入框ESC事件"""
        self._hide_dropdown()
        if not self.entry_var.get():
            self._set_placeholder()
    
    def _on_entry_up(self, event):
        """输入框上箭头事件"""
        if self.is_dropdown_visible and self.filtered_values:
            self._navigate_listbox(-1)
        return 'break'
    
    def _on_entry_down(self, event):
        """输入框下箭头事件"""
        if self.is_dropdown_visible and self.filtered_values:
            self._navigate_listbox(1)

    def _call_back(self, event):
        if self.is_date_lab:
            self.entry_var.set(event)
    
    def _on_entry_click(self, event):
        """输入框点击事件"""
        # 点击输入框时显示下拉列表
        if not self.is_dropdown_visible:
            self._show_dropdown()
        if self.is_date_lab:
            self.is_placeholder = False
            today = datetime.now()
            result_date = f"{today.year}-{today.month:02d}-{int(today.day):02d}"
            self.entry_var.set(result_date)
            dateEntry = dateshow.DateTimePickerDialog(self.main_frame, self, "300x350")
    
    def _on_listbox_select(self, event):
        """列表框选择事件"""
        if self.listbox.curselection():
            self.selected_index = self.listbox.curselection()[0]
    
    def _on_listbox_double_click(self, event):
        """列表框双击事件"""
        if self.listbox.curselection():
            self._select_value(self.listbox.curselection()[0])

    def _on_listbox_return(self, event):
        """列表框回车事件"""
        if self.listbox.curselection():
            self._select_value(self.listbox.curselection()[0])
        return 'break'
    
    def _on_listbox_escape(self, event):
        """列表框ESC事件"""
        self._hide_dropdown()
        self.entry.focus_set()
    
    def _on_listbox_click(self, event):
        """列表框点击事件"""
        # 阻止事件冒泡
        return 'break'
    
    def _filter_values(self, search_text):
        """筛选选项"""
        if not search_text:
            self.filtered_values = self.original_values.copy()
            return
        
        search_lower = search_text.lower()
        self.filtered_values = [
            value for value in self.original_values 
            if search_lower in str(value).lower()
        ]
    
    def _update_listbox(self):
        if False == self.show_down_icon:
            return
        """更新列表框内容"""
        # 清空列表框
        self.listbox.delete(0, tk.END)
        
        # 添加筛选后的选项
        for i, value in enumerate(self.filtered_values):
            self.listbox.insert(tk.END, str(value))
            
            # # 设置交替行颜色
            # if i % 2 == 0:
            #     self.listbox.itemconfig(i, bg='#f8f8f8' if self.theme == 'light' else '#444444')
        
        # 如果有选项，选择第一个
        if self.filtered_values:
            self.listbox.selection_set(0)
            self.listbox.see(0)
            self.selected_index = 0
    
    def _update_display(self):
        """更新显示"""
        if not self.entry_var.get():
            self._set_placeholder()
    
    def _set_placeholder(self):
        """设置占位文本"""
        self.entry_var.set(self.placeholder)
        self.is_placeholder = True
        self.entry.configure(fg=self.colors['placeholder_fg'])
    
    def _show_dropdown(self):
        if False == self.show_down_icon:
            return
        """显示下拉列表"""
        if not self.is_dropdown_visible:
            self.is_dropdown_visible = True
            
            # 确保有数据
            if not self.filtered_values:
                self.filtered_values = self.original_values.copy()
                self._update_listbox()
            
            # 计算位置
            entry_col = 1 if hasattr(self, 'label') else 0
            
            # 显示在下拉按钮下方
            self.listbox_frame.grid(
                row=1, 
                column=entry_col, 
                columnspan=2 if hasattr(self, 'label') else 1,
                sticky=tk.W+tk.E, 
                pady=(5, 0)
            )
            
            # 确保列表框可见
            self.listbox_frame.lift()
            
            # 设置列表框高度（不超过指定行数）
            listbox_height = min(len(self.filtered_values), 4)
            self.listbox.configure(height=listbox_height)
    
    def _hide_dropdown(self):
        """隐藏下拉列表"""
        if self.is_dropdown_visible:
            self.is_dropdown_visible = False
            self.listbox_frame.grid_remove()
    
    def _check_and_hide_dropdown(self):
        """检查并隐藏下拉列表"""
        # 检查焦点是否还在组件内
        focused_widget = self.focus_get()
        if focused_widget not in [self.entry, self.listbox]:
            self._hide_dropdown()
    
    def _navigate_listbox(self, direction):
        """在列表框中导航"""
        if not self.filtered_values:
            return
        
        # 计算新索引
        new_index = self.selected_index + direction
        
        # 确保索引在有效范围内
        if new_index < 0:
            new_index = 0
        elif new_index >= len(self.filtered_values):
            new_index = len(self.filtered_values) - 1
        
        # 更新选择
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(new_index)
        self.listbox.see(new_index)
        self.selected_index = new_index
        
        # 更新输入框显示
        if self.filtered_values:
            self.entry_var.set(str(self.filtered_values[new_index]))
            self.is_placeholder = False
            self.entry.configure(fg=self.colors['entry_fg'])
    
    def _select_value(self, index):
        """选择指定索引的值"""
        if 0 <= index < len(self.filtered_values):
            value = self.filtered_values[index]
            self.entry_var.set(str(value))
            self.is_placeholder = False
            self.entry.configure(fg=self.colors['entry_fg'])
            self._hide_dropdown()
            self.entry.focus_set()
            
            # 触发选择事件
            self._trigger_event('<<ComboboxSelected>>')
    
    def _trigger_event(self, event_name):
        """触发事件"""
        self.event_generate(event_name)
    
    def get(self):
        """获取当前值"""
        if self.is_placeholder:
            return ''
        return self.entry_var.get()
    
    def set(self, value):
        """设置值"""
        if value:
            self.entry_var.set(str(value))
            self.is_placeholder = False
            self.entry.configure(fg=self.colors['entry_fg'])
        else:
            self._set_placeholder()
    
    def set_values(self, values):
        """设置选项列表"""
        self.original_values = values or []
        self.filtered_values = self.original_values.copy()
        
        # 更新当前显示
        current_value = self.get()
        if current_value:
            self._filter_values(current_value)
            self._update_listbox()
    
    def clear(self):
        """清空"""
        self._set_placeholder()
        self.filtered_values = self.original_values.copy()
        self._update_listbox()
        self._hide_dropdown()
    
    def bind(self, sequence=None, func=None, add=None):
        """绑定事件"""
        if sequence == '<<ComboboxSelected>>':
            super().bind(sequence, func, add)
        else:
            self.entry.bind(sequence, func, add)
    
    def set_theme(self, theme):
        """设置主题"""
        if theme in self.themes:
            self.theme = theme
            self.colors = self.themes[theme]
            self._apply_theme()
    
    def _apply_theme(self):
        """应用主题"""
        # 更新组件颜色
        self.configure(bg=self.colors['bg'])
        
        if hasattr(self, 'label'):
            self.label.configure(bg=self.colors['bg'], fg=self.colors['fg'])
        
        self.main_frame.configure(
            bg=self.colors['entry_bg'],
            highlightbackground=self.colors['entry_border']
        )
        
        self.entry.configure(bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        
        if self.is_placeholder:
            self.entry.configure(fg=self.colors['placeholder_fg'])
        
        self.button_frame.configure(bg=self.colors['entry_bg'])
        
        # 更新按钮
        for btn_name in ['search_btn', 'dropdown_btn', 'clear_btn']:
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                btn.configure(bg=self.colors['button_bg'], fg=self.colors['button_fg'])
        
        self.listbox_frame.configure(
            bg=self.colors['listbox_bg'],
            highlightbackground=self.colors['entry_border']
        )
        
        self.listbox.configure(
            bg=self.colors['listbox_bg'],
            fg=self.colors['listbox_fg'],
            selectbackground=self.colors['listbox_select_bg'],
            selectforeground=self.colors['listbox_select_fg']
        )

# 使用示例
def createComboBox(main_frame, products, showSearch, showDown, showClear, width):
    """美化样式示例"""
    # # 标题
    # tk.Label(
    #     main_frame, 
    #     text="美化样式的筛选下拉框示例", 
    #     font=('微软雅黑', 16, 'bold'),
    #     bg='#f5f5f5',
    #     fg='#333333'
    # ).pack(pady=(0, 30))
    
    combobox = StyledFilteredCombobox(
        main_frame,
        values=products,
        width=width,
        placeholder="",
        label_text="",
        theme='blue',
        show_search_icon=showSearch,
        show_down_icon= showDown,
        show_clear_button=showClear
    )

    # def get_selection(combobox, name):
    #     value = combobox.get()
    #     if value:
    #         tk.messagebox.showinfo("选择结果", f"{name}: {value}")
    #     else:
    #         tk.messagebox.showwarning("提示", f"请先选择{name}")

    # tk.Button(
    #     button_frame,
    #     text="获取选择1",
    #     command=lambda: get_selection(combobox1, "浅色主题"),
    #     font=('微软雅黑', 9),
    #     bg='#4CAF50',
    #     fg='white',
    #     activebackground='#45a049',
    #     padx=15,
    #     pady=5,
    #     relief=tk.FLAT,
    #     cursor='hand2'
    # ).pack(side=tk.LEFT, padx=(0, 10))
    return combobox
