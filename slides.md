---
title: '新员工月度答辩'
logo: '/avator.jpg'
favicon: '/avator.jpg'
colorSchema: light
layout: Bg
---

<div class="font-serif text-center text-5xl mt-40 text-white relative z-10">
    新员工月度答辩
</div>

<div class="text-center text-sm mt-8 text-white/60 relative z-10">
    赵麟　·　2026.09
</div>

<!--
各位老师、各位同事好，我是赵麟。今天做本月的工作答辩。

本月有两项重点工作，都已经跑完并出了结论。

第一项是 KAOT 调优模板在 openGauss 上的适配性分析。一句话概括：它最初的结论是"调优之后性能下降 24.5%"，但这个结论被我自己推翻了两次，最终答案是"提升 116.1%"，而且其中 90.3% 只来自一个参数。

第二项是 PaddleOCR 在昇腾 910B4 上的性能摸测和算力切分。一句话概括：单卡最高吞吐 27.96 QPS，瓶颈不是算力而是显存容量；只改一个环境变量就让单卡吞吐提升了 36.6%。

两项工作各讲三页，最后一页讲它们之间的联系。
-->

---

## 本月工作概览

<div class="grid grid-cols-2 gap-6 mt-5">

<v-click>

<div class="p-4 rounded-lg bg-green-600/8 border border-green-600/30 h-[228px]">

<div class="text-green-700 font-bold">项目一　KAOT 模板在小规模 TPC-C 场景下的适配性分析</div>

<div class="text-sm mt-3 leading-relaxed">

Kunpeng 920 7260 · openGauss · BenchmarkSQL TPC-C · 六阶段 / 14 天

</div>

<div class="mt-3 flex gap-6">
<div><div class="text-2xl font-bold text-green-700 font-mono">+116.1%</div><div class="text-xs opacity-70">100 并发 tpmC 提升</div></div>
<div><div class="text-2xl font-bold text-green-700 font-mono">90.3%</div><div class="text-xs opacity-70">增益来自单个参数</div></div>
</div>

<div class="text-xs mt-3 opacity-70">结论被自己推翻两次；产出推荐配置 + 四条工具改进建议</div>

</div>

</v-click>

<v-click>

<div class="p-4 rounded-lg bg-sky-600/8 border border-sky-600/30 h-[228px]">

<div class="text-sky-700 font-bold">项目二　PaddleOCR 昇腾平台性能摸测与算力切分</div>

<div class="text-sm mt-3 leading-relaxed">

Atlas 800I A2 · 8 × Ascend 910B4-1 · PP-OCRv5 · 客户真实数据集

</div>

<div class="mt-3 flex gap-6">
<div><div class="text-2xl font-bold text-sky-700 font-mono">27.96</div><div class="text-xs opacity-70">单卡峰值 QPS</div></div>
<div><div class="text-2xl font-bold text-sky-700 font-mono">+36.6%</div><div class="text-xs opacity-70">改一个环境变量的收益</div></div>
</div>

<div class="text-xs mt-3 opacity-70">定位瓶颈为 HBM 而非算力；发现官方文档一处功能性错误</div>

</div>

</v-click>

</div>

<v-click>

<div class="mt-5 p-3 rounded-lg bg-gray-500/8 border border-gray-400/30 text-sm text-center">

<span class="opacity-70">两个项目的连接点：</span>**项目一用四次返工换来的实验纪律，直接变成了项目二的操作规程** —— 最后一页展开。

</div>

</v-click>

<!--
本月两项重点工作。

左边项目一，KAOT 模板适配性分析。环境是鲲鹏 920 加 openGauss，用 BenchmarkSQL 跑 TPC-C，六个阶段、14 天。两个关键数字：100 并发下 tpmC 提升 116.1%；而这份增益的 90.3% 只来自一个参数。过程中结论被我自己推翻了两次，最后产出了一份推荐配置和四条对工具本身的改进建议。

右边项目二，PaddleOCR 昇腾平台性能摸测。环境是 Atlas 800I A2，8 张 910B4-1，模型是 PP-OCRv5，数据是客户真实的招投标扫描件。两个关键数字：单卡峰值吞吐 27.96 QPS；只改一个环境变量就拿到 36.6% 的吞吐提升。过程中定位到瓶颈是显存容量而不是算力，还发现了昇腾社区官方文档里的一处功能性错误。

