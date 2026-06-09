## Metadata
- **Date:** 23-05-2026
- **Source:** 07_single_node_patterns.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-07 · Single-Node Patterns

The instinct, when you hear "distributed systems patterns," is to skip ahead to the multi-node material — replication, sharding, leader election, the things that obviously involve a network. Single-node patterns feel like a warm-up. They are not. They are the layer where the separation of concerns principle stops being a software design slogan and becomes a deployment-level structural choice — and if you skip past them, you will spend the rest of your career looking at sidecars, service meshes, and logging agents as operational accidents rather than as deliberate architecture.

The mental model worth building is this: a container is not the smallest unit of deployment. A group of containers running together on a single node — sharing a network namespace, sharing a lifecycle, scheduled together — is the smallest unit of deployment. Once you accept that, the question changes from "what goes in my container?" to "what concerns belong to my application, and what concerns belong to the node it runs on?" Single-node patterns are the named answers to that second question. They are how you decompose a single logical unit of compute into multiple cooperating containers without crossing a network boundary, and without rebuilding the application every time a cross-cutting concern changes.

The sidecar pattern is the foundational one. You have a primary container — your application — and you attach a secondary container alongside it that extends or modifies its behaviour without touching its code. The classic example is a legacy HTTP service that knows nothing about TLS; you put an nginx sidecar next to it that terminates TLS on the way in and forwards plain HTTP to the primary over localhost. The application stays simple. The TLS configuration is owned by the sidecar, deployed independently, upgraded independently, and reusable across every service in your fleet. The same shape works for log shipping, configuration reloading, secrets injection, and dozens of other cross-cutting concerns. The pattern is not about TLS or logging specifically — it is about giving cross-cutting concerns their own deployable home.

The ambassador pattern is the sidecar's outbound-facing cousin. Instead of modifying or augmenting the primary's behaviour, an ambassador container handles outbound communication on the primary's behalf. The application talks to localhost; the ambassador handles the actual remote call — sharding the request across backends, retrying on failure, translating protocols, applying circuit breakers. This is the pattern that lets you take an application that thinks it is talking to a single Redis instance and silently fan its requests across a sharded Redis cluster, without the application ever knowing. It is also, in essence, what a service mesh sidecar is doing for every service in your cluster: the ambassador pattern, applied uniformly.

The adapter pattern points the other direction. The primary produces output — metrics, logs, health information — in whatever format it happens to produce, and the adapter container normalises that output into a standard format for external consumption. The Prometheus exporter ecosystem is the adapter pattern made flesh: a Redis exporter, a Postgres exporter, a JVM exporter, each one a small container that scrapes the primary's native interface and re-emits it in Prometheus's format. Without the adapter pattern, every monitoring change requires modifying every application. With it, you have a translation layer that absorbs the heterogeneity of your fleet at the infrastructure level.

What makes these three patterns more than container trivia is the principle they share: containers should be designed for reuse across applications, not coupled to a single one. A well-designed sidecar is not "the TLS termination for service X" — it is "TLS termination, period," with configuration injected at deploy time. The same nginx sidecar serves a hundred different primaries. The same logging adapter serves every application that writes to stderr. Once you internalise this, the question of what belongs inside an application image versus what belongs in a sidecar becomes a real design decision with real consequences — not a packaging convention.

The practical payoff is that a lot of what looks like operational mystery in modern infrastructure becomes legible. A service mesh is sidecars all the way down — every service gets an Envoy proxy alongside it, doing ambassador-pattern work for outbound traffic and reverse-sidecar work for inbound traffic, and the mesh control plane is the thing configuring all those proxies coherently. A monitoring agent on every node is the adapter pattern at scale. A secrets-injection container is a sidecar. None of these are arbitrary infrastructural decisions; they are all the same handful of single-node patterns, applied at fleet scale, solving the problem of where cross-cutting concerns should live when you have decided they do not belong inside your application code.

The skill this topic builds is the ability to look at a deployment manifest and see the architecture in it — to recognise that the three containers running together in a pod are not an arbitrary collection but a deliberate decomposition, and to ask the right question when you are designing your own: what concerns am I about to bake into my application that should instead live next to it?

## Level 2 candidates

**The sidecar pattern** — How a secondary container extends or modifies a primary's behaviour without changing the primary's code, and the design choices around configuration, lifecycle coupling, and resource sharing. Worth going deeper because the sidecar is the most general of the three patterns and shows up in the widest range of real systems — service meshes, secrets management, configuration reloading — and reasoning about its tradeoffs (resource overhead, debugging complexity, version skew between primary and sidecar) is what makes those systems legible.

**The ambassador pattern** — A proxy container that mediates the primary's outbound communication, handling sharding, retries, circuit breaking, and protocol translation. Worth going deeper because the ambassador is the conceptual basis of the service mesh data plane, and understanding it directly is what lets you reason about what a mesh is actually doing — and what it is costing you — rather than treating it as opaque infrastructure.

**The adapter pattern** — A container that normalises the primary's output for consumption by external systems, most commonly for monitoring and logging. Worth going deeper because the adapter pattern is the structural answer to fleet heterogeneity, and understanding it explains why the observability ecosystem is shaped the way it is — a constellation of small exporters and translators rather than a single integrated agent.

**Modular container design** — The principle that containers should be designed for reuse across applications rather than coupled to a single one, and the design discipline that makes this possible (parameterised configuration, narrow interfaces, single responsibility). Worth going deeper because this is the principle that turns the three patterns above from named tricks into a coherent design philosophy — and because most teams violate it by default, producing sidecars that are really just deployment artifacts of one specific application.

---


<details>
<summary>Concept Sketches</summary>

## Concept Sketches

### 1) The deployment unit is the *group*, not the container

