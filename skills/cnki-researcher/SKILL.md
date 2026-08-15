---
name: cnki-researcher
description: Coordinate CNKI research workflows in Codex using Chrome DevTools MCP. Use when the user asks to search CNKI papers, inspect paper details, browse journals or issues, check journal indexing, download CNKI files, export citations, handle institution/off-campus CNKI login, or combine these tasks into a literature research workflow.
---

# CNKI Researcher

Coordinate the CNKI skills as a single research workflow. Use Chrome through a Chrome DevTools MCP server; the user handles captcha and may need to handle login manually.

## Prerequisites

Before using browser automation, confirm a Chrome DevTools MCP server is available in the current Codex environment. If the tool is not available, explain that CNKI browser automation cannot run until Chrome DevTools MCP is configured.

Use an existing CNKI tab when possible. If a CNKI tab is already open, select it. If not, open `https://www.cnki.net`.

## Institution Login

When CNKI access requires login, use the off-campus institution login path and select National University of Defense Technology (NUDT). In the Chinese UI, the labels are institution login/off-campus access (`\u673a\u6784\u767b\u5f55` / `\u6821\u5916\u8bbf\u95ee`) and the institution name is `\u56fd\u9632\u79d1\u6280\u5927\u5b66`.

Do not store CNKI usernames or passwords in skill files, scripts, logs, or generated artifacts. If credentials are not already available in the current conversation, ask the user to enter them manually in Chrome. If credentials are available in the current conversation and browser automation is available, use them only for the active login attempt.

## Captcha Handling

CNKI uses a Tencent slider captcha. The Chinese prompt is `\u62d6\u52a8\u4e0b\u65b9\u62fc\u56fe\u5b8c\u6210\u9a8c\u8bc1`. Do not try to solve it programmatically.

When a visible captcha is detected, stop browser actions and tell the user:

```text
CNKI is showing a slider captcha. Please complete it manually in Chrome, then tell me to continue.
```

Use the selector rule from the task-specific skills: `#tcaptcha_transform_dy` is active only when `getBoundingClientRect().top >= 0`. CNKI may preload the captcha SDK off-screen at `top: -1000000px`; do not treat that hidden element as an active captcha.

## Task Routing

Use the most specific skill for the user's requested operation:

- Use `$cnki-search` for keyword paper search and first-page structured results.
- Use `$cnki-advanced-search` for author, title, journal, year range, or source-category filters such as SCI, EI, CSSCI, Peking University Core, or CSCD.
- Use `$cnki-parse-results` when a CNKI results page is already open and the user asks to extract or summarize it.
- Use `$cnki-navigate-pages` for next/previous/page-number navigation or sorting by date, citations, downloads, relevance, or comprehensive ranking.
- Use `$cnki-paper-detail` for abstract, keywords, affiliations, fund, classification, publication data, and citation-network counts.
- Use `$cnki-journal-search` to find a journal by name, ISSN, CN number, or sponsor.
- Use `$cnki-journal-index` to answer whether a journal is Peking University Core, CSSCI, CSCD, SCI, EI, Scopus, AMI, etc., and to extract impact factors.
- Use `$cnki-journal-toc` to browse a journal issue table of contents or download the original TOC PDF.
- Use `$cnki-download` to trigger PDF or CAJ download from a paper detail page. This requires a logged-in CNKI session.
- Use `$cnki-export` to export citations, batch-save search results, or push metadata into Zotero.

## Workflow Patterns

For a simple paper search:

```text
User asks for papers on a topic
-> use $cnki-search
-> present title, authors, source, date, citations, downloads, and result URLs
```

For filtered literature review:

```text
User asks for papers with filters
-> use $cnki-advanced-search
-> use $cnki-parse-results if structured rows are needed
-> use $cnki-navigate-pages for more pages or sorting
-> use $cnki-export for Zotero or citation output
```

For paper-level analysis:

```text
User references a paper result or URL
-> navigate directly to the result href rather than clicking result links
-> use $cnki-paper-detail
-> optionally use $cnki-download or $cnki-export
```

For journal evaluation:

```text
User asks whether a journal is core/indexed or asks for impact factors
-> use $cnki-journal-index
-> if only a journal name is provided, search first and pick the best matching detail page
```

For combined research:

```text
User asks to search a topic and evaluate venues
-> use $cnki-search or $cnki-advanced-search
-> extract the result journals
-> use $cnki-journal-index for selected journals
-> summarize papers and journal status together
```

## Browser Rules

Prefer `navigate_page` with known URLs over clicking CNKI links. CNKI often opens links in new tabs, and direct navigation avoids extra tab management.

After page navigation, wait for a stable page-specific selector or text before extracting data. For most data extraction and page operations, prefer a single async `evaluate_script` that waits internally, checks captcha, performs the action, and returns structured JSON.

Do not rapidly cycle through pages. Pace operations and stop when login, permission, or captcha blocks appear.

## Output Rules

Match the user's language. For Chinese queries, answer in Chinese.

For literature search results, include total count, page marker, numbered titles, authors, source, date, citations, downloads, and URLs when useful.

For journal indexing results, clearly separate indexing tags, ISSN/CN, sponsor, publication cycle, impact factors, and publication volume.

For downloads and Zotero exports, report whether the action was triggered or completed, and name the affected paper(s).