下面这一条是我认为本月最值得讲的：项目一用四次返工换来的实验纪律，直接变成了项目二的操作规程。这个我放在最后一页展开。
-->

---

## 项目一 ①　结论被推翻两次：从 −24.5% 到 +116.1%

<div class="flex justify-center mt-1">
<img src="/charts/fig9_timeline.svg" class="w-[800px]">
</div>

<style>
.slidev-layout table { font-size: 0.76rem; line-height: 1.35; }
.slidev-layout th, .slidev-layout td { padding: 5px 10px !important; }
</style>

<v-click>

| | |
|---|---|
| **任务** | 验证 KAOT `opengauss_database` 模板在本机型是否有效、**靠哪些参数**起作用（模板一次性下发 40+ 项） |
| **两次推翻的原因** | ① 未在每轮压测前还原数据 → 结果被数据磨损污染，−24.5% 严重高估；② 前三阶段只测 16 终端 → **恰好是模板价值为零的并发区间** |
| **由此建立的纪律** | 每轮从干净备份还原 · 同批次交叉执行 + A/B 锚点组 · **跨批次数据不可直接比较**（同样 16 终端，三个批次跑出 −24.5% / −5.2% / +6.1%） |

</v-click>

<!--
先看项目一的整体脉络。

任务是验证 KAOT 的 opengauss_database 模板在我们这台鲲鹏 920 上有没有效，以及——更重要的——是靠哪些参数起作用。因为这个模板是一次性下发 40 多项参数，它是一个整体。

上面这条时间线是结论的三次修正。

阶段一：下降 24.5%。当时归因是 shared_buffers 被设成了 151GB。

阶段二：我引入了"每轮压测前从干净备份还原数据"，同口径复测，变成 −5.2%。为什么差这么多？因为 TPC-C 会持续往表里写数据，同一份数据跑的轮次越多成绩越差。我当时是 9 月 2 号跑基线、9 月 4 号跑 KAOT，KAOT 跑在已经被磨损过的数据上。所以 −24.5% 里绝大部分是方法缺陷，不是参数。

阶段三：定位到元凶确实是 shared_buffers=151GB，改成 8GB 可以 +14.6%。

阶段四到六：把并发拉上去之后发现，100 终端下模板实际提升 116.1%。前三个阶段全部固定在 16 终端，而 16 终端恰恰是整条曲线上唯一看不出模板价值的区间。这是第二次推翻。

表格最后一行是我觉得代价最大、也最该记住的一条纪律：跨批次数据不可直接比较。同样是 16 终端、同样已还原数据，三个批次跑出了 −24.5%、−5.2%、+6.1% 三种符号不同的结果。机器状态在批次之间的漂移能达到 20%，比我要测的很多效应都大。所以从阶段三开始，所有核心结论都必须基于同一批次内的对比，每个批次都放 A、B 两组做锚点。
-->

---

## 项目一 ②　归因：+116% 里有 90.3% 来自一个参数

<div class="flex justify-center mt-1">
<img src="/charts/fig5_isolation.svg" class="w-[700px]">
</div>

<style>
.slidev-layout table { font-size: 0.75rem; line-height: 1.3; }
.slidev-layout th, .slidev-layout td { padding: 4px 12px !important; }
</style>

<div class="grid grid-cols-2 gap-8 mt-1">

<div>

<v-click>

| 增益来源（总 +96,054 tpmC） | 增量 | 占比 |
|---|---|---|
| `shared_buffers` 1GB → 8GB | +86,731 | **90.3%** |
| `wal_level` + `max_connections` | +6,540 | 6.8% |
| 其余全部 40+ 项 KAOT 参数 | +2,783 | 2.9% |

</v-click>

</div>

<div class="text-xs leading-relaxed">

<v-click>

**交叉印证**：C1@100（8GB + KAOT 全部其他参数）= 169,968，F（8GB，什么都不加）= 169,457，两次独立测量**相差 0.3%**。

</v-click>

<v-click>

