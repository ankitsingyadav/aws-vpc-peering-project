#──────────────────────────────────────────────────────────────────────────────
# main.tf – EWB VPC Peering Lab  (same account, same region)
#
# Architecture overview:
#   VPC A (10.10.0.0/16) ←── VPC Peering ──→ VPC B (10.20.0.0/16)
#     ├─ public subnet  10.10.1.0/24  (bastion host)
#     └─ private subnet 10.10.2.0/24  (app-a)
#                                        └─ private subnet 10.20.1.0/24 (app-b)
#
# Connectivity path:
#   Internet → IGW → bastion (public) → SSH → app-a (private, VPC A)
#                                       → SSH → app-b (private, VPC B via peering)
#──────────────────────────────────────────────────────────────────────────────

# ═══════════════════════════════════════════════════════════════════════════════
# PROVIDER
# ═══════════════════════════════════════════════════════════════════════════════

terraform {
  required_version = ">= 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project = var.project_tag
      Student = var.student_name
    }
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# DATA SOURCES
# ═══════════════════════════════════════════════════════════════════════════════

# Automatically fetch the latest Amazon Linux 2023 AMI for the current region.
# This is used when var.ami_id is left empty (the default).
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

# Resolve the AMI to use: explicit override or auto-detected.
locals {
  ami_id = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux_2023.id

  # Common tags applied to resources that don't inherit provider default_tags.
  common_tags = {
    Project = var.project_tag
    Student = var.student_name
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# VPC A  (10.10.0.0/16)
# ═══════════════════════════════════════════════════════════════════════════════

resource "aws_vpc" "vpc_a" {
  cidr_block           = var.vpc_a_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "ewb-vpc-a"
  }
}

# ─── Subnets in VPC A ───────────────────────────────────────────────────────

# Public subnet – hosts the bastion instance with internet access via IGW.
resource "aws_subnet" "vpc_a_public" {
  vpc_id                  = aws_vpc.vpc_a.id
  cidr_block              = var.vpc_a_public_subnet_cidr
  map_public_ip_on_launch = true          # Auto-assign public IP to instances
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name = "ewb-a-public"
  }
}

# Private subnet – hosts app-a. No direct internet access.
resource "aws_subnet" "vpc_a_private" {
  vpc_id            = aws_vpc.vpc_a.id
  cidr_block        = var.vpc_a_private_subnet_cidr
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "ewb-a-private"
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# VPC B  (10.20.0.0/16)
# ═══════════════════════════════════════════════════════════════════════════════

resource "aws_vpc" "vpc_b" {
  cidr_block           = var.vpc_b_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "ewb-vpc-b"
  }
}

# ─── Subnets in VPC B ───────────────────────────────────────────────────────

