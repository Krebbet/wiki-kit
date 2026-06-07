# Home-IoT Device-to-Device Connectivity Patterns

How shipping smart-home / connected-AV products get devices talking when the ISP gateway does WiFi client/AP isolation, multicast filtering, double-NAT, and IGMP snooping (the failure documented in [[home-gateway-client-isolation]]). Five patterns, each with a fit verdict for a **local-first home robot** needing **<200 ms safety reactions** and **~10 Hz telemetry**. Bottom line: **no shipping product surveyed puts the home network in a hard-real-time path** — they push realtime to the edge and/or relay control outbound-to-cloud. This is the precedent behind the drone-app architecture pivot (push <200 ms onboard the drone; brain↔drone link low-frequency + cloud/overlay-relayed — see [[user-comms-layer]] and drone-app `docs/00-framing.md`).

---

## 1. Cloud-relay (device → vendor cloud → app)

Nest thermostats, Ring/Nest cameras, ecobee default to this: the device opens an **outbound** TLS connection to the vendor cloud; the app reaches the device only through that cloud. Outbound-to-cloud sidesteps client/AP isolation and inbound NAT entirely — isolation and NAT block *inbound LAN-to-LAN* and *inbound WAN*, never a device-initiated outbound session. Cameras add **WebRTC**: ICE tries a STUN-discovered P2P path, falls back to a **TURN relay** when NAT/isolation blocks P2P (Nest and Ring both). Local paths are partial: ecobee + **HomeKit** gives true local control bypassing ecobee's cloud (no native ecobee LAN API); Nest runs its *schedule* locally on outage but loses app/voice/notifications, and the fallback is **model-dependent** (3rd-gen graceful, 4th-gen cloud-leaning). **Verdict: doesn't fit the safety path** (relay RTT tens-to-hundreds of ms, internet-dependent); good as the *low-frequency control/telemetry backhaul*.

## 2. Dedicated low-power radio + hub (Zigbee / Z-Wave / Thread)

Hue (Zigbee + Ethernet bridge), SmartThings/Aqara (Zigbee/Z-Wave), and **Matter-over-Thread** move the device layer *off home WiFi entirely* onto an 802.15.4 mesh; only the bridge/border-router touches the LAN. **Thread = IPv6 low-power secure mesh on 802.15.4** (same PHY as Zigbee, different stack); **Thread Border Routers** (HomePod/mini, Apple TV 4K, Nest, eero, iPhone 15 Pro+) bridge the mesh to the LAN. Matter is **local-by-design** — a controller sends the encrypted command straight to the device's IPv6 address, no cloud — so the device tier never depends on WiFi isolation/multicast behaviour (commissioning + remote access still need an IP/hub path). **Verdict: partial fit** — the "own the radio, don't trust WiFi" principle is exactly right, but 802.15.4's ~250 kbps + mesh-hop latency can't carry 10 Hz robot telemetry/rich state.

## 3. Own-mesh / wired-anchor (latency-critical local AV) — Sonos

The closest analog to a local realtime robot. **SonosNet** is a proprietary 2.4 GHz mesh: wire one node to Ethernet and it anchors a separate AV mesh on its own channel, decoupling audio sync from flaky home WiFi (the "WiFi/Standard" mode instead rides the home WLAN). Discovery uses **SSDP + mDNS multicast**. Sonos's published router guidance is a catalogue of hostile-gateway fixes: **disable client/AP isolation**, disable multicast-to-unicast / Proxy ARP, **enable IGMP snooping + mDNS**, allow SSDP (UDP 1900 → 239.255.255.250) and mDNS (UDP 5353), **avoid double-NAT** (bridge the ISP gateway), and for wired/mixed setups configure **STP 802.1d** (priority 4096/8192) to prevent loops. **Verdict: best-fit *shape*** (a wired-or-self-meshed anchor giving deterministic local latency) — but its cost is exactly what a mass-market product wants to avoid: asking the customer to wire a node / tune the router (the "Sonos tax").

## 4. mDNS/Bonjour discover-then-direct — Chromecast, AirPlay, Spotify Connect

Discover the peer via **mDNS/DNS-SD** (Spotify Connect advertises `_spotify-connect._tcp`), then open a direct local socket. Fast when it works — but it breaks precisely on hostile gateways: mDNS is link-local multicast that **client isolation drops** and **multicast filtering / aggressive IGMP snooping** blackholes, so discovery fails even between two devices on the same AP. Spotify discovers locally but fetches credentials via its servers; casting products fall back to cloud when local discovery fails. **Verdict: doesn't fit the safety loop** — multicast discovery is the single most fragile thing on bad networks; usable only with a non-multicast discovery fallback.

