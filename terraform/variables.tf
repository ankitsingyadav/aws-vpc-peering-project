#──────────────────────────────────────────────────────────────────────────────
# variables.tf – Input variables for the EWB VPC Peering Lab
#──────────────────────────────────────────────────────────────────────────────

# ─── General Settings ────────────────────────────────────────────────────────

variable "aws_region" {
  description = "AWS region where all resources will be provisioned."
  type        = string
  default     = "ap-south-1"
}

variable "student_name" {
  description = "Name of the student running this lab (used in resource tags)."
  type        = string
}

variable "my_ip" {
  description = "Your public IP address in CIDR notation (e.g. 203.0.113.42/32). Used to allow SSH into the bastion host."
  type        = string

  validation {
    condition     = can(cidrhost(var.my_ip, 0))
    error_message = "my_ip must be a valid CIDR block, e.g. 203.0.113.42/32."
  }
}

# ─── Key Pair ────────────────────────────────────────────────────────────────

variable "key_name" {
  description = "Name of an existing EC2 key pair to attach to instances for SSH access."
  type        = string
  default     = "ewb-lab"
}

# ─── AMI ─────────────────────────────────────────────────────────────────────

variable "ami_id" {
  description = "Optional: Override the AMI ID for EC2 instances. Leave empty to auto-detect the latest Amazon Linux 2023 AMI."
  type        = string
  default     = ""
}

# ─── Networking CIDRs (hard-coded per lab spec, exposed for transparency) ───

variable "vpc_a_cidr" {
  description = "CIDR block for VPC A."
  type        = string
  default     = "10.10.0.0/16"
}

variable "vpc_b_cidr" {
  description = "CIDR block for VPC B."
  type        = string
  default     = "10.20.0.0/16"
}

variable "vpc_a_public_subnet_cidr" {
  description = "CIDR block for VPC A's public subnet."
  type        = string
  default     = "10.10.1.0/24"
}

variable "vpc_a_private_subnet_cidr" {
  description = "CIDR block for VPC A's private subnet."
  type        = string
  default     = "10.10.2.0/24"
}

variable "vpc_b_private_subnet_cidr" {
  description = "CIDR block for VPC B's private subnet."
  type        = string
  default     = "10.20.1.0/24"
}

# ─── Instance Type ───────────────────────────────────────────────────────────

variable "instance_type" {
  description = "EC2 instance type for all lab instances."
  type        = string
  default     = "t3.micro"
}

# ─── Common Tags ─────────────────────────────────────────────────────────────

variable "project_tag" {
  description = "Value for the 'Project' tag applied to every resource."
  type        = string
  default     = "EWB-VPC-Peering"
}
