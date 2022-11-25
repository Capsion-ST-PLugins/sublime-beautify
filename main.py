# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2021-04-12 03:25:48.660601
# @file_path "D:\CPS\IDE\JS_SublmieText\Data\Packages\CPS"
# @Filename "main.py"
# @Description: 功能描述
#


import sublime
import sublime_plugin
import os
from imp import reload


if int(sublime.version()) < 3176:
    raise ImportWarning("本插件不支持当前版本，请使用大于等于3176的sublime Text")


from .core import utils
from .core import beautify

SETTING_KEY = "cps_beautify"
SETTING_FILE = "cps.sublime-settings"
SETTINGS = {}


def plugin_loaded():
    print(f"{__package__} 加载成功")

    global SETTINGS, SETTING_KEY
    SETTINGS = SettingManager(SETTING_KEY, SETTING_FILE)


class SettingManager:
    def __init__(self, setting_key: str, default_settings: str):
        self.setting_key = setting_key
        self.default_settings = default_settings
        self.default_settings_path = os.path.join(
            sublime.packages_path(), "cps-plugins", ".sublime", default_settings
        )

        self.data = {}

        sublime.set_timeout_async(self.plugin_loaded_async)

    def __getitem__(self, key: str, default={}):
        if key in self.data:
            return self.data.get(key, default)
        else:
            return {}

    def get(self, key: str, default={}):
        return self.__getitem__(key, default)

    def plugin_loaded_async(self):
        """
        @Description 监听用户配置文件
        """
        with open(self.default_settings_path, "r", encoding="utf8") as f:
            self.data = sublime.decode_value(f.read()).get(self.setting_key, {})

        # 读取现有配置
        user_settings = sublime.load_settings(self.default_settings)
        # 添加配置更新事件
        user_settings.add_on_change(self.default_settings, self._on_settings_change)
        # 将最新的配置更新到内部的data，最终以data为准
        utils.recursive_update(self.data, user_settings.to_dict()[self.setting_key])

    def _on_settings_change(self):
        new_settings = sublime.load_settings(self.default_settings).get(
            self.setting_key, {}
        )

        utils.recursive_update(self.data, new_settings)

        return self


# 常用声明周期钩子
class ExecEventListener(sublime_plugin.EventListener):
    # 文件保存前
    def on_pre_save(self, view):
        global SETTINGS
        if SETTINGS.get("format_on_save"):
            sublime.active_window().run_command("testt_beautify_currt_file")


# 重新加载
class CpsSyntaxBeautifyReloadCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        print(f"重新加载 {__package__}")
        reload(beautify)


# 格式化当前文件[支持格式： vue/js/ts/pug/stylus/css]
class CpsBeautifyCurrtFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax=None):
        # 异步格式化文件，不卡主程序执行
        sublime.set_timeout_async(self.beautify(edit, syntax), 0)

    def beautify(self, edit, syntax=None) -> None:
        global SETTINGS

        # 当前文件内容转换成字符串
        region = sublime.Region(0, self.view.size())
        buffer_str = self.view.substr(region)

        # 获取当前文件语法
        if not syntax:
            syntax = utils.check_stynax(self.view.file_name()) or utils.check_stynax(
                self.view.settings().get("syntax")
            )
        if not syntax:
            return print("无法识别当前语法： ", self.view.file_name())
        if syntax in ["python"]:
            return print("不支持当前文件语法解析： ", syntax)

        # 获取当前鼠标位置
        cursor_offset = self.view.sel()[0].a

        # 获取当前语法配置
        _settings = SETTINGS.get("global", {})
        syntax_options = SETTINGS.get(syntax, {})
        options = utils.recursive_update(_settings, syntax_options)

        # 传送数据
        res = beautify.beautifyStr(
            buffer_str, syntax, cursor_offset, options, self.view.file_name()
        )

        if res and isinstance(res, dict) and "formatted" in res:
            # 替换新数据到当前文件
            self.view.replace(edit, region, res["formatted"])
            if _settings.get("show_view_at_center_when_format", False):
                self.view.show_at_center(res["cursorOffset"])

            if int(res["cursorOffset"]) > 0:
                sublime.Region((res["cursorOffset"], res["cursorOffset"]))


# 已选内容的格式化
class CpsBeautifySelectRegionCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax=None):
        global SETTINGS

        # 检测选区
        if self.view.sel()[0].empty():
            return print("当前没有任何文件")

        # 检测语法是否支持
        if not syntax:
            return False

        # 当前文件第一个选区
        region = self.view.sel()[0]
        buffer_str = self.view.substr(region)

        # 获取当前鼠标位置
        cursor_offset = self.view.sel()[0].a

        # 获取当前配置
        options = SETTINGS.get(syntax, {})

        # 先格式化
        res = beautify.beautifyStr(buffer_str, syntax, cursor_offset, options)

        # 如果时html转换pug，
        if syntax == "html2pug":
            syntax = "pug"
            options = SETTINGS.get(syntax, {})
            res = beautify.beautifyStr(res["formatted"], syntax, cursor_offset, options)

        # 格式化成功
        if res and "formatted" in res:
            # 替换新数据到当前文件
            self.view.replace(edit, region, res["formatted"])
            self.view.show_at_center(res["cursorOffset"])

            if int(res["cursorOffset"]) > 0:
                sublime.Region((res["cursorOffset"], res["cursorOffset"]))
            print("格式化成功:", os.path.basename(self.view.file_name()))