**机制**：A 与 B 命中率差 1 个百分点（98.95% vs 99.93%），换算物理读差 **7.5 倍**。每次缺页都要改全局 buffer 映射哈希表并**加锁** —— 小 buffer 的代价不是慢一点，而是多一段**串行路径**：低并发下隐形，高并发下即天花板。

</v-click>

</div>

</div>

<!--
这一页是本次工作证据强度最高的一组数据：六组配置，同一批次执行，全部 100 终端。

图上 A 是默认 1GB 作为基准，82,726。

G 组只改一个 xloginsert_locks 到 48。这个参数原本是我的重点怀疑对象，因为 WAL 插入锁竞争是 PostgreSQL 系数据库高并发下的经典瓶颈。但实测只有 +2.6%，在噪声量级内。

F 组是重点，虚线框出来的：在默认配置上只改一个 shared_buffers，从 1GB 改到 8GB，其他什么都不动，结果 +104.8%。它一个参数就拿到了全量模板绝对吞吐的 94.8%。

左下表格是增益拆解：总增量 96,054 tpmC，其中 shared_buffers 贡献 86,731，占 90.3%；wal_level 加 max_connections 贡献 6.8%；其余四十多项参数合计只有 2.9%。

右边第一条是交叉印证：阶段四里的 C1@100，也就是 8GB 加上 KAOT 全部其他参数，是 169,968；而 F 组 8GB 什么都不加是 169,457。两次独立测量相差 0.3%。说明在 8GB 的基础上，其余参数几乎不产生额外收益。

右边第二条是机制。100 并发下 A 和 B 的缓存命中率只差 1 个百分点——98.95% 对 99.93%。听起来微不足道，但未命中率是从 1.05% 降到 0.07%，换算成物理读差了 7.5 倍。每一次缺页都要走 clock-sweep 挑牺牲页、脏页刷盘，最后修改全局的 buffer 映射哈希表，而这一步需要加锁，这把锁被所有连接共用。

所以小 buffer 的代价不是"每次读盘慢一点"这种线性代价，而是多出了一段串行路径。串行路径在低并发下隐形，在高并发下就是天花板——这也解释了为什么同一个参数在 16 终端无关紧要、在 100 终端价值翻倍。
-->

---

## 项目一 ③　151GB 落在曲线最低点：推荐配置与工具建议

<div class="flex justify-center mt-0">
<img src="/charts/fig6_buffer_scan.svg" class="w-[620px]">
</div>

<style>
.slidev-layout table { font-size: 0.68rem; line-height: 1.25; }
.slidev-layout th, .slidev-layout td { padding: 3px 9px !important; }
</style>

<div class="grid grid-cols-2 gap-6 mt-1">

<div>

<v-click>

```ini
shared_buffers   = 4GB      # 数据集 ~1.5GB，留 2-3 倍余量
wal_level        = minimal  # 单机无备机
hot_standby      = off
max_connections  = 200      # 非 2048
full_page_writes = on       # openGauss 上不要关
```

<div class="text-xs mt-1">五项即得 <span class="text-green-700 font-bold">+112%</span>（D 组），无需下发全量模板。适用边界：<strong>10 仓 ≈ 1.5GB 数据集</strong>。</div>

</v-click>

</div>

<div>

<v-click>

| 对 KAOT 的四条改进建议 |
|---|
| ① `shared_buffers` 应按**数据集规模**推导，而非物理内存 30% |
| ② 模板应**声明**其验证时的数据规模与并发量级 |
| ③ 大内存配置缺 `config_hugepages` 联动（3,958 万页表项） |
| ④ `full_page_writes=off` 与 double-write 重叠，实测 **−3.2%** |

</v-click>

</div>

</div>

<!--
既然 90% 的收益来自一个参数，那这个参数的最优值是多少？KAOT 给的 151GB 对不对？

上面这张是 100 终端下扫的 7 个容量点。

第一个结论：这是悬崖，不是缓坡。1GB 是 82,726，2GB 直接跳到 169,604，吞吐翻倍。然后 2GB 到 16GB 四个点极差只有 1.3%，是一个平台。

