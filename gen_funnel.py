"""
五盘链路框架 - Apple Dark 风格 v20
深灰背景 + 半透明卡片 + 克制渐变色
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1600, 920
# 苹果深色背景：不是纯黑，是 #1C1C1E（iOS systemBackground dark）
img = Image.new("RGB", (W, H), "#1C1C1E")
d = ImageDraw.Draw(img)

def font(size, bold=False):
    for p in ["/System/Library/Fonts/PingFang.ttc",
              "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try:    return ImageFont.truetype(p, size, index=(1 if bold else 0))
            except:
                try: return ImageFont.truetype(p, size)
                except: pass
    return ImageFont.load_default()

Fb = lambda s: font(s, True)
Fn = lambda s: font(s, False)

# ── Apple Dark 配色 ──
BG      = "#1C1C1E"   # systemBackground
CARD    = "#2C2C2E"   # secondarySystemBackground
CARD2   = "#3A3A3C"   # tertiarySystemBackground
SEP     = "#48484A"   # separator
WHITE   = "#FFFFFF"
LABEL   = "#EBEBF5"   # label
SEC     = "#EBEBF599" # secondaryLabel（用字符串近似）
DIM     = "#8E8E93"   # secondaryLabel
DIM2    = "#636366"   # tertiaryLabel

# Apple 系统色（克制、不过饱和）
C1 = ("#32D74B", "#1A3A20")   # green  → L1
C2 = ("#0A84FF", "#0A2A4A")   # blue   → L2
C3 = ("#BF5AF2", "#2D1A3A")   # purple → L3
C4 = ("#FF9F0A", "#3A2800")   # orange → L4
C5 = ("#30D5C8", "#0A2E2C")   # teal   → L5

LAYER_COLORS = [C1, C2, C3, C4, C5]

def ln(x1,y1,x2,y2,c,w=1):
    d.line([(x1,y1),(x2,y2)],fill=c,width=w)
def tx(x,y,s,f,c,anchor="la"):
    d.text((x,y),s,font=f,fill=c,anchor=anchor)
def rct(x,y,w,h,fill,r=6):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill)
def rct_o(x,y,w,h,fill,outline,r=6,lw=1):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=outline,width=lw)
def diamond(cx,cy,r,fill):
    d.polygon([(cx,cy-r),(cx+r,cy),(cx,cy+r),(cx-r,cy)],fill=fill)
def fit_text(text, avail, fnt):
    while text and d.textlength(text, font=fnt) > avail:
        text = text[:-1]
    return text

# ══════════════════════════════════════════════════════
# 标题栏
# ══════════════════════════════════════════════════════
rct(0,0,W,50,CARD,r=0)
ln(0,50,W,50,SEP)
d.rectangle([0,0,3,50],fill="#0A84FF")
tx(20,7,  "MARKETING FRAMEWORK  ·  FIVE-LAYER MODEL", Fn(9),  DIM)
tx(20,24, "商品营销五盘链路  ·  角色定位与作用框架",   Fb(16), WHITE)
for i,(col,lbl) in enumerate([("#32D74B","商运主导"),("#0A84FF","PM主导"),("#BF5AF2","PM+商运协同")]):
    bx=1060+i*166; rct(bx,20,8,8,col,r=2); tx(bx+12,20,lbl,Fn(9),DIM)
tx(1060,36,"供给筹备（商运）× 营销放大（PM）× 需求运营（PM）→ 目标达成",Fn(9),DIM2)

# ══════════════════════════════════════════════════════
# 布局
# ══════════════════════════════════════════════════════
CTOP  = 54
CBOT  = 848
CH    = CBOT - CTOP   # 794

DIV_X   = 756
PANEL_X = 768
PANEL_W = W - PANEL_X - 12
COL_W   = PANEL_W // 3

WH = 14
LH = (CH - WH) // 5   # 156

y1t = CTOP;   y1b = y1t + LH
y2t = y1b;    y2b = y2t + LH
y3t = y2b;    y3b = y3t + LH
ywt = y3b;    ywb = ywt + WH
y4t = ywb;    y4b = y4t + LH
y5t = y4b;    y5b = CBOT

S   = 50
FXL = 24
FXR = 744
XW  = (FXL,      FXR)
XM  = (FXL+S,    FXR-S)
XN  = (FXL+S*2,  FXR-S*2)

# ══════════════════════════════════════════════════════
# 左侧底板
# ══════════════════════════════════════════════════════
d.rectangle([FXL, CTOP, FXR+1, CBOT+1], fill=CARD)

# ══════════════════════════════════════════════════════
# 五层梯形
# ══════════════════════════════════════════════════════
LAYERS = [
    (y1t,y1b, XW,XM, 0, "OBJECTIVE","盘目标","商运主导",
     "活动目标拆解到品牌/商家粒度，对齐GMV/订单量/新客数口径，前中后分阶段管控"),
    (y2t,y2b, XM,XN, 1, "SUPPLY","盘供给","商运",
     "价格力保障（活动价/补贴/满减），货盘覆盖（门店/SKU/备货），供给质量达标"),
    (y3t,y3b, XN,XN, 2, "MARKETING","盘营销","PM",
     "福利设计（券/满减/赠品），玩法机制（限时/打卡/任务链），落地页转化路径"),
    (y4t,y4b, XN,XM, 3, "EXPOSURE","盘曝光","PM",
     "媒介矩阵（Banner/搜索/Push/短信/外投），按ROI分配资源，精准时段触达"),
    (y5t,y5b, XM,XW, 4, "USER","盘用户","PM",
     "新客/老客/流失客分层，场景洞察（时间/地点/状态），即时/计划/冲动需求分级"),
]

for idx,(yt,yb,xtop,xbot,ci,en,zh,role,desc) in enumerate(LAYERS):
    acc, dark = LAYER_COLORS[ci]
    xl_t,xr_t = xtop
    xl_b,xr_b = xbot
    lh = yb - yt
    is_rect = (xl_t==xl_b and xr_t==xr_b)

    # 梯形：用深色调背景（不是纯黑）
    pts = [(xl_t,yt),(xr_t,yt),(xr_b,yb),(xl_b,yb)]
    if is_rect:
        d.rectangle([xl_t,yt,xr_t,yb], fill=dark)
    else:
        d.polygon(pts, fill=dark)

    # 顶边彩色线（1px，克制）
    ln(xl_t, yt, xr_t, yt, acc, 1)

    # 左侧序号竖条（窄，24px）
    d.rectangle([xl_t, yt, xl_t+24, yb], fill=acc+"28")
    tx(xl_t+12, yt+lh//2, f"0{idx+1}", Fb(13), acc, anchor="mm")

    # 文字区
    tx_x = xl_t + 36

    # EN 小标 + 角色 pill
    tx(tx_x, yt+10, en, Fn(9), acc)
    rw = len(role)*7+12
    rx = tx_x + len(en)*6 + 10
    rct(rx, yt+7, rw, 15, acc+"22", r=3)
    tx(rx+rw//2, yt+14, role, Fb(8), acc, anchor="mm")

    # 中文大标（白色，干净）
    tx(tx_x, yt+26, zh, Fb(17), WHITE)

    # 描述文字（精确截断）
    f10 = Fn(10)
    r50 = min(50/lh, 1.0); xr_50 = xr_t + int((xr_b-xr_t)*r50)
    r63 = min(63/lh, 1.0); xr_63 = xr_t + int((xr_b-xr_t)*r63)
    line1 = fit_text(desc, xr_50-tx_x-10, f10)
    rest  = desc[len(line1):]
    line2 = fit_text(rest, xr_63-tx_x-10, f10) if rest else ""
    tx(tx_x, yt+48, line1, f10, DIM)
    if line2:
        tx(tx_x, yt+62, line2, f10, DIM)

# ── 腰部 ──
d.rectangle([XN[0], ywt, XN[1]+1, ywb+1], fill=CARD2)
ln(XN[0], ywt, XN[1], ywt, SEP, 1)
ln(XN[0], ywb, XN[1], ywb, SEP, 1)
diamond(XN[0]+16, ywt+WH//2, 4, "#BF5AF2")
tx(XN[0]+28, ywt+WH//2, "营销 = 商品 × 用户之间的放大器", Fn(10), DIM, anchor="lm")

# 左侧外框线
ln(FXL, CTOP, FXR, CTOP, SEP)
ln(FXL, CTOP, FXL, CBOT, SEP)
ln(FXR, CTOP, FXR, CBOT, SEP)

# ══════════════════════════════════════════════════════
# 双向弧形箭头（沿漏斗真实轮廓外侧）
# ══════════════════════════════════════════════════════
# 漏斗左边线关键点（x, y）：顶→收→最窄→最窄→展→底
# 对应层边界：y1t, y2t, y3t, ywt, y4t, y5t, CBOT
# 左边 x：XW[0], XM[0], XN[0], XN[0], XN[0], XM[0], XW[0]
# 右边 x：XW[1], XM[1], XN[1], XN[1], XN[1], XM[1], XW[1]

FUNNEL_YS = [y1t, y2t, y3t, ywt, y4b, y5t, CBOT]
FUNNEL_XL = [XW[0], XM[0], XN[0], XN[0], XN[0], XM[0], XW[0]]
FUNNEL_XR = [XW[1], XM[1], XN[1], XN[1], XN[1], XM[1], XW[1]]

ARROW_COLOR_L = "#0A84FF"   # 蓝色：目标/供给 → 推导用户需求（向下）
ARROW_COLOR_R = "#32D74B"   # 绿色：用户需求 → 反推目标与供给（向上）
ARROW_OFFSET  = 14          # 弧线距边线向外偏移量
ARROW_BULGE   = 22          # 弧线中段额外向外凸出量

def make_funnel_edge_pts(ys, xs, side, offset, bulge, n_per_seg=20):
    """
    沿漏斗边线（折线）生成平滑弧线点列。
    每段用二次贝塞尔：控制点在折线外侧凸出。
    offset: 整体向外偏移（贴边但不重叠）
    bulge:  每段中点额外向外凸出
    """
    sign = -1 if side == 'left' else 1
    all_pts = []
    for seg in range(len(ys)-1):
        y0, y1 = ys[seg], ys[seg+1]
        x0 = xs[seg]  + sign * offset
        x1 = xs[seg+1]+ sign * offset
        # 控制点：中间 y，x 取两端平均再向外凸出
        cx = (x0 + x1) / 2 + sign * bulge
        cy = (y0 + y1) / 2
        for k in range(n_per_seg + (1 if seg==len(ys)-2 else 0)):
            t = k / n_per_seg
            bx = (1-t)**2 * x0 + 2*(1-t)*t * cx + t**2 * x1
            by = (1-t)**2 * y0 + 2*(1-t)*t * cy + t**2 * y1
            all_pts.append((bx, by))
    return all_pts

def draw_arrowhead(draw, tip, frm, color, size=8):
    dx, dy = tip[0]-frm[0], tip[1]-frm[1]
    angle = math.atan2(dy, dx)
    a1, a2 = angle+math.radians(145), angle-math.radians(145)
    w1 = (tip[0]+size*math.cos(a1), tip[1]+size*math.sin(a1))
    w2 = (tip[0]+size*math.cos(a2), tip[1]+size*math.sin(a2))
    draw.polygon([tip, w1, w2], fill=color)

def draw_funnel_arrow(draw, side, color, direction, offset=ARROW_OFFSET, bulge=ARROW_BULGE, lw=2):
    xs = FUNNEL_XL if side == 'left' else FUNNEL_XR
    pts = make_funnel_edge_pts(FUNNEL_YS, xs, side, offset, bulge)
    for k in range(len(pts)-1):
        draw.line([pts[k], pts[k+1]], fill=color, width=lw)
    # 箭头：direction='down' → 底部箭头+顶部反向小箭头
    if direction == 'down':
        draw_arrowhead(draw, pts[-1], pts[-4], color)   # 底部主箭头
        draw_arrowhead(draw, pts[0],  pts[4],  color)   # 顶部反向箭头
    else:
        draw_arrowhead(draw, pts[0],  pts[4],  color)   # 顶部主箭头
        draw_arrowhead(draw, pts[-1], pts[-4], color)   # 底部反向箭头

draw_funnel_arrow(d, 'left',  ARROW_COLOR_L, 'down')
draw_funnel_arrow(d, 'right', ARROW_COLOR_R, 'up')

# 标注文字（在弧线外侧中段）
MID_Y = (CTOP + CBOT) // 2
# 左侧：蓝色，向下方向
LBL_X_L = FUNNEL_XL[3] - ARROW_OFFSET - ARROW_BULGE - 28
for i, txt in enumerate(["目标", "供给", "↓", "推导", "需求"]):
    tx(LBL_X_L, MID_Y - 36 + i*17, txt, Fn(9), ARROW_COLOR_L, anchor="mm")

# 右侧：绿色，向上方向
LBL_X_R = FUNNEL_XR[3] + ARROW_OFFSET + ARROW_BULGE + 28
for i, txt in enumerate(["需求", "反推", "↑", "目标", "供给"]):
    tx(LBL_X_R, MID_Y - 36 + i*17, txt, Fn(9), ARROW_COLOR_R, anchor="mm")

# ══════════════════════════════════════════════════════
# 分隔线
# ══════════════════════════════════════════════════════
ln(DIV_X, CTOP, DIV_X, CBOT, SEP)

# ══════════════════════════════════════════════════════
# 右侧面板
# ══════════════════════════════════════════════════════
tx(PANEL_X, CTOP+4, "DETAILED BREAKDOWN  ·  各层精细化拆解", Fn(9), DIM2)
ln(PANEL_X, CTOP+16, PANEL_X+PANEL_W, CTOP+16, SEP)

BLOCK_H  = [LH, LH, LH+WH, LH, CBOT-y5t]
block_ys = [y1t, y2t, y3t, y4t, y5t]

RIGHT_BLOCKS = [
    {"ci":0,"en":"01  OBJECTIVE","title":"拆解目标 · 对齐口径 · 分配责任",
     "cols":[
         ("目标分层",  ["总目标 → 品类 → 品牌/商家","逐级拆解，可追踪可归因"]),
         ("口径对齐",  ["GMV / GTV / 订单量 / 新客数","PM与商运统一计量标准"]),
         ("时间节点",  ["活动前/中/后分阶段目标","节奏管控，防止目标失焦"]),
     ],"insight":None},
    {"ci":1,"en":"02  SUPPLY","title":"价格力 · 货盘覆盖 · 库存保障",
     "cols":[
         ("价格机制",["活动价 / 补贴 / 满减门槛","价格力是转化的底座"]),
         ("货盘覆盖",["门店数 / SKU覆盖率 / 备货量","防断货，保障活动履约"]),
         ("供给质量",["评分 / 履约率 / 时效达标","供给体验决定复购口碑"]),
     ],"insight":"洞察：没有有竞争力的货盘，再好的营销也是空炮"},
    {"ci":2,"en":"03  MARKETING  ·  放大器","title":"福利设计 · 玩法机制 · 转化路径",
     "cols":[
         ("福利设计",["券 / 满减 / 赠品 / 积分","福利强度决定决策速度"]),
         ("玩法机制",["限时 / 打卡 / 任务链 / 裂变","稀缺感+参与感提升留存"]),
         ("转化路径",["落地页→加购→下单→支付","每步漏斗专项优化"]),
     ],"insight":"洞察：放大倍数 = 福利强度 × 玩法创意 × 转化效率"},
    {"ci":3,"en":"04  EXPOSURE","title":"媒介矩阵 · 资源分配 · 触达效率",
     "cols":[
         ("媒介矩阵",["Banner / 搜索词 / Push","短信 / 外投，分层触达"]),
         ("资源分配",["按ROI优先级分配坑位","高价值用户优先高质量媒介"]),
         ("触达时机",["活跃时段 / 场景触发","时机决定打开率"]),
     ],"insight":"洞察：触达精准度 × 触达量级 = 实际影响力"},
    {"ci":4,"en":"05  USER","title":"用户分层 · 场景洞察 · 需求分级",
     "cols":[
         ("用户分层",["新客 / 老客 / 流失客","差异化权益，精准圈选"]),
         ("场景洞察",["时间/地点/状态/触发点","场景匹配度决定转化上限"]),
         ("需求分级",["即时 / 计划 / 冲动需求","对应不同营销策略"]),
     ],"insight":None},
]

for i, blk in enumerate(RIGHT_BLOCKS):
    y   = block_ys[i]
    h   = BLOCK_H[i]
    ci  = blk["ci"]
    acc, dark = LAYER_COLORS[ci]
    has_ins = blk["insight"] is not None
    ins_h   = 20
    inner_h = h - (ins_h if has_ins else 0)

    # 卡片：CARD2 背景，SEP 边框
    rct_o(PANEL_X, y, PANEL_W, h, CARD2, SEP, r=4, lw=1)
    # 左侧彩色竖条（3px）
    d.rectangle([PANEL_X, y, PANEL_X+3, y+h], fill=acc)

    # 内容均匀分布
    total_fixed = 12 + 16 + 14 + 13 + 13
    gap = max(6, (inner_h - total_fixed) // 4)

    ry0 = y + gap//2
    ry1 = ry0 + 12 + gap//2
    ry2 = ry1 + 16 + gap
    ry3 = ry2 + 14 + gap//2
    ry4 = ry3 + 13 + gap//2

    tx(PANEL_X+12, ry0, blk["en"],    Fn(9),  acc)
    tx(PANEL_X+12, ry1, blk["title"], Fb(12), WHITE)

    for ci2,(ctitle,clines) in enumerate(blk["cols"]):
        cx = PANEL_X+12+ci2*COL_W
        if ci2>0:
            ln(PANEL_X+ci2*COL_W, ry2, PANEL_X+ci2*COL_W, y+inner_h-4, SEP)
        tx(cx, ry2, ctitle,    Fb(11), LABEL)
        tx(cx, ry3, clines[0], Fn(10), DIM)
        if len(clines)>1:
            tx(cx, ry4, clines[1], Fn(10), DIM2)

    if has_ins:
        iy = y + inner_h
        d.rectangle([PANEL_X+3, iy, PANEL_X+PANEL_W-1, iy+ins_h], fill=acc+"18")
        ln(PANEL_X+3, iy, PANEL_X+PANEL_W-3, iy, acc+"55")
        diamond(PANEL_X+12, iy+ins_h//2, 4, acc)
        tx(PANEL_X+22, iy+ins_h//2, blk["insight"], Fn(9), acc, anchor="lm")

# ══════════════════════════════════════════════════════
# 底部总结栏
# ══════════════════════════════════════════════════════
FOOT_Y = CBOT + 6
ln(20, CBOT+2, W-20, CBOT+2, SEP)
BW = (W-44)//3
for bi,(col,title,lines) in enumerate([
    ("#32D74B","供给侧筹备  ·  商运主导",["目标→供给：自上而下拆解","货盘与价格机制支撑目标达成"]),
    ("#BF5AF2","营销放大器  ·  PM主导",  ["营销层连接供给与用户","福利玩法将供给转化为购买"]),
    ("#0A84FF","需求侧运营  ·  PM主导",  ["用户→曝光：自下而上洞察","触达策略匹配用户场景需求"]),
]):
    bx = 22+bi*(BW+2)
    rct_o(bx, FOOT_Y, BW, 56, CARD2, SEP, r=4, lw=1)
    d.rectangle([bx, FOOT_Y, bx+3, FOOT_Y+56], fill=col)
    tx(bx+12, FOOT_Y+8,  title,   Fb(11), WHITE)
    for li,lt in enumerate(lines):
        tx(bx+12, FOOT_Y+24+li*15, lt, Fn(10), DIM)

tx(22, H-12, "五盘链路框架  ·  商品营销角色定位  ·  供给筹备 × 营销放大 × 需求运营", Fn(9), DIM2)

out = "/Users/lisicong/Desktop/kancong-daily/marketing_funnel.png"
img.save(out, "PNG", dpi=(144,144))
print(f"saved {W}x{H}  LH={LH}")
