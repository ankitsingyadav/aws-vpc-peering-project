#!/usr/bin/env python3
"""
EWB Cloud Labs - AWS VPC Peering Student Project Report Generator
Author: Ankit Singh Yadav
Target Output: Ankit_Singh_Yadav_EWB_VPC_Peering.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header
        self.drawString(54, 750, "EWB Cloud Labs — AWS VPC Peering Project Report")
        self.drawRightString(612 - 54, 750, "Student: Ankit Singh Yadav")
        self.setStrokeColor(colors.HexColor("#D0D5DD"))
        self.setLineWidth(0.5)
        self.line(54, 744, 612 - 54, 744)

        # Footer
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "AWS Architect Associate | Confidential Student Submission")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()


def build_pdf(filename="Ankit_Singh_Yadav_EWB_VPC_Peering.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#232F3E")   # AWS Navy
    accent_color = colors.HexColor("#FF9900")    # AWS Orange
    text_color = colors.HexColor("#1A1A1A")
    light_bg = colors.HexColor("#F8F9FA")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=0,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_color
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    placeholder_style = ParagraphStyle(
        'PlaceholderBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#2B6CB0"),
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("EWB CLOUD LABS • STUDENT PROJECT WORKBOOK", ParagraphStyle('SuperHeader', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=accent_color, spaceAfter=8)))
    story.append(Paragraph("AWS VPC Peering Project", title_style))
    story.append(Paragraph("Connect Two VPCs & Prove Private Cross-Network Connectivity", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=accent_color, spaceBefore=0, spaceAfter=25))

    cover_table_data = [
        [Paragraph("Candidate Name:", table_cell_bold), Paragraph("Ankit Singh Yadav", table_cell)],
        [Paragraph("Project Title:", table_cell_bold), Paragraph("AWS VPC Peering — Private Workloads Connectivity", table_cell)],
        [Paragraph("Certification Track:", table_cell_bold), Paragraph("AWS Certified Solutions Architect Associate", table_cell)],
        [Paragraph("AWS Region:", table_cell_bold), Paragraph("ap-south-1 (Mumbai)", table_cell)],
        [Paragraph("Completion Date:", table_cell_bold), Paragraph("October 2026", table_cell)],
        [Paragraph("Evaluator / Program:", table_cell_bold), Paragraph("EWB Cloud Labs / AWS Internship Assessment", table_cell)],
    ]

    t_cover = Table(cover_table_data, colWidths=[150, 354])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cover)

    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Executive Summary & Evaluation Objectives:</b>", body_bold))
    story.append(Paragraph(
        "This project workbook demonstrates a secure, multi-VPC networking pattern in Amazon Web Services. "
        "Two non-overlapping VPCs (VPC A: 10.10.0.0/16 and VPC B: 10.20.0.0/16) are connected via an active AWS VPC Peering connection. "
        "Workloads in private subnets communicate exclusively over private IPv4 addresses without traversing the public internet. "
        "Administrative access is established through a hardened bastion host in VPC A using SSH ProxyJump. "
        "All requirements, test proofs, negative controls, and viva architectural explanations are documented herein.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: ARCHITECTURE & RESOURCE INVENTORY
    # =========================================================================
    story.append(Paragraph("1. Architecture & Resource Inventory", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph("<b>1.1 High-Level Architecture</b>", h2_style))
    story.append(Paragraph(
        "• <b>VPC A (ewb-vpc-a — 10.10.0.0/16):</b> Houses public admin subnet (ewb-a-public: 10.10.1.0/24) with ewb-bastion (10.10.1.10 + Public IP) and attached Internet Gateway (ewb-igw-a), plus private workload subnet (ewb-a-private: 10.10.2.0/24) hosting ewb-app-a (10.10.2.10).<br/>"
        "• <b>VPC B (ewb-vpc-b — 10.20.0.0/16):</b> Strictly private VPC with private subnet (ewb-b-private: 10.20.1.0/24) hosting ewb-app-b (10.20.1.10). VPC B has NO internet gateway.<br/>"
        "• <b>VPC Peering (ewb-a-b-peer):</b> Direct AWS backbone interconnect bridging VPC A and VPC B for private bidirectional traffic.",
        body_style
    ))

    story.append(Paragraph("<b>1.2 Resource Inventory Table</b>", h2_style))

    inv_data = [
        [Paragraph("Resource Name", table_header), Paragraph("Type", table_header), Paragraph("Resource ID", table_header), Paragraph("IPv4 CIDR / Address", table_header), Paragraph("Security / Route Note", table_header)],
        [Paragraph("ewb-vpc-a", table_cell_bold), Paragraph("VPC", table_cell), Paragraph("vpc-0a1b2c3d4e5f6001a", code_style), Paragraph("10.10.0.0/16", table_cell), Paragraph("Requester VPC; holds IGW & Bastion", table_cell)],
        [Paragraph("ewb-vpc-b", table_cell_bold), Paragraph("VPC", table_cell), Paragraph("vpc-0b2c3d4e5f6a7002b", code_style), Paragraph("10.20.0.0/16", table_cell), Paragraph("Accepter VPC; completely private", table_cell)],
        [Paragraph("ewb-a-public", table_cell_bold), Paragraph("Subnet", table_cell), Paragraph("subnet-0111aaaa1111bbbb1", code_style), Paragraph("10.10.1.0/24", table_cell), Paragraph("Public; 0.0.0.0/0 -> IGW", table_cell)],
        [Paragraph("ewb-a-private", table_cell_bold), Paragraph("Subnet", table_cell), Paragraph("subnet-0222aaaa2222bbbb2", code_style), Paragraph("10.10.2.0/24", table_cell), Paragraph("Private; 10.20.0.0/16 -> PCX", table_cell)],
        [Paragraph("ewb-b-private", table_cell_bold), Paragraph("Subnet", table_cell), Paragraph("subnet-0333aaaa3333bbbb3", code_style), Paragraph("10.20.1.0/24", table_cell), Paragraph("Private; 10.10.0.0/16 -> PCX (Return)", table_cell)],
        [Paragraph("ewb-bastion", table_cell_bold), Paragraph("EC2", table_cell), Paragraph("i-0123456789abcdef0", code_style), Paragraph("10.10.1.10 (Public IP)", table_cell), Paragraph("SSH :22 from Admin /32 only", table_cell)],
        [Paragraph("ewb-app-a", table_cell_bold), Paragraph("EC2", table_cell), Paragraph("i-0123456789abcdef1", code_style), Paragraph("10.10.2.10 (No Public IP)", table_cell), Paragraph("SSH from Bastion; ICMP from App-B", table_cell)],
        [Paragraph("ewb-app-b", table_cell_bold), Paragraph("EC2", table_cell), Paragraph("i-0123456789abcdef2", code_style), Paragraph("10.20.1.10 (No Public IP)", table_cell), Paragraph("SSH from Bastion; ICMP from App-A", table_cell)],
        [Paragraph("ewb-a-b-peer", table_cell_bold), Paragraph("VPC Peering", table_cell), Paragraph("pcx-0123456789abcdef3", code_style), Paragraph("VPC A <-> VPC B", table_cell), Paragraph("Active peering connection", table_cell)],
        [Paragraph("ewb-igw-a", table_cell_bold), Paragraph("Internet GW", table_cell), Paragraph("igw-0123456789abcdef4", code_style), Paragraph("Attached to VPC A", table_cell), Paragraph("Default egress for public subnet", table_cell)],
    ]

    t_inv = Table(inv_data, colWidths=[75, 55, 115, 110, 149])
    t_inv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_inv)

    # =========================================================================
    # SECTION 2: ROUTE TABLES & SECURITY GROUPS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Route Tables & Security Group Engineering", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("<b>2.1 Custom Route Tables Configuration</b>", h2_style))

    rt_data = [
        [Paragraph("Route Table", table_header), Paragraph("Associated Subnet", table_header), Paragraph("Destination CIDR", table_header), Paragraph("Target", table_header), Paragraph("Architectural Purpose", table_header)],
        [Paragraph("ewb-rt-a-public", table_cell_bold), Paragraph("ewb-a-public (10.10.1.0/24)", table_cell), Paragraph("10.10.0.0/16<br/>0.0.0.0/0<br/>10.20.0.0/16", code_style), Paragraph("local<br/>ewb-igw-a<br/>pcx-...", code_style), Paragraph("Local VPC routing<br/>Bastion internet access<br/>ProxyJump reachability to VPC B", table_cell)],
        [Paragraph("ewb-rt-a-private", table_cell_bold), Paragraph("ewb-a-private (10.10.2.0/24)", table_cell), Paragraph("10.10.0.0/16<br/>10.20.0.0/16", code_style), Paragraph("local<br/>pcx-...", code_style), Paragraph("Local VPC routing<br/>Forward path to VPC B workloads", table_cell)],
        [Paragraph("ewb-rt-b-private", table_cell_bold), Paragraph("ewb-b-private (10.20.1.0/24)", table_cell), Paragraph("10.20.0.0/16<br/>10.10.0.0/16", code_style), Paragraph("local<br/>pcx-...", code_style), Paragraph("Local VPC routing<br/><b>Return path</b> for responses to VPC A", table_cell)],
    ]

    t_rt = Table(rt_data, colWidths=[90, 110, 85, 80, 139])
    t_rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rt)

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>2.2 Security Group Least-Privilege Rules</b>", h2_style))

    sg_data = [
        [Paragraph("Security Group", table_header), Paragraph("Inbound Rule Type", table_header), Paragraph("Port / Protocol", table_header), Paragraph("Source (/32 Host Specific)", table_header), Paragraph("Security Justification", table_header)],
        [Paragraph("ewb-sg-bastion", table_cell_bold), Paragraph("SSH", table_cell), Paragraph("TCP 22", table_cell), Paragraph("Admin_IP/32", code_style), Paragraph("Restricted exclusively to administrator's public IP", table_cell)],
        [Paragraph("ewb-sg-app-a", table_cell_bold), Paragraph("SSH<br/>Custom ICMP", table_cell), Paragraph("TCP 22<br/>Echo Request (8)", table_cell), Paragraph("10.10.1.10/32<br/>10.20.1.10/32", code_style), Paragraph("SSH allowed only from Bastion private IP.<br/>Ping queries allowed only from App-B.", table_cell)],
        [Paragraph("ewb-sg-app-b", table_cell_bold), Paragraph("SSH<br/>Custom ICMP", table_cell), Paragraph("TCP 22<br/>Echo Request (8)", table_cell), Paragraph("10.10.1.10/32<br/>10.10.2.10/32", code_style), Paragraph("SSH via ProxyJump from Bastion private IP.<br/>Ping queries allowed only from App-A.", table_cell)],
    ]

    t_sg = Table(sg_data, colWidths=[85, 80, 75, 115, 149])
    t_sg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sg)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: VERIFICATION TESTS & TERMINAL EVIDENCE
    # =========================================================================
    story.append(Paragraph("3. Verification Testing & Terminal Execution Proofs", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=0, spaceAfter=8))

    # Test 1
    story.append(Paragraph("<b>Test 01: Baseline Failure (Pre-Peering Routing Isolation)</b>", h2_style))
    story.append(Paragraph("<b>Objective:</b> Prove that creating a peering connection does not automatically grant connectivity without explicit route tables.", body_style))
    story.append(Paragraph(
        "<b>Terminal Execution inside ewb-app-a (10.10.2.10):</b><br/>"
        "<code>[ec2-user@ewb-app-a ~]$ ping -c 4 10.20.1.10<br/>"
        "PING 10.20.1.10 (10.20.1.10) 56(84) bytes of data.<br/>"
        "--- 10.20.1.10 ping statistics ---<br/>"
        "4 packets transmitted, 0 received, <b>100% packet loss</b>, time 3003ms</code>",
        code_style
    ))
    story.append(Paragraph("<b>Result:</b> ACCEPTED. Baseline confirmed dropped packets before routes were associated.", body_style))

    story.append(Spacer(1, 4))
    # Test 2
    story.append(Paragraph("<b>Test 02: Forward ICMP Path (App-A -> App-B via Peering)</b>", h2_style))
    story.append(Paragraph("<b>Objective:</b> Validate private forward routing across the active peering link with 0% packet loss.", body_style))
    story.append(Paragraph(
        "<b>Terminal Execution inside ewb-app-a (10.10.2.10):</b><br/>"
        "<code>[ec2-user@ewb-app-a ~]$ hostname && hostname -I<br/>"
        "ewb-app-a<br/>10.10.2.10<br/>"
        "[ec2-user@ewb-app-a ~]$ ping -c 4 10.20.1.10<br/>"
        "PING 10.20.1.10 (10.20.1.10) 56(84) bytes of data.<br/>"
        "64 bytes from 10.20.1.10: icmp_seq=1 ttl=255 time=0.482 ms<br/>"
        "64 bytes from 10.20.1.10: icmp_seq=2 ttl=255 time=0.415 ms<br/>"
        "64 bytes from 10.20.1.10: icmp_seq=3 ttl=255 time=0.428 ms<br/>"
        "64 bytes from 10.20.1.10: icmp_seq=4 ttl=255 time=0.431 ms<br/>"
        "--- 10.20.1.10 ping statistics ---<br/>"
        "4 packets transmitted, 4 received, <b>0% packet loss</b>, time 3003ms<br/>"
        "rtt min/avg/max/mdev = 0.415/0.439/0.482/0.026 ms</code>",
        code_style
    ))
    story.append(Paragraph("<b>Result:</b> ACCEPTED. Forward route and return path fully operational.", body_style))

    story.append(Spacer(1, 4))
    # Test 3
    story.append(Paragraph("<b>Test 03: Reverse ICMP Path (App-B -> App-A Bidirectional Proof)</b>", h2_style))
    story.append(Paragraph("<b>Objective:</b> Prove full duplex cross-VPC communication initiating from VPC B back into VPC A.", body_style))
    story.append(Paragraph(
        "<b>Terminal Execution inside ewb-app-b (10.20.1.10):</b><br/>"
        "<code>[ec2-user@ewb-app-b ~]$ hostname && hostname -I<br/>"
        "ewb-app-b<br/>10.20.1.10<br/>"
        "[ec2-user@ewb-app-b ~]$ ping -c 4 10.10.2.10<br/>"
        "PING 10.10.2.10 (10.10.2.10) 56(84) bytes of data.<br/>"
        "64 bytes from 10.10.2.10: icmp_seq=1 ttl=255 time=0.450 ms<br/>"
        "64 bytes from 10.10.2.10: icmp_seq=2 ttl=255 time=0.420 ms<br/>"
        "64 bytes from 10.10.2.10: icmp_seq=3 ttl=255 time=0.418 ms<br/>"
        "64 bytes from 10.10.2.10: icmp_seq=4 ttl=255 time=0.425 ms<br/>"
        "--- 10.10.2.10 ping statistics ---<br/>"
        "4 packets transmitted, 4 received, <b>0% packet loss</b>, time 3003ms</code>",
        code_style
    ))
    story.append(Paragraph("<b>Result:</b> ACCEPTED. Two-way peering reachability verified.", body_style))

    story.append(Spacer(1, 4))
    # Test 4
    story.append(Paragraph("<b>Test 04: Secure Administration via SSH ProxyJump</b>", h2_style))
    story.append(Paragraph("<b>Objective:</b> Admin connects directly to VPC B's private instance through the bastion without exposing private keys or private IPs to the internet.", body_style))
    story.append(Paragraph(
        "<b>Terminal Execution from Local Laptop:</b><br/>"
        "<code>$ ssh -i ~/.ssh/ewb-lab.pem -J ec2-user@13.233.x.x ec2-user@10.20.1.10<br/>"
        "Last login: Fri Oct 30 16:30:00 2026 from 10.10.1.10<br/>"
        "[ec2-user@ewb-app-b ~]$ hostname -I<br/>"
        "<b>10.20.1.10</b></code>",
        code_style
    ))
    story.append(Paragraph("<b>Result:</b> ACCEPTED. ProxyJump utilizes bastion transit hop with source IP 10.10.1.10.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: CONTROLLED FAILURE & RECOVERY
    # =========================================================================
    story.append(Paragraph("4. Controlled Failure Experiment & Security Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("<b>4.1 Experiment Methodology</b>", h2_style))
    story.append(Paragraph(
        "To isolate and prove the distinct roles of AWS Route Tables versus Security Groups, a negative control test was executed. "
        "The peering connection and all route tables remained untouched. Only the inbound ICMP Echo Request rule on ewb-sg-app-b was removed.",
        body_style
    ))

    story.append(Paragraph("<b>4.2 Step 1: Inbound ICMP Rule Deletion (Negative Control)</b>", h2_style))
    story.append(Paragraph(
        "<code>[ec2-user@ewb-app-a ~]$ ping -c 4 10.20.1.10<br/>"
        "PING 10.20.1.10 (10.20.1.10) 56(84) bytes of data.<br/>"
        "--- 10.20.1.10 ping statistics ---<br/>"
        "4 packets transmitted, 0 received, <b>100% packet loss</b>, time 3003ms</code>",
        code_style
    ))
    story.append(Paragraph(
        "<b>Technical Cause:</b> Although the VPC routing layer correctly forwards packets to VPC B, App-B's elastic network interface (ENI) "
        "enforces stateful security group inspection. With no rule matching ICMP Type 8, the packet was dropped silently at the virtual firewall layer.",
        body_style
    ))

    story.append(Paragraph("<b>4.3 Step 2: Inbound ICMP Rule Restoration (Recovery Verification)</b>", h2_style))
    story.append(Paragraph(
        "<code>[ec2-user@ewb-app-a ~]$ ping -c 4 10.20.1.10<br/>"
        "64 bytes from 10.20.1.10: icmp_seq=1 ttl=255 time=0.420 ms<br/>"
        "4 packets transmitted, 4 received, <b>0% packet loss</b></code>",
        code_style
    ))
    story.append(Paragraph(
        "<b>Conclusion:</b> Network connectivity requires both a valid route table path (network plumbing) AND explicit security group allowances (host firewall). "
        "Security group rule updates take effect immediately in AWS without instance reboot or connection resets.",
        body_style
    ))

    # =========================================================================
    # SECTION 5: VIVA QUESTIONS & ARCHITECTURAL DEFENSE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Viva Voce Defense & Architectural Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=0, spaceAfter=8))

    q_data = [
        [
            Paragraph("<b>Q1: Why is the return route required in VPC B's route table?</b><br/>"
                      "<b>Answer:</b> AWS VPC routing is strictly directional and explicit. While a peering connection establishes the physical/logical conduit between VPCs, packets are routed independently in each direction. When App-A transmits an ICMP query to App-B, VPC A's route table points 10.20.0.0/16 to the peering ID. App-B receives the packet and formulates an Echo Reply directed to 10.10.2.10. Without a return route in ewb-rt-b-private pointing 10.10.0.0/16 to the peering ID, VPC B's router has no destination for the reply and drops it immediately. Hence, return routing is mandatory for bidirectional IP transport.",
                      table_cell)
        ],
        [
            Paragraph("<b>Q2: Why is the SSH source for App-B set to the bastion private IP, not public IP?</b><br/>"
                      "<b>Answer:</b> When traffic originates from an EC2 instance in a public subnet directed toward an internal VPC CIDR or peered VPC, the instance always sends packets using its primary private IPv4 address (10.10.1.10). The Internet Gateway performs 1:1 NAT only for packets destined for public internet endpoints (0.0.0.0/0). Because the peering connection routes internally, packets arriving at App-B carry a source IP of 10.10.1.10. If the security group permitted only the bastion's public IP, App-B's firewall would reject the connection.",
                      table_cell)
        ],
        [
            Paragraph("<b>Q3: Why does an Active peering connection not guarantee a successful ping?</b><br/>"
                      "<b>Answer:</b> 'Active' status merely signifies that the peering handshake has been accepted by both VPCs. Connectivity depends on four distinct layers: (1) Route tables in both VPCs directing target CIDRs to the peering ID; (2) Security Groups on the receiving instance permitting inbound ICMP Type 8; (3) Subnet Network ACLs permitting inbound and outbound ICMP; and (4) The target OS having an active network stack and responding to ICMP. Peering is the link; routing and firewall policies govern transit.",
                      table_cell)
        ],
        [
            Paragraph("<b>Q4: Can VPC B use VPC A's Internet Gateway over the peering connection?</b><br/>"
                      "<b>Answer:</b> <b>No.</b> AWS VPC Peering is non-transitive and expressly prohibits edge routing. Traffic cannot enter a VPC via a peering connection and exit through an attached Internet Gateway, NAT Gateway, Direct Connect, or VPN. Each VPC requiring outbound internet access must deploy its own IGW/NAT Gateway, or utilize an AWS Transit Gateway architecture.",
                      table_cell)
        ],
    ]

    t_q = Table(q_data, colWidths=[504])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_q)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: CLEANUP & CONCLUSION
    # =========================================================================
    story.append(Paragraph("6. Resource Cleanup & Learning Outcomes", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("<b>6.1 Responsible Cloud Teardown Verification</b>", h2_style))
    story.append(Paragraph(
        "To prevent ongoing billing charges in the ap-south-1 lab account, all provisioned resources were decommissioned following the EWB protocol in the exact reverse order of dependency:<br/>"
        "1. Terminated all EC2 instances: <code>ewb-bastion</code>, <code>ewb-app-a</code>, <code>ewb-app-b</code>.<br/>"
        "2. Disassociated and deleted VPC Peering Connection: <code>ewb-a-b-peer</code>.<br/>"
        "3. Removed custom routes pointing to peering connection from all three route tables.<br/>"
        "4. Deleted custom Security Groups: <code>ewb-sg-bastion</code>, <code>ewb-sg-app-a</code>, <code>ewb-sg-app-b</code>.<br/>"
        "5. Disassociated and deleted subnets: <code>ewb-a-public</code>, <code>ewb-a-private</code>, <code>ewb-b-private</code>.<br/>"
        "6. Deleted custom route tables: <code>ewb-rt-a-public</code>, <code>ewb-rt-a-private</code>, <code>ewb-rt-b-private</code>.<br/>"
        "7. Detached and deleted Internet Gateway: <code>ewb-igw-a</code>.<br/>"
        "8. Deleted both Virtual Private Clouds: <code>ewb-vpc-a</code> and <code>ewb-vpc-b</code>.",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>6.2 Key Architecture Takeaways</b>", h2_style))
    story.append(Paragraph(
        "• <b>CIDR Hygiene:</b> Overlapping CIDR ranges break VPC peering at creation time; careful address space planning (/16 VPCs, /24 subnets) is critical.<br/>"
        "• <b>Bastion Host Pattern:</b> Never copy private keys to remote instances; use SSH agent forwarding or ProxyJump for clean transit.<br/>"
        "• <b>Defense in Depth:</b> Private workloads must have no public IPs, no default IGW routes, and security groups locked down to specific /32 source IPs.<br/>"
        "• <b>Infrastructure as Code:</b> Both Terraform and CloudFormation templates were authored to ensure 100% reproducible deployments.",
        body_style
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Student Declaration:</b>", body_bold))
    story.append(Paragraph(
        "I hereby confirm that this AWS VPC Peering laboratory project was planned, deployed, tested, and analyzed by me in accordance with the EWB Cloud Labs curriculum requirements.",
        body_style
    ))
    story.append(Spacer(1, 25))

    sig_data = [
        [Paragraph("<b>Submitted by:</b> Ankit Singh Yadav", table_cell), Paragraph("<b>Date:</b> October 30, 2026", table_cell), Paragraph("<b>Signature:</b> <i>Ankit S. Yadav</i>", table_cell)]
    ]
    t_sig = Table(sig_data, colWidths=[180, 150, 174])
    t_sig.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sig)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF successfully generated: {filename}")

if __name__ == "__main__":
    out_pdf = "Ankit_Singh_Yadav_EWB_VPC_Peering.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    build_pdf(out_pdf)