第二个结论：从 16GB 峰值往后单调下降，KAOT 推荐的 151GB 是全扫描表现最差的一档。不过这里我必须谨慎表述——这些点都是单次测量，历史变异系数是 4 到 6%，这个 3.4% 的降幅落在单次测量误差范围内，只能说是趋势，不能当定量结论。

黄色虚线是物理读每秒，它解释了为什么我推荐 4 到 8GB 而不是看起来够用的 2GB：2GB 虽然吞吐已经满了，但物理读仍是平台底值的 2.2 倍，缓存并没有饱和。2GB 刚好踩在悬崖边缘，数据集稍有增长就可能跌回去。

左下是推荐配置，五项，就能拿到大约 +112% 的收益，对应实验里的 D 组，不需要下发全量模板的四十多项。这里我也写明了适用边界：严格来说只在 10 仓、约 1.5GB 数据集下成立。因为 shared_buffers 的需求上限由数据量本身决定，我们的数据只有 1.5GB，151GB 里 99% 永远是空的。KAOT 按 502GB 物理内存推出 151GB，它的假设场景是数据集达到百 GB 量级。所以我证明的不是"KAOT 错了"，而是"它的假设和我们的场景不匹配"。

右下是四条改进建议。最重要的是第一条：shared_buffers 应该按数据集规模推导，而不是按物理内存比例——数据库需要多大 buffer 取决于热点数据有多大，跟机器插了多少内存没有直接关系。第四条也值得说：full_page_writes 在 openGauss 上关掉是负收益，因为 openGauss 有 double-write 兜底，关掉 FPW 不减少 WAL 写入量反而多走一层。这一项明显是沿用了 PostgreSQL 的经验。
-->

---

## 项目二 ①　PaddleOCR 单实例基线：耗时的六成在 rec

<div class="flex justify-center mt-1">
<img src="/charts/figP1_latency.svg" class="w-[800px]">
</div>

<style>
.slidev-layout table { font-size: 0.75rem; line-height: 1.3; }
.slidev-layout th, .slidev-layout td { padding: 4px 10px !important; }
</style>

<v-click>

| | |
|---|---|
| **数据集** | 104 张招投标扫描件 · 尺寸仅 3 种（全 RGB，A4 ≈175 DPI）· 每页文本行数 min/中位/P90/max = **13 / 41 / 69 / 209** |
| **单实例基线** | **1.21 QPS** · avg 825 ms · P50 833 ms · P99 1592 ms（三次重复，**变异系数 0.67%**） |
| **精度**（om vs Paddle CPU） | 平均字符一致率 **99.88%**，最低 99.17%，**零推理失败** → 可用于生产 |
| **资源占用** | AICore avg **2.9%** · HBM 9% —— 单实例下 NPU 与 CPU 均严重空闲，瓶颈是**串行等待** |

</v-click>

<!--
项目二第一页，单实例摸测。

先说数据集。104 张招投标文档扫描件，尺寸只有三种，全部 RGB，A4 比例大约 175 DPI。

这里有一个关键认知：因为尺寸高度统一，图片分辨率不是性能变量。真正决定单页耗时的是每页的文本行数——det 检出多少个框，rec 就要执行多少次推理。每页行数的分布是最小 13、中位 41、P90 是 69、最大 209，跨度很大。

所以我没有按目录分组测试，而是以文本行数为自变量做了线性回归，就是上面这张图。结果是：单页耗时约等于 398.6 毫秒加上 12.50 毫秒乘以文本行数，R 方 0.681。

右边是典型页的耗时构成。一个 45 行的典型页，总耗时约 961 毫秒，其中固定开销 399 毫秒占 41%，rec 推理 562 毫秒占 59%。

这里最值得注意的是：固定开销那 399 毫秒里面，det 推理只占几十毫秒，其余三百多毫秒全是 CPU 单线程的工作——PNG 解码、resize、DB 后处理的轮廓提取，还有 45 个文本框的裁剪和透视变换。这段完全不使用 NPU。

表格里第三行是精度。以 Paddle 后端 CPU 的输出作为参考答案，om 后端的平均字符一致率是 99.88%，最低 99.17%，零推理失败，可以用于生产。

