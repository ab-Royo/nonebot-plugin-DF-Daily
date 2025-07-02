# delta_report/__init__.py
import asyncio
from pathlib import Path
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot import require
from nonebot.exception import FinishedException
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic

from .data_source import fetch_data, fetch_ammo_trade_data
from .html_render import generate_html
from .trade_html_render import generate_ammo_trade_html

__plugin_meta__ = PluginMetadata(
    name="三角洲日报",
    description="获取三角洲行动每日战报和子弹交易推荐",
    usage=(
        "发送'三角洲日报'获取最新战报图片\n"
        "发送'三角洲倒子弹'获取最佳子弹交易推荐"
    ),
    type="application",
)

daily_report = on_command("三角洲日报", aliases={"三角洲战报", "三角洲每日战报"}, priority=10, block=True)
ammo_trade = on_command("三角洲倒子弹", aliases={"倒子弹", "子弹交易"}, priority=10, block=True)

@daily_report.handle()
async def handle_daily_report():
    # 获取数据
    data = await fetch_data()
    if not data:
        await daily_report.finish("获取战报数据失败，请稍后再试")
        return
    
    # 生成HTML
    html_content = generate_html(data)
    
    # 渲染为图片
    try:
        img = await html_to_pic(html_content, viewport={"width": 480, "height": 1200})
        await daily_report.finish(MessageSegment.image(img))
    except FinishedException:
        pass  # 直接忽略正常终止
    except Exception as e:
        logger.error(f"生成战报图片失败: {str(e)}")
        await daily_report.finish("生成战报图片失败，请查看日志")

@ammo_trade.handle()
async def handle_ammo_trade():
    """处理倒子弹命令"""
    # 获取数据
    try:
        data = await fetch_ammo_trade_data()
        if not data:
            await ammo_trade.finish("获取子弹交易数据失败，请稍后再试")
            return
        
        # 生成HTML
        html_content = generate_ammo_trade_html(data)
        
        # 渲染为图片 - 修正 template_path 问题
        img = await html_to_pic(
            html_content, 
            viewport={"width": 480, "height": 1200}
        )
        await ammo_trade.finish(MessageSegment.image(img))
    except FinishedException:
        pass  # 直接忽略正常终止
    except Exception as e:
        logger.error(f"生成子弹交易图片失败: {str(e)}")
        await ammo_trade.finish("生成子弹交易图片失败，请查看日志")