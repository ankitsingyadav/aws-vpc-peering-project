# Screenshot Checklist — AWS VPC Peering Project

Use this checklist to ensure you've captured all required screenshots before submitting your report. Each screenshot should be **clearly visible**, with relevant details highlighted or circled if needed.

> [!IMPORTANT]
> Take all screenshots **before** performing cleanup. Once resources are deleted, you cannot recapture them.

---

## 1. Infrastructure Resources

- [ ] **01. VPC A details** — VPC console → `ewb-vpc-a` selected → Details tab showing VPC ID, CIDR (`10.10.0.0/16`), State: Available.
- [ ] **02. VPC B details** — VPC console → `ewb-vpc-b` selected → Details tab showing VPC ID, CIDR (`10.20.0.0/16`), State: Available.
- [ ] **03. Subnet details (all 3 subnets)** — Subnets console showing:
  - `ewb-a-public` (`10.10.1.0/24`) in VPC A
  - `ewb-a-private` (`10.10.2.0/24`) in VPC A
  - `ewb-b-private` (`10.20.1.0/24`) in VPC B
- [ ] **04. Route table `ewb-rt-a-public`** — Routes tab showing:
  - `10.10.0.0/16` → local
  - `0.0.0.0/0` → `ewb-igw-a`
  - `10.20.0.0/16` → `ewb-a-b-peer` (pcx-...)
  - Subnet Associations tab showing `ewb-a-public`
- [ ] **05. Route table `ewb-rt-a-private`** — Routes tab showing:
  - `10.10.0.0/16` → local
  - `10.20.0.0/16` → `ewb-a-b-peer` (pcx-...)
  - Subnet Associations tab showing `ewb-a-private`
- [ ] **06. Route table `ewb-rt-b-private`** — Routes tab showing:
  - `10.20.0.0/16` → local
  - `10.10.0.0/16` → `ewb-a-b-peer` (pcx-...)
  - Subnet Associations tab showing `ewb-b-private`
- [ ] **07. Internet Gateway** — Internet Gateways console showing `ewb-igw-a` Attached to `ewb-vpc-a`.

---

## 2. Security Groups

- [ ] **08. `ewb-sg-bastion` inbound rules** — Inbound Rules tab showing SSH (TCP 22) from your IP (`var.my_ip/32`).
- [ ] **09. `ewb-sg-app-a` inbound rules** — Inbound Rules tab showing:
  - SSH (TCP 22) from `10.10.1.10/32` (bastion private IP)
  - Custom ICMP Echo Request (Type 8) from `10.20.1.10/32` (App-B)
- [ ] **10. `ewb-sg-app-b` inbound rules** — Inbound Rules tab showing:
  - SSH (TCP 22) from `10.10.1.10/32` (bastion private IP)
  - Custom ICMP Echo Request (Type 8) from `10.10.2.10/32` (App-A)

---

## 3. EC2 Instances & Public IP Isolation

- [ ] **11. EC2 instances list** — EC2 console showing all 3 instances (`ewb-bastion`, `ewb-app-a`, `ewb-app-b`) in "Running" state.
- [ ] **12. `ewb-bastion` details** — Showing Public IPv4 address assigned AND Private IPv4 address `10.10.1.10`.
- [ ] **13. `ewb-app-a` details** — Showing Private IPv4 `10.10.2.10` and **Public IPv4 address empty / "—"**.
- [ ] **14. `ewb-app-b` details** — Showing Private IPv4 `10.20.1.10` and **Public IPv4 address empty / "—"**.

---

## 4. VPC Peering Connection

- [ ] **15. Peering connection** — Peering Connections console showing `ewb-a-b-peer`, Status: Active, Requester `ewb-vpc-a` (`10.10.0.0/16`), Accepter `ewb-vpc-b` (`10.20.0.0/16`).

---

## 5. Verification & Test Terminal Proofs

- [ ] **16. Baseline ping failure** — Terminal on App-A showing `ping -c 4 10.20.1.10` with **100% packet loss** before routes are added.
- [ ] **17. Forward ping success** — Terminal on App-A showing `ping -c 4 10.20.1.10` with **0% packet loss** after peering routes are added.
- [ ] **18. Reverse ping success** — Terminal on App-B showing `ping -c 4 10.10.2.10` with **0% packet loss**.
- [ ] **19. SSH to App-B through bastion** — Terminal showing `ssh ewb-app-b` (via ProxyJump) landing directly inside App-B (`10.20.1.10`).

---

## 6. Controlled Failure & Recovery

- [ ] **20. ICMP rule removal failure** — Terminal showing `ping 10.20.1.10` failing with 100% loss when ICMP rule is deleted from `ewb-sg-app-b`.
- [ ] **21. ICMP rule restored recovery** — Terminal showing `ping 10.20.1.10` immediately succeeding again once the rule is restored.

---

## 7. Resource Cleanup Evidence

- [ ] **22. Terminated instances** — EC2 console showing all 3 instances in "Terminated" state.
- [ ] **23. Clean VPC dashboard** — Showing lab VPCs and peering connections removed.