```yaml
# One logical app unit: three containers, one pod, one lifecycle.
apiVersion: v1
kind: Pod
metadata:
  name: app-with-helpers
spec:
  containers:
    - name: app
      image: myapp:1.0
      ports:
        - containerPort: 8080

    - name: tls-sidecar
      image: nginx:alpine
      ports:
        - containerPort: 8443

    - name: metrics-adapter
      image: prom/statsd-exporter
      ports:
        - containerPort: 9102
```

The point is structural: users may think “my app runs in one container,” but deployment often says “my app runs as a small cooperating set.” These containers are scheduled together, restarted together, and usually communicate over `localhost`. Cost: more moving parts in one unit means more logs, more resource tuning, and harder debugging.

---

### 2) Sidecar pattern: add inbound behavior without changing the app

**Before: app handles TLS itself**

```python
# app.py
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

server = HTTPServer(("0.0.0.0", 8443), SimpleHTTPRequestHandler)
server.socket = ssl.wrap_socket(
    server.socket,
    certfile="cert.pem",
    keyfile="key.pem",
    server_side=True,
)
server.serve_forever()

# App now owns web logic + TLS certs + TLS config.
```

**After: app stays plain HTTP, sidecar owns TLS**

```python
# app.py
from http.server import HTTPServer, SimpleHTTPRequestHandler

HTTPServer(("127.0.0.1", 8080), SimpleHTTPRequestHandler).serve_forever()
```

```nginx
# nginx.conf in sidecar
server {
  listen 8443 ssl;
  ssl_certificate     /certs/cert.pem;
  ssl_certificate_key /certs/key.pem;

  location / {
    proxy_pass http://127.0.0.1:8080;
  }
}
```

The app keeps only application logic. The sidecar owns the cross-cutting concern. Benefit: TLS can be upgraded or standardized without touching app code. Cost: when requests fail, you now debug two processes, not one.

---

### 3) Ambassador pattern: app talks to localhost, proxy handles outbound complexity

```python
# app.py
import requests

# App thinks there is just one local cache endpoint.
r = requests.get("http://127.0.0.1:9000/user/42")
print(r.text)
```

```python
# ambassador.py (precise pseudocode)
backends = ["redis-a:6379", "redis-b:6379"]

def handle_request(user_id):
    shard = hash(user_id) % len(backends)
    target = backends[shard]

    for attempt in [1, 2, 3]:
        try:
            return call(target, user_id, timeout="50ms")
        except Timeout:
            continue

    return "cache unavailable"
```

The primary container only knows `localhost:9000`. The ambassador hides sharding, retries, failover, or protocol translation. Benefit: old apps can gain smarter networking behavior unchanged. Cost: latency and failures become less obvious because the “real” network path is hidden behind the proxy.

---

### 4) Adapter pattern: translate app output into a standard external format

```python
# app.py exposes its own weird stats format
from flask import Flask
app = Flask(__name__)

@app.get("/internal-stats")
def stats():
    return "users=12;errors=3;latency_ms=41"
```

```python
# adapter.py converts to Prometheus text format
import requests
from flask import Flask, Response

app = Flask(__name__)

@app.get("/metrics")
def metrics():
    raw = requests.get("http://127.0.0.1:5000/internal-stats").text
    parts = dict(item.split("=") for item in raw.split(";"))
    body = f"""users {parts['users']}
errors {parts['errors']}
latency_ms {parts['latency_ms']}
"""
    return Response(body, mimetype="text/plain")
```

Monitoring systems scrape the adapter, not the app’s custom format. Benefit: infrastructure gets one standard interface even if apps are inconsistent. Cost: if the app changes its internal format, the adapter can silently break.

---

### 5) Good single-node patterns depend on reusable containers, not app-specific hacks

**Bad: sidecar coupled to one app**

```sh
#!/bin/sh
# start-tls.sh
# Hardcoded for service-x only
nginx -g "daemon off;" \
  -c /etc/nginx/service-x.conf
```

**Better: reusable sidecar configured at deploy time**

```sh
#!/bin/sh
cat >/etc/nginx/conf.d/default.conf <<EOF
server {
  listen ${TLS_PORT};
  location / {
    proxy_pass http://${UPSTREAM_HOST}:${UPSTREAM_PORT};
  }
}
EOF

nginx -g "daemon off;"
```

The second version is “TLS termination” as a reusable unit, not “the TLS helper for service X.” That is what makes sidecars, ambassadors, and adapters worth having at all. Cost: reusable containers need cleaner interfaces and better configuration discipline.

---

### 6) Choosing the pattern: where does the concern live?

```text
If the concern is...
- "Handle inbound TLS / secrets / config reload"   -> Sidecar
- "Control outbound calls to remote services"      -> Ambassador
- "Translate logs/metrics/health into a standard"  -> Adapter

If the concern is core business logic:
- Keep it in the app, not in a helper container.
```

Counter-example:

```python
# Wrong use of a sidecar: business rule moved out of app code
def sidecar_decide_discount(user):
    if user == "vip":
        return 0.20
```

That is not a cross-cutting concern; it is product behavior. Single-node patterns help separate infrastructure concerns from application logic, not hide business logic in neighboring containers.

## Key Ideas

Single-node patterns are about decomposing one deployed unit into cooperating containers with distinct responsibilities. The sidecar adds or modifies inbound/local behavior, the ambassador mediates outbound communication, and the adapter translates app-specific output into standard formats. The important design move is not “use more containers,” but “move cross-cutting concerns out of the app and into reusable helpers.” That makes deployments more modular and consistent, but it also adds process boundaries, resource overhead, and debugging complexity—so the boundary only pays off when the concern is truly infrastructural rather than core application logic.

</details>