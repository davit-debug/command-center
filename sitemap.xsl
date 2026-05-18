<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <xsl:output method="html" version="5.0" encoding="UTF-8" indent="yes" omit-xml-declaration="yes"/>
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="robots" content="noindex"/>
        <title>XML Sitemap — 10xseo.ge</title>
        <link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg"/>
        <style>
          :root{--bg:#0a0a0f;--panel:#11131c;--border:#1f2233;--text:#e7e9f1;--muted:#8a8fa3;--accent:#9b8cff;--accent2:#5fe1c5;--row:#13151f;--rowAlt:#0f111a}
          *{box-sizing:border-box}
          body{margin:0;background:var(--bg);color:var(--text);font:14px/1.55 -apple-system,BlinkMacSystemFont,"SF Pro Text","Inter",system-ui,sans-serif;padding:32px 20px}
          .wrap{max-width:1200px;margin:0 auto}
          header{display:flex;flex-wrap:wrap;gap:16px 32px;align-items:end;justify-content:space-between;margin-bottom:24px}
          h1{font-size:24px;font-weight:700;margin:0;letter-spacing:-.01em}
          h1 .accent{background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}
          .lede{color:var(--muted);max-width:720px;margin:6px 0 0;font-size:13px}
          .lede a{color:var(--accent);text-decoration:none}
          .lede a:hover{text-decoration:underline}
          .stats{display:flex;gap:12px;flex-wrap:wrap}
          .stat{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 14px;min-width:120px}
          .stat .n{font-size:20px;font-weight:700;color:var(--accent2);font-variant-numeric:tabular-nums}
          .stat .l{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-top:2px}
          .filter{margin:0 0 14px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
          .filter input{background:var(--panel);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:9px 12px;font:inherit;flex:1;min-width:200px;outline:none}
          .filter input:focus{border-color:var(--accent)}
          .filter .lang{display:inline-flex;background:var(--panel);border:1px solid var(--border);border-radius:8px;overflow:hidden}
          .filter .lang button{background:transparent;border:0;color:var(--muted);padding:8px 14px;font:inherit;cursor:pointer}
          .filter .lang button.on{background:var(--accent);color:#0a0a0f;font-weight:600}
          table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden}
          th,td{padding:10px 14px;text-align:left;font-size:13px;border-bottom:1px solid var(--border)}
          th{background:#15182580;color:var(--muted);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.06em;position:sticky;top:0}
          tr:last-child td{border-bottom:0}
          tr:nth-child(even) td{background:var(--rowAlt)}
          tr:hover td{background:#1a1d2c}
          tr.hidden{display:none}
          a.url{color:var(--text);text-decoration:none;word-break:break-all}
          a.url:hover{color:var(--accent)}
          .badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;background:#1f2233;color:var(--muted)}
          .badge.ka{background:rgba(155,140,255,.15);color:var(--accent)}
          .badge.en{background:rgba(95,225,197,.15);color:var(--accent2)}
          .pri{font-variant-numeric:tabular-nums;color:var(--muted)}
          .pri.hi{color:var(--accent2);font-weight:600}
          footer{margin-top:24px;color:var(--muted);font-size:12px;text-align:center}
          @media(max-width:640px){
            body{padding:16px 10px}
            header{flex-direction:column;align-items:flex-start}
            th:nth-child(3),td:nth-child(3),th:nth-child(4),td:nth-child(4){display:none}
          }
        </style>
      </head>
      <body>
        <div class="wrap">
          <header>
            <div>
              <h1><span class="accent">XML</span> Sitemap</h1>
              <p class="lede">Machine-readable index of every page on <a href="https://10xseo.ge/">10xseo.ge</a>. Crawlers like Googlebot and Bingbot consume the raw XML; this view is for humans.</p>
            </div>
            <div class="stats">
              <div class="stat"><div class="n"><xsl:value-of select="count(s:urlset/s:url)"/></div><div class="l">Total URLs</div></div>
              <div class="stat"><div class="n"><xsl:value-of select="count(s:urlset/s:url[not(starts-with(s:loc,'https://10xseo.ge/en/'))])"/></div><div class="l">KA Pages</div></div>
              <div class="stat"><div class="n"><xsl:value-of select="count(s:urlset/s:url[starts-with(s:loc,'https://10xseo.ge/en/')])"/></div><div class="l">EN Pages</div></div>
            </div>
          </header>
          <div class="filter">
            <input type="search" id="q" placeholder="Filter URLs…" oninput="filterRows()"/>
            <div class="lang">
              <button class="on" data-lang="all" onclick="setLang(this)">All</button>
              <button data-lang="ka" onclick="setLang(this)">KA</button>
              <button data-lang="en" onclick="setLang(this)">EN</button>
            </div>
          </div>
          <table id="t">
            <thead>
              <tr><th style="width:55%">URL</th><th>Lang</th><th>Last Mod</th><th>Freq</th><th>Priority</th></tr>
            </thead>
            <tbody>
              <xsl:for-each select="s:urlset/s:url">
                <xsl:variable name="isEn" select="starts-with(s:loc,'https://10xseo.ge/en/')"/>
                <tr>
                  <xsl:attribute name="data-lang"><xsl:choose><xsl:when test="$isEn">en</xsl:when><xsl:otherwise>ka</xsl:otherwise></xsl:choose></xsl:attribute>
                  <td><a class="url" href="{s:loc}"><xsl:value-of select="s:loc"/></a></td>
                  <td>
                    <xsl:choose>
                      <xsl:when test="$isEn"><span class="badge en">EN</span></xsl:when>
                      <xsl:otherwise><span class="badge ka">KA</span></xsl:otherwise>
                    </xsl:choose>
                  </td>
                  <td><xsl:value-of select="s:lastmod"/></td>
                  <td><xsl:value-of select="s:changefreq"/></td>
                  <td>
                    <xsl:attribute name="class">
                      <xsl:choose>
                        <xsl:when test="number(s:priority) &gt;= 0.8">pri hi</xsl:when>
                        <xsl:otherwise>pri</xsl:otherwise>
                      </xsl:choose>
                    </xsl:attribute>
                    <xsl:value-of select="s:priority"/>
                  </td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>
          <footer>Generated from <code>command-center/sitemap.xml</code> · <a href="/" style="color:inherit">10xseo.ge</a></footer>
        </div>
        <script>
          function filterRows(){
            var q=document.getElementById('q').value.toLowerCase();
            var lang=document.querySelector('.lang .on').dataset.lang;
            document.querySelectorAll('#t tbody tr').forEach(function(r){
              var matchQ=!q||r.textContent.toLowerCase().indexOf(q)>-1;
              var matchL=lang=='all'||r.dataset.lang==lang;
              r.classList.toggle('hidden',!(matchQ&amp;&amp;matchL));
            });
          }
          function setLang(btn){
            document.querySelectorAll('.lang button').forEach(function(b){b.classList.remove('on')});
            btn.classList.add('on');
            filterRows();
          }
        </script>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
