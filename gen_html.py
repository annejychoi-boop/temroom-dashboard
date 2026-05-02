import json, os

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, 'discovery.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

tag_colors = {
    'IT': '#2196f3', '뷰티': '#e91e63', '주방': '#ff9800', '패션': '#9c27b0',
    '생활': '#4caf50', '인테리어': '#00bcd4', '정리': '#607d8b', '육아': '#ff5722',
    '문구': '#795548', '캠핑': '#8bc34a', '피크닉': '#cddc39', '웰니스': '#009688',
    '건강식품': '#2e7d32', '바디케어': '#f06292', '선케어': '#ffb300', '헤어케어': '#7b1fa2',
    '가드닝': '#66bb6a', '생활가전': '#1565c0', '주방가전': '#e65100', '이벤트': '#d32f2f',
    '식품': '#bf360c',
}
viral_colors = {
    '품절대란': '#ff4444', 'SNS바이럴': '#e040fb', 'SNS화제': '#e040fb', '가성비': '#4caf50',
    '영상적합': '#2196f3', '스테디': '#607d8b', '트렌드': '#9c27b0', '인기': '#ff9800',
    '시즌한정': '#00bcd4', '시즌인기': '#00bcd4', '한정판': '#ff6f00', '올영픽': '#66bb6a',
    '올영1위': '#ffd43b', '올영단독': '#66bb6a', '쿠가세특가': '#1565c0',
}
source_emoji = {'다이소': '🛒', '올리브영': '🟢', '쿠팡': '🟠'}
source_order = ['다이소', '올리브영', '쿠팡']

import re
def make_id(name):
    return re.sub(r'[^가-힣a-zA-Z0-9]', '_', name)

def render_item(p):
    pid = make_id(p['name'])
    type_class = 'type-reels' if p['type'] == '릴스' else 'type-feed'
    tc = tag_colors.get(p['tag'], '#6a7090')
    vc = viral_colors.get(p['viral'], '#6a7090')
    esc_name = p['name'].replace("'", "\\'")
    return f'''<div class="disc-item" id="disc-{pid}" data-type="{p['type']}">
  <div class="disc-top">
    <span class="disc-name">{p['name']}</span>
    <div style="display:flex;gap:6px;align-items:center;">
      <span class="disc-price">{p['price']}</span>
      <button class="save-btn" id="save-{pid}" onclick="toggleSave('{pid}','{esc_name}','{p['source']}')">☆</button>
    </div>
  </div>
  <div class="disc-why">{p['why']}</div>
  <div class="disc-tags">
    <span class="{type_class}">{p['type']}</span>
    <span class="disc-tag" style="background:{tc}20;color:{tc};">{p['tag']}</span>
    <span class="disc-viral" style="background:{vc}20;color:{vc};">{p['viral']}</span>
  </div>
</div>'''

# Group by source
groups = {s: [] for s in source_order}
for p in data['products']:
    src = p['source']
    if src not in groups:
        groups[src] = []
    groups[src].append(p)

disc_html = ''
for src in source_order:
    if not groups.get(src):
        continue
    emoji = source_emoji.get(src, '📦')
    disc_html += f'<div class="disc-group"><div class="disc-source">{emoji} {src}</div>'
    for p in groups[src]:
        disc_html += render_item(p)
    disc_html += '</div>\n'

# Read existing HTML
with open(os.path.join(DIR, 'index.html'), 'r', encoding='utf-8') as f:
    old_html = f.read()

start_marker = '<!-- 제품 발굴 탭 -->'
end_marker = '<!-- 저장됨 탭 -->'

before_idx = old_html.index(start_marker)
after_idx = old_html.index(end_marker)

before = old_html[:before_idx]
after = old_html[after_idx:]

new_disc = f'''<!-- 제품 발굴 탭 -->
<div class="tab-content" id="content-disc">

<div class="disc-header">
  <div class="title">🔍 제품 발굴</div>
  <div class="updated">업데이트: {data['updated']}</div>
</div>

<div class="disc-filters">
  <div class="disc-filter active" onclick="filterDisc('all')">전체</div>
  <div class="disc-filter" onclick="filterDisc('릴스')">릴스용</div>
  <div class="disc-filter" onclick="filterDisc('피드')">피드용</div>
</div>

{disc_html}
<div style="text-align:center;padding:20px;color:#5a6080;font-size:12px;">
  ☆ 버튼을 눌러 관심 제품을 저장하세요
</div>

</div>

'''

new_html = before + new_disc + after

with open(os.path.join(DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(new_html)

total = len(data['products'])
print(f'Dashboard updated: {total} products, date: {data["updated"]}')
