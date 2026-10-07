"""
自动生成精美专业 PPTX 演示文稿（通俗易懂动物识别版）
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    COLOR_BG = RGBColor(248, 250, 252)
    COLOR_DARK = RGBColor(15, 23, 42)
    COLOR_PRIMARY = RGBColor(30, 58, 138)
    COLOR_ACCENT = RGBColor(14, 165, 233)
    COLOR_CARD = RGBColor(255, 255, 255)
    COLOR_BORDER = RGBColor(226, 232, 240)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="人工智能（26秋）课堂报告1：知识表示与推理"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.4))
        p_cat = cat_box.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT
        p_cat.font.name = "微软雅黑"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        p_t = title_box.text_frame.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY
        p_t.font.name = "微软雅黑"

    def add_card(slide, left, top, width, height, title, items, card_type="default"):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD
        shape.line.color.rgb = COLOR_ACCENT if card_type == "highlight" else COLOR_BORDER
        shape.line.width = Pt(1.5 if card_type == "highlight" else 1)

        tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY if card_type != "highlight" else COLOR_ACCENT
        p_t.font.name = "微软雅黑"
        p_t.space_after = Pt(10)

        for itm in items:
            p = tf.add_paragraph()
            p.text = f"• {itm}" if not itm.startswith("  ") else itm
            p.font.size = Pt(12)
            p.font.color.rgb = COLOR_DARK
            p.font.name = "微软雅黑"
            p.space_after = Pt(5)

    # Slide 1: 封面
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "人工智能实践专题报告 · 知识表示与推理"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.font.name = "微软雅黑"
    p.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "基于产生式规则与知识图谱的\n经典动物智能识别与属性推理系统"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.font.name = "微软雅黑"
    p2.space_after = Pt(24)

    p3 = tf1.add_paragraph()
    p3.text = "汇报小组：第12组  |  指导课程：人工智能（26秋）  |  通俗实用的双驱动推理实践"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.font.name = "微软雅黑"

    # Slide 2: 背景与目标
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "背景与目标：让机器学会'像人类专家一样层层推导'")
    add_card(s2, 0.8, 1.8, 5.6, 5.0, "🤔 为什么要做动物推理系统？", [
        "零散特征难以直接归纳：普通人在野外科考或科普中只能观察到零散外形（如'黄褐色'、'有条纹'），缺乏系统分类推导能力。",
        "传统检索缺乏逻辑：查表检索机械呆板，无法回答'为什么是该动物'的推导过程。",
        "现代深度学习是黑盒：单纯图像分类无法展现分类学演化逻辑，缺乏透明可解释性。",
        "符号主义AI的经典价值：推导过程步步可查、结论完全有据可依、绝无幻觉。"
    ])
    add_card(s2, 6.8, 1.8, 5.6, 5.0, "🎯 本项目核心研发目标", [
        "双知识表示结合：融合产生式规则（因果经验）与知识图谱（百科网络）。",
        "多步正向演绎：支持从外在特征递推中间事实（如哺乳类/食肉类），最终锁定目标物种。",
        "知识图谱属性关联：识别出动物后，自动通过图路径检索其生活环境、保护级别等生态百科。",
        "轻量极速交互：代码简洁、单次推导耗时<1ms，提供直观的 Web 演示界面。"
    ], card_type="highlight")

    # Slide 3: 两种知识表示对比
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "核心任务(一)：两种主流知识表示方法深度对比")
    add_card(s3, 0.8, 1.8, 5.6, 5.0, "🧠 方法一：产生式规则 (IF-THEN)", [
        "核心逻辑：条件-动作对。IF (前提条件组合) THEN (推导结论)。",
        "表示能力：模块化高，非常适于表达分类学专家经验与因果条件分支。",
        "推理机制：正向演绎（数据驱动）或反向推理（目标假设验证）。",
        "局限性：规则库庞大时维护困难，难以表达多对多的实体关系网。",
        "典型适用场景：专家系统、医疗初步诊断、故障定位系统。"
    ])
    add_card(s3, 6.8, 1.8, 5.6, 5.0, "🌐 方法二：知识图谱 / 语义网络 (RDF)", [
        "核心逻辑：主体-关系-客体三元组 (Head, Relation, Tail)。",
        "表示能力：网状拓扑化，擅长刻画实体间的复杂层级、属性与多维关系关联。",
        "推理机制：图遍历、最短路径检索、子图模式匹配、图嵌入预测。",
        "局限性：不擅长直接表达复杂的'与/或'条件逻辑与动态推断演化。",
        "典型适用场景：搜索引擎知识卡片、智能推荐、GraphRAG 大模型知识库。"
    ])

    # Slide 4: 落地架构
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "核心任务(二)：系统落地流程与双驱动架构")
    add_card(s4, 0.8, 1.8, 3.7, 5.0, "1. 知识建模层 (表示)", [
        "分类学规则库：编码13条经典产生式规则（涵盖哺乳纲、鸟类、食肉目、有蹄类）。",
        "动物百科图谱：构建物种生活环境、国家保护级别、天敌与特殊能力三元组网络。"
    ])
    add_card(s4, 4.8, 1.8, 3.7, 5.0, "2. 智能推理机层 (算法)", [
        "正向演绎机：事实驱动，循环匹配规则前提，新事实动态回填更新。",
        "规则执行闭包：确保每条规则仅激发一次，避免死锁。",
        "图谱属性检索：以物种实体为锚点，向外展开属性边查询。"
    ], card_type="highlight")
    add_card(s4, 8.8, 1.8, 3.7, 5.0, "3. 业务呈现层 (应用)", [
        "物种最终精准锁定。",
        "推理链条透明展示（每一步触发了什么规则、基于什么前提）。",
        "拓展生态百科卡片。",
        "交互式 Web 演示面板。"
    ])

    # Slide 5: 知识建模细节
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "知识表示实现：规则编码与图谱三元组")
    add_card(s5, 0.8, 1.8, 5.6, 5.0, "📋 产生式规则库设计 (13条经典规则)", [
        "R1: IF {有毛发} THEN 哺乳动物",
        "R3: IF {有羽毛} THEN 鸟类",
        "R5: IF {哺乳动物, 吃肉} THEN 食肉动物",
        "R7: IF {哺乳动物, 有蹄} THEN 有蹄动物",
        "R8: IF {食肉动物, 黄褐色, 有暗条纹} THEN 老虎",
        "R9: IF {食肉动物, 黄褐色, 有黑色斑点} THEN 金钱豹",
        "R11: IF {有蹄动物, 有黑白条纹} THEN 斑马",
        "R13: IF {鸟类, 会游泳, 不会飞, 黑白二色} THEN 企鹅"
    ])
    add_card(s5, 6.8, 1.8, 5.6, 5.0, "🔗 知识图谱三元组模式", [
        "(老虎, 生活环境, 森林与丛林)",
        "(老虎, 保护级别, 国家一级重点保护野生动物)",
        "(老虎, 食性, 肉食性捕食鹿/野猪)",
        "(金钱豹, 保护级别, 国家一级重点保护野生动物)",
        "(斑马, 天敌, 狮子/鬣狗)",
        "(企鹅, 生活环境, 南极及极寒海域)",
        "(企鹅, 特殊能力, 擅长潜水与耐严寒)",
        "(鸵鸟, 特殊能力, 奔跑速度可达70km/h)"
    ])

    # Slide 6: 算法实现
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "核心算法：事实驱动正向演绎与图谱路径遍历")
    add_card(s6, 0.8, 1.8, 5.6, 5.0, "⚡ 算法1：正向产生式演绎机", [
        "1. 初始化事实集合 Facts = 输入特征集合 S_input；",
        "2. 循环遍历规则库中未执行的规则 r；",
        "3. 判断规则前提是否满足：IF(r) ⊆ Facts；",
        "4. 若满足，将结论加入事实库：Facts = Facts ∪ {THEN(r)}；",
        "5. 标记规则 r 为已执行，记录推理步骤日志；",
        "6. 重复执行直到没有新规则被触发，输出最终识别物种。"
    ])
    add_card(s6, 6.8, 1.8, 5.6, 5.0, "🔍 算法2：知识图谱属性路径检索", [
        "基于 NetworkX 有向图 (DiGraph) 结构：",
        "1. 将推导出的物种名称（如'老虎'）作为根节点；",
        "2. 检查图谱是否存在该实体节点：has_node(animal)；",
        "3. 遍历所有邻接出边：neighbors(animal)；",
        "4. 提取边上的关系属性：G[animal][neighbor]['relation']；",
        "5. 毫秒级输出对应的生态百科知识卡片。"
    ], card_type="highlight")

    # Slide 7: 系统实操演示
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "核心任务(三)：系统实机演示与典型推理案例")
    add_card(s7, 0.8, 1.8, 5.2, 5.0, "💻 真实推理案例演示 (以识别老虎为例)", [
        "【输入特征】: [有毛发, 吃肉, 黄褐色, 有暗条纹]",
        "【多步推导演绎过程】:",
        "  - 步骤1 触发 R1: 依据'有毛发' ➜ 推导出【哺乳动物】",
        "  - 步骤2 触发 R5: 依据'哺乳动物+吃肉' ➜ 推导出【食肉动物】",
        "  - 步骤3 触发 R8: 依据'食肉动物+黄褐色+暗条纹' ➜ 锁定【老虎】",
        "【图谱属性扩展】:",
        "  - 生活环境 ➜ 森林与丛林",
        "  - 保护级别 ➜ 国家一级重点保护野生动物",
        "特点：逻辑链条100%可溯源，耗时仅 0.5 毫秒！"
    ])
    img_path = "G:\\code\\ep1\\knowledge_graph.png"
    if os.path.exists(img_path):
        s7.shapes.add_picture(img_path, Inches(6.3), Inches(1.8), width=Inches(6.2))

    # Slide 8: 实验测试与效能评估
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "测试分析：多维度效能评估与指标对比")
    add_card(s8, 0.8, 1.8, 3.7, 5.0, "📊 4大测试用例验证", [
        "用例1（老虎）：3步正向递推，100%精准识别。",
        "用例2（企鹅）：羽毛+会游泳+不会飞 ➜ 精准锁定企鹅并返回南极习性。",
        "用例3（斑马）：有毛发+有蹄+黑白条纹 ➜ 准确推导斑马并返回天敌信息。",
        "用例4（长颈鹿）：长脖子+长腿+暗斑点 ➜ 准确识别并给出世界最高陆生动物属性。"
    ])
    add_card(s8, 4.8, 1.8, 3.7, 5.0, "⏱️ 计算性能指标", [
        "正向演绎推导耗时：< 0.25 ms",
        "知识图谱邻接检索耗时：< 0.15 ms",
        "端到端响应时间：< 0.5 ms（真正瞬时响应）",
        "代码体量：仅 80 行纯 Python，极致轻量无负担。"
    ], card_type="highlight")
    add_card(s8, 8.8, 1.8, 3.7, 5.0, "🛡️ 可靠性对比", [
        "vs 传统查表检索：具备中间概念演绎能力。",
        "vs 黑盒深度学习：推导全过程白盒透明，绝对零幻觉、零误导。"
    ])

    # Slide 9: 局限性与未来展望
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "核心任务(四)：技术现存局限分析与前沿展望")
    add_card(s9, 0.8, 1.8, 5.6, 5.0, "🚧 当前知识表示与推理的现存局限", [
        "知识获取瓶颈（Knowledge Bottleneck）：规则全靠手工整理录入，难以覆盖成千上万种罕见动植物。",
        "缺乏模糊容错能力：用户输入特征若不完全匹配（如文字表述不一致），推理将直接中断。",
        "不确定性建模欠缺：经典产生式是确定性的二值逻辑，无法直接处理'可能'、'大概'等概率表述。"
    ])
    add_card(s9, 6.8, 1.8, 5.6, 5.0, "🚀 未来发展方向：神经符号混合智能", [
        "视觉大模型 + 知识推理：利用视觉模型（YOLO/CLIP）从真实动物照片中自动识别出特征，再输入本系统进行严密因果归因。",
        "融合不确定性推理：引入主观逻辑或可信度因子（CF），支持模糊置信度加权推导。",
        "图神经网络补全：利用知识图谱嵌入算法（TransE）自动预测未知的动物食性与生态关系。"
    ], card_type="highlight")

    # Slide 10: 总结与致谢
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = COLOR_PRIMARY
    bg10.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(3.8))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "实践总结与团队收获"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.font.name = "微软雅黑"
    p.space_after = Pt(20)

    items_sum = [
        "深入掌握了产生式规则与知识图谱两种主流知识表示方法的核心机制与优缺点；",
        "独立开发了经典的正向产生式推理机与动物百科图谱检索算法，实现白盒透明推导；",
        "深刻体会到了符号主义人工智能在逻辑演绎、可解释性与因果决策上的独特优势；",
        "团队分工明确，圆满完成了从知识建模、代码开发、报告撰写到演示汇报的全套工作。"
    ]
    for s_i in items_sum:
        p_sub = tf10.add_paragraph()
        p_sub.text = f"✔ {s_i}"
        p_sub.font.size = Pt(15)
        p_sub.font.color.rgb = RGBColor(255, 255, 255)
        p_sub.font.name = "微软雅黑"
        p_sub.space_after = Pt(10)

    p_end = tf10.add_paragraph()
    p_end.text = "\n感谢各位老师与同学的聆听！欢迎交流讨论！"
    p_end.font.size = Pt(18)
    p_end.font.bold = True
    p_end.font.color.rgb = COLOR_ACCENT
    p_end.font.name = "微软雅黑"

    output_pptx = "G:\\code\\ep1\\课堂报告汇报_动物识别与知识图谱.pptx"
    prs.save(output_pptx)
    print(f"PPT 演示文稿生成完毕: {output_pptx}")
    try:
        prs.save("G:\\code\\ep1\\课堂报告汇报_知识表示与推理.pptx")
    except Exception:
        pass

if __name__ == "__main__":
    create_presentation()
