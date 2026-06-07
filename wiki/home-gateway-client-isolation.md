# Home-Gateway WiFi Client Isolation

Consumer ISP gateways (notably the **Bell Home Hub** in Canada) frequently enable **WiFi client / AP isolation** — devices associated to the same gateway cannot reach each other on the private LAN. This silently breaks any architecture that assumes free device-to-device comms over home WiFi, including the [[user-comms-layer]] (robot ↔ World Brain ↔ phone). It is a **distinct, more fundamental** failure mode than the DDS multicast-discovery problem in [[drone-comms-wifi]]: isolation blocks even plain unicast L3 between clients, so discovery fixes (Discovery Server / Zenoh) do not help. This page documents the failure, the measured evidence, and the workaround ladder. *Distinguish: shipping-known engineering fact + one measured case; exact Bell-Hub UI steps are `claimed`/need a `/research` pass.*

---

## The failure mode

"Client isolation" (a.k.a. AP isolation, station isolation, wireless isolation) makes the access point drop frames between associated stations. Intent is guest-network security; some ISP gateways enable it on the **main** SSID or segment devices such that:

- WiFi-client ↔ WiFi-client traffic is blocked (the common case).
- Sometimes WiFi ↔ wired is *also* segmented, but more often wired hosts remain reachable from wireless clients.
- mDNS/`.local` discovery and multicast are additionally mangled (compounds the [[drone-comms-wifi]] DDS issue).

Symptom signature: two hosts on the **same gateway / same public IP** get **100% packet loss to each other's private (RFC-1918) addresses**, while both still reach the internet fine. An overlay VPN (Tailscale/ZeroTier) can still connect them — but only via an internet relay or a NAT **hairpin through the WAN IP**, never via a direct LAN path, which is the tell-tale that the LAN path itself is severed.

---

## Measured case (drone-app dev network, Bell Home Hub, 2026-06-06)

Two hosts, both behind the Bell Hub (`192.168.2.1`), both egressing public IP `76.69.4.85`:

| Host | LAN IP | Result |
|---|---|---|
| World Brain (workstation, WiFi `wlp0s20f3`) | 192.168.2.20 | — |
| gpu_workstation | 192.168.2.194 | `ping` → **100% loss**, `ssh` → **no route to host** |

Yet gpu_workstation was alive the whole time:

- `tailscale ping` → first 4 packets via **DERP relay (Toronto) ~11 ms**, then **direct via `76.69.4.85:41641` ~4 ms** — i.e. a **NAT hairpin out the WAN and back**, never via `192.168.2.x`.
- `tailscale netcheck` → both hosts share public IP `76.69.4.85`; UPnP IGD present on `192.168.2.1`; `MappingVariesByDestIP:false` (not symmetric NAT — hole-punching works, which is why the hairpin direct path formed).

Conclusion: the gateway permits internet egress and WAN hairpin but **blocks intra-LAN client-to-client traffic** — classic client isolation. This makes pure-WiFi LAN benchmarking (drone-app EXP002) impossible on this network without a workaround, and would break the product on any similarly-configured customer gateway.

---

## Workaround ladder

1. **Wire the hub host (cheapest; fits hub-and-spoke).** In [[user-comms-layer]] the robot and phone talk **only** to the World Brain, never each other. Gateways that isolate wireless↔wireless usually still pass wireless↔**wired**. Put the **World Brain on Ethernet** to the gateway, keep robot/phone on WiFi → the load-bearing paths likely work under isolation, and the EXP002 measurement becomes a representative "WiFi client → wired hub" number (arguably the realistic deployment topology anyway).
2. **Own the AP (most robust; product recommendation).** Run a router you control for the robot subnet — a cheap OpenWrt/Ubiquiti/travel router as a second AP behind the gateway, or put the gateway in **bridge / Advanced-DMZ mode**. You then control client-isolation (off), IGMP snooping, and multicast — which *also* mitigates the [[drone-comms-wifi]] DDS-discovery problem. **Product implication:** a mass-market home robot should not depend on the customer's ISP-gateway L2 behaviour; bundle/recommend a dedicated AP, or have the robot stand up its own WiFi with the gateway as uplink only. This is the durable answer.
3. **Overlay mesh VPN (functional fallback only).** Tailscale/ZeroTier/self-hosted headscale connect through isolation today (verified). But the path is internet-dependent (relay or WAN hairpin), adds WireGuard overhead, and its latency is **not** representative of local WiFi — and it violates the local-only / survive-WiFi-dropout tenets of [[user-comms-layer]]. Use for demos / remote access, not as the primary local transport.
4. **Disable AP/client isolation in the gateway UI** if exposed. Bell Hub firmware buries or omits this and it varies by version — not dependable for a shipped product. Verify-then-distrust.

**Do not confuse with the DDS fix.** [[drone-comms-wifi]] (Discovery Server / Zenoh / IGMP snooping) addresses multicast *discovery* once L3 connectivity exists. If client isolation severs L3 between clients, none of those help — fix isolation first (workaround 1 or 2), then apply the DDS fix on top.

---

## Source

- Empirical measurement on the drone-app dev network (Bell Home Hub), 2026-06-06: `ping`/`ssh`/`tailscale ping`/`tailscale netcheck`. Captured in `drone-app/docs/parked.md` P-008 and `docs/prototype-diary.md`.
- Engineering synthesis (client/AP isolation behaviour, NAT hairpin, overlay traversal) — general networking knowledge; **follow-up:** a `/research` pass for authoritative Bell-Hub-specific settings and a survey of Canadian ISP gateway defaults would strengthen the `claimed` items.

## Related

- [[home-iot-connectivity-patterns]]
- [[user-comms-layer]]
- [[drone-comms-wifi]]
- [[comms-prototype-mandate]]
- [[ros2-server-bridge]]
