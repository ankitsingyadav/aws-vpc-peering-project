# 📘 Step-by-Step Guide — AWS VPC Peering (Console Walkthrough)

This guide walks you through building the entire VPC Peering project **manually in the AWS Console**. Follow each step carefully and take screenshots at each checkpoint.

---

## Table of Contents

1. [Create VPC A](#step-1--create-vpc-a)
2. [Create Subnets for VPC A](#step-2--create-subnets-for-vpc-a)
3. [Create & Attach Internet Gateway](#step-3--create--attach-internet-gateway)
4. [Create Route Tables for VPC A](#step-4--create-route-tables-for-vpc-a)
5. [Create VPC B with Subnet & Route Table](#step-5--create-vpc-b-with-subnet--route-table)
6. [Create Security Groups](#step-6--create-security-groups)
7. [Create Key Pair & Launch EC2 Instances](#step-7--create-key-pair--launch-ec2-instances)
8. [Configure SSH with ProxyJump](#step-8--configure-ssh-with-proxyjump)
9. [Capture Baseline (Before Peering)](#step-9--capture-baseline-before-peering)
10. [Create VPC Peering Connection](#step-10--create-vpc-peering-connection)
11. [Run Verification Tests](#step-11--run-verification-tests)
12. [Controlled Failure Test](#step-12--controlled-failure-test)
13. [Screenshot Checklist](#step-13--screenshot-checklist)
14. [Cleanup](#step-14--cleanup)

---

## Step 1 — Create VPC A

1. Navigate to **VPC Console** → **Your VPCs** → **Create VPC**.
2. Select **VPC only** (not "VPC and more").
3. Configure:

   | Setting              | Value            |
   | -------------------- | ---------------- |
   | **Name tag**         | `ewb-vpc-a`     |
   | **IPv4 CIDR block**  | `10.10.0.0/16`  |
   | **IPv6 CIDR block**  | No IPv6          |
   | **Tenancy**          | Default          |

4. Click **Create VPC**.

> [!IMPORTANT]
> 📸 **Checkpoint 1** — Take a screenshot showing VPC A created with CIDR `10.10.0.0/16`.

---

## Step 2 — Create Subnets for VPC A

### 2a. Public Subnet

1. Go to **Subnets** → **Create subnet**.
2. Select **VPC**: `ewb-vpc-a`.
3. Configure:

   | Setting                         | Value            |
   | ------------------------------- | ---------------- |
   | **Subnet name**                 | `ewb-a-public`  |
   | **Availability Zone**           | Pick any (e.g., `us-east-1a`) |
   | **IPv4 subnet CIDR block**      | `10.10.1.0/24`  |

4. Click **Create subnet**.
5. Select the new subnet → **Actions** → **Edit subnet settings** → ✅ **Enable auto-assign public IPv4 address** → **Save**.

### 2b. Private Subnet

1. Go to **Subnets** → **Create subnet**.
2. Select **VPC**: `ewb-vpc-a`.
3. Configure:

   | Setting                         | Value            |
   | ------------------------------- | ---------------- |
   | **Subnet name**                 | `ewb-a-private` |
   | **Availability Zone**           | Same AZ as above |
   | **IPv4 subnet CIDR block**      | `10.10.2.0/24`  |

4. Click **Create subnet**.

> [!NOTE]
> Do **not** enable auto-assign public IP on the private subnet.

> [!IMPORTANT]
> 📸 **Checkpoint 2** — Screenshot showing both subnets (`ewb-a-public`, `ewb-a-private`) under VPC A.

---

## Step 3 — Create & Attach Internet Gateway

1. Go to **Internet Gateways** → **Create internet gateway**.
2. Set **Name tag**: `ewb-igw-a`.
3. Click **Create internet gateway**.
4. Select the new IGW → **Actions** → **Attach to VPC** → Select `ewb-vpc-a` → **Attach**.

> [!IMPORTANT]
> 📸 **Checkpoint 3** — Screenshot showing `ewb-igw-a` attached to `ewb-vpc-a`.

---

## Step 4 — Create Route Tables for VPC A

### 4a. Public Route Table

1. Go to **Route Tables** → **Create route table**.
2. Configure:

   | Setting        | Value              |
   | -------------- | ------------------ |
   | **Name**       | `ewb-rt-a-public` |
   | **VPC**        | `ewb-vpc-a`       |

3. Click **Create route table**.
4. Select the route table → **Routes** tab → **Edit routes** → **Add route**:

   | Destination    | Target         |
   | -------------- | -------------- |
   | `0.0.0.0/0`   | `ewb-igw-a`   |

5. Click **Save changes**.
6. Go to **Subnet associations** tab → **Edit subnet associations** → Select `ewb-a-public` → **Save associations**.

### 4b. Private Route Table

1. Go to **Route Tables** → **Create route table**.
2. Configure:

   | Setting        | Value               |
   | -------------- | ------------------- |
   | **Name**       | `ewb-rt-a-private`  |
   | **VPC**        | `ewb-vpc-a`        |

3. Click **Create route table**.
4. Go to **Subnet associations** tab → **Edit subnet associations** → Select `ewb-a-private` → **Save associations**.

> [!IMPORTANT]
> 📸 **Checkpoint 4** — Screenshot showing both route tables and their routes.

---

## Step 5 — Create VPC B with Subnet & Route Table

### 5a. Create VPC B

1. Go to **Your VPCs** → **Create VPC**.
2. Select **VPC only**.
3. Configure:

   | Setting              | Value            |
   | -------------------- | ---------------- |
   | **Name tag**         | `ewb-vpc-b`     |
   | **IPv4 CIDR block**  | `10.20.0.0/16`  |
   | **Tenancy**          | Default          |

4. Click **Create VPC**.

### 5b. Create Private Subnet B

1. Go to **Subnets** → **Create subnet**.
2. Select **VPC**: `ewb-vpc-b`.
3. Configure:

   | Setting                         | Value            |
   | ------------------------------- | ---------------- |
   | **Subnet name**                 | `ewb-b-private` |
   | **Availability Zone**           | Any AZ           |
   | **IPv4 subnet CIDR block**      | `10.20.1.0/24`  |

4. Click **Create subnet**.

### 5c. Create Route Table for VPC B

1. Go to **Route Tables** → **Create route table**.
2. Configure:

   | Setting        | Value               |
   | -------------- | ------------------- |
   | **Name**       | `ewb-rt-b-private`  |
   | **VPC**        | `ewb-vpc-b`        |

3. Click **Create route table**.
4. Go to **Subnet associations** → **Edit subnet associations** → Select `ewb-b-private` → **Save associations**.

> [!IMPORTANT]
> 📸 **Checkpoint 5** — Screenshot showing VPC B, its subnet, and route table.

---

## Step 6 — Create Security Groups

### 6a. Bastion Security Group (VPC A)

1. Go to **EC2 Console** → **Security Groups** → **Create security group**.
2. Configure:

   | Setting                | Value                          |
   | ---------------------- | ------------------------------ |
   | **Name**               | `ewb-sg-bastion`              |
   | **Description**        | Allow SSH from anywhere        |
   | **VPC**                | `ewb-vpc-a`                   |

3. **Inbound rules** → **Add rule**:

   | Type | Protocol | Port Range | Source       | Description          |
   | ---- | -------- | ---------- | ------------ | -------------------- |
   | SSH  | TCP      | 22         | `0.0.0.0/0` | SSH from your laptop |

4. Click **Create security group**.

### 6b. App-A Security Group (VPC A)

1. Create another security group:

   | Setting                | Value                                  |
   | ---------------------- | -------------------------------------- |
   | **Name**               | `ewb-sg-app-a`                        |
   | **Description**        | Allow SSH from Bastion, ICMP from VPC B |
   | **VPC**                | `ewb-vpc-a`                           |

2. **Inbound rules** → **Add rules**:

   | Type       | Protocol | Port Range | Source            | Description        |
   | ---------- | -------- | ---------- | ----------------- | ------------------ |
   | SSH        | TCP      | 22         | `ewb-sg-bastion`  | SSH from Bastion   |
   | All ICMP   | ICMP     | All        | `10.20.0.0/16`    | Ping from VPC B    |

3. Click **Create security group**.

### 6c. App-B Security Group (VPC B)

1. Create another security group:

   | Setting                | Value                                  |
   | ---------------------- | -------------------------------------- |
   | **Name**               | `ewb-sg-app-b`                        |
   | **Description**        | Allow SSH and ICMP from VPC A          |
   | **VPC**                | `ewb-vpc-b`                           |

2. **Inbound rules** → **Add rules**:

   | Type       | Protocol | Port Range | Source            | Description        |
   | ---------- | -------- | ---------- | ----------------- | ------------------ |
   | SSH        | TCP      | 22         | `10.10.0.0/16`    | SSH from VPC A     |
   | All ICMP   | ICMP     | All        | `10.10.0.0/16`    | Ping from VPC A    |

3. Click **Create security group**.

> [!IMPORTANT]
> 📸 **Checkpoint 6** — Screenshot showing all three security groups with their inbound rules.

---

## Step 7 — Create Key Pair & Launch EC2 Instances

### 7a. Create Key Pair

1. Go to **EC2 Console** → **Key Pairs** → **Create key pair**.
2. Configure:

   | Setting        | Value            |
   | -------------- | ---------------- |
   | **Name**       | `ewb-key`        |
   | **Type**       | RSA              |
   | **Format**     | `.pem`           |

3. Click **Create key pair** — the `.pem` file will download automatically.
4. Secure the key:

   ```bash
   # Linux/macOS
   chmod 400 ~/Downloads/ewb-key.pem
   mv ~/Downloads/ewb-key.pem ~/.ssh/

   # Windows (PowerShell)
   Move-Item ~/Downloads/ewb-key.pem ~/.ssh/
   ```

### 7b. Launch Bastion Host

1. Go to **EC2** → **Launch instances**.
2. Configure:

   | Setting              | Value                                    |
   | -------------------- | ---------------------------------------- |
   | **Name**             | `ewb-bastion`                            |
   | **AMI**              | Amazon Linux 2023 (Free tier eligible)   |
   | **Instance type**    | `t2.micro`                               |
   | **Key pair**         | `ewb-key`                                |
   | **VPC**              | `ewb-vpc-a`                              |
   | **Subnet**           | `ewb-a-public`                           |
   | **Auto-assign IP**   | Enable                                   |
   | **Security group**   | `ewb-sg-bastion` (select existing)       |

3. Under **Advanced details** → **Private IP**: enter `10.10.1.10` (optional, for consistency).
4. Click **Launch instance**.

### 7c. Launch App-A

1. Launch another instance:

   | Setting              | Value                                    |
   | -------------------- | ---------------------------------------- |
   | **Name**             | `ewb-app-a`                              |
   | **AMI**              | Amazon Linux 2023                        |
   | **Instance type**    | `t2.micro`                               |
   | **Key pair**         | `ewb-key`                                |
   | **VPC**              | `ewb-vpc-a`                              |
   | **Subnet**           | `ewb-a-private`                          |
   | **Auto-assign IP**   | Disable                                  |
   | **Security group**   | `ewb-sg-app-a` (select existing)         |

2. Under **Advanced details** → **Private IP**: enter `10.10.2.10`.
3. Click **Launch instance**.

### 7d. Launch App-B

1. Launch another instance:

   | Setting              | Value                                    |
   | -------------------- | ---------------------------------------- |
   | **Name**             | `ewb-app-b`                              |
   | **AMI**              | Amazon Linux 2023                        |
   | **Instance type**    | `t2.micro`                               |
   | **Key pair**         | `ewb-key`                                |
   | **VPC**              | `ewb-vpc-b`                              |
   | **Subnet**           | `ewb-b-private`                          |
   | **Auto-assign IP**   | Disable                                  |
   | **Security group**   | `ewb-sg-app-b` (select existing)         |

2. Under **Advanced details** → **Private IP**: enter `10.20.1.10`.
3. Click **Launch instance**.

> [!IMPORTANT]
> 📸 **Checkpoint 7** — Screenshot showing all three instances in "Running" state.

---

## Step 8 — Configure SSH with ProxyJump

1. Find the **public IP** of your bastion host from the EC2 console.
2. Edit your SSH config file (`~/.ssh/config`) and add:

```ssh-config
# Bastion Host
Host bastion
    HostName <BASTION_PUBLIC_IP>
    User ec2-user
    IdentityFile ~/.ssh/ewb-key.pem
    StrictHostKeyChecking no

# App-A via Bastion
Host app-a
    HostName 10.10.2.10
    User ec2-user
    IdentityFile ~/.ssh/ewb-key.pem
    ProxyJump bastion
    StrictHostKeyChecking no

# App-B via Bastion (cross-VPC)
Host app-b
    HostName 10.20.1.10
    User ec2-user
    IdentityFile ~/.ssh/ewb-key.pem
    ProxyJump bastion
    StrictHostKeyChecking no
```

3. Test connectivity to the bastion:

```bash
ssh bastion
# Expected: Successful login
```

4. Test connectivity to App-A:

```bash
ssh app-a
# Expected: Successful login (via Bastion jump)
```

> [!NOTE]
> SSH to App-B will **not** work yet — VPC peering is not configured.

> [!IMPORTANT]
> 📸 **Checkpoint 8** — Screenshot showing successful SSH to bastion and App-A.

---

## Step 9 — Capture Baseline (Before Peering)

This step proves that **without VPC peering, cross-VPC traffic fails**.

1. SSH to App-A:

```bash
ssh app-a
```

2. Attempt to ping App-B:

```bash
[ec2-user@app-a ~]$ ping -c 4 10.20.1.10
```

3. **Expected result**: 100% packet loss — the ping should time out.

```
PING 10.20.1.10 (10.20.1.10) 56(84) bytes of data.

--- 10.20.1.10 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 3056ms
```

> [!WARNING]
> If this ping **succeeds**, something is misconfigured. Verify your VPCs, subnets, and route tables before proceeding.

> [!IMPORTANT]
> 📸 **Checkpoint 9** — Screenshot showing the failed ping (100% packet loss) from App-A to App-B.

---

## Step 10 — Create VPC Peering Connection

### 10a. Create the Peering Request

1. Go to **VPC Console** → **Peering Connections** → **Create peering connection**.
2. Configure:

   | Setting                        | Value                  |
   | ------------------------------ | ---------------------- |
   | **Name**                       | `ewb-peer-a-to-b`    |
   | **VPC (Requester)**            | `ewb-vpc-a`           |
   | **Account**                    | My account             |
   | **Region**                     | This Region            |
   | **VPC (Accepter)**             | `ewb-vpc-b`           |

3. Click **Create peering connection**.

### 10b. Accept the Peering Request

1. Select the new peering connection (status: **Pending Acceptance**).
2. **Actions** → **Accept request** → **Accept request**.
3. Wait for status to change to **Active**.

### 10c. Add Routes for Peering

You must add routes in **all three** route tables.

#### Route Table: `ewb-rt-a-public`

1. Go to **Route Tables** → Select `ewb-rt-a-public` → **Routes** tab → **Edit routes**.
2. **Add route**:

   | Destination    | Target                       |
   | -------------- | ---------------------------- |
   | `10.20.0.0/16` | Peering Connection (`ewb-peer-a-to-b`) |

3. **Save changes**.

#### Route Table: `ewb-rt-a-private`

1. Select `ewb-rt-a-private` → **Routes** → **Edit routes**.
2. **Add route**:

   | Destination    | Target                       |
   | -------------- | ---------------------------- |
   | `10.20.0.0/16` | Peering Connection (`ewb-peer-a-to-b`) |

3. **Save changes**.

#### Route Table: `ewb-rt-b-private`

1. Select `ewb-rt-b-private` → **Routes** → **Edit routes**.
2. **Add route**:

   | Destination    | Target                       |
   | -------------- | ---------------------------- |
   | `10.10.0.0/16` | Peering Connection (`ewb-peer-a-to-b`) |

3. **Save changes**.

> [!IMPORTANT]
> 📸 **Checkpoint 10** — Screenshots showing:
> - Peering connection in "Active" state
> - All three route tables with the peering routes added

---

## Step 11 — Run Verification Tests

### Test 1 — Forward Ping (App-A → App-B) ✅

```bash
ssh app-a
[ec2-user@app-a ~]$ ping -c 4 10.20.1.10
```

**Expected**: 0% packet loss, replies from `10.20.1.10`.

### Test 2 — Reverse Ping (App-B → App-A) ✅

```bash
ssh app-b
[ec2-user@app-b ~]$ ping -c 4 10.10.2.10
```

**Expected**: 0% packet loss, replies from `10.10.2.10`.

### Test 3 — SSH to App-B via Bastion ✅

```bash
ssh app-b
```

**Expected**: Successful login to App-B through bastion and VPC peering.

### Test 4 — Isolation Check (App-B → Internet) ❌

```bash
# From App-B:
[ec2-user@app-b ~]$ ping -c 4 8.8.8.8
```

**Expected**: 100% packet loss — App-B has no internet access (no IGW or NAT Gateway in VPC B).

### Test 5 — DNS Resolution Across Peering (Optional) ✅

```bash
# From App-A:
[ec2-user@app-a ~]$ nslookup 10.20.1.10
```

**Expected**: Resolves the internal hostname of App-B (if DNS resolution is enabled on the peering connection).

> [!IMPORTANT]
> 📸 **Checkpoint 11** — Screenshots of all five test results.

---

## Step 12 — Controlled Failure Test

This test demonstrates that **security group rules are enforced** even with peering active.

### 12a. Remove the ICMP Rule

1. Go to **EC2** → **Security Groups** → Select `ewb-sg-app-b`.
2. **Inbound rules** → **Edit inbound rules**.
3. **Delete** the ICMP rule (All ICMP — `10.10.0.0/16`).
4. **Save rules**.

### 12b. Test the Failure

```bash
ssh app-a
[ec2-user@app-a ~]$ ping -c 4 10.20.1.10
```

**Expected**: 100% packet loss — ICMP is now blocked by the security group.

### 12c. Restore the ICMP Rule

1. Go back to `ewb-sg-app-b` → **Inbound rules** → **Edit inbound rules**.
2. **Add rule**:

   | Type       | Protocol | Port Range | Source         | Description     |
   | ---------- | -------- | ---------- | -------------- | --------------- |
   | All ICMP   | ICMP     | All        | `10.10.0.0/16` | Ping from VPC A |

3. **Save rules**.

### 12d. Verify Restoration

```bash
[ec2-user@app-a ~]$ ping -c 4 10.20.1.10
```

**Expected**: 0% packet loss — connectivity is restored.

> [!IMPORTANT]
> 📸 **Checkpoint 12** — Screenshots showing:
> - Ping failure after removing the ICMP rule
> - Ping success after restoring the ICMP rule

---

## Step 13 — Screenshot Checklist

Use this checklist to ensure you have all required screenshots:

| # | Checkpoint Description                           | Captured? |
|---|--------------------------------------------------|-----------|
| 1 | VPC A created (`10.10.0.0/16`)                   | ☐         |
| 2 | Both subnets in VPC A                            | ☐         |
| 3 | IGW attached to VPC A                            | ☐         |
| 4 | Route tables for VPC A                           | ☐         |
| 5 | VPC B with subnet and route table                | ☐         |
| 6 | All three security groups with rules             | ☐         |
| 7 | All three EC2 instances running                  | ☐         |
| 8 | Successful SSH to bastion and App-A              | ☐         |
| 9 | Baseline failed ping (before peering)            | ☐         |
| 10 | Peering active + route tables updated           | ☐         |
| 11 | All five verification tests                     | ☐         |
| 12 | Controlled failure (remove/restore ICMP rule)   | ☐         |

---

## Step 14 — Cleanup

> [!CAUTION]
> Complete these steps to avoid ongoing AWS charges!

### Order of Deletion

1. **EC2 Instances**
   - Select all three instances → **Instance state** → **Terminate instance**.
   - Wait for all instances to reach "Terminated" state.

2. **VPC Peering Connection**
   - Go to **VPC** → **Peering Connections** → Select `ewb-peer-a-to-b`.
   - **Actions** → **Delete peering connection** → Confirm.

3. **Security Groups**
   - Delete `ewb-sg-app-b` (VPC B — no dependencies after instances are terminated).
   - Delete `ewb-sg-app-a` (VPC A).
   - Delete `ewb-sg-bastion` (VPC A).

   > [!NOTE]
   > You cannot delete the **default** security group — that's expected.

4. **Subnets**
   - Delete `ewb-b-private`, `ewb-a-private`, `ewb-a-public`.

5. **Route Tables**
   - Delete `ewb-rt-b-private`, `ewb-rt-a-private`, `ewb-rt-a-public`.
   - You cannot delete the **main** route table — that will be removed with the VPC.

6. **Internet Gateway**
   - Select `ewb-igw-a` → **Actions** → **Detach from VPC** → Confirm.
   - Select `ewb-igw-a` → **Actions** → **Delete internet gateway** → Confirm.

7. **VPCs**
   - Delete `ewb-vpc-b`.
   - Delete `ewb-vpc-a`.

8. **Key Pair** (Optional)
   - Delete `ewb-key` from EC2 → Key Pairs if no longer needed.
   - Delete the local `.pem` file.

> [!IMPORTANT]
> 📸 **Final Checkpoint** — Screenshot showing both VPCs deleted (empty VPC list or only default VPC remaining).

---

**Congratulations!** 🎉 You've successfully built, tested, and torn down a VPC Peering connection between two AWS VPCs.