第四行是这一页最重要的观察：单实例状态下 AICore 平均只有 2.9%，HBM 9%，NPU 和 CPU 都严重空闲。这不是算力不足，而是单进程串行等待——每个环节都在等上一环节，硬件大部分时间在空转。

这个观察直接决定了第二个任务的方向：多实例的扩展空间极大。
-->

---

## 项目二 ②　多实例爬坡：瓶颈是 HBM 容量，不是算力

<div class="flex justify-center mt-1">
<img src="/charts/figP2_ramp.svg" class="w-[810px]">
</div>

<style>
.slidev-layout table { font-size: 0.73rem; line-height: 1.25; }
.slidev-layout th, .slidev-layout td { padding: 3px 14px !important; }
</style>

<v-click>

| 实例数 | 1 | 2 | 4 | 8 | 16 | **24（拐点）** | 32 |
|---|---|---|---|---|---|---|---|
| 聚合 QPS | 1.21 | 2.31 | 4.45 | 8.31 | 15.13 | **20.47** | 20.02 |
| 扩展效率 | 100% | 95.6% | 92.1% | 86.0% | 78.3% | **70.7%** | 69.1% |
| AICore avg | 2.9% | — | — | ~23% | 41.8% | **53.6%** | 52.4% |
| HBM | 9% | — | — | — | 69% | **98%** | 99% |

</v-click>

<!--
这是本次摸测最重要的一张图。

绿色实线是聚合 QPS，随实例数上升，在 24 实例处出现拐点，达到 20.47 QPS，之后 32 实例反而略降到 20.02。

关键在另外两条虚线。橙色是 AICore 利用率，红色是 HBM 占用率，都读右轴。

AICore 在拐点处只有 53.6%，从头到尾从未接近饱和。而 HBM 在同一位置已经达到 98%，32 实例时 99%。

拐点位置和 HBM 饱和位置完全重合。

所以结论很明确：本负载的单卡实例数上限是由显存容量决定的，不是算力。

这个结论还有一个独立的验证。每实例显存占用是实测的 2686 MB，单卡可用显存 62.1 GB，理论上限算下来是 23 个实例，实测拐点在 24——吻合。后来把每实例显存降到 1726 MB，理论上限 36，实测约 38——同样吻合。两次理论推算都对得上实测，说明显存约束这个模型是站得住的。

右下角是显存优化之后的结果：单卡峰值 27.96 QPS，约 38 实例。这个下一页展开。

最后说明一句：图下面那行注释，两组爬坡测试的 limit、loop、warmup 参数不同，所以绝对 QPS 不能跨组比较。我在这里只用同一组内的趋势和拐点位置。这是我自己在报告局限性里列出来的一条。
-->

---

## 项目二 ③　两个核心工程发现与部署建议

<div class="flex justify-center mt-0">
<img src="/charts/figP3_memory.svg" class="w-[600px]">
</div>

<div class="grid grid-cols-2 gap-6 mt-1 text-xs">

<div class="text-[10.5px] leading-snug">

<v-click>

<div class="p-2.5 rounded bg-red-600/8 border border-red-600/30">

**① `onnxsim` 会破坏动态 shape 模型**　昇腾社区《PaddleOCR优化参考实践》3.4 节建议对 rec 执行 `onnxsim`，实测导致 **34.6%（36/104）** 的图片推理失败。开 `ASCEND_GLOBAL_LOG_LEVEL=1` 查 plog 定位：常量折叠把 reshape 输出固化为 `[40,40,120]`，与 `[1600,1,120]` 无法广播。**已列为上游反馈项。**

</div>

</v-click>

<v-click>

<div class="p-2.5 rounded bg-amber-600/8 border border-amber-600/30 mt-2">

**② `ASCEND_OM_OUTPUTSIZE` 两个隐蔽行为**　超出合法范围时**静默回退**到默认 64MB（排错期间造成误导）；该值是**预分配**的，直接决定单实例显存占用。

</div>

</v-click>

</div>

<div>

<style>
.slidev-layout table { font-size: 0.7rem; line-height: 1.25; }
.slidev-layout th, .slidev-layout td { padding: 3px 8px !important; }
</style>

<v-click>

