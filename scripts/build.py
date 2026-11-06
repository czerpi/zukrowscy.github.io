#!/usr/bin/env python3
"""Build the static archive using only the Python standard library."""
from pathlib import Path
from string import Template
from html import escape, unescape
import json,re,os
ROOT=Path(__file__).resolve().parent.parent
os.chdir(ROOT)
books=json.loads(Path('content/books.json').read_text())
pages=json.loads(Path('content/pages.json').read_text())
template=Template(Path('templates/page.html').read_text())
nav=[('index.html','Strona główna'),('zyciorys.html','Biografia'),('ksiazki.html','Książki'),('filmografia.html','Filmy'),('teksty.html','Wspomnienia'),('zdjecia.html','Archiwum')]
def render(path,title,section,content):
 prefix='../'*len(Path(path).parent.parts)
 navigation=''.join(f'<a href="{prefix}{url}"'+(' class="active" aria-current="page"' if url==section else '')+f'>{label}</a>' for url,label in nav)
 breadcrumbs=''
 if path!='index.html':
  section_label=dict(nav).get(section,'Archiwum')
  trail=f'<a href="{prefix}index.html">Strona główna</a>'
  if path!=section:
   trail+=f'<span aria-hidden="true">/</span><a href="{prefix}{section}">{section_label}</a>'
   current=re.split(r' — | \| ',unescape(title))[0]
  else: current=section_label
  breadcrumbs=f'<nav class="container breadcrumbs" aria-label="Ścieżka nawigacji">{trail}<span aria-hidden="true">/</span><span aria-current="page">{escape(current)}</span></nav>'
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(template.substitute(title=escape(unescape(title)),prefix=prefix,navigation=navigation,breadcrumbs=breadcrumbs,content=content,body_class='home' if path=='index.html' else 'inner-page'))
def url(b):return 'ksiazki/'+b['slug']+'.html'
def bookcard(b):
 cover=f'<img src="{b["covers"][0]}" alt="Okładka: {escape(b["title"])}" loading="lazy">' if b.get('covers') else f'<span class="type-cover">Wojciech Żukrowski<strong>{escape(b["title"])}</strong>{b["year"]}</span>'
 return f'<a class="book-card" href="{url(b)}"><div class="book-art">{cover}</div><div class="book-meta">{b["year"]} · WOJCIECH ŻUKROWSKI <span>↗</span></div><h3>{escape(b["title"])}</h3><p>{b.get("intro", "Poznaj zapis bibliograficzny i materiały archiwalne.")}</p></a>'
for page in pages:
 content=(Path('content/pages')/page['path']).read_text()
 if page['path']=='ksiazki.html':
  featured=[b for title in ['Kamienne tablice','Porwanie w Tiutiurlistanie','Z kraju milczenia'] for b in books if b['title']==title]
  shelf='<section class="container catalog-featured" aria-labelledby="selected-books"><div class="collection-heading"><h2 id="selected-books">Wybrane książki</h2><span>Na początek lektury</span></div><div class="book-grid">'+''.join(bookcard(b) for b in featured)+'</div></section>'
  rows=''
  for b in books:
   thumb=f'<img src="{b["covers"][0]}" alt="" loading="lazy">' if b.get('covers') else '<span class="cover-placeholder" aria-hidden="true">WŻ</span>'
   search_text=' '.join([b['title'],b['year'],b.get('genre',''),b.get('intro','')])
   rows+=f'<a class="catalog-row enriched-row" data-book="{escape(search_text)}" href="{url(b)}"><span class="catalog-thumb">{thumb}</span><div><span class="catalog-kind">{b["year"]} · {escape(b.get("genre","Literatura"))}</span><h2>{escape(b["title"])}</h2><p>{escape(b.get("intro",""))}</p></div><span aria-hidden="true">↗</span></a>'

  content=f'<section class="container page-opening"><div class="eyebrow">BIBLIOTEKA AUTORA</div><h1>Książki</h1><p>Powieści, opowiadania, poezja i historie dla najmłodszych. Odkrywaj twórczość Wojciecha Żukrowskiego chronologicznie lub znajdź konkretny tytuł.</p></section>{shelf}<section class="container catalog"><div class="collection-heading"><h2>Pełna bibliografia</h2><span>W porządku chronologicznym</span></div><div class="search-bar" hidden><label for="book-search">Znajdź książkę</label><input id="book-search" type="search" placeholder="Tytuł, rok lub temat…" aria-controls="book-list"><span id="book-count" role="status">{len(books)} pozycji</span></div><div id="book-list">{rows}</div><p id="no-results" hidden>Nie znaleziono książek. Spróbuj innego tytułu lub roku.</p></section>'
 render(page['path'],page['title'],page['section'],content)
