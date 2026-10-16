#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 LITEARM SE 产品手册 / 软件开发手册 两份 markdown 生成一个类似飞书 wiki 的
静态网页站点（manual_site/index.html）。

处理要点：
- 删除 ```{=latex} 原始 LaTeX 块，按需重建为 HTML：
    封面 titlepage      -> 封面卡片（解析出标题/副标题/版本信息表）
    \tableofcontents    -> 丢弃（改由左侧目录树承担）
    \begin{figure} 安全图-> 产品：2x2 网格；开发手册：逐条配图
- 正文 markdown 交给 pandoc 转 html（表格/代码块/图片等复用既有渲染）。
- 图片不拷贝：index.html 以 ../LITEARM_SE_images/ 引用仓库根目录的图，避免仓库里
  多存一份 7 MB 的二进制副本。所以站点要连着仓库一起看（浏览器直接打开
  manual_site/index.html 即可），单独把 index.html 拷出去图片会失效。
"""
import re, os, subprocess, sys

# 本脚本在 build/ 下，仓库根目录是它的上一级。
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "manual_site")
os.makedirs(SITE, exist_ok=True)

LATEX_RE = re.compile(r"```\{=latex\}\n(.*?)```", re.S)

# ---------------------------------------------------------------- 小工具
def decode_tex(s):
    """粗解 LaTeX 片段成可读文本（去掉 \hspace/\quad/\textit 等）。"""
    s = s.replace("\\,", " ").replace("\\quad", " ")
    s = re.sub(r"\\hspace\{[^}]*\}", "", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"\1", s)
    s = s.replace("~", " ")
    return re.sub(r"\s+", " ", s).strip()

def parse_cover(latex):
    d = {}
    m = re.search(r"\\fontsize\{36\}\{44\}\\selectfont\\bfseries\s+([^\\{]+)", latex)
    d["big"] = decode_tex(m.group(1)) if m else "LITEARM SE"
    m = re.search(r"\\fontsize\{24\}\{34\}\\selectfont\\bfseries\s+([^\\{]+)", latex)
    d["big2"] = decode_tex(m.group(1)) if m else ""
    m = re.search(r"\\fontsize\{13\}\{19\}\\selectfont\s+([^\\]+)", latex)
    d["tag"] = decode_tex(m.group(1)) if m else ""
    rows = []
    tb = re.search(r"\\begin{tabular}.*?\\end{tabular}", latex, re.S)
    if tb:
        for rl in tb.group(0).splitlines():
            rl = rl.strip()
            if rl.startswith("\\begin") or rl.startswith("\\end") or not rl:
                continue
            mm = re.match(r"([^&]+)&([^\\\\]+)\\\\", rl)
            if mm:
                rows.append((decode_tex(mm.group(1)), decode_tex(mm.group(2))))
    m = re.search(r"\\small\s+([^}]+?)\s*\}\s*$", latex, re.S)
    d["bottom"] = decode_tex(m.group(1)) if m else "NEXFORM ROBOTICS"
    d["rows"] = rows
    return d

def cover_html(d):
    rows = "".join(
        "<tr><th>%s</th><td>%s</td></tr>" % (k, v) for k, v in d["rows"]
    )
    big2 = ('<span class="cover-big2">%s</span>' % d["big2"]) if d["big2"] else ""
    return (
        '<section class="doc-cover">'
        '<p class="cover-brand">NEXFORM&nbsp;ROBOTICS</p>'
        '<h1 class="cover-title">%s %s</h1>'
        '<p class="cover-sub">%s</p>'
        '<table class="cover-meta">%s</table>'
        '<p class="cover-foot">%s</p>'
        "</section>"
    ) % (d["big"], big2, d["tag"], rows, d["bottom"])

def safety_html_product():
    items = [
        ("danger.png", "危险"),
        ("warning.png", "警告"),
        ("high_temp.png", "高温"),
        ("notice.png", "注意"),
    ]
    figs = ""
    for f, lab in items:
        figs += (
            '<figure class="s-item"><img src="LITEARM_SE_images/safety/%s" alt="%s">'
            "<figcaption>%s</figcaption></figure>" % (f, lab, lab)
        )
    return (
        '<div class="safety-grid" aria-label="安全警示标志">'
        '<div class="s-row">%s</div>'
        "<p class=\"fig-note\">安全警示标志（图样以产品随附标识为准）</p></div>"
    ) % figs

def safety_html_dev():
    items = [
        ("danger.png", "危险", "用于可能导致人员伤亡或设备严重损坏的危险情况。"),
        ("warning.png", "警告", "用于如不避免，可导致人员伤亡或设备严重损坏的危险情况。"),
        ("high_temp.png", "高温", "用于存在高温部件、接触可能造成灼烫伤害或设备损坏的危险情况。"),
        ("notice.png", "注意", "用于如不避免，可能导致人员伤害或设备损坏的一般警示。"),
    ]
    parts = ""
    for f, lab, txt in items:
        parts += (
            '<div class="safe-item">'
            "<p class=\"safe-text\"><strong>%s</strong>：%s</p>"
            '<img class="s-icon" src="LITEARM_SE_images/safety/%s" alt="%s">'
            "</div>" % (lab, txt, f, lab)
        )
    return '<div class="safety-list" aria-label="安全警示标志">%s</div>' % parts

def process(md_path):
    t = open(md_path, encoding="utf-8").read()

    def repl_cover(m):
        d = parse_cover(m.group(1))
        had_rev = "\\section*{修订记录}" in m.group(1)
        out = cover_html(d)
        if had_rev:
            out += "\n\n## 修订记录\n\n"
        return out

    def repl_safety(m):
        body = m.group(1)
        # 产品手册：\begin{figure} 里的 2x2 网格；开发手册：\textbullet 逐条配图
        if "\\begin{figure}" in body:
            return safety_html_product()
        return safety_html_dev()

    def classify(m):
        body = m.group(1)
        if "\\begin{titlepage}" in body:
            return repl_cover(m)
        if "\\tableofcontents" in body:
            return ""  # 目录 -> 侧栏导航
        if "\\begin{figure}" in body or "danger.png" in body:
            return repl_safety(m)
        return ""

    out = LATEX_RE.sub(classify, t)
    return out

def pandoc_fragment(md_text, name):
    tmp = os.path.join(SITE, "_" + name + ".md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(md_text)
    r = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html", tmp],
        capture_output=True, text=True,
    )
    os.remove(tmp)
    if r.returncode != 0:
        print("pandoc error:", r.stderr); sys.exit(1)
    return r.stdout

# ---------------------------------------------------------------- 渲染两份文档
def load(name, human):
    md = os.path.join(ROOT, name)
    return human, process(md)

docs = [
    load("LITEARM_SE产品手册.md", "产品手册"),
    load("LITEARM SE软件开发手册.md", "软件开发手册"),
]

frags = {}
for key, (human, md_text) in zip(["product", "dev"], docs):
    frags[key] = pandoc_fragment(md_text, key)
    print("fragment %s: %d chars" % (key, len(frags[key])))

# 图片不拷贝，改为把下文所有 LITEARM_SE_images/ 引用指回仓库根目录（见文件头说明）。
def rebase_images(html):
    return html.replace('"LITEARM_SE_images/', '"../LITEARM_SE_images/')


# ---------------------------------------------------------------- 页面壳
CSS = r"""
:root{
  --accent:#3370ff; --accent-weak:#eaf1ff;
  --bg:#f4f5f7; --card:#ffffff; --line:#e4e6eb;
  --text:#1f2329; --muted:#646a73; --muted2:#8f959e;
  --code-bg:#f6f8fa; --hover:#f2f3f5;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"Noto Sans CJK SC","Noto Sans SC","Source Han Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  background:var(--bg);color:var(--text);font-size:15px;line-height:1.75;}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}

/* 顶栏 */
.topbar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:24px;
  background:#fff;border-bottom:1px solid var(--line);height:52px;padding:0 20px;}
.brand{display:flex;align-items:center;gap:9px;font-weight:700;font-size:15px;white-space:nowrap}
.brand .logo{width:24px;height:24px;border-radius:6px;background:linear-gradient(135deg,#3370ff,#0f3fd0);
  color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800}
.tabs{margin-left:auto;display:flex;background:var(--bg);border-radius:8px;padding:3px;gap:2px}
.tab{border:0;background:transparent;padding:5px 16px;border-radius:6px;cursor:pointer;
  font-size:14px;color:var(--muted);font-family:inherit}
.tab.active{background:#fff;color:var(--accent);font-weight:600;box-shadow:0 1px 3px rgba(0,0,0,.08)}

/* 布局 */
.layout{display:flex;align-items:flex-start;max-width:1240px;margin:0 auto}
.sidebar{position:sticky;top:52px;align-self:flex-start;width:264px;flex:none;height:calc(100vh - 52px);
  overflow:auto;padding:14px 10px 40px;border-right:1px solid var(--line)}
.search input{width:100%;border:1px solid var(--line);border-radius:6px;padding:6px 10px;
  font-size:13px;background:#fff;outline:none;margin-bottom:8px}
.search input:focus{border-color:var(--accent)}
.tree ul{list-style:none;margin:0;padding-left:0}
.tree .lv1>a{font-weight:600;color:var(--text)}
.tree a{display:block;padding:3px 8px;border-radius:5px;color:var(--muted);font-size:13.5px;
  text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tree ul ul a{padding-left:20px}
.tree ul ul ul a{padding-left:34px;font-size:13px;color:var(--muted2)}
.tree a:hover{background:var(--hover);color:var(--accent);text-decoration:none}
.tree a.cur{background:var(--accent-weak);color:var(--accent);font-weight:600}
.tree .none{color:var(--muted2);padding:6px 8px;font-size:13px}

/* 正文 */
.content{flex:1;min-width:0;padding:20px 28px 80px}
.doc{background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:34px 44px 40px;max-width:900px;margin:0 auto}
.doc h1,.doc h2,.doc h3,.doc h4{line-height:1.4;color:#101419;scroll-margin-top:70px}
.doc h1{font-size:24px;border-bottom:2px solid var(--line);padding-bottom:10px;margin:10px 0 20px}
.doc h2{font-size:19px;margin:28px 0 12px;padding-left:10px;border-left:4px solid var(--accent)}
.doc h3{font-size:16px;margin:20px 0 8px}
.doc h4{font-size:15px;margin:16px 0 6px;color:#3a3f47}
.doc p{margin:8px 0}
.doc hr{border:0;border-top:1px dashed var(--line);margin:26px 0}
.doc blockquote{margin:10px 0;padding:10px 16px;background:#fafbfc;border-left:4px solid var(--accent);
  border-radius:4px;color:#333}
.doc ul,.doc ol{padding-left:26px;margin:8px 0}
.doc li{margin:4px 0}
.doc strong{font-weight:700}
code{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;font-size:12.5px;
  background:var(--code-bg);border:1px solid #e6e8eb;border-radius:4px;padding:1px 5px;color:#c7254e}
pre{background:#f7f9fb;border:1px solid var(--line);border-radius:8px;padding:12px 14px;
  overflow-x:auto;line-height:1.5;margin:10px 0}
pre code{background:transparent;border:0;padding:0;color:#2b2f36;font-size:12.5px;white-space:pre}
.doc img{max-width:100%;height:auto}
.doc figure{margin:16px auto;text-align:center}
.doc figure img{display:block;margin:0 auto;max-height:520px;border:1px solid #edf0f3;border-radius:6px}
.doc figure figcaption{color:var(--muted);font-size:13px;margin-top:6px}
.doc table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13.5px}
.doc th,.doc td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
.doc thead th,.doc tr:first-child th{background:#f7f8fa;font-weight:600}
.doc tbody tr:nth-child(even){background:#fafbfc}
.doc th[rowspan]{vertical-align:middle}

/* 封面卡片 */
.doc-cover{border:1px solid var(--line);border-radius:12px;padding:30px 34px;margin:6px 0 26px;
  background:linear-gradient(180deg,#ffffff,#f7f9ff)}
.cover-brand{letter-spacing:2px;color:var(--muted2);font-size:12.5px;margin:0 0 4px}
.cover-title{margin:0 0 2px;font-size:34px;font-weight:800;border:0;padding:0;letter-spacing:1px}
.cover-big2{color:var(--accent)}
.cover-sub{color:var(--muted);font-size:14px;margin:2px 0 16px}
.cover-meta{margin:0;max-width:460px;border:0}
.cover-meta th,.cover-meta td{border:0;border-bottom:1px dashed var(--line);background:transparent!important;
  padding:5px 8px;font-size:13.5px}
.cover-meta th{color:var(--muted);width:96px;font-weight:500;text-align:left}
.cover-foot{margin:18px 0 0;color:var(--muted2);font-size:12px}

/* 安全标志 */
.safety-grid{margin:14px 0;text-align:center}
.safety-grid .s-row{display:flex;justify-content:center;gap:22px;flex-wrap:wrap}
.s-item{margin:8px 6px;text-align:center}
.s-item img{width:54px;height:54px;object-fit:contain}
.s-item figcaption{font-size:13px;color:var(--muted)}
.fig-note{color:var(--muted);font-size:12.5px;margin-top:8px}
.safety-list{margin:12px 0;display:flex;flex-direction:column;gap:16px}
.safe-item{text-align:center}
.safe-item .safe-text{display:block;text-align:left;max-width:520px;margin:0 auto 6px}
.s-icon{width:44px;height:44px;object-fit:contain}
.doc-footer{color:var(--muted2);text-align:center;font-size:12.5px;border-top:1px solid var(--line);
  padding-top:14px;margin-top:34px}
@media (max-width:820px){.sidebar{display:none}.content{padding:12px}.doc{padding:20px 18px}}
"""

JS = r"""
(function(){
  var DOCS={product:"产品手册",dev:"软件开发手册"};
  var articles={},trees={};
  Object.keys(DOCS).forEach(function(k){
    var art=document.getElementById("doc-"+k);
    var nav=document.getElementById("tree-"+k);
    articles[k]=art;trees[k]=nav;
    buildTree(art,nav);
  });
  function levelName(h){return h.tagName.toLowerCase()}
  function buildTree(art,nav){
    var lis=[];
    art.querySelectorAll("h1,h2,h3,h4").forEach(function(h){
      if(h.closest(".doc-cover"))return;   // 封面大标题不进目录
      var id=h.id||("sec-"+Math.random().toString(36).slice(2,8));
      if(!h.id)h.id=id;
      var lv=parseInt(levelName(h).slice(1));
      var a=document.createElement("a");
      a.href="#"+id;a.textContent=h.textContent;
      var li=document.createElement("li");li.className="lv"+lv;
      li.appendChild(a);lis.push({li:li,lv:lv,a:a});
    });
    var stack=[{ul:document.createElement("ul"),lv:0}];
    lis.forEach(function(it){
      while(stack[stack.length-1].lv>=it.lv)stack.pop();
      var top=stack[stack.length-1];
      top.ul.appendChild(it.li);
      var ul=document.createElement("ul");
      it.li.appendChild(ul);
      stack.push({ul:ul,lv:it.lv});
    });
    nav.appendChild(stack[0].ul);
    if(!lis.length){var p=document.createElement("p");p.className="none";p.textContent="暂无目录";nav.appendChild(p);}
  }
  function activeTab(k){
    Object.keys(DOCS).forEach(function(x){
      articles[x].style.display=(x===k)?"":"none";
      trees[x].style.display=(x===k)?"":"none";
      document.querySelector('.tab[data-doc="'+x+'"]').classList.toggle("active",x===k);
    });
    document.title="LITEARM SE 资料 · "+DOCS[k]+" · NEXFORM ROBOTICS";
  }
  document.querySelectorAll(".tab").forEach(function(b){
    b.addEventListener("click",function(){
      activeTab(b.getAttribute("data-doc"));
      history.replaceState(null,"","#"+b.getAttribute("data-doc"));
    });
  });
  var initedHash=location.hash.replace("#","");
  if(DOCS[initedHash])activeTab(initedHash);else activeTab("product");
  function current(){for(var k in DOCS){if(articles[k].style.display!=="none")return k;}return "product"}
  function clearCur(){for(var k in DOCS)trees[k].querySelectorAll("a.cur").forEach(function(a){a.classList.remove("cur")})}
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      var h=e.target,art=h.closest(".doc"),k=null;
      Object.keys(DOCS).forEach(function(x){if(art===articles[x])k=x});
      if(!k)return;
      clearCur();
      var n=trees[k].querySelector('a[href="#'+h.id+'"]');
      if(n)n.classList.add("cur");
    });
  },{rootMargin:"-70px 0px -70% 0px",threshold:0});
  Object.keys(DOCS).forEach(function(k){
    articles[k].querySelectorAll("h1,h2,h3,h4").forEach(function(h){io.observe(h)});
  });
  var q=document.getElementById("q");
  q.addEventListener("input",function(){
    var s=q.value.trim().toLowerCase(),k=current();
    trees[k].querySelectorAll("li").forEach(function(li){
      if(!s){li.style.display="";return}
      var a=li.querySelector(":scope > a");
      var me=a&&a.textContent.toLowerCase().indexOf(s)>=0;
      var hasChild=[].some.call(li.querySelectorAll("a"),function(x){
        return x!==a&&x.textContent.toLowerCase().indexOf(s)>=0;});
      li.style.display=(me||hasChild)?"":"none";
    });
  });
})();
"""

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LITEARM SE 资料 · 产品手册 · NEXFORM ROBOTICS</title>
<style>%s</style>
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="logo">N</span>LITEARM SE 资料</div>
  <nav class="tabs">
    <button class="tab active" data-doc="product">产品手册</button>
    <button class="tab" data-doc="dev">软件开发手册</button>
  </nav>
</header>
<div class="layout">
  <aside class="sidebar">
    <div class="search"><input id="q" placeholder="搜索当前文档章节…" autocomplete="off"></div>
    <nav id="tree-product" class="tree"></nav>
    <nav id="tree-dev" class="tree" style="display:none"></nav>
  </aside>
  <main class="content">
    <article id="doc-product" class="doc">%s</article>
    <article id="doc-dev" class="doc" style="display:none">%s</article>
  </main>
</div>
<script>%s</script>
</body>
</html>
"""

index = rebase_images(HTML % (CSS, frags["product"], frags["dev"], JS))
with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index)
print("written", os.path.join(SITE, "index.html"), len(index), "bytes")
