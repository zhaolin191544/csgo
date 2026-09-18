#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 slides.md 中使用的全部图表（SVG）。
数据来源：《KAOT 模板在小规模 TPC-C 场景下的适配性分析》
用法：python3 scripts/gen_charts.py   ->  public/charts/*.svg
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "charts")
os.makedirs(OUT, exist_ok=True)

FONT = "'Noto Sans SC','PingFang SC','Microsoft YaHei','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,monospace"

FG      = "#e8eaed"   # 主文字
MUTED   = "#9aa0a6"   # 次级文字
GRID    = "rgba(255,255,255,0.08)"
AXIS    = "rgba(255,255,255,0.22)"

C_A     = "#94a3b8"   # A 默认 1GB
C_B     = "#27FF64"   # B KAOT 全量
C_C1    = "#38bdf8"   # C1 / F  8GB
C_D     = "#a78bfa"   # D
C_E     = "#fbbf24"   # E / E'
C_BAD   = "#f87171"   # 负收益 / 劣化
C_DIM   = "#475569"


def head(w, h, title=None, sub=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         f'font-family="{FONT}">']
    s.append(f'<rect width="{w}" height="{h}" fill="none"/>')
    if title:
        s.append(f'<text x="0" y="20" fill="{FG}" font-size="17" font-weight="600">{title}</text>')
    if sub:
        # 无标题时条件行上移到标题位（幻灯片的 ## 标题已承担命名职责）
        s.append(f'<text x="0" y="{41 if title else 22}" fill="{MUTED}" font-size="12.5">{sub}</text>')
    return s


def write(name, parts):
    parts.append("</svg>")
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("wrote", path)


def fmt(n):
    return f"{n:,.0f}"


def legend(x, y, items, size=12):
    """items: [(color,label), ...] 横向图例"""
    out, cx = [], x
    for color, label in items:
        out.append(f'<rect x="{cx}" y="{y-8}" width="11" height="11" rx="2.5" fill="{color}"/>')
        out.append(f'<text x="{cx+17}" y="{y+1}" fill="{MUTED}" font-size="{size}">{label}</text>')
        cx += 17 + len(label) * (size * 0.95 if any('一' <= c <= '鿿' for c in label) else size * 0.55) + 26
    return out


# ---------------------------------------------------------------- fig1
def fig1():
    """阶段一：基线 vs KAOT（16 终端，未还原数据）"""
    W, H = 880, 370
    s = head(W, H, None,
             "tpmC 均值 ± 标准差，n=3 · Welch t = 6.64, p ≈ 0.003")
    x0, y0, pw, ph = 70, 78, 430, 230
    rows = [("基线（默认参数）", 47152.6, 1990.8, C_A), ("KAOT 全量模板", 35599.9, 2261.1, C_BAD)]
    vmax = 56000
    # 网格
    for i in range(5):
        v = vmax * i / 4
        y = y0 + ph - ph * i / 4
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{x0-10}" y="{y+4:.1f}" fill="{MUTED}" font-size="11" text-anchor="end" '
                 f'font-family="{MONO}">{fmt(v)}</text>')
    bw = 96
    for i, (label, v, sd, color) in enumerate(rows):
        cx = x0 + pw * (0.3 + 0.42 * i)
        bh = ph * v / vmax
        y = y0 + ph - bh
        s.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" rx="4" fill="{color}" opacity="0.85"/>')
        # 误差棒
        hi, lo = y0 + ph - ph * (v + sd) / vmax, y0 + ph - ph * (v - sd) / vmax
        s.append(f'<line x1="{cx}" y1="{hi:.1f}" x2="{cx}" y2="{lo:.1f}" stroke="{FG}" stroke-width="1.4" opacity="0.7"/>')
        for yy in (hi, lo):
            s.append(f'<line x1="{cx-11}" y1="{yy:.1f}" x2="{cx+11}" y2="{yy:.1f}" stroke="{FG}" stroke-width="1.4" opacity="0.7"/>')
        s.append(f'<text x="{cx}" y="{hi-12:.1f}" fill="{FG}" font-size="15" font-weight="700" '
                 f'text-anchor="middle" font-family="{MONO}">{fmt(v)}</text>')
        s.append(f'<text x="{cx}" y="{y0+ph+20}" fill="{FG}" font-size="12.5" text-anchor="middle">{label}</text>')
        s.append(f'<text x="{cx}" y="{y0+ph+38}" fill="{MUTED}" font-size="11" text-anchor="middle" '
                 f'font-family="{MONO}">CV {sd/v*100:.1f}%</text>')
    s.append(f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="{AXIS}"/>')
    # 降幅标注
    ax, ay = x0 + pw * 0.3, y0 + ph - ph * 47152.6 / vmax
    bx, by = x0 + pw * 0.72, y0 + ph - ph * 35599.9 / vmax
    s.append(f'<path d="M{ax+bw/2+6},{ay-2} L{bx+bw/2+6},{ay-2} L{bx+bw/2+6},{by-2}" fill="none" '
             f'stroke="{C_BAD}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    s.append(f'<text x="{bx+bw/2+16}" y="{(ay+by)/2:.1f}" fill="{C_BAD}" font-size="22" font-weight="700" '
             f'font-family="{MONO}">−24.5%</text>')
    # 右侧结论卡
    cx0 = 590
    s.append(f'<rect x="{cx0}" y="78" width="290" height="230" rx="10" fill="rgba(248,113,113,0.07)" '
             f'stroke="rgba(248,113,113,0.3)"/>')
    s.append(f'<text x="{cx0+18}" y="106" fill="{C_BAD}" font-size="13" font-weight="700">当时的结论</text>')
    lines = ["KAOT 调优后性能下降 24.5%", "", "疑点（未排除）：", "· 基线三轮逐次下降 ≈3%", "· 两组测试相隔两天",
             "· 基线 shared_buffers 未记录"]
    for i, t in enumerate(lines):
        c = MUTED if t.startswith("·") or t.startswith("疑点") else FG
        s.append(f'<text x="{cx0+18}" y="{132+i*23}" fill="{c}" font-size="12.5">{t}</text>')
    s.append(f'<text x="{cx0+18}" y="292" fill="{C_E}" font-size="12.5" font-weight="600">→ 该结论后被推翻</text>')
    write("fig1_stage1.svg", s)


# ---------------------------------------------------------------- fig2
def fig2():
    """阶段二：每轮还原数据前后对比"""
    W, H = 880, 360
    s = head(W, H, None,
             "同一份配置，只改测试方法，不改任何数据库参数")
    x0, y0, pw, ph = 70, 82, 560, 208
    groups = [("默认参数", 47153, 51579, "+9.4%", C_A), ("KAOT 全量", 35600, 48883, "+37.3%", C_B)]
    vmax = 60000
    for i in range(4):
        v = vmax * i / 3
        y = y0 + ph - ph * i / 3
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{x0-10}" y="{y+4:.1f}" fill="{MUTED}" font-size="11" text-anchor="end" '
                 f'font-family="{MONO}">{fmt(v)}</text>')
    bw = 74
    for gi, (label, before, after, delta, color) in enumerate(groups):
        gx = x0 + pw * (0.26 + 0.46 * gi)
        for bi, (v, tag, op) in enumerate([(before, "未还原", 0.28), (after, "已还原", 0.92)]):
            cx = gx + (bi - 0.5) * (bw + 16)
            bh = ph * v / vmax
            y = y0 + ph - bh
            s.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" rx="4" '
                     f'fill="{color}" opacity="{op}"/>')
            s.append(f'<text x="{cx}" y="{y-9:.1f}" fill="{FG}" font-size="13" font-weight="700" '
                     f'text-anchor="middle" font-family="{MONO}">{fmt(v)}</text>')
            s.append(f'<text x="{cx}" y="{y0+ph+18}" fill="{MUTED}" font-size="11.5" text-anchor="middle">{tag}</text>')
        s.append(f'<text x="{gx}" y="{y0+ph+40}" fill="{FG}" font-size="13.5" font-weight="600" '
                 f'text-anchor="middle">{label}</text>')
        yb = y0 + ph - ph * before / vmax
        ya = y0 + ph - ph * after / vmax
        s.append(f'<text x="{gx}" y="{ya-34:.1f}" fill="{color}" font-size="17" font-weight="700" '
                 f'text-anchor="middle" font-family="{MONO}">{delta}</text>')
    s.append(f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="{AXIS}"/>')
    cx0 = 660
    s.append(f'<rect x="{cx0}" y="82" width="220" height="208" rx="10" fill="rgba(39,255,100,0.06)" '
             f'stroke="rgba(39,255,100,0.28)"/>')
    for i, t in enumerate(["KAOT 涨 37.3%", "默认只涨 9.4%", "", "−24.5% 中的绝大部分", "来自数据磨损，", "而非参数本身。"]):
        c = C_B if i == 0 else (FG if i < 3 else MUTED)
        w = "700" if i == 0 else "400"
        s.append(f'<text x="{cx0+18}" y="{112+i*26}" fill="{c}" font-size="13" font-weight="{w}">{t}</text>')
    s.append(f'<text x="{cx0+18}" y="272" fill="{C_E}" font-size="13" font-weight="600" '
             f'font-family="{MONO}">同口径复测：−5.2%</text>')
    write("fig2_methodology.svg", s)


# ---------------------------------------------------------------- fig3
def fig3():
    """阶段三：16 终端七组消融"""
    W, H = 880, 444
    s = head(W, H, None,
             "相对 A 组（默认 1GB）的 tpmC 变化")
    rows = [
        ("A",  "默认 1GB",            51579, 0.0,   C_A),
        ("B",  "KAOT 全量 151GB",     48883, -5.2,  C_BAD),
        ("C1", "B 但 buffer→8GB",     59092, 14.6,  C_B),
        ("C2", "B 但降刷盘频率",       47715, -7.5,  C_BAD),
        ("D",  "8GB + 三项裁剪",       58329, 13.1,  C_C1),
        ("E",  "安全子集 FPW off",     55179, 7.0,   C_E),
        ("E'", "安全子集 FPW on",      56943, 10.4,  C_E),
    ]
    y0, rh = 78, 42
    pl, pr = 300, 862          # 绘图区左右边界
    lo, hi = -10.0, 19.0       # 百分比映射范围
    scale = (pr - pl) / (hi - lo)
    zero = pl + (0 - lo) * scale
    bottom = y0 + rh * len(rows) - 8
    s.append(f'<line x1="{zero:.1f}" y1="{y0-8}" x2="{zero:.1f}" y2="{bottom}" stroke="{AXIS}" stroke-width="1.2"/>')
    for g in (-10, -5, 5, 10, 15):
        x = zero + g * scale
        s.append(f'<line x1="{x:.1f}" y1="{y0-8}" x2="{x:.1f}" y2="{bottom}" stroke="{GRID}"/>')
        s.append(f'<text x="{x:.1f}" y="{bottom+17}" fill="{MUTED}" font-size="10.5" '
                 f'text-anchor="middle" font-family="{MONO}">{g:+d}%</text>')
    for i, (code, desc, tpmc, pct, color) in enumerate(rows):
        y = y0 + i * rh
        s.append(f'<text x="14" y="{y+15}" fill="{FG}" font-size="14" font-weight="700" font-family="{MONO}">{code}</text>')
        s.append(f'<text x="48" y="{y+15}" fill="{MUTED}" font-size="12">{desc}</text>')
        s.append(f'<text x="252" y="{y+15}" fill="{FG}" font-size="12.5" text-anchor="end" font-family="{MONO}">{fmt(tpmc)}</text>')
        if abs(pct) < 0.01:
            s.append(f'<text x="{zero+9:.1f}" y="{y+15}" fill="{MUTED}" font-size="12">基准</text>')
            continue
        w = abs(pct) * scale
        bx = zero if pct > 0 else zero - w
        s.append(f'<rect x="{bx:.1f}" y="{y}" width="{w:.1f}" height="20" rx="3.5" fill="{color}" opacity="0.88"/>')
        lx = bx + w + 8 if pct > 0 else bx - 8
        anc = "start" if pct > 0 else "end"
        s.append(f'<text x="{lx:.1f}" y="{y+15}" fill="{color}" font-size="13" font-weight="700" '
                 f'text-anchor="{anc}" font-family="{MONO}">{pct:+.1f}%</text>')
    # C1 / C2 判别对高亮
    s.append(f'<rect x="8" y="{y0+2*rh-6}" width="854" height="{2*rh-4}" rx="8" fill="rgba(39,255,100,0.05)" '
             f'stroke="{C_B}" stroke-dasharray="5 4" opacity="0.6"/>')
    s.append(f'<text x="14" y="{H-38}" fill="{FG}" font-size="12.5">'
             f'C1 只把 buffer 从 151GB 改为 8GB → <tspan fill="{C_B}" font-weight="700">+14.6%</tspan>；'
             f'C2 保留 151GB、只把刷盘频率降回默认 → <tspan fill="{C_BAD}" font-weight="700">−7.5%</tspan></text>')
    s.append(f'<text x="14" y="{H-15}" fill="{MUTED}" font-size="11.5">'
             f'⇒ 问题出在 buffer 池容量本身，与刷盘频率无关——「大池 + 高频扫描组合失配」的假设被 C2 排除</text>')
    write("fig3_ablation16.svg", s)


# ---------------------------------------------------------------- fig4
def fig4():
    """阶段四：并发扫描折线图"""
    W, H = 880, 400
    s = head(W, H, None,
             "模板收益高度依赖并发量级——前三阶段恰好都落在 16 终端")
    x0, y0, pw, ph = 76, 86, 496, 232
    xs = [16, 32, 64, 100]
    series = [
        ("A  默认 1GB",        [55840, 64546, 76983, 81954], C_A),
        ("B  KAOT 全量 151GB", [59226, 107735, 154527, 170522], C_B),
        ("C1 KAOT + 8GB",      [60623, 103675, 155990, 169968], C_C1),
    ]
    vmax = 190000
    for i in range(5):
        v = vmax * i / 4
        y = y0 + ph - ph * i / 4
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{x0-10}" y="{y+4:.1f}" fill="{MUTED}" font-size="11" text-anchor="end" '
                 f'font-family="{MONO}">{fmt(v)}</text>')
    def px(i): return x0 + pw * i / (len(xs) - 1)
    def py(v): return y0 + ph - ph * v / vmax
    for i, t in enumerate(xs):
        s.append(f'<text x="{px(i):.1f}" y="{y0+ph+20}" fill="{FG}" font-size="12.5" text-anchor="middle" '
                 f'font-family="{MONO}">{t}</text>')
    s.append(f'<text x="{x0+pw/2}" y="{y0+ph+42}" fill="{MUTED}" font-size="12" text-anchor="middle">并发终端数</text>')
    s.append(f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="{AXIS}"/>')
    # 16 终端「盲区」阴影
    s.append(f'<rect x="{x0-10}" y="{y0}" width="46" height="{ph}" fill="rgba(251,191,36,0.10)"/>')
    s.append(f'<text x="{x0+13}" y="{y0+ph-12}" fill="{C_E}" font-size="10.5" text-anchor="middle" '
             f'font-weight="700">前三阶段</text>')
    s.append(f'<text x="{x0+13}" y="{y0+ph-1}" fill="{C_E}" font-size="10.5" text-anchor="middle" '
             f'font-weight="700">的盲区</text>')
    dy = {0: 4, 1: -9, 2: 15}          # B 与 C1 末端几乎重合，标签错开
    for si, (label, vals, color) in enumerate(series):
        d = " ".join(f'{"M" if i==0 else "L"}{px(i):.1f},{py(v):.1f}' for i, v in enumerate(vals))
        s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round"/>')
        for i, v in enumerate(vals):
            s.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="4.4" fill="#0f1115" stroke="{color}" stroke-width="2.4"/>')
        s.append(f'<text x="{px(len(vals)-1)+10:.1f}" y="{py(vals[-1])+dy[si]:.1f}" fill="{color}" font-size="12" '
                 f'font-weight="700" font-family="{MONO}">{fmt(vals[-1])}</text>')
    s.extend(legend(x0, 64, [(c, l) for l, _, c in series]))
    # 右侧：扩展性倍数
    cx0 = 664
    s.append(f'<text x="{cx0}" y="100" fill="{FG}" font-size="13" font-weight="700">16 → 100 终端吞吐倍数</text>')
    for i, (code, mult, color) in enumerate([("A", 1.47, C_A), ("B", 2.88, C_B), ("C1", 2.80, C_C1)]):
        y = 126 + i * 46
        s.append(f'<text x="{cx0}" y="{y+14}" fill="{FG}" font-size="13" font-weight="700" font-family="{MONO}">{code}</text>')
        w = 118 * mult / 3.0
        s.append(f'<rect x="{cx0+30}" y="{y}" width="{w:.1f}" height="17" rx="3.5" fill="{color}" opacity="0.85"/>')
        s.append(f'<text x="{cx0+30+w+8:.1f}" y="{y+14}" fill="{color}" font-size="13" font-weight="700" '
                 f'font-family="{MONO}">{mult:.2f}×</text>')
    s.append(f'<rect x="{cx0}" y="268" width="210" height="52" rx="8" fill="rgba(148,163,184,0.10)"/>')
    s.append(f'<text x="{cx0+14}" y="290" fill="{MUTED}" font-size="12">A 组在 ≈8.2 万 tpmC 处撞墙；</text>')
    s.append(f'<text x="{cx0+14}" y="309" fill="{MUTED}" font-size="12">B 与 C1 在 100 终端仅差 0.3%。</text>')
    s.append(f'<text x="14" y="{H-12}" fill="{MUTED}" font-size="11.5">'
             f'151GB 的管理开销是固定成本：吞吐涨到 2.9 倍后被摊薄至不可见</text>')
    write("fig4_concurrency.svg", s)


# ---------------------------------------------------------------- fig5
def fig5():
    """阶段五：100 终端单参数隔离"""
    W, H = 880, 390
    s = head(W, H, None,
             "本报告证据强度最高的一组数据")
    rows = [
        ("A",  "默认 1GB（基准）",                 82726,  0.0,   C_A),
        ("G",  "A + 仅 xloginsert_locks=48",      84908,  2.6,   C_DIM),
        ("E'", "4GB + 监控关闭项",                164871, 99.3,  C_E),
        ("F",  "A + 仅 buffer→8GB",              169457, 104.8, C_C1),
        ("D",  "8GB + wal_level + max_conn",      175998, 112.8, C_D),
        ("B",  "KAOT 全量 151GB",                178780, 116.1, C_B),
    ]
    x0, y0, pw, rh = 300, 78, 420, 46
    vmax = 190000
    for i, (code, desc, v, pct, color) in enumerate(rows):
        y = y0 + i * rh
        s.append(f'<text x="14" y="{y+17}" fill="{FG}" font-size="14" font-weight="700" font-family="{MONO}">{code}</text>')
        s.append(f'<text x="48" y="{y+17}" fill="{MUTED}" font-size="12">{desc}</text>')
        s.append(f'<text x="292" y="{y+17}" fill="{FG}" font-size="12.5" text-anchor="end" font-family="{MONO}">{fmt(v)}</text>')
        w = pw * v / vmax
        s.append(f'<rect x="{x0}" y="{y+2}" width="{w:.1f}" height="22" rx="4" fill="{color}" opacity="0.88"/>')
        lbl = "—" if pct == 0 else f"{pct:+.1f}%"
        s.append(f'<text x="{x0+w+9:.1f}" y="{y+18}" fill="{color if pct else MUTED}" font-size="13.5" '
                 f'font-weight="700" font-family="{MONO}">{lbl}</text>')
    s.append(f'<line x1="{x0}" y1="{y0-4}" x2="{x0}" y2="{y0+rh*len(rows)-8}" stroke="{AXIS}"/>')
    # F 高亮
    yF = y0 + 3 * rh
    s.append(f'<rect x="8" y="{yF-4}" width="836" height="34" rx="7" fill="none" stroke="{C_C1}" '
             f'stroke-dasharray="5 4" opacity="0.6"/>')
    s.append(f'<text x="14" y="{H-34}" fill="{FG}" font-size="12.5">'
             f'F 组只改一个参数即达到 +104.8%——占全量模板绝对吞吐的 94.8%、增益的 90.3%</text>')
    s.append(f'<text x="14" y="{H-13}" fill="{MUTED}" font-size="11.5">'
             f'G 组（xloginsert_locks，曾被怀疑是高并发关键项）实测仅 +2.6%，在噪声量级内</text>')
    write("fig5_isolation.svg", s)


# ---------------------------------------------------------------- fig6
def fig6():
    """阶段六：shared_buffers 容量扫描"""
    W, H = 880, 400
    s = head(W, H, None,
             "这是悬崖，不是缓坡——1→2GB 吞吐翻倍，2GB 之后进入平台")
    labels = ["1GB", "2GB", "4GB", "8GB", "16GB", "32GB", "151GB"]
    tpmc   = [82726, 169604, 168538, 169457, 170730, 166236, 164932]
    reads  = [15140, 4282, 2147, 1970, 1980, 1957, 1953]
    x0, y0, pw, ph = 72, 92, 600, 216
    vmax = 190000
    for i in range(5):
        v = vmax * i / 4
        y = y0 + ph - ph * i / 4
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{x0-10}" y="{y+4:.1f}" fill="{MUTED}" font-size="11" text-anchor="end" '
                 f'font-family="{MONO}">{fmt(v)}</text>')
    n = len(labels)
    step = pw / n
    bw = step * 0.5
    def cx(i): return x0 + step * (i + 0.5)
    # 平台区底纹
    s.append(f'<rect x="{cx(1)-step*0.5:.1f}" y="{y0}" width="{step*4:.1f}" height="{ph}" '
             f'fill="rgba(39,255,100,0.07)"/>')
    s.append(f'<text x="{cx(2.5):.1f}" y="{y0-8}" fill="{C_B}" font-size="11.5" text-anchor="middle" '
             f'font-weight="600">吞吐平台区（极差 1.3%）</text>')
    for i, (lb, v) in enumerate(zip(labels, tpmc)):
        bh = ph * v / vmax
        y = y0 + ph - bh
        color = C_BAD if i == 0 else (C_C1 if lb in ("4GB", "8GB") else (C_E if i >= 5 else C_B))
        s.append(f'<rect x="{cx(i)-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3.5" '
                 f'fill="{color}" opacity="0.82"/>')
        s.append(f'<text x="{cx(i):.1f}" y="{y-8:.1f}" fill="{FG}" font-size="11.5" font-weight="700" '
                 f'text-anchor="middle" font-family="{MONO}">{fmt(v)}</text>')
        w = "700" if lb in ("4GB", "8GB") else "400"
        c = C_C1 if lb in ("4GB", "8GB") else FG
        s.append(f'<text x="{cx(i):.1f}" y="{y0+ph+19}" fill="{c}" font-size="12.5" text-anchor="middle" '
                 f'font-weight="{w}" font-family="{MONO}">{lb}</text>')
    s.append(f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="{AXIS}"/>')
    # 物理读/秒 折线（右轴，对数感知：用 sqrt 压缩）
    rmax = 16000
    def ry(v): return y0 + ph - ph * (v / rmax) ** 0.5
    d = " ".join(f'{"M" if i==0 else "L"}{cx(i):.1f},{ry(v):.1f}' for i, v in enumerate(reads))
    s.append(f'<path d="{d}" fill="none" stroke="{C_E}" stroke-width="2.2" stroke-dasharray="6 4"/>')
    for i, v in enumerate(reads):
        s.append(f'<circle cx="{cx(i):.1f}" cy="{ry(v):.1f}" r="3.6" fill="#0f1115" stroke="{C_E}" stroke-width="2"/>')
    for i in (0, 1, 2, 6):
        s.append(f'<text x="{cx(i)+10:.1f}" y="{ry(reads[i])-9:.1f}" fill="{C_E}" font-size="11" '
                 f'font-family="{MONO}" paint-order="stroke" stroke="#101418" stroke-width="3.5" '
                 f'stroke-linejoin="round">{fmt(reads[i])}/s</text>')
    s.extend(legend(x0 + 4, y0 + ph + 44, [(C_B, "tpmC"), (C_E, "物理读 / 秒（非线性刻度）")]))
    # 右侧结论
    cx0 = 692
    s.append(f'<rect x="{cx0}" y="92" width="188" height="216" rx="10" fill="rgba(56,189,248,0.07)" '
             f'stroke="rgba(56,189,248,0.3)"/>')
    items = [("推荐 4~8GB", C_C1, "700", 13.5),
             ("", MUTED, "400", 12),
             ("2GB 吞吐已满，", MUTED, "400", 12),
             ("但物理读仍是平台", MUTED, "400", 12),
             ("底值的 2.2 倍", MUTED, "400", 12),
             ("——踩在悬崖边缘", C_E, "600", 12),
             ("", MUTED, "400", 12),
             ("KAOT 的 151GB", FG, "400", 12),
             ("比合理区间大", FG, "400", 12),
             ("19~38 倍", C_BAD, "700", 13.5)]
    for i, (t, c, w, fs) in enumerate(items):
        s.append(f'<text x="{cx0+16}" y="{120+i*21}" fill="{c}" font-size="{fs}" font-weight="{w}">{t}</text>')
    write("fig6_buffer_scan.svg", s)


# ---------------------------------------------------------------- fig7
def fig7():
    """增益归因堆叠条"""
    W, H = 880, 300
    s = head(W, H, None,
             "100 终端 · A（82,726）→ B（178,780）· 总增幅 +116.1%")
    x0, y, pw, bh = 40, 108, 800, 58
    parts = [("shared_buffers 1GB → 8GB", 86731, 90.3, C_B),
             ("wal_level + max_connections", 6540, 6.8, C_D),
             ("其余全部 KAOT 参数（40+ 项）", 2783, 2.9, C_DIM)]
    total = sum(p[1] for p in parts)
    cx = x0
    for i, (label, v, pct, color) in enumerate(parts):
        w = pw * v / total
        s.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="{bh}" fill="{color}" opacity="0.9" '
                 f'{"rx=\"6\"" if i in (0, len(parts)-1) else ""}/>')
        if w > 90:
            s.append(f'<text x="{cx+w/2:.1f}" y="{y+37}" fill="#0b0d10" font-size="19" font-weight="800" '
                     f'text-anchor="middle" font-family="{MONO}">{pct}%</text>')
        cx += w
    # 段 1 直接标在下方；两个窄段改用色块清单，避免引线穿字
    w0 = pw * parts[0][1] / total
    s.append(f'<text x="{x0+w0/2:.1f}" y="{y+bh+30}" fill="{parts[0][3]}" font-size="14" font-weight="700" '
             f'text-anchor="middle">{parts[0][0]}</text>')
    s.append(f'<text x="{x0+w0/2:.1f}" y="{y+bh+51}" fill="{MUTED}" font-size="12.5" text-anchor="middle" '
             f'font-family="{MONO}">+{fmt(parts[0][1])} tpmC</text>')
    lx = x0 + pw - 336
    for i, (label, v, pct, color) in enumerate(parts[1:]):
        ly = y + bh + 24 + i * 24
        s.append(f'<rect x="{lx}" y="{ly-9}" width="10" height="10" rx="2.5" fill="{color}"/>')
        s.append(f'<text x="{lx+16}" y="{ly}" fill="{FG}" font-size="11.5">{label}</text>')
        s.append(f'<text x="{x0+pw}" y="{ly}" fill="{MUTED}" font-size="12" text-anchor="end" '
                 f'font-family="{MONO}">+{fmt(v)}（{pct}%）</text>')
        # 从窄段引一条细竖线到清单
        cx2 = x0 + pw - (pw * sum(p[1] for p in parts[i+1:]) / total) + (pw * v / total) / 2
        s.append(f'<line x1="{cx2:.1f}" y1="{y+bh}" x2="{cx2:.1f}" y2="{ly-9}" stroke="{color}" '
                 f'stroke-width="1" opacity="0.45"/>')
    s.append(f'<text x="{x0}" y="{y-16}" fill="{MUTED}" font-size="12">总增量 +96,054 tpmC</text>')
    s.append(f'<rect x="{x0}" y="{H-58}" width="800" height="42" rx="8" fill="rgba(39,255,100,0.07)" '
             f'stroke="rgba(39,255,100,0.25)"/>')
    s.append(f'<text x="{x0+18}" y="{H-32}" fill="{FG}" font-size="13">'
             f'交叉印证：C1@100（8GB + KAOT 全部其他参数）= 169,968　vs　F（8GB，什么都不加）= 169,457，'
             f'<tspan fill="{C_B}" font-weight="700">相差 0.3%</tspan></text>')
    write("fig7_attribution.svg", s)


# ---------------------------------------------------------------- fig8
def fig8():
    """机制：命中率 → 物理读 → 串行路径"""
    W, H = 880, 330
    s = head(W, H, None,
             "100 终端 · pg_stat_database")
    # 左：命中率
    cards = [
        ("A  默认 1GB", "98.953", "%", 4542035, 15140, C_A),
        ("B  KAOT 151GB", "99.934", "%", 600831, 2000, C_B),
    ]
    for i, (name, hit, unit, reads, per_s, color) in enumerate(cards):
        x = 30 + i * 300
        s.append(f'<rect x="{x}" y="76" width="270" height="180" rx="12" fill="rgba(255,255,255,0.035)" '
                 f'stroke="rgba(255,255,255,0.10)"/>')
        s.append(f'<text x="{x+20}" y="104" fill="{color}" font-size="13.5" font-weight="700" font-family="{MONO}">{name}</text>')
        s.append(f'<text x="{x+20}" y="150" fill="{FG}" font-size="34" font-weight="800" font-family="{MONO}">{hit}'
                 f'<tspan font-size="18" fill="{MUTED}">{unit}</tspan></text>')
        s.append(f'<text x="{x+20}" y="170" fill="{MUTED}" font-size="11.5">缓存命中率</text>')
        s.append(f'<line x1="{x+20}" y1="188" x2="{x+250}" y2="188" stroke="rgba(255,255,255,0.09)"/>')
        s.append(f'<text x="{x+20}" y="212" fill="{MUTED}" font-size="12">物理读总数</text>')
        s.append(f'<text x="{x+250}" y="212" fill="{FG}" font-size="12.5" text-anchor="end" font-family="{MONO}">{fmt(reads)}</text>')
        s.append(f'<text x="{x+20}" y="236" fill="{MUTED}" font-size="12">折合每秒</text>')
        s.append(f'<text x="{x+250}" y="236" fill="{color}" font-size="14" font-weight="700" text-anchor="end" '
                 f'font-family="{MONO}">≈ {fmt(per_s)}</text>')
    s.append(f'<text x="308" y="172" fill="{C_E}" font-size="26" font-weight="800" text-anchor="middle" '
             f'font-family="{MONO}">7.5×</text>')
    # 右：并发放大
    x = 630
    s.append(f'<rect x="{x}" y="76" width="250" height="180" rx="12" fill="rgba(251,191,36,0.07)" '
             f'stroke="rgba(251,191,36,0.28)"/>')
    s.append(f'<text x="{x+18}" y="104" fill="{C_E}" font-size="13" font-weight="700">为什么只在高并发致命</text>')
    txt = ["每次缺页都要走 clock-sweep", "选牺牲页，并修改全局 buffer", "映射哈希表 —— 需要加锁。",
           "", "16 终端：撞锁概率低，可忽略", "100 终端：排队时间超线性增长"]
    for i, t in enumerate(txt):
        c = FG if i >= 4 else MUTED
        s.append(f'<text x="{x+18}" y="{128+i*20}" fill="{c}" font-size="11.8">{t}</text>')
    s.append(f'<text x="30" y="{H-16}" fill="{FG}" font-size="13">'
             f'小 buffer 的代价不是「慢一点」，而是<tspan fill="{C_E}" font-weight="700">多出一段串行路径</tspan>'
             f'——阿姆达尔定律的典型表现</text>')
    write("fig8_mechanism.svg", s)


# ---------------------------------------------------------------- fig9
def fig9():
    """结论演进时间线"""
    W, H = 880, 250
    s = head(W, H, None, "2026-09-02 ~ 09-16 · 六个阶段")
    x0, y = 40, 120
    pw = 800
    stops = [
        ("阶段一", "−24.5%", "KAOT 使性能下降", C_BAD),
        ("阶段二", "−5.2%", "还原数据后同口径复测", C_E),
        ("阶段三", "+14.6%", "buffer 改 8GB（仅 16 终端）", C_C1),
        ("阶段四~六", "+116.1%", "100 终端下模板实际提升", C_B),
    ]
    s.append(f'<line x1="{x0}" y1="{y}" x2="{x0+pw}" y2="{y}" stroke="{AXIS}" stroke-width="1.4"/>')
    for i, (stage, val, desc, color) in enumerate(stops):
        cx = x0 + pw * (i + 0.5) / len(stops)
        s.append(f'<circle cx="{cx:.1f}" cy="{y}" r="8" fill="#0f1115" stroke="{color}" stroke-width="3"/>')
        s.append(f'<text x="{cx:.1f}" y="{y-44}" fill="{color}" font-size="26" font-weight="800" '
                 f'text-anchor="middle" font-family="{MONO}">{val}</text>')
        s.append(f'<text x="{cx:.1f}" y="{y-22}" fill="{MUTED}" font-size="11.5" text-anchor="middle">{stage}</text>')
        s.append(f'<text x="{cx:.1f}" y="{y+30}" fill="{FG}" font-size="12.5" text-anchor="middle">{desc}</text>')
        if i < len(stops) - 1:
            nx = x0 + pw * (i + 1.5) / len(stops)
            s.append(f'<path d="M{cx+14:.1f},{y} L{nx-14:.1f},{y}" stroke="{color}" stroke-width="1.6" opacity="0.45"/>')
    s.append(f'<text x="{x0}" y="{H-20}" fill="{MUTED}" font-size="12">'
             f'前三个阶段的结论全部被后续实验推翻——单点对比只能得到「有没有效」，无法得到「为什么」</text>')
    write("fig9_timeline.svg", s)


for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9):
    fn()
print("done")
