#──────────────────────────────────────────────────────────────────────────────
# outputs.tf – Exported values for the EWB VPC Peering Lab
#──────────────────────────────────────────────────────────────────────────────

# ═══════════════════════════════════════════════════════════════════════════════
# VPC IDs
# ═══════════════════════════════════════════════════════════════════════════════

output "vpc_a_id" {
  description = "ID of VPC A (10.10.0.0/16)."
  value       = aws_vpc.vpc_a.id
}

output "vpc_b_id" {
  description = "ID of VPC B (10.20.0.0/16)."
  value       = aws_vpc.vpc_b.id
}

# ═══════════════════════════════════════════════════════════════════════════════
# Subnet IDs
# ═══════════════════════════════════════════════════════════════════════════════

output "vpc_a_public_subnet_id" {
  description = "ID of the public subnet in VPC A."
  value       = aws_subnet.vpc_a_public.id
}

output "vpc_a_private_subnet_id" {
  description = "ID of the private subnet in VPC A."
  value       = aws_subnet.vpc_a_private.id
}

output "vpc_b_private_subnet_id" {
  description = "ID of the private subnet in VPC B."
  value       = aws_subnet.vpc_b_private.id
}

# ═══════════════════════════════════════════════════════════════════════════════
# VPC Peering Connection
# ═══════════════════════════════════════════════════════════════════════════════

output "peering_connection_id" {
  description = "ID of the VPC Peering Connection between VPC A and VPC B."
  value       = aws_vpc_peering_connection.a_to_b.id
}

output "peering_connection_status" {
  description = "Status of the VPC Peering Connection."
  value       = aws_vpc_peering_connection.a_to_b.accept_status
}

# ═══════════════════════════════════════════════════════════════════════════════
# EC2 Instance IDs
# ═══════════════════════════════════════════════════════════════════════════════

output "bastion_instance_id" {
  description = "Instance ID of the bastion host."
  value       = aws_instance.bastion.id
}

output "app_a_instance_id" {
  description = "Instance ID of app-a."
  value       = aws_instance.app_a.id
}

output "app_b_instance_id" {
  description = "Instance ID of app-b."
  value       = aws_instance.app_b.id
}

# ═══════════════════════════════════════════════════════════════════════════════
# EC2 Instance IPs
# ═══════════════════════════════════════════════════════════════════════════════

output "bastion_public_ip" {
  description = "Public IP address of the bastion host (use this to SSH in)."
  value       = aws_instance.bastion.public_ip
}

output "bastion_private_ip" {
  description = "Private IP address of the bastion host."
  value       = aws_instance.bastion.private_ip
}

output "app_a_private_ip" {
  description = "Private IP address of app-a."
  value       = aws_instance.app_a.private_ip
}

output "app_b_private_ip" {
  description = "Private IP address of app-b."
  value       = aws_instance.app_b.private_ip
}

# ═══════════════════════════════════════════════════════════════════════════════
# AMI Used
# ═══════════════════════════════════════════════════════════════════════════════

output "ami_id_used" {
  description = "AMI ID that was used for all instances."
  value       = local.ami_id
}

# ═══════════════════════════════════════════════════════════════════════════════
# SSH Connection Helper
# ═══════════════════════════════════════════════════════════════════════════════

output "ssh_bastion_command" {
  description = "SSH command to connect to the bastion host."
  value       = "ssh -i ${var.key_name}.pem ec2-user@${aws_instance.bastion.public_ip}"
}

output "ssh_app_a_via_bastion" {
  description = "SSH command to connect to app-a via the bastion (requires agent forwarding)."
  value       = "ssh -A -J ec2-user@${aws_instance.bastion.public_ip} ec2-user@${aws_instance.app_a.private_ip}"
}

output "ssh_app_b_via_bastion" {
  description = "SSH command to connect to app-b via the bastion (requires agent forwarding, crosses VPC peering)."
  value       = "ssh -A -J ec2-user@${aws_instance.bastion.public_ip} ec2-user@${aws_instance.app_b.private_ip}"
}