for b in books:
 covers=b.get('covers',[])
 art=f'<img class="detail-cover" src="../{covers[0]}" alt="Okładka: {escape(b["title"])}">' if covers else f'<div class="type-cover detail-cover"><span class="eyebrow">KARTA KSIĄŻKI</span>Wojciech Żukrowski<strong>{escape(b["title"])}</strong>{b["year"]}</div>'
 related=''.join(f'<a href="../{r["url"]}">{escape(r["title"])} ↗</a>' for r in b.get('related',[]))
 editions=''.join(f'<figure><a href="../{c}"><img src="../{c}" alt="{escape(b["title"])} — okładka {i+1}" loading="lazy"></a><figcaption>Okładka ze zbiorów archiwum · {i+1}</figcaption></figure>' for i,c in enumerate(covers))
 content=f'<div class="container"><a class="back-link" href="../ksiazki.html">← Wszystkie książki</a><section class="book-detail"><div class="detail-art">{art}</div><div><div class="eyebrow">BIBLIOTEKA WOJCIECHA ŻUKROWSKIEGO</div><h1>{escape(b["title"])}</h1><p class="detail-intro">{b.get("intro", "Pozycja w bibliografii Wojciecha Żukrowskiego.")}</p><dl><dt>{escape(b.get("author_label", "Autor"))}</dt><dd>{escape(", ".join(b.get("authors", ["Wojciech Żukrowski"])))}</dd><dt>Rodzaj</dt><dd>{escape(b.get("genre", "Literatura"))}</dd><dt>Rok w bibliografii</dt><dd>{b["year"]}</dd></dl><div class="link-list">{related}</div></div></section>'
 if b.get('notes'):
  content+=f'<section class="section"><h2>O książce</h2><p>{escape(b["notes"])}</p></section>'
 if b.get('editions'):
  edition_rows=''.join(f'<li><span>{escape(e["year"])}</span><p>{escape(e["description"])}</p></li>' for e in b['editions'])
  content+=f'<section class="section book-editions"><h2>Wydania, przekłady i audiobooki</h2><ul>{edition_rows}</ul></section>'
 if b.get('sources'):
  source_links=''.join(f'<li><a href="{escape(source["url"])}">{escape(source["title"])}</a></li>' for source in b['sources'])
  content+=f'<details class="book-sources"><summary>Bibliografia i źródła opisu</summary><ul>{source_links}</ul></details>'
 if editions: content+=f'<section class="section"><div class="eyebrow">ŚLADY KOLEJNYCH WYDAŃ</div><h2>Okładki z archiwum</h2><p class="muted">Zachowane okładki mogą pochodzić z różnych wydań książki.</p><div class="edition-grid">{editions}</div></section>'
 index=books.index(b)
 previous=books[index-1] if index else None
 following=books[index+1] if index+1<len(books) else None
 content+='<nav class="book-pagination" aria-label="Kolejne książki">'
 if previous: content+=f'<a href="{previous["slug"]}.html"><span>← Poprzednia książka</span>{escape(previous["title"])}</a>'
 if following: content+=f'<a href="{following["slug"]}.html"><span>Następna książka →</span>{escape(following["title"])}</a>'
 content+='</nav></div>'
 render(url(b),b['title']+' — Wojciech Żukrowski','ksiazki.html',content)
print(f'Built {len(pages)} archive pages and {len(books)} book pages.')