| 部署场景 | 建议配置 | 预期表现 |
|---|---|---|
| 吞吐优先（批处理） | 单卡 36~38 实例，`OUTPUTSIZE=64` | ~28 QPS/卡，P99 ≈ 4 s |
| 时延优先（在线） | 单卡 8~16 实例 | 8~15 QPS/卡，P99 < 2 s |
| 多租户隔离 | `vir10_3c_32g` 切分 | 吞吐低于物理卡，换隔离性 |

</v-click>

<v-click>

<div class="mt-2 p-2 rounded bg-gray-500/8 border border-gray-400/30">

**算力切分（vNPU）对本负载无吞吐收益**：切分后各份显存之和不超过整卡，实例总数只减不增；而所需算力仅约整卡 50%。其价值在**多租户隔离与 QoS**，不在提吞吐。<span class="opacity-70">（vNPU 容器 ACL 初始化未打通，该结论为基于已测显存与 AICore 数据的推算，已在报告中标注。）</span>

</div>

</v-click>

</div>

</div>

<!--
这一页讲两个核心工程发现和最终的部署建议。

上面这张图是本次投入产出比最高的一项优化。把 ASCEND_OM_OUTPUTSIZE 从 1024 MB 降到 64 MB，单实例显存从 2686 降到 1726，降了 35.7%；而三档配置下单实例 QPS 完全一致，1.211、1.211、1.208，差异在噪声范围内——说明降低这个值不带来任何性能损失。

顺带一提，三档的显存差值精确等于配置差，由此可以推出固定基础占用大约是 1662 MB。

因为瓶颈正是显存，这一项直接把单卡实例上限从 24 提到约 38，单卡峰值吞吐从 20.47 提到 27.96，提升 36.6%。只改一个环境变量，不改模型、不影响精度、全量回归 104 张全部通过。

左下是两个核心发现。

第一个我认为价值最高：昇腾社区那篇《PaddleOCR优化参考实践》的 3.4 节建议对 rec 模型执行 onnxsim，但这个建议在动态 shape 场景下会导致功能性错误。实测让 36 张图、也就是 34.6% 的数据推理失败。

这个问题排查了很久，我先后试过提高输出内存、重启容器、单独测特殊尺寸的图、转固定 batch，全都无效。最后是开了 ASCEND_GLOBAL_LOG_LEVEL=1 去读 CANN 底层的 plog 日志才定位到：onnxsim 在简化模型时做常量折叠，按静态输入假设把某个 reshape 的输出形状固化成了 [40,40,120]，运行时实际序列长度不同，跟另一分支的 [1600,1,120] 无法广播。

这一条我已经列为需要向上游反馈的问题。教训是：遇到 ACL 错误码应该尽早开底层日志，我在好几个错误假设上耗了几个小时，而 plog 一次就定位到了根因。

第二个发现是 ASCEND_OM_OUTPUTSIZE 的两个隐蔽行为：超出合法范围时不报错，而是静默回退到默认的 64MB——我在排错期间设过 1288，以为提高了配额，实际反而降低了，造成了误导；另外这个值是预分配的，直接决定单实例显存占用。

右边是最终的部署建议。吞吐优先就上 36 到 38 实例，约 28 QPS 每卡，但 P99 接近 4 秒；时延优先就用 8 到 16 实例，P99 控制在 2 秒内。具体取哪个点取决于客户的 SLA。

最后是算力切分的结论：对本负载没有吞吐收益。理由是切分后各份显存之和不超过整卡，实例总数只减不增；而实测所需算力只有整卡的 50% 左右，算力本来就不是瓶颈。vNPU 的价值在多租户隔离和 QoS 保障。

这里要如实说明：vNPU 的容器 ACL 初始化我没有打通，所以这个结论是基于已实测的显存和 AICore 数据做的推算，不是压测实测。我在报告里明确标注了这一点。
-->

---

## 本月总结：项目一的教训，逐条变成了项目二的操作规程

<style>
.slidev-layout table { font-size: 0.76rem; line-height: 1.35; }
.slidev-layout th, .slidev-layout td { padding: 6px 10px !important; }
</style>

<v-click>

