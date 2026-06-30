"""审美训练题库与每日选题逻辑。"""

from __future__ import annotations

import hashlib
from datetime import date
from typing import Any

QUESTION_BANK: list[dict[str, Any]] = [
    # ── 色彩 ──────────────────────────────────────────────────────
    {
        "id": "color-001",
        "category": "color",
        "category_label": "色彩",
        "title": "哪一组配色更和谐？",
        "hint": "注意色相之间的关系与明度平衡",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "palette",
                    "colors": ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"],
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "palette",
                    "colors": ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"],
                },
            },
        ],
        "correct": "A",
        "explanation": "方案 A 采用类比色与互补色的克制搭配，明度层次清晰；方案 B 为高饱和原色硬拼，缺乏过渡，视觉冲突强烈。",
    },
    {
        "id": "color-002",
        "category": "color",
        "category_label": "色彩",
        "title": "哪个背景更能突出主体？",
        "hint": "主体与背景的明度/饱和度对比是关键",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "card_on_bg",
                    "bg": "#1A1A2E",
                    "card": "#E94560",
                    "text": "重点信息",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "card_on_bg",
                    "bg": "#F5C6CB",
                    "card": "#E94560",
                    "text": "重点信息",
                },
            },
        ],
        "correct": "A",
        "explanation": "深色背景与亮色卡片形成强烈明度对比，主体更突出；相近色相的浅色背景会削弱层次感。",
    },
    {
        "id": "color-003",
        "category": "color",
        "category_label": "色彩",
        "title": "哪组渐变更自然？",
        "hint": "渐变的起止色应在色轮上相邻或协调",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "gradient",
                    "from": "#667EEA",
                    "to": "#764BA2",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "gradient",
                    "from": "#00FF00",
                    "to": "#FF0000",
                },
            },
        ],
        "correct": "A",
        "explanation": "蓝紫渐变属于邻近色相过渡，中间色自然；绿到红的渐变跨越色轮对立面，中间会出现不自然的灰浊色带。",
    },
    {
        "id": "color-004",
        "category": "color",
        "category_label": "色彩",
        "title": "哪个界面配色更专业？",
        "hint": "专业界面通常控制色彩数量，用中性色打底",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "ui_mock",
                    "bg": "#F8F9FA",
                    "accent": "#4361EE",
                    "text": "#212529",
                    "secondary": "#6C757D",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "ui_mock",
                    "bg": "#FFE066",
                    "accent": "#FF6B6B",
                    "text": "#4ECDC4",
                    "secondary": "#FF9F43",
                },
            },
        ],
        "correct": "A",
        "explanation": "中性底色 + 单一强调色是经典的专业配色模式；多色高饱和混搭容易显得杂乱、缺乏层级。",
    },
    {
        "id": "color-005",
        "category": "color",
        "category_label": "色彩",
        "title": "哪组文字配色可读性更好？",
        "hint": "文字与背景的对比度影响阅读体验",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "text_block",
                    "bg": "#FFFFFF",
                    "text_color": "#1A1A1A",
                    "text": "清晰易读的正文内容",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "text_block",
                    "bg": "#FFFFFF",
                    "text_color": "#D4D4D4",
                    "text": "清晰易读的正文内容",
                },
            },
        ],
        "correct": "A",
        "explanation": "深色文字在白色背景上对比度充足；浅灰文字对比不足，长时间阅读易疲劳。",
    },
    # ── 排版 ──────────────────────────────────────────────────────
    {
        "id": "type-001",
        "category": "typography",
        "category_label": "排版",
        "title": "哪组标题层级更清晰？",
        "hint": "字号、字重差异应足够明显",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "typography",
                    "title_size": 28,
                    "title_weight": 700,
                    "subtitle_size": 16,
                    "subtitle_weight": 400,
                    "title": "主标题",
                    "subtitle": "副标题说明文字",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "typography",
                    "title_size": 20,
                    "title_weight": 600,
                    "subtitle_size": 18,
                    "subtitle_weight": 500,
                    "title": "主标题",
                    "subtitle": "副标题说明文字",
                },
            },
        ],
        "correct": "A",
        "explanation": "主标题 28px/700 与副标题 16px/400 形成明确层级；方案 B 字号过于接近，视觉权重差异不足。",
    },
    {
        "id": "type-002",
        "category": "typography",
        "category_label": "排版",
        "title": "哪段正文行高更舒适？",
        "hint": "行高影响阅读节奏与密度感",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "paragraph",
                    "line_height": 1.75,
                    "font_size": 15,
                    "text": "好的行高能提升长文阅读体验，让眼睛在行间移动更自然流畅。",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "paragraph",
                    "line_height": 1.1,
                    "font_size": 15,
                    "text": "好的行高能提升长文阅读体验，让眼睛在行间移动更自然流畅。",
                },
            },
        ],
        "correct": "A",
        "explanation": "1.75 倍行高为中文正文常用舒适区间；1.1 行高过于紧凑，段落显得拥挤。",
    },
    {
        "id": "type-003",
        "category": "typography",
        "category_label": "排版",
        "title": "哪个段落对齐更整齐？",
        "hint": "左对齐是中文排版的常见最佳实践",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "paragraph",
                    "align": "left",
                    "line_height": 1.6,
                    "font_size": 14,
                    "text": "设计不仅是视觉呈现，更是信息传达的艺术。",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "paragraph",
                    "align": "justify",
                    "line_height": 1.6,
                    "font_size": 14,
                    "text": "设计不仅是视觉呈现，更是信息传达的艺术。",
                },
            },
        ],
        "correct": "A",
        "explanation": "短文本左对齐更自然；两端对齐在短行时容易产生不均匀的词间距。",
    },
    {
        "id": "type-004",
        "category": "typography",
        "category_label": "排版",
        "title": "哪组数字排版更规范？",
        "hint": "数字与中文混排时注意等宽与对齐",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "number_list",
                    "tabular": True,
                    "items": ["¥1,280.00", "¥9,999.00", "¥128.50"],
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "number_list",
                    "tabular": False,
                    "items": ["¥1,280.00", "¥9,999.00", "¥128.50"],
                },
            },
        ],
        "correct": "A",
        "explanation": "等宽数字（tabular figures）让金额纵向对齐，更利于快速比较；比例数字会造成小数点错位。",
    },
    {
        "id": "type-005",
        "category": "typography",
        "category_label": "排版",
        "title": "哪个按钮文字更易识别？",
        "hint": "按钮文字需要足够的字号与字重",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "button",
                    "font_size": 16,
                    "font_weight": 600,
                    "padding": 14,
                    "text": "立即开始",
                    "bg": "#4361EE",
                    "color": "#FFFFFF",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "button",
                    "font_size": 11,
                    "font_weight": 400,
                    "padding": 6,
                    "text": "立即开始",
                    "bg": "#4361EE",
                    "color": "#FFFFFF",
                },
            },
        ],
        "correct": "A",
        "explanation": "16px/600 字重配合充足内边距，点击目标明确；过小过轻的按钮降低可发现性与可点击性。",
    },
    # ── 构图 ──────────────────────────────────────────────────────
    {
        "id": "layout-001",
        "category": "layout",
        "category_label": "构图",
        "title": "哪个卡片布局更平衡？",
        "hint": "留白与对齐影响整体平衡感",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "card_layout",
                    "padding": 24,
                    "gap": 16,
                    "align": "left",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "card_layout",
                    "padding": 8,
                    "gap": 4,
                    "align": "left",
                },
            },
        ],
        "correct": "A",
        "explanation": "充足的内边距与元素间距让内容呼吸感更好；过于紧凑的布局显得压迫、缺乏品质感。",
    },
    {
        "id": "layout-002",
        "category": "layout",
        "category_label": "构图",
        "title": "哪组元素对齐更规整？",
        "hint": "对齐线是视觉秩序的基础",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "alignment",
                    "aligned": True,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "alignment",
                    "aligned": False,
                },
            },
        ],
        "correct": "A",
        "explanation": "左边缘对齐形成清晰的视觉轴线，信息扫描更高效；随意偏移会破坏秩序感。",
    },
    {
        "id": "layout-003",
        "category": "layout",
        "category_label": "构图",
        "title": "哪个网格布局更整洁？",
        "hint": "等宽列与一致间距是网格的基本原则",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "grid",
                    "columns": 3,
                    "gap": 12,
                    "equal": True,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "grid",
                    "columns": 3,
                    "gap": 12,
                    "equal": False,
                },
            },
        ],
        "correct": "A",
        "explanation": "等宽列与统一间距构成稳定的网格系统；不规则列宽让布局显得随意、不专业。",
    },
    {
        "id": "layout-004",
        "category": "layout",
        "category_label": "构图",
        "title": "哪个页面留白更得体？",
        "hint": "留白不是浪费，而是视觉呼吸空间",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "whitespace",
                    "margin": 32,
                    "density": "comfortable",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "whitespace",
                    "margin": 4,
                    "density": "cramped",
                },
            },
        ],
        "correct": "A",
        "explanation": "适度留白引导视线聚焦核心内容；填满每一寸空间会让界面显得廉价、压迫。",
    },
    {
        "id": "layout-005",
        "category": "layout",
        "category_label": "构图",
        "title": "哪个列表视觉节奏更好？",
        "hint": "一致的间距创造可预期的阅读节奏",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "list",
                    "item_gap": 16,
                    "consistent": True,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "list",
                    "item_gap": 16,
                    "consistent": False,
                },
            },
        ],
        "correct": "A",
        "explanation": "统一间距建立稳定的视觉节奏，用户可快速扫描；不规则间距增加认知负担。",
    },
    # ── 对比 ──────────────────────────────────────────────────────
    {
        "id": "contrast-001",
        "category": "contrast",
        "category_label": "对比",
        "title": "哪个按钮对比度达标？",
        "hint": "WCAG 建议正文对比度至少 4.5:1",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "button",
                    "font_size": 16,
                    "font_weight": 600,
                    "padding": 14,
                    "text": "确认提交",
                    "bg": "#1B4332",
                    "color": "#FFFFFF",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "button",
                    "font_size": 16,
                    "font_weight": 600,
                    "padding": 14,
                    "text": "确认提交",
                    "bg": "#B7E4C7",
                    "color": "#D8F3DC",
                },
            },
        ],
        "correct": "A",
        "explanation": "深绿底 + 白字对比度远超 4.5:1；浅绿底 + 更浅文字几乎不可读，不符合无障碍标准。",
    },
    {
        "id": "contrast-002",
        "category": "contrast",
        "category_label": "对比",
        "title": "哪组图标更易辨认？",
        "hint": "图标需要与背景有足够对比",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "icon_row",
                    "bg": "#FFFFFF",
                    "icon_color": "#374151",
                    "icons": ["★", "♥", "⚙"],
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "icon_row",
                    "bg": "#FFFFFF",
                    "icon_color": "#E5E7EB",
                    "icons": ["★", "♥", "⚙"],
                },
            },
        ],
        "correct": "A",
        "explanation": "深灰图标在白色背景上清晰可辨；极浅灰图标几乎融入背景，可用性大幅下降。",
    },
    {
        "id": "contrast-003",
        "category": "contrast",
        "category_label": "对比",
        "title": "哪个标签更易区分？",
        "hint": "状态标签需要色彩 + 明度双重区分",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "tags",
                    "tags": [
                        {"text": "成功", "bg": "#D1FAE5", "color": "#065F46"},
                        {"text": "警告", "bg": "#FEF3C7", "color": "#92400E"},
                        {"text": "错误", "bg": "#FEE2E2", "color": "#991B1B"},
                    ],
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "tags",
                    "tags": [
                        {"text": "成功", "bg": "#F0FDF4", "color": "#BBF7D0"},
                        {"text": "警告", "bg": "#FFFBEB", "color": "#FDE68A"},
                        {"text": "错误", "bg": "#FEF2F2", "color": "#FECACA"},
                    ],
                },
            },
        ],
        "correct": "A",
        "explanation": "深色文字配浅色底，每种状态对比充足；方案 B 文字与底色明度接近，状态难以辨认。",
    },
    {
        "id": "contrast-004",
        "category": "contrast",
        "category_label": "对比",
        "title": "哪个输入框状态更清晰？",
        "hint": "边框与占位符需要足够对比",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "input",
                    "border": "#9CA3AF",
                    "placeholder": "#6B7280",
                    "bg": "#FFFFFF",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "input",
                    "border": "#F3F4F6",
                    "placeholder": "#F3F4F6",
                    "bg": "#FFFFFF",
                },
            },
        ],
        "correct": "A",
        "explanation": "可见的边框与占位符帮助用户识别输入区域；几乎不可见的边框让表单难以操作。",
    },
    {
        "id": "contrast-005",
        "category": "contrast",
        "category_label": "对比",
        "title": "哪张卡片层次更分明？",
        "hint": "背景、卡片、文字三级对比建立层次",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "layered_card",
                    "page_bg": "#F3F4F6",
                    "card_bg": "#FFFFFF",
                    "text": "#111827",
                    "shadow": True,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "layered_card",
                    "page_bg": "#FAFAFA",
                    "card_bg": "#F5F5F5",
                    "text": "#D1D5DB",
                    "shadow": False,
                },
            },
        ],
        "correct": "A",
        "explanation": "灰底 + 白卡片 + 深色文字 + 阴影，三级层次分明；方案 B 各层明度过于接近，扁平含混。",
    },
    # ── 间距 ──────────────────────────────────────────────────────
    {
        "id": "space-001",
        "category": "spacing",
        "category_label": "间距",
        "title": "哪组按钮间距更合理？",
        "hint": "相关按钮靠近，独立操作留足间距",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "button_group",
                    "gap": 12,
                    "buttons": ["取消", "确认"],
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "button_group",
                    "gap": 2,
                    "buttons": ["取消", "确认"],
                },
            },
        ],
        "correct": "A",
        "explanation": "12px 间距避免误触，视觉上也是独立操作；过窄间距让按钮像连体，容易点错。",
    },
    {
        "id": "space-002",
        "category": "spacing",
        "category_label": "间距",
        "title": "哪个表单字段间距更舒服？",
        "hint": "字段组内紧、组间松",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "form_fields",
                    "field_gap": 20,
                    "label_gap": 6,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "form_fields",
                    "field_gap": 4,
                    "label_gap": 2,
                },
            },
        ],
        "correct": "A",
        "explanation": "标签与输入框 6px、字段间 20px 符合 8pt 网格；过于紧凑让表单难以填写。",
    },
    {
        "id": "space-003",
        "category": "spacing",
        "category_label": "间距",
        "title": "哪组图标与文字间距更协调？",
        "hint": "图标与文字需要视觉关联但不过紧",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "icon_text",
                    "gap": 8,
                    "icon": "🏠",
                    "text": "首页",
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "icon_text",
                    "gap": 0,
                    "icon": "🏠",
                    "text": "首页",
                },
            },
        ],
        "correct": "A",
        "explanation": "8px 间距让图标与文字成组又各自清晰；零间距显得拥挤、像是一个元素。",
    },
    {
        "id": "space-004",
        "category": "spacing",
        "category_label": "间距",
        "title": "哪个内容区边距更规范？",
        "hint": "页面边距通常遵循 16/24/32 倍数",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "page_margin",
                    "margin": 20,
                    "on_grid": True,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "page_margin",
                    "margin": 7,
                    "on_grid": False,
                },
            },
        ],
        "correct": "A",
        "explanation": "20px（接近 8pt 网格的 16/24）是移动端常见边距；7px 这类随意数值破坏系统性。",
    },
    {
        "id": "space-005",
        "category": "spacing",
        "category_label": "间距",
        "title": "哪组卡片内边距更精致？",
        "hint": "内边距影响内容的品质感",
        "options": [
            {
                "key": "A",
                "label": "方案 A",
                "visual": {
                    "type": "card_padding",
                    "padding": 20,
                },
            },
            {
                "key": "B",
                "label": "方案 B",
                "visual": {
                    "type": "card_padding",
                    "padding": 6,
                },
            },
        ],
        "correct": "A",
        "explanation": "20px 内边距让内容不贴边，品质感更好；6px 内边距让内容拥挤，显得粗糙。",
    },
]

