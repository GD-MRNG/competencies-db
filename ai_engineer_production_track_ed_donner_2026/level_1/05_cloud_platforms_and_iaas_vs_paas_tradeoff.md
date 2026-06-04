## Metadata
- **Date:** 05-06-2026
- **Source:** 05_cloud_platforms_and_iaas_vs_paas_tradeoff.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# L1-05 · Cloud Platforms and the IaaS vs. PaaS Trade-off

The choice of where to host your AI system is usually framed as a technical decision, but it is really a decision about how much of your future you want to mortgage to a vendor in exchange for shipping faster today. Every team makes this trade — explicitly or by accident — and the ones who make it by accident almost always regret it eighteen months in, when they discover that the platform that took five minutes to deploy to has now grown roots through their entire architecture.

The two ends of the spectrum are Platform as a Service and Infrastructure as a Service. PaaS, exemplified by providers like Vercel, Railway, or Heroku, hides the machine from you. You push code to a git repository, the platform builds it, deploys it, scales it, gives it a URL, and handles the boring parts (TLS certificates, load balancing, log aggregation, basic metrics). The cost is that you live inside the platform's opinions: their supported runtimes, their function timeout limits, their idea of how a backend should be shaped. IaaS, exemplified by AWS, GCP, and Azure, gives you the machine and nothing else. You decide what runs on it, how it networks, how it scales, how it fails over. The cost is that all of those decisions are now yours, and so are the consequences of getting them wrong.

The mental model worth holding is that PaaS and IaaS are not really competitors — they sit at different points on a curve that trades control for velocity. At the PaaS end, you move fast and accept that someone else's defaults are now your architecture. At the IaaS end, you move slowly and accept that you are now responsible for things you have never thought about, like whether your private subnet has a NAT gateway and what that costs per hour. In between sit managed services like AWS App Runner or Google Cloud Run, which give you containerised deployment with some of the PaaS ergonomics — a meaningful middle ground that most production AI systems eventually land in.

For an MVP, this is not a hard call. PaaS wins, because the thing that kills early-stage products is not vendor lock-in; it is failing to ship. You should be able to get a FastAPI backend and a frontend deployed in an afternoon and spend your real engineering hours on the AI logic that actually differentiates your product. If your prototype dies because nobody wants it, your hosting choice was irrelevant. If it succeeds, you will have time to migrate. The mistake here is treating "but what if we need to scale?" as a reason to start on Kubernetes — you almost certainly do not, and the time you spend building infrastructure for users you do not have is time stolen from building the product that might attract them.

The calculus inverts when you hit certain thresholds. Enterprise compliance regimes (SOC 2, HIPAA, data residency requirements) often demand controls that PaaS providers either do not offer or charge enterprise-tier prices for — audit trails of who accessed what, the ability to keep all data in a specific geography, network isolation guarantees. Cost is another lever: PaaS pricing is convenient at low volume and punishing at high volume, because you are paying for someone else's margin on top of the underlying compute. Once your monthly bill is large enough to fund a part-time DevOps engineer, raw IaaS starts to look cheaper. And then there is the question of architectural fit — if your workload involves long-running jobs, GPU inference, or a job queue with worker pools, you may simply hit the ceiling of what PaaS abstractions are willing to do for you.

The hidden cost in this trade-off, and the one people underestimate, is switching cost. PaaS providers offer convenience by abstracting away the underlying primitives — but every abstraction is also a coupling. The serverless function format Vercel deploys is not exactly the same as an AWS Lambda; the way Railway handles environment variables is not the way ECS does; the build pipeline that "just works" on one platform requires recreating from scratch on another. The more deeply you lean on platform-specific features (their cron, their queue, their KV store, their auth), the harder migration becomes. This is not a reason to avoid PaaS — it is a reason to use it deliberately, knowing which features will travel and which will need to be rebuilt.

This is why infrastructure-as-code matters so much for IaaS, and why it barely exists for PaaS: when you own the infrastructure, the only sane way to manage it is to describe it in version-controlled code (which is the whole point of Terraform, the subject of L1-06). PaaS replaces that discipline with a vendor's defaults, which is great until you need to reproduce your environment somewhere the vendor does not reach.

The practical pattern, then, looks like this. Start on PaaS. Ship something. Learn what your system actually needs under real load. When you hit a real reason to move — compliance, cost, an architectural requirement the platform cannot meet — migrate to managed IaaS (App Runner, Cloud Run) before considering raw IaaS, and consider raw IaaS or Kubernetes only when you have specific requirements that justify the operational burden. The skill this topic builds is not knowing which platform is best; there is no such thing. The skill is recognising which trade-off you are making, when the conditions have changed enough that the old trade-off no longer holds, and how to migrate before the lock-in becomes terminal.

## Level 2 candidates

**PaaS (Vercel, Railway, Heroku) vs. IaaS (AWS, GCP, Azure)** — A side-by-side of the major providers in each camp, what they actually do well, and the specific workloads where each shines or struggles. Worth deeper treatment because the marketing material from each vendor is misleading, and the real differences only become clear when you compare deployment models, pricing curves, and failure modes head-to-head.

**Managed Services vs. Raw Compute** — The middle ground between full PaaS and bare IaaS: App Runner, Cloud Run, ECS Fargate, Lambda. Worth a Level 2 because most production AI systems eventually live here, and the decision between (say) Lambda and App Runner has cascading consequences for cold starts, cost, and how you structure your code.

**Cold Starts and Serverless Latency** — Why serverless platforms have a 30–60 second latency penalty on the first request after idle, and what that means specifically for AI workloads where inference is already slow. Deserves its own treatment because the mitigations (provisioned concurrency, warming pings, container reuse) have non-obvious cost and architectural implications.

**Auto-Scaling and Load Balancing** — How traffic gets distributed across instances, how new instances spin up under load, and how everything scales back down to save money. Worth depth because the defaults on most platforms are wrong for AI workloads (which have long request durations and bursty traffic patterns), and getting this wrong shows up as either runaway bills or dropped requests.

**Multi-Region and Disaster Recovery** — Running your system in multiple geographies for resilience, latency, and compliance. A Level 2 topic because the design decisions (active-active vs. active-passive, data replication strategy, where state lives) are genuinely hard and have major cost implications.

**Vendor Lock-in and Migration Strategy** — A deeper treatment of which platform features create the hardest dependencies, how to architect for portability without sacrificing all the convenience, and what an actual platform migration looks like in practice. Worth its own post because most teams discover this too late, and the migration playbooks are not well documented.

---