# Private subnet – hosts app-b. Reachable only via VPC peering from VPC A.
resource "aws_subnet" "vpc_b_private" {
  vpc_id            = aws_vpc.vpc_b.id
  cidr_block        = var.vpc_b_private_subnet_cidr
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "ewb-b-private"
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# INTERNET GATEWAY  (VPC A only)
# ═══════════════════════════════════════════════════════════════════════════════

# The IGW gives the public subnet in VPC A outbound internet connectivity.
resource "aws_internet_gateway" "igw_a" {
  vpc_id = aws_vpc.vpc_a.id

  tags = {
    Name = "ewb-igw-a"
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# VPC PEERING  (VPC A ↔ VPC B, same account, same region)
# ═══════════════════════════════════════════════════════════════════════════════

# Create the peering connection – requester side.
resource "aws_vpc_peering_connection" "a_to_b" {
  vpc_id      = aws_vpc.vpc_a.id   # Requester VPC
  peer_vpc_id = aws_vpc.vpc_b.id   # Accepter VPC
  auto_accept = true                # Same account + same region → auto-accept

  tags = {
    Name = "ewb-a-b-peer"
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTE TABLES
# ═══════════════════════════════════════════════════════════════════════════════

# ─── VPC A – Public Route Table ─────────────────────────────────────────────
# Routes:
#   local        (implicit, VPC A CIDR)
#   0.0.0.0/0  → Internet Gateway
#   10.20.0.0/16 → VPC Peering Connection
resource "aws_route_table" "vpc_a_public" {
  vpc_id = aws_vpc.vpc_a.id

  tags = {
    Name = "ewb-rt-a-public"
  }
}

resource "aws_route" "vpc_a_public_internet" {
  route_table_id         = aws_route_table.vpc_a_public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw_a.id
}

resource "aws_route" "vpc_a_public_to_vpc_b" {
  route_table_id            = aws_route_table.vpc_a_public.id
  destination_cidr_block    = var.vpc_b_cidr
  vpc_peering_connection_id = aws_vpc_peering_connection.a_to_b.id
}

resource "aws_route_table_association" "vpc_a_public" {
  subnet_id      = aws_subnet.vpc_a_public.id
  route_table_id = aws_route_table.vpc_a_public.id
}

# ─── VPC A – Private Route Table ────────────────────────────────────────────
# Routes:
#   local        (implicit, VPC A CIDR)
#   10.20.0.0/16 → VPC Peering Connection
resource "aws_route_table" "vpc_a_private" {
  vpc_id = aws_vpc.vpc_a.id

  tags = {
    Name = "ewb-rt-a-private"
  }
}

resource "aws_route" "vpc_a_private_to_vpc_b" {
  route_table_id            = aws_route_table.vpc_a_private.id
  destination_cidr_block    = var.vpc_b_cidr
  vpc_peering_connection_id = aws_vpc_peering_connection.a_to_b.id
}

resource "aws_route_table_association" "vpc_a_private" {
  subnet_id      = aws_subnet.vpc_a_private.id
  route_table_id = aws_route_table.vpc_a_private.id
}

# ─── VPC B – Private Route Table ────────────────────────────────────────────
# Routes:
#   local        (implicit, VPC B CIDR)
#   10.10.0.0/16 → VPC Peering Connection
resource "aws_route_table" "vpc_b_private" {
  vpc_id = aws_vpc.vpc_b.id

  tags = {
    Name = "ewb-rt-b-private"
  }
}

resource "aws_route" "vpc_b_private_to_vpc_a" {
  route_table_id            = aws_route_table.vpc_b_private.id
  destination_cidr_block    = var.vpc_a_cidr
  vpc_peering_connection_id = aws_vpc_peering_connection.a_to_b.id
}

resource "aws_route_table_association" "vpc_b_private" {
  subnet_id      = aws_subnet.vpc_b_private.id
  route_table_id = aws_route_table.vpc_b_private.id
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECURITY GROUPS
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Bastion Security Group (VPC A) ─────────────────────────────────────────
# Allows inbound SSH from the student's public IP only.
resource "aws_security_group" "bastion" {
  name        = "ewb-sg-bastion"
  description = "Allow SSH from student IP to bastion host"
  vpc_id      = aws_vpc.vpc_a.id

  # Inbound: SSH from the student's public IP
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # Outbound: allow all (needed for SSH agent-forwarding to private instances)
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ewb-sg-bastion"
  }
}

# ─── App-A Security Group (VPC A) ───────────────────────────────────────────
# Allows:
#   - SSH from bastion (10.10.1.10/32)
#   - ICMP Echo Request from app-b (10.20.1.10/32)
resource "aws_security_group" "app_a" {
  name        = "ewb-sg-app-a"
  description = "Allow SSH from bastion and ICMP from app-b"
  vpc_id      = aws_vpc.vpc_a.id

  # Inbound: SSH from bastion private IP
  ingress {
    description = "SSH from bastion"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.10.1.10/32"]
  }

  # Inbound: ICMP Echo Request (type 8) from app-b in VPC B
  ingress {
    description = "ICMP Echo Request from app-b"
    from_port   = 8       # ICMP type 8 = Echo Request
    to_port     = -1      # ICMP code: -1 = all codes
    protocol    = "icmp"
    cidr_blocks = ["10.20.1.10/32"]
  }

  # Outbound: allow all
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ewb-sg-app-a"
  }
}

# ─── App-B Security Group (VPC B) ───────────────────────────────────────────
# Allows:
#   - SSH from bastion (10.10.1.10/32) – via VPC peering
#   - ICMP Echo Request from app-a (10.10.2.10/32) – via VPC peering
resource "aws_security_group" "app_b" {
  name        = "ewb-sg-app-b"
  description = "Allow SSH from bastion and ICMP from app-a via peering"
  vpc_id      = aws_vpc.vpc_b.id

  # Inbound: SSH from bastion private IP (crosses VPC peering)
  ingress {
    description = "SSH from bastion via peering"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.10.1.10/32"]
  }

  # Inbound: ICMP Echo Request (type 8) from app-a in VPC A
  ingress {
    description = "ICMP Echo Request from app-a"
    from_port   = 8       # ICMP type 8 = Echo Request
    to_port     = -1      # ICMP code: -1 = all codes
    protocol    = "icmp"
    cidr_blocks = ["10.10.2.10/32"]
  }

  # Outbound: allow all
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ewb-sg-app-b"
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# EC2 INSTANCES
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Bastion Host (VPC A / Public Subnet) ───────────────────────────────────
# Jump box with a public IP – the only entry point from the internet.
resource "aws_instance" "bastion" {
  ami                         = local.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.vpc_a_public.id
  vpc_security_group_ids      = [aws_security_group.bastion.id]
  key_name                    = var.key_name
  private_ip                  = "10.10.1.10"
  associate_public_ip_address = true

  tags = {
    Name = "ewb-bastion"
  }
}

# ─── App-A (VPC A / Private Subnet) ─────────────────────────────────────────
# Application server reachable only from the bastion via SSH.
resource "aws_instance" "app_a" {
  ami                         = local.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.vpc_a_private.id
  vpc_security_group_ids      = [aws_security_group.app_a.id]
  key_name                    = var.key_name
  private_ip                  = "10.10.2.10"
  associate_public_ip_address = false

  tags = {
    Name = "ewb-app-a"
  }
}

# ─── App-B (VPC B / Private Subnet) ─────────────────────────────────────────
# Application server reachable from VPC A only through VPC peering.
resource "aws_instance" "app_b" {
  ami                         = local.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.vpc_b_private.id
  vpc_security_group_ids      = [aws_security_group.app_b.id]
  key_name                    = var.key_name
  private_ip                  = "10.20.1.10"
  associate_public_ip_address = false

  tags = {
    Name = "ewb-app-b"
  }
}