## 5. Vendor / standards statements on local vs cloud

- **Matter/CSA:** explicitly local-IP-first — devices "communicate directly with each other (without the cloud — all locally)."
- **Apple HomeKit:** basic local control needs no hub; a home hub (HomePod/Apple TV) adds remote access, automations, Thread border-routing. Local-first, cloud-for-remote.
- **Sonos:** doesn't market "local control" but its entire troubleshooting corpus assumes a local multicast LAN and tells users to defang the gateway.
- **Nest:** local fallback is limited and model-dependent (`unverified` exactly which features survive per firmware).

---

## Implication for the home robot (recommendation)

For **<200 ms** reactions, **do not put the safety loop on any home-network or cloud path** — no shipping product surveyed does. Precedent supports the drone-app split:

- **Push all <200 ms reactions fully onboard the robot** (the edge we control), mirroring how Sonos anchors its own mesh and Thread devices run their own radio.
- **Make the robot↔hub link low-frequency (~seconds) and outbound/cloud-relayable**, like Nest/Ring/ecobee — outbound-to-cloud is the one pattern that reliably traverses client isolation + double-NAT with **zero customer router config**.
- **For richer local telemetry (~10 Hz)**, prefer a direct robot↔hub TCP/UDP session after a *non-multicast* discovery (assume mDNS is blocked; have the hub announce via a cloud rendezvous, robot dials a known address). Treat the 10 Hz feed as best-effort, not safety-load-bearing.
- **Avoid forcing a separate network or router tuning** (the Sonos tax). A small wired-or-self-radio hub is the architectural ideal if BOM allows; if it must ride home WiFi, design for isolation/multicast-hostile conditions from day one.

Net: **onboard real-time + low-rate outbound-relay control + best-effort direct-local telemetry** — never a cloud or WiFi dependency inside the <200 ms loop.

## Source

- Sonos + UniFi best practices (isolation, multicast, IGMP, mDNS, SSDP, STP, double-NAT): https://en.community.sonos.com/tutorials-and-how-to-s-229149/sonos-unifi-best-practices-recommended-settings-6933597
- Sonos STP configuration (802.1d, switch priority): https://support.sonos.com/en/article/configure-stp-settings-to-work-with-sonos
- Sonos cross-subnet SSDP+mDNS multicast (UDP 1900 / 239.255.255.250, UDP 5353): https://community.ui.com/questions/Configure-Sonos-across-subnets-on-USG/a758382b-72e4-446b-90cc-ea353482ff1a
- mDNS / client-isolation / multicast filtering breakage (Chromecast/AirPlay/Sonos): https://shiftctrl.net/articles/sonos-chromecast-airplay-unifi-vlans
- Firewalla on AirPlay/Chromecast across segmented networks (mDNS link-local): https://help.firewalla.com/hc/en-us/articles/360049613014
- Spotify Connect ZeroConf API (`_spotify-connect._tcp`, mDNS/DNS-SD, cloud credential exchange): https://developer.spotify.com/documentation/commercial-hardware/implementation/guides/zeroconf
- WebRTC STUN/TURN NAT traversal for IoT/cameras (ICE then TURN relay): https://www.nabto.com/understanding-stun-servers-in-webrtc-and-iot/
- Google Nest camera WebRTC (STUN/TURN): https://developers.home.google.com/cloud-to-cloud/traits/camerastream
- Thread = IPv6 mesh over 802.15.4; Matter local-direct-to-IPv6; Thread Border Router role: https://www.derekseaman.com/2023/10/part-1-smart-home-matter-and-thread-deep-dive.html
- Matter local IP-based control / CSA backing: https://www.home-assistant.io/integrations/matter/
- Apple Thread Border Router devices + Thread/HomeKit local control: https://support.apple.com/en-us/102078
- Apple home hub local vs remote control (HomePod/Apple TV): https://support.apple.com/en-us/102557
- Nest thermostat offline behavior, model-dependent cloud reliance, Matter local: https://www.bgr.com/2105399/can-you-use-google-thermostat-without-internet/
- ecobee + HomeKit local control bypassing ecobee cloud: https://community.home-assistant.io/t/how-to-migrate-from-ecobee-cloud-integration-to-local-homekit-controller/491319

*Provenance: web research 2026-06-07 (dispatched by the drone-app prototyper) cross-checked against the measured [[home-gateway-client-isolation]] case. `unverified` flags: exact per-firmware Nest outage behaviour; Sonos's own "local control" framing.*

## Related

- [[home-gateway-client-isolation]]
- [[user-comms-layer]]
- [[drone-comms-wifi]]
- [[comms-prototype-mandate]]
