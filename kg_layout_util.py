"""
专业美观的动物知识图谱绘制逻辑
包含：
1. 全局图谱绘制（极坐标开阔布局，杜绝重叠）
2. 单物种聚焦子图绘制（结构精炼，大字体卡片设计，用于专注展示）
"""

import math
import textwrap
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def generate_beautiful_kg(graph, output_path="knowledge_graph.png", highlight_animal=None):
    fig, ax = plt.subplots(figsize=(15, 15), dpi=300)
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')

    animals = ["长颈鹿", "金钱豹", "老虎", "鸵鸟", "企鹅", "斑马"]
    n_animals = len(animals)
    
    pos = {}
    r_center = 3.6    # 中心动物分布半径
    r_prop = 7.4      # 外围属性分布半径

    for i, animal in enumerate(animals):
        # 均匀分布在圆周各角度
        base_angle = (2 * math.pi / n_animals) * i + (math.pi / 6)
        pos[animal] = (r_center * math.cos(base_angle), r_center * math.sin(base_angle))
        
        neighbors = list(graph.neighbors(animal)) if graph.has_node(animal) else []
        k = len(neighbors)
        if k == 0:
            continue
            
        span = 0.48  # 扇区张开角度
        if k == 1:
            offsets = [0]
        else:
            offsets = [ -span/2 + (span / (k - 1)) * j for j in range(k) ]
            
        for neighbor, off in zip(neighbors, offsets):
            ang = base_angle + off
            # 如果是已有坐标（共享节点），稍微做微调避免覆盖
            if neighbor in pos:
                # 共享节点居中取平均位置
                prev_x, prev_y = pos[neighbor]
                pos[neighbor] = ((prev_x + r_prop * math.cos(ang)) / 2, (prev_y + r_prop * math.sin(ang)) / 2)
            else:
                pos[neighbor] = (r_prop * math.cos(ang), r_prop * math.sin(ang))

    # 绘制边与箭头
    for u, v, d in graph.edges(data=True):
        is_highlight = (u == highlight_animal)
        edge_color = "#E11D48" if is_highlight else "#94A3B8"
        edge_width = 2.8 if is_highlight else 1.3
        edge_alpha = 0.95 if is_highlight else 0.65
        
        ax.annotate(
            "",
            xy=pos[v],
            xytext=pos[u],
            arrowprops=dict(
                arrowstyle="-|>",
                color=edge_color,
                lw=edge_width,
                alpha=edge_alpha,
                mutation_scale=16,
                shrinkA=30,
                shrinkB=34
            )
        )
        
        # 关系文字标签
        rel_text = d.get("relation", "")
        if rel_text:
            x_m = (pos[u][0] + pos[v][0]) / 2
            y_m = (pos[u][1] + pos[v][1]) / 2
            ax.text(
                x_m, y_m, rel_text,
                fontsize=9,
                ha='center', va='center',
                color='#0F172A',
                fontweight='bold' if is_highlight else 'normal',
                bbox=dict(
                    boxstyle='round,pad=0.25',
                    facecolor='#FFFFFF' if not is_highlight else '#FFF1F2',
                    edgecolor='#CBD5E1' if not is_highlight else '#FB7185',
                    linewidth=1,
                    alpha=0.96
                )
            )

    # 绘制外围属性节点
    for node in graph.nodes():
        if node not in animals:
            x, y = pos[node]
            wrapped_text = "\n".join(textwrap.wrap(node, width=7))
            ax.text(
                x, y, wrapped_text,
                fontsize=9.5,
                ha='center', va='center',
                color='#0F172A',
                weight='500',
                bbox=dict(
                    boxstyle='round,pad=0.55',
                    facecolor='#F0F9FF',
                    edgecolor='#0284C7',
                    linewidth=1.2,
                    alpha=0.98
                )
            )

    # 绘制核心动物节点
    for animal in animals:
        if animal in pos:
            x, y = pos[animal]
            is_hl = (animal == highlight_animal)
            bg_col = "#E11D48" if is_hl else "#2563EB"
            border_col = "#FFE4E6" if is_hl else "#DBEAFE"
            
            ax.text(
                x, y, animal,
                fontsize=13.5,
                fontweight='bold',
                ha='center', va='center',
                color='#FFFFFF',
                bbox=dict(
                    boxstyle='circle,pad=0.68',
                    facecolor=bg_col,
                    edgecolor=border_col,
                    linewidth=2.8,
                    alpha=0.98
                )
            )

    all_x = [p[0] for p in pos.values()]
    all_y = [p[1] for p in pos.values()]
    pad = 1.6
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)
    ax.axis("off")
    
    plt.title("经典动物百科知识图谱 (实体-关系-属性星型放射拓扑)", fontsize=18, pad=25, fontweight="bold", color="#1E293B")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def generate_focus_kg(animal, graph, output_path="focus_graph.png"):
    """为指定动物生成专属的聚焦知识子图（用于在 Web 和汇报中精美特写呈现）"""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    neighbors = list(graph.neighbors(animal)) if graph.has_node(animal) else []
    k = len(neighbors)
    if k == 0:
        plt.close()
        return None

    # 中心动物放左侧 x=1.5, y=3
    pos = {animal: (1.5, 3.0)}
    y_step = 4.0 / max(k - 1, 1) if k > 1 else 0
    y_start = 5.0

    for i, neighbor in enumerate(neighbors):
        y_pos = y_start - i * y_step if k > 1 else 3.0
        pos[neighbor] = (5.5, y_pos)

    # 绘制边
    for neighbor in neighbors:
        d = graph[animal][neighbor]
        ax.annotate(
            "",
            xy=pos[neighbor],
            xytext=pos[animal],
            arrowprops=dict(
                arrowstyle="-|>",
                color="#2563EB",
                lw=2.2,
                mutation_scale=18,
                shrinkA=35,
                shrinkB=38
            )
        )
        # 关系文字
        rel_text = d.get("relation", "")
        x_m = (pos[animal][0] + pos[neighbor][0]) / 2
        y_m = (pos[animal][1] + pos[neighbor][1]) / 2
        ax.text(
            x_m, y_m, rel_text,
            fontsize=10.5,
            fontweight='bold',
            ha='center', va='center',
            color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#BFDBFE', linewidth=1)
        )

    # 绘制中心动物
    ax.text(
        pos[animal][0], pos[animal][1], f"【{animal}】",
        fontsize=15,
        fontweight='bold',
        ha='center', va='center',
        color='#FFFFFF',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#E11D48', edgecolor='#FDA4AF', linewidth=2)
    )

    # 绘制属性
    for neighbor in neighbors:
        wrapped_text = "\n".join(textwrap.wrap(neighbor, width=12))
        ax.text(
            pos[neighbor][0], pos[neighbor][1], wrapped_text,
            fontsize=11,
            ha='center', va='center',
            color='#0F172A',
            weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0FDF4', edgecolor='#86EFAC', linewidth=1.5)
        )

    ax.set_xlim(0, 7.5)
    ax.set_ylim(0.5, 5.5)
    ax.axis("off")
    plt.title(f"【{animal}】专属知识图谱属性关联子图", fontsize=14, pad=15, fontweight="bold", color="#1E293B")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path
