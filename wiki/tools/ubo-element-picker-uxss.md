# uBlock Origin element-picker universal XSS (Nov 2026)

In November 2026 an independent researcher disclosed a one-click universal XSS (UXSS) in uBlock Origin MV2 (Firefox); a similar but less severe issue affected uBO Lite (MV3). A malicious website could embed the extension's element-picker iframe, drive it over postMessage, and inject an arbitrary *trusted* filter (scriptlet injection) targeting any other site, yielding script execution in that site's context. Fixed upstream (GitHub advisory GHSA-cmqw-9r2w-6wv2); one fix is a secret handshake between content script and picker. The case is a concrete reference for the security surface of consumer-protection browser extensions, which can become an attack vector against their own users.

## Attack chain (per the write-up)

1. **Leak the per-install extension UUID.** On Firefox the `moz-extension://<UUID>/` origin is random per install, but a default uAssets filter (`lootdest.*##+js(no-fetch-if, adsbygoogle, ...)`) hooks `fetch` and issues an XHR to a `web_accessible_resources` dummy script. The attacker page hooks `XMLHttpRequest.prototype.open`, triggers the filter, and reads the UUID. The author notes other leak routes exist.
2. **Iframe the picker.** `web_accessible_resources/epicker-ui.html` can be embedded by any page that knows the UUID.
3. **Drive it via unauthenticated postMessage.** The page opens a `MessageChannel`, sends `epickerStart`, then `showDialog` and `resultsetDetails` messages. The picker accepted messages from the attacker.
4. **Newline injection in `opt`.** `opt` (normally a request type such as `image`, appended after `$`) was not sanitised; `"image\ngoogle.com##+js(trusted-rpnt, script, ...)"` smuggles in a second, scriptlet filter the picker UI would normally refuse.
5. **Trusted by construction.** Picker-added filters are treated as trusted until a recompile, so scriptlet injection is permitted.
6. **Obtain the click.** An opacity-0 iframe positioned over the page tricks the user into pressing the hidden "Create" button (described, not implemented, by the author). The attacker can then open the victim site immediately, so the recompile trust-reset gives little protection.

## Fix and discovery

- Fix cited: a secret password the real picker obtains from the content script and returns in its initial postMessage, so the picker rejects unauthenticated senders. Further fixes are in the advisory.
- Discovery was largely LLM-driven (disclosed as GPT-5.6 Sol, verified by the author); PoC code was written mostly by Claude. Public PoC release is not clear from the post; the advisory is public.

## Design lessons for extension-based collective tooling

*(editorial)* Applicable to any price observatory, data-donation, or transparency extension (see [[transparency-tools]], [[gesis-surf-data-donation]]):

- Authenticate every message to extension UI frames (content-script-issued secret), never trust `postMessage` origin alone.
- Minimise `web_accessible_resources`; every exposed page is attacker-embeddable. Avoid resources whose fetch reveals the install UUID to page-level hooks (cf. identifier leakage in [[browser-fingerprinting]]).
- Sanitise every field that is concatenated into a rule/command string (newline and delimiter injection).
- Do not grant "trusted" status by provenance of UI path; trust should come from an auditable source.
- Extension distribution is not only a bootstrap entry point ([[bootstrap-strategy]]) but a liability: a tool that holds user data or injects scripts needs a security-response process and external review. LLM-assisted auditing now lowers attacker cost, so assume extensions will be probed.

Conflict note: no contradiction with existing wiki framing of uBlock Origin as an acquisition window; this adds a trust and security caveat.

## Source

- `raw/research/weekly-2026-11-16/03-ubo-element-picker-uxss.md` — personal security blog post (iter.ca), by an independent researcher, for extension developers and security-aware readers; purpose is to disclose and explain a patched vulnerability. Trust: medium-high (author-verified PoC, fixed upstream, advisory public; AI-assisted discovery disclosed). Captured 2026-11-16 from https://iter.ca/post/ubo-uxss/.

## Related

- [[consumer-price-tools]]
- [[privacy-badger]]
- [[transparency-tools]]
- [[bootstrap-strategy]]
- [[gesis-surf-data-donation]]
- [[browser-fingerprinting]]
