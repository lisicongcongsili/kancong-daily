#!/usr/bin/env python3
"""
逐段向学城编辑器粘贴汇报内容
每段之间加 sleep，确保编辑器处理完毕
"""
import subprocess, time, json

def paste(text):
    # 转义单引号和反斜杠
    escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    script = f'(function(){{var editor=document.querySelector(".ProseMirror"); editor.focus(); var children=editor.children; var last=children[children.length-1]; last.click(); var dt=new DataTransfer(); dt.setData("text/plain","{escaped}"); var ev=new ClipboardEvent("paste",{{bubbles:true,cancelable:true,clipboardData:dt}}); editor.dispatchEvent(ev); return "ok"}})()'
    cmd = ["~/.catpaw/bin/catdesk", "browser-action", json.dumps({"action": "evaluate", "script": script})]
    result = subprocess.run(
        f"""~/.catpaw/bin/catdesk browser-action '{json.dumps({"action": "evaluate", "script": script})}'""",
        shell=True, capture_output=True, text=True
    )
    print(f"Pasted: {text[:40].replace(chr(10),' ')}... -> {result.stdout[-100:]}")
    time.sleep(1.5)

# 内容块列表，每块单独粘贴
blocks = [
    # 总结论
    "\n\n**【总结论】** 营销投放整体有效，外卖柜和信息流用户价值最高；CPS规模最大但渗透偏弱；小红书利益点驱动效果显著；三八节为全渠道效率洼地。当前缺LTV模型，建议尽快建立。\n\n",

    # 背景
    "## 背景\n\n评估覆盖小红书、信息流、CPS、免单玩法、外卖柜五个渠道，横跨双十一、双旦、年货节(CNY)、三八节四个大促节点。核心衡量维度：下单用户在官旗/非食/闪购三个业务圈层的复购率、购买频次及人均GTV，以同期非活动自然用户作为参照组。\n\n",

    # 论点一
    "## 论点一：所有渠道复购率均显著超参照组，营销投放有效\n\n60天闪购复购率：外卖柜 **94.3%**、信息流 **93.9%**、CPS **85.3%**、小红书 **80.0%**，参照组仅 **73.7%**，各渠道超出约 6~21pp。60天非食复购率：外卖柜 **66.4%**、信息流 **63.3%**，参照组 **45.3%**，超出约 18~21pp。\n\n",

    # 论点二
    "## 论点二：外卖柜 & 信息流用户价值最高，三层渗透最深\n\n官旗→非食渗透跨度：信息流和外卖柜的非食60天复购率（63.3%、66.4%）与官旗60天复购率（16.9%、18.9%）差距约 **45~47pp**，参照组差距仅 31pp，外溢效果显著。\n\n官旗→闪购渗透跨度：两渠道闪购60天复购率（93.9%、94.3%）与官旗差距高达 **77pp**，参照组差距仅 59pp。\n\n60天购买频次：信息流非食 5.08次/闪购 14.77次，外卖柜非食 5.32次/闪购 14.01次，均约为参照组（2.77次/5.99次）的 **2.4倍**。\n\n",

    # 论点三
    "## 论点三：CPS规模最大，官旗即时转化最强，但非食/闪购渗透偏弱\n\n规模：非食GTV达 **3.27亿**（全渠道最高），官旗订单量 1.56万单。即时转化：24h官旗复购率 **9.6%**，全渠道最高。渗透偏弱：60天非食复购率 **43.0%**，低于外卖柜 66.4% 和信息流 63.3%。瓶颈：商品覆盖不足，对比屈臣氏等竞品无优势，激励虽高但规模难以突破。\n\n",

    # 论点四
    '## 论点四：小红书利益点驱动效果显著，CNY最强，38节最弱\n\nCNY节点24h官旗复购率 **16.4%**，为小红书全年最高，归因为"满299送行李箱"强利益点精准触达年货节囤货及礼赠需求，是三八节（5.9%）的 **2.8倍**。38节为全渠道全节促效率最低，建议评估投入产出比。\n\n',

    # 论点五
    "## 论点五：外投用户中约25%为平台老用户，并非真正业态增量\n\n品牌新客占比：各渠道 92%~97%，与参照组（95.1%）基本持平，拉新效率相当。业态新客占比：外投渠道 **74%~78%**，低于参照组 89.6%，说明外投引入的用户中有相当比例已是平台老用户，只是官旗品牌新客，并非真正的业态增量。\n\n",

    # 行动建议
    "## 三项行动建议\n\n**建议1 · 建立LTV模型**：以60天GTV/获客成本作为核心ROI评估指标，当前仅有短期复购指标，无法判断各渠道回本周期。\n\n**建议2 · 优化38节投放**：38节为全渠道效率洼地，建议降低预算或设计更强利益点（参考CNY满赠模式）。\n\n**建议3 · 补强CPS商品覆盖**：CPS规模受商品覆盖制约，建议补充SKU或调整合作策略，释放规模潜力。\n\n",
]

for block in blocks:
    paste(block)

print("✅ 全部内容已粘贴完成")