DAILY_QUESTION_COUNT = 5

CATEGORY_INFO = {
    "color": {"label": "色彩", "icon": "🎨", "color": "#E91E63"},
    "typography": {"label": "排版", "icon": "✏️", "color": "#3F51B5"},
    "layout": {"label": "构图", "icon": "📐", "color": "#009688"},
    "contrast": {"label": "对比", "icon": "◐", "color": "#FF9800"},
    "spacing": {"label": "间距", "icon": "↔", "color": "#9C27B0"},
}


def _date_seed(d: date) -> int:
    raw = d.isoformat().encode()
    return int(hashlib.md5(raw).hexdigest(), 16)


def _shuffle_indices(seed: int, n: int) -> list[int]:
    """Deterministic Fisher-Yates shuffle."""
    indices = list(range(n))
    state = seed
    for i in range(n - 1, 0, -1):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        j = state % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    return indices


def get_daily_questions(target_date: date | None = None) -> list[dict[str, Any]]:
    """按日期确定性选取每日题目，保证同一天所有用户题目一致。"""
    d = target_date or date.today()
    seed = _date_seed(d)
    order = _shuffle_indices(seed, len(QUESTION_BANK))
    picked = [QUESTION_BANK[order[i]] for i in range(DAILY_QUESTION_COUNT)]
    return [_public_question(q, idx + 1) for idx, q in enumerate(picked)]


