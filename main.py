# 作者：谢建波
# 文件目的：实现物品复活系统（大学生闲置物品交易平台）的核心功能，包括用户管理（注册、登录、审核）、物品分类管理（创建、修改类型及属性）、物品管理（添加、删除、搜索）等，满足管理员和普通用户的不同操作需求。

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import uuid


class ItemResurrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活 - 大学生闲置物品交易平台")
        self.root.geometry("1000x600")
        self.root.minsize(800, 600)

        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("SimHei", 10, "bold"))
        self.style.configure("Treeview", font=("SimHei", 10), rowheight=25)

        # 数据文件路径
        self.data_files = {
            "items": "items.json",
            "item_types": "item_types.json",
            "users": "users.json"
        }

        # 初始化数据
        self.items = self.load_data("items")
        self.item_types = self.load_data("item_types")
        self.users = self.load_data("users")
        self.current_user = None  # 当前登录用户

        # 初始化默认物品类型（如果为空）
        if not self.item_types:
            self.init_default_item_types()

        # 显示登录界面
        self.show_login_screen()

    def load_data(self, data_type):
        """加载指定类型的数据"""
        file_path = self.data_files[data_type]
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self, data_type, data):
        """保存数据到指定文件"""
        try:
            with open(self.data_files[data_type], "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("保存失败", f"无法保存数据: {str(e)}")
            return False

    def init_default_item_types(self):
        """初始化默认物品类型"""
        self.item_types = [
            {
                "type_id": 1,
                "name": "食品",
                "attributes": ["保质期", "数量"]
            },
            {
                "type_id": 2,
                "name": "书籍",
                "attributes": ["作者", "出版社", "ISBN"]
            },
            {
                "type_id": 3,
                "name": "工具",
                "attributes": ["品牌", "使用时长"]
            }
        ]
        self.save_data("item_types", self.item_types)

    def show_login_screen(self):
        """显示登录界面"""
        # 清空现有界面
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="物品复活系统", font=("SimHei", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # 用户名
        ttk.Label(frame, text="用户名:", font=("SimHei", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=25).grid(row=1, column=1, pady=5)

        # 密码
        ttk.Label(frame, text="密码:", font=("SimHei", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=25).grid(row=2, column=1, pady=5)

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="登录", command=self.login).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="注册", command=self.register).pack(side=tk.LEFT, padx=10)

    def login(self):
        """用户登录"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("输入错误", "用户名和密码不能为空")
            return

        # 查找用户
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                if user["status"] == "approved" or user["role"] == "admin":
                    self.current_user = user
                    self.create_main_widgets()
                    return
                else:
                    messagebox.showinfo("登录失败", "您的账号正在审核中，请等待管理员批准")
                    return

        messagebox.showwarning("登录失败", "用户名或密码错误")

    def register(self):
        """用户注册"""
        dialog = tk.Toplevel(self.root)
        dialog.title("用户注册")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
        y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
        dialog.geometry(f"+{x}+{y}")

        frame = ttk.Frame(dialog, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        # 注册表单
        ttk.Label(frame, text="用户名:", font=("SimHei", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        reg_user_var = tk.StringVar()
        ttk.Entry(frame, textvariable=reg_user_var, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="密码:", font=("SimHei", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        reg_pwd_var = tk.StringVar()
        ttk.Entry(frame, textvariable=reg_pwd_var, show="*", width=30).grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="住址:", font=("SimHei", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        reg_addr_var = tk.StringVar()
        ttk.Entry(frame, textvariable=reg_addr_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="手机:", font=("SimHei", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        reg_phone_var = tk.StringVar()
        ttk.Entry(frame, textvariable=reg_phone_var, width=30).grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="邮箱:", font=("SimHei", 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        reg_email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=reg_email_var, width=30).grid(row=4, column=1, pady=5)

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def save_registration():
            username = reg_user_var.get().strip()
            password = reg_pwd_var.get().strip()
            address = reg_addr_var.get().strip()
            phone = reg_phone_var.get().strip()
            email = reg_email_var.get().strip()

            # 验证
            if not all([username, password, address, phone, email]):
                messagebox.showwarning("输入错误", "所有字段不能为空")
                return

            # 检查用户名是否已存在
            if any(u["username"] == username for u in self.users):
                messagebox.showwarning("注册失败", "用户名已存在")
                return

            # 创建新用户
            new_user = {
                "user_id": str(uuid.uuid4()),
                "username": username,
                "password": password,
                "address": address,
                "phone": phone,
                "email": email,
                "role": "user",
                "status": "pending"  # 待审核
            }

            self.users.append(new_user)
            if self.save_data("users", self.users):
                messagebox.showinfo("注册成功", "注册已提交，请等待管理员批准")
                dialog.destroy()

        ttk.Button(btn_frame, text="注册", command=save_registration).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def create_main_widgets(self):
        """创建主界面"""
        # 清空现有界面
        for widget in self.root.winfo_children():
            widget.destroy()

        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部操作区
        top_frame = ttk.Frame(main_frame, padding="5")
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # 用户信息
        ttk.Label(top_frame, text=f"当前用户: {self.current_user['username']} ({self.current_user['role']})",
                  font=("SimHei", 10)).pack(side=tk.LEFT, padx=(0, 20))

        # 搜索区
        ttk.Label(top_frame, text="物品类型:", font=("SimHei", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.type_var = tk.StringVar()
        type_combobox = ttk.Combobox(top_frame, textvariable=self.type_var, state="readonly", width=15)
        type_combobox['values'] = ["全部"] + [t["name"] for t in self.item_types]
        type_combobox.current(0)
        type_combobox.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(top_frame, text="搜索:", font=("SimHei", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_btn = ttk.Button(top_frame, text="搜索", command=self.search_items)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 操作按钮
        logout_btn = ttk.Button(top_frame, text="退出登录", command=self.show_login_screen)
        logout_btn.pack(side=tk.RIGHT, padx=(5, 0))

        add_btn = ttk.Button(top_frame, text="添加物品", command=self.add_item)
        add_btn.pack(side=tk.RIGHT, padx=(5, 0))

        delete_btn = ttk.Button(top_frame, text="删除物品", command=self.delete_item)
        delete_btn.pack(side=tk.RIGHT, padx=(5, 0))

        refresh_btn = ttk.Button(top_frame, text="刷新列表", command=self.refresh_item_list)
        refresh_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # 管理员特有按钮
        if self.current_user["role"] == "admin":
            manage_type_btn = ttk.Button(top_frame, text="管理物品类型", command=self.manage_item_types)
            manage_type_btn.pack(side=tk.RIGHT, padx=(5, 0))

            approve_btn = ttk.Button(top_frame, text="审核用户", command=self.approve_users)
            approve_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # 物品列表
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # 创建表格
        columns = ("id", "name", "type", "description", "contact", "date")
        self.item_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        # 设置列标题
        self.item_tree.heading("id", text="ID")
        self.item_tree.heading("name", text="物品名称")
        self.item_tree.heading("type", text="物品类型")
        self.item_tree.heading("description", text="物品描述")
        self.item_tree.heading("contact", text="联系人")
        self.item_tree.heading("date", text="发布日期")

        # 设置列宽
        self.item_tree.column("id", width=60, anchor=tk.CENTER)
        self.item_tree.column("name", width=120, anchor=tk.W)
        self.item_tree.column("type", width=100, anchor=tk.W)
        self.item_tree.column("description", width=300, anchor=tk.W)
        self.item_tree.column("contact", width=150, anchor=tk.W)
        self.item_tree.column("date", width=120, anchor=tk.CENTER)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.item_tree.yview)
        self.item_tree.configure(yscroll=scrollbar.set)

        # 布局表格和滚动条
        self.item_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 底部状态栏
        status_frame = ttk.Frame(main_frame, padding="5")
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_var = tk.StringVar(value="就绪 - 共有 0 件物品")
        ttk.Label(status_frame, textvariable=self.status_var, font=("SimHei", 9)).pack(side=tk.LEFT)

        # 刷新列表
        self.refresh_item_list()

    def manage_item_types(self):
        """管理物品类型（管理员功能）"""
        dialog = tk.Toplevel(self.root)
        dialog.title("管理物品类型")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # 左侧类型列表
        left_frame = ttk.Frame(dialog, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="物品类型列表", font=("SimHei", 12)).pack(pady=10)

        self.type_tree = ttk.Treeview(left_frame, columns=("id", "name"), show="headings", height=10)
        self.type_tree.heading("id", text="ID")
        self.type_tree.heading("name", text="类型名称")
        self.type_tree.column("id", width=50, anchor=tk.CENTER)
        self.type_tree.column("name", width=150, anchor=tk.W)
        self.type_tree.pack(fill=tk.BOTH, expand=True)

        # 右侧属性编辑区
        right_frame = ttk.Frame(dialog, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="类型属性", font=("SimHei", 12)).pack(pady=10)

        self.type_name_var = tk.StringVar()
        ttk.Label(right_frame, text="类型名称:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(right_frame, textvariable=self.type_name_var).pack(fill=tk.X, pady=5)

        ttk.Label(right_frame, text="属性列表:").pack(anchor=tk.W, pady=(10, 0))
        self.attr_frame = ttk.Frame(right_frame)
        self.attr_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 属性输入区
        attr_input_frame = ttk.Frame(right_frame)
        attr_input_frame.pack(fill=tk.X, pady=10)

        self.new_attr_var = tk.StringVar()
        ttk.Entry(attr_input_frame, textvariable=self.new_attr_var, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(attr_input_frame, text="添加属性", command=self.add_type_attribute).pack(side=tk.LEFT, padx=5)

        # 按钮区
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=20)

        ttk.Button(btn_frame, text="新建类型", command=self.create_new_type).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存修改", command=self.save_type_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除类型", command=self.delete_item_type).pack(side=tk.LEFT, padx=5)

        # 加载类型列表
        self.refresh_type_list()

        # 绑定选择事件
        self.type_tree.bind("<<TreeviewSelect>>", self.on_type_select)

    def refresh_type_list(self):
        """刷新类型列表"""
        for item in self.type_tree.get_children():
            self.type_tree.delete(item)

        for type_info in self.item_types:
            self.type_tree.insert("", tk.END, values=(type_info["type_id"], type_info["name"]),
                                  iid=str(type_info["type_id"]))

    def on_type_select(self, event):
        """选择类型时加载属性"""
        selected = self.type_tree.selection()
        if not selected:
            return

        type_id = int(selected[0])
        type_info = next(t for t in self.item_types if t["type_id"] == type_id)

        # 清空现有属性
        for widget in self.attr_frame.winfo_children():
            widget.destroy()

        # 显示属性
        self.current_type_attrs = type_info["attributes"].copy()
        self.type_name_var.set(type_info["name"])
        self.current_editing_type_id = type_id

        for i, attr in enumerate(self.current_type_attrs):
            frame = ttk.Frame(self.attr_frame)
            frame.pack(fill=tk.X, pady=2)

            ttk.Label(frame, text=attr, width=15).pack(side=tk.LEFT)
            ttk.Button(frame, text="删除", command=lambda idx=i: self.remove_type_attribute(idx)).pack(side=tk.RIGHT)

    def add_type_attribute(self):
        """添加类型属性"""
        attr_name = self.new_attr_var.get().strip()
        if not attr_name:
            return

        if not hasattr(self, "current_type_attrs"):
            self.current_type_attrs = []

        self.current_type_attrs.append(attr_name)
        self.new_attr_var.set("")
        self.on_type_select(None)  # 刷新显示

    def remove_type_attribute(self, index):
        """删除类型属性"""
        if 0 <= index < len(self.current_type_attrs):
            del self.current_type_attrs[index]
            self.on_type_select(None)  # 刷新显示

    def create_new_type(self):
        """创建新类型"""
        new_id = 1
        if self.item_types:
            new_id = max(t["type_id"] for t in self.item_types) + 1

        self.item_types.append({
            "type_id": new_id,
            "name": "新类型",
            "attributes": []
        })

        self.save_data("item_types", self.item_types)
        self.refresh_type_list()
        self.type_tree.selection_set(str(new_id))
        self.on_type_select(None)

    def save_type_changes(self):
        """保存类型修改"""
        if not hasattr(self, "current_editing_type_id"):
            return

        type_name = self.type_name_var.get().strip()
        if not type_name:
            messagebox.showwarning("输入错误", "类型名称不能为空")
            return

        for i, t in enumerate(self.item_types):
            if t["type_id"] == self.current_editing_type_id:
                self.item_types[i]["name"] = type_name
                self.item_types[i]["attributes"] = self.current_type_attrs
                break

        self.save_data("item_types", self.item_types)
        self.refresh_type_list()
        messagebox.showinfo("成功", "类型修改已保存")

    def delete_item_type(self):
        """删除物品类型"""
        if not hasattr(self, "current_editing_type_id"):
            return

        # 检查是否有关联物品
        has_items = any(item["type_id"] == self.current_editing_type_id for item in self.items)
        if has_items:
            messagebox.showwarning("删除失败", "该类型下有关联物品，无法删除")
            return

        if messagebox.askyesno("确认删除", "确定要删除该类型吗？"):
            self.item_types = [t for t in self.item_types if t["type_id"] != self.current_editing_type_id]
            self.save_data("item_types", self.item_types)
            self.refresh_type_list()

            # 清空编辑区
            for widget in self.attr_frame.winfo_children():
                widget.destroy()
            self.type_name_var.set("")
            self.current_editing_type_id = None

    def approve_users(self):
        """审核用户（管理员功能）"""
        dialog = tk.Toplevel(self.root)
        dialog.title("审核用户")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="待审核用户列表", font=("SimHei", 12)).pack(pady=10)

        # 创建表格
        columns = ("username", "address", "phone", "email")
        user_tree = ttk.Treeview(dialog, columns=columns, show="headings")

        user_tree.heading("username", text="用户名")
        user_tree.heading("address", text="住址")
        user_tree.heading("phone", text="电话")
        user_tree.heading("email", text="邮箱")

        user_tree.column("username", width=100, anchor=tk.W)
        user_tree.column("address", width=150, anchor=tk.W)
        user_tree.column("phone", width=100, anchor=tk.W)
        user_tree.column("email", width=200, anchor=tk.W)

        # 滚动条
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=user_tree.yview)
        user_tree.configure(yscroll=scrollbar.set)

        user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # 加载待审核用户
        pending_users = [u for u in self.users if u["status"] == "pending"]
        for user in pending_users:
            user_tree.insert("", tk.END, values=(
                user["username"],
                user["address"],
                user["phone"],
                user["email"]
            ), iid=user["user_id"])

        # 按钮
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)

        def approve_selected():
            selected = user_tree.selection()
            if not selected:
                messagebox.showwarning("选择错误", "请先选择用户")
                return

            user_id = selected[0]
            for user in self.users:
                if user["user_id"] == user_id:
                    user["status"] = "approved"
                    break

            self.save_data("users", self.users)
            messagebox.showinfo("成功", "用户已批准")
            # 刷新列表
            for item in user_tree.get_children():
                user_tree.delete(item)
            for user in [u for u in self.users if u["status"] == "pending"]:
                user_tree.insert("", tk.END, values=(
                    user["username"],
                    user["address"],
                    user["phone"],
                    user["email"]
                ), iid=user["user_id"])

        ttk.Button(btn_frame, text="批准选中用户", command=approve_selected).pack(side=tk.LEFT, padx=10)

    def add_item(self):
        """添加新物品"""
        if not self.item_types:
            messagebox.showwarning("错误", "没有可用的物品类型，请联系管理员添加")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("添加物品")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # 滚动框架
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        frame = ttk.Frame(scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        # 物品类型选择
        ttk.Label(frame, text="物品类型:", font=("SimHei", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar()
        type_combobox = ttk.Combobox(frame, textvariable=type_var, state="readonly", width=25)
        type_combobox['values'] = [t["name"] for t in self.item_types]
        if self.item_types:
            type_combobox.current(0)
        type_combobox.grid(row=0, column=1, pady=5)

        # 存储属性变量的字典
        self.attr_vars = {}

        # 公共属性
        row = 1
        ttk.Label(frame, text="物品名称:", font=("SimHei", 10)).grid(row=row, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(frame, text="物品描述:", font=("SimHei", 10)).grid(row=row, column=0, sticky=tk.W, pady=5)
        desc_var = tk.StringVar()
        ttk.Entry(frame, textvariable=desc_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(frame, text="所在地址:", font=("SimHei", 10)).grid(row=row, column=0, sticky=tk.W, pady=5)
        addr_var = tk.StringVar()
        ttk.Entry(frame, textvariable=addr_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(frame, text="联系电话:", font=("SimHei", 10)).grid(row=row, column=0, sticky=tk.W, pady=5)
        phone_var = tk.StringVar()
        ttk.Entry(frame, textvariable=phone_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(frame, text="联系邮箱:", font=("SimHei", 10)).grid(row=row, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=email_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        # 动态属性框架
        self.dynamic_attr_frame = ttk.Frame(frame)
        self.dynamic_attr_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        # 加载选中类型的属性
        def load_type_attributes(event=None):
            # 清空现有属性
            for widget in self.dynamic_attr_frame.winfo_children():
                widget.destroy()

            # 获取选中的类型
            type_name = type_var.get()
            type_info = next(t for t in self.item_types if t["name"] == type_name)

            # 添加类型特有属性
            self.attr_vars.clear()
            for i, attr in enumerate(type_info["attributes"]):
                ttk.Label(self.dynamic_attr_frame, text=f"{attr}:", font=("SimHei", 10)).grid(
                    row=i, column=0, sticky=tk.W, pady=5)
                attr_var = tk.StringVar()
                ttk.Entry(self.dynamic_attr_frame, textvariable=attr_var, width=30).grid(
                    row=i, column=1, pady=5)
                self.attr_vars[attr] = attr_var

        # 绑定类型选择事件
        type_combobox.bind("<<ComboboxSelected>>", load_type_attributes)
        # 初始加载
        load_type_attributes()

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=15)
        row += 1

        def save_new_item():
            type_name = type_var.get()
            type_info = next(t for t in self.item_types if t["name"] == type_name)

            name = name_var.get().strip()
            description = desc_var.get().strip()
            address = addr_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()

            # 验证公共信息
            if not all([name, description, address, phone, email]):
                messagebox.showwarning("输入错误", "公共信息不能为空")
                return

            # 验证类型属性
            type_attrs = {}
            for attr, var in self.attr_vars.items():
                val = var.get().strip()
                if not val:
                    messagebox.showwarning("输入错误", f"{attr}不能为空")
                    return
                type_attrs[attr] = val

            # 生成ID
            new_id = 1
            if self.items:
                new_id = max(item["id"] for item in self.items) + 1

            # 当前日期
            current_date = datetime.now().strftime("%Y-%m-%d")

            # 创建新物品
            new_item = {
                "id": new_id,
                "name": name,
                "description": description,
                "address": address,
                "contact_phone": phone,
                "contact_email": email,
                "type_id": type_info["type_id"],
                "type_name": type_info["name"],
                "type_attrs": type_attrs,
                "date": current_date,
                "user_id": self.current_user["user_id"]
            }

            # 保存
            self.items.append(new_item)
            if self.save_data("items", self.items):
                messagebox.showinfo("成功", "物品添加成功!")
                dialog.destroy()
                self.refresh_item_list()

        ttk.Button(btn_frame, text="保存", command=save_new_item).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def delete_item(self):
        """删除物品"""
        selected_items = self.item_tree.selection()
        if not selected_items:
            messagebox.showwarning("选择错误", "请先选择要删除的物品!")
            return

        # 获取选中物品的ID
        item_id = int(self.item_tree.item(selected_items[0])["values"][0])
        item = next(i for i in self.items if i["id"] == item_id)

        # 权限检查
        if self.current_user["role"] != "admin" and item["user_id"] != self.current_user["user_id"]:
            messagebox.showwarning("权限不足", "您只能删除自己发布的物品")
            return

        # 确认删除
        if messagebox.askyesno("确认删除", "确定要删除这件物品吗?"):
            self.items = [item for item in self.items if item["id"] != item_id]
            if self.save_data("items", self.items):
                messagebox.showinfo("成功", "物品已删除!")
                self.refresh_item_list()

    def refresh_item_list(self):
        """刷新物品列表"""
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)

        # 添加所有物品
        for item in self.items:
            self.item_tree.insert("", tk.END, values=(
                item["id"],
                item["name"],
                item["type_name"],
                item["description"],
                f"{item['contact_phone']}\n{item['contact_email']}",
                item["date"]
            ))

        # 更新状态栏
        self.status_var.set(f"就绪 - 共有 {len(self.items)} 件物品")

    def search_items(self):
        """搜索物品"""
        keyword = self.search_var.get().strip().lower()
        selected_type = self.type_var.get()

        # 清空现有列表
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)

        # 筛选物品
        count = 0
        for item in self.items:
            # 类型筛选
            if selected_type != "全部" and item["type_name"] != selected_type:
                continue

            # 关键字筛选
            if keyword and keyword not in item["name"].lower() and keyword not in item["description"].lower():
                continue

            # 显示符合条件的物品
            self.item_tree.insert("", tk.END, values=(
                item["id"],
                item["name"],
                item["type_name"],
                item["description"],
                f"{item['contact_phone']}\n{item['contact_email']}",
                item["date"]
            ))
            count += 1

        # 更新状态栏
        self.status_var.set(f"搜索完成 - 找到 {count} 件匹配的物品")


if __name__ == "__main__":
    # 初始化管理员账号（如果不存在）
    if not os.path.exists("users.json"):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump([{
                "user_id": "admin",
                "username": "admin",
                "password": "admin123",
                "address": "管理员地址",
                "phone": "12345678901",
                "email": "admin@example.com",
                "role": "admin",
                "status": "approved"
            }], f, ensure_ascii=False, indent=2)

    root = tk.Tk()
    app = ItemResurrectionApp(root)
    root.mainloop()