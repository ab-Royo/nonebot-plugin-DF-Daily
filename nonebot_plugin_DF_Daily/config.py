# delta_report/config.py
API_URLS = {
    "map_pwd": "https://tool.zxfps.com/api/sjz/map_pwd",
    "tech_center": "https://tool.zxfps.com/api/sjz/manufacture?t=1",
    "workbench": "https://tool.zxfps.com/api/sjz/manufacture?t=2",
    "pharmacy": "https://tool.zxfps.com/api/sjz/manufacture?t=3",
    "armor": "https://tool.zxfps.com/api/sjz/manufacture?t=4",
    "bullet_increase": "https://tool.zxfps.com/api/sjz/item_top?a=ammo&top=7-2",
    "bullet_decrease": "https://tool.zxfps.com/api/sjz/item_top?a=ammo&top=7-1",
    # 倒子弹API
    "ammo_trade": "https://tool.zxfps.com/api/sjz/ammo_zr_yc?grade=-1",
    "ammo_history": "https://tool.zxfps.com/api/sjz/hour?id={id}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

MAP_NAMES = ["零号大坝", "长弓溪谷", "巴克什", "航天基地"]
MAP_KEYS = ["a", "b", "c", "d"]

# 颜色映射
GRADE_COLORS = {
    0: "transparent",    # 无背景
    1: "#a3a8a8",        # 灰色
    2: "#0c9507",        # 绿色
    3: "#317fd1",        # 蓝色
    4: "#9b61c8",        # 紫色
    5: "#e8a64e",        # 橙色
    6: "#cb464a",        # 红色
}