def _public_question(q: dict[str, Any], index: int) -> dict[str, Any]:
    """返回给前端的题目（不含正确答案）。"""
    return {
        "id": q["id"],
        "index": index,
        "total": DAILY_QUESTION_COUNT,
        "category": q["category"],
        "category_label": q["category_label"],
        "category_icon": CATEGORY_INFO[q["category"]]["icon"],
        "category_color": CATEGORY_INFO[q["category"]]["color"],
        "title": q["title"],
        "hint": q["hint"],
        "options": q["options"],
    }


def check_answer(question_id: str, choice: str) -> dict[str, Any]:
    """校验答案并返回解析。"""
    q = next((item for item in QUESTION_BANK if item["id"] == question_id), None)
    if q is None:
        return {"correct": False, "error": "题目不存在"}
    is_correct = choice.upper() == q["correct"]
    return {
        "correct": is_correct,
        "correct_answer": q["correct"],
        "explanation": q["explanation"],
        "category": q["category"],
        "category_label": q["category_label"],
    }


def get_stats_summary() -> dict[str, Any]:
    return {
        "total_questions": len(QUESTION_BANK),
        "daily_count": DAILY_QUESTION_COUNT,
        "categories": [
            {
                "key": key,
                "label": info["label"],
                "icon": info["icon"],
                "color": info["color"],
                "count": sum(1 for q in QUESTION_BANK if q["category"] == key),
            }
            for key, info in CATEGORY_INFO.items()
        ],
    }
