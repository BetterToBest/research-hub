<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title>Better To Best Research Hub - Sitemap</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <style type="text/css">
          /* Inherit Better To Best Research Hub design patterns */
          * { box-sizing: border-box; }
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background: #fff;
          }
          h1, h2, h3 {
            color: #222;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
          }
          h1 {
            font-size: 1.8em;
            text-align: center;
            border-bottom: 1px solid #ddd;
            padding-bottom: 20px;
            margin-bottom: 30px;
          }
          h2 {
            font-size: 1.5em;
            color: #222;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
          }
          .url-info {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
          }
          .url-info:last-child {
            border-bottom: none;
          }
          .url-link {
            color: #0066cc;
            text-decoration: none;
            transition: color 0.2s ease;
            font-weight: 500;
            word-break: break-all;
            display: block;
            margin-bottom: 8px;
          }
          .url-link:hover {
            text-decoration: underline;
            color: #0052a3;
          }
          .url-meta {
            margin: 8px 0;
            color: #555;
            font-size: 14px;
          }
          .paper-type-badge {
            background: #1e40af;
            color: white;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 600;
            display: inline-block;
            margin-right: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }
          .priority-badge {
            background: #0066cc;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-right: 8px;
          }
          .changefreq-badge {
            background: #555;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
          }
          .summary {
            background: #f4f4f4;
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 40px;
            text-align: center;
          }
          section {
            margin-bottom: 40px;
          }
          /* Mobile optimizations matching research hub */
          @media (max-width: 768px) {
            body {
              padding: 15px;
              font-size: 16px;
            }
            h1 { font-size: 1.6em; }
            h2 { font-size: 1.4em; }
            .url-info { margin-bottom: 25px; }
            section { margin-bottom: 30px; }
          }
          /* Print optimizations */
          @media print {
            body {
              max-width: none;
              padding: 0;
              color: #000;
            }
            .url-link {
              color: #000;
              text-decoration: underline;
            }
            h1 {
              border-bottom: 2px solid #000;
            }
          }
        </style>
      </head>
      <body>
        <header>
          <h1>Better To Best Research Hub - XML Sitemap</h1>
          <div class="summary">
            <strong>Total URLs:</strong> <xsl:value-of select="count(sitemap:urlset/sitemap:url)"/> |
            <strong>Last Updated:</strong> <xsl:value-of select="sitemap:urlset/sitemap:url[1]/sitemap:lastmod"/>
          </div>
        </header>

        <section>
          <h2>Main Hub Pages</h2>
          <xsl:for-each select="sitemap:urlset/sitemap:url[contains(sitemap:loc, '/research-hub/') and not(contains(sitemap:loc, '/wiki/')) and not(contains(sitemap:loc, '.html'))]">
            <div class="url-info">
              <a href="{sitemap:loc}" class="url-link">
                <xsl:value-of select="sitemap:loc"/>
              </a>
              <div class="url-meta">
                <span class="paper-type-badge">Hub Page</span>
                <span class="priority-badge">Priority: <xsl:value-of select="sitemap:priority"/></span>
                <span class="changefreq-badge"><xsl:value-of select="sitemap:changefreq"/></span>
              </div>
            </div>
          </xsl:for-each>
        </section>

        <section>
          <h2>Research Papers</h2>
          <xsl:for-each select="sitemap:urlset/sitemap:url[contains(sitemap:loc, '.html') and not(contains(sitemap:loc, '/wiki/'))]">
            <div class="url-info">
              <a href="{sitemap:loc}" class="url-link">
                <xsl:value-of select="sitemap:loc"/>
              </a>
              <div class="url-meta">
                <span class="paper-type-badge">Research Paper</span>
                <span class="priority-badge">Priority: <xsl:value-of select="sitemap:priority"/></span>
                <span class="changefreq-badge"><xsl:value-of select="sitemap:changefreq"/></span>
              </div>
            </div>
          </xsl:for-each>
        </section>

        <section>
          <h2>Wiki Documentation</h2>
          <xsl:for-each select="sitemap:urlset/sitemap:url[contains(sitemap:loc, '/wiki/')]">
            <div class="url-info">
              <a href="{sitemap:loc}" class="url-link">
                <xsl:value-of select="sitemap:loc"/>
              </a>
              <div class="url-meta">
                <span class="paper-type-badge">Documentation</span>
                <span class="priority-badge">Priority: <xsl:value-of select="sitemap:priority"/></span>
                <span class="changefreq-badge"><xsl:value-of select="sitemap:changefreq"/></span>
              </div>
            </div>
          </xsl:for-each>
        </section>

        <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #555; text-align: center;">
          <p>This sitemap contains <xsl:value-of select="count(sitemap:urlset/sitemap:url)"/> URLs for Better To Best Research Hub</p>
          <p>Generated for search engines and AI systems | Open access research under CC BY 4.0</p>
        </footer>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