| 项目一踩过的坑 | 得到的纪律 | 在项目二的落地 |
|---|---|---|
| 未还原数据 → −24.5% 严重高估 | **每轮从干净基线开始** | 每次模型改动先跑 `regress.sh` 全量 104 张，再跑性能 |
| 跨批次相减 → 三个批次符号都不同 | **同批次 + 重复取中位** | 基线三次重复，CV 0.67% 才采信 |
| 只测单一并发点 → 落在价值为零的区间 | **必须扫参数空间** | 实例数 1 → 72 爬坡，找到拐点与显存墙 |
| 只报性能不报精度 | **结论必须带边界** | 精度校验前置：om vs Paddle 一致率 99.88% |
| CPU 采集漏字段 → 数据整段作废 | **坏数据整段弃用** | 本次 CPU 采集同样失败 → 同样整段弃用，瓶颈判断改用 HBM + AICore |

</v-click>

<div class="grid grid-cols-3 gap-4 mt-4 text-xs">

<v-click>

<div class="p-3 rounded bg-green-600/8 border border-green-600/30">

**交付**　两份完整报告；KAOT 五项推荐配置（+112%）+ 四条工具建议；PaddleOCR 部署配置 + 上游问题反馈 3 条

</div>

</v-click>

<v-click>

<div class="p-3 rounded bg-sky-600/8 border border-sky-600/30">

**方法**　单变量隔离做归因 · 判别对排除竞争假设 · 理论推算与实测互证（23 vs 24、36 vs 38）

</div>

</v-click>

<v-click>

<div class="p-3 rounded bg-amber-600/8 border border-amber-600/30">

**认识**　结论要落到**机制**（串行路径 / 显存墙）· 要带**适用边界** · 方向明确的**负面结论**同样有价值

</div>

</v-click>

</div>

<!--
最后一页，讲两个项目的连接点。

上面这张表，左边一列是项目一实际踩过的坑，中间是提炼出的纪律，右边是这些纪律在项目二的具体落地。

第一行，没还原数据导致结果被磨损污染。纪律是每轮从干净基线开始。落到项目二，就是每次模型改动之后先跑全量 104 张的回归脚本，确认功能不退化，再跑性能测试。这一条在项目二救了我好几次——中间有好几次单张图通过、全量却失败的情况。

第二行，跨批次相减，三个批次跑出三种符号。纪律是同批次加重复取中位。落到项目二，就是单实例基线跑三次重复，变异系数 0.67% 才采信。

第三行，只在单一并发点测，恰好落在模板价值为零的区间。纪律是必须扫参数空间。落到项目二，就是实例数从 1 一路爬到 72，才找到 24 这个拐点和背后的显存墙。

第四行，只报性能不报精度。纪律是结论必须带边界。落到项目二，就是把精度校验放在性能测试之前做。

第五行我想专门说一下，因为它有点尴尬但我觉得必须讲：项目一里我的 CPU 利用率数据因为读 /proc/stat 漏了几个字段而整段作废。项目二里，CPU 采集又失败了一次——这次是采集脚本的 sed 修改因为正则没匹配缩进行而静默失败，全程记录为 0。

同样的坑踩了两次。但两次的处理是一样的：发现坏数据就整段弃用，不修修补补继续用。项目二的瓶颈判断完全基于 HBM 和 AICore 两项指标，结论不受影响。这一条我也如实写在报告的局限性里了。

下面三个框是本月的总结。

交付：两份完整报告；KAOT 给出五项推荐配置，能拿到 +112% 的收益，加四条工具改进建议；PaddleOCR 给出部署配置，以及三条需要向上游反馈的问题。

方法：用单变量隔离做归因；用判别对排除竞争假设；用理论推算和实测互相印证——显存上限推算 23 对实测 24、推算 36 对实测 38，两次都吻合，这让显存约束这个结论站得很稳。

认识：结论要落到机制上，不能停在现象；结论必须带适用边界；还有，一个方向明确的负面结论——比如算力切分对本负载没有吞吐收益——和正面结论同样有价值。

以上就是我本月的汇报，请各位老师和同事批评指正，谢谢。
-->

---
layout: Ballpit
---

<!--
汇报到此结束，感谢各位的聆听，欢迎提问和指正。
-->
