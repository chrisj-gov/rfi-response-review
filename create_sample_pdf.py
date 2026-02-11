#!/usr/bin/env python3
"""
Create a sample RFI response PDF for testing purposes.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def create_sample_rfi_pdf(filename="sample_rfi_response.pdf"):
    """Create a sample RFI response PDF for testing."""
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("RFI Response: Cloud Infrastructure Implementation", title_style))
    story.append(Spacer(1, 20))
    
    # Introduction
    story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
    intro_text = """
    This document provides our comprehensive response to the Request for Information (RFI) 
    regarding cloud infrastructure implementation, security measures, and deployment timeline.
    Our approach focuses on security, scalability, and compliance with federal regulations.
    """
    story.append(Paragraph(intro_text, styles['BodyText']))
    story.append(Spacer(1, 15))
    
    # Technical Implementation Section
    story.append(Paragraph("<b>Technical Implementation</b>", styles['Heading2']))
    tech_text = """
    <b>Key Actions and Timeline:</b><br/>
    <br/>
    1. <b>Infrastructure Setup:</b> We will implement a multi-region cloud infrastructure 
    within 45 days of contract award. This includes setting up VPCs, subnets, and 
    network security groups across us-east-1 and us-west-2 regions.<br/>
    <br/>
    2. <b>Development Environment:</b> Complete development environment setup within 30 days, 
    including CI/CD pipelines, automated testing frameworks, and containerization with 
    Docker and Kubernetes.<br/>
    <br/>
    3. <b>Monitoring and Logging:</b> Implement comprehensive monitoring and logging solutions 
    within 60 days, utilizing CloudWatch, Prometheus, and Grafana for real-time system 
    visibility.
    """
    story.append(Paragraph(tech_text, styles['BodyText']))
    story.append(Spacer(1, 15))
    
    # Security Section
    story.append(Paragraph("<b>Security and Compliance</b>", styles['Heading2']))
    security_text = """
    <b>Security Measures:</b><br/>
    <br/>
    1. <b>Multi-Factor Authentication:</b> Implement MFA for all user accounts within 15 days. 
    This is a high-priority action that will use hardware tokens and authenticator apps.<br/>
    <br/>
    2. <b>Encryption:</b> Deploy end-to-end encryption for data in transit and at rest 
    within 30 days. This includes TLS 1.3 for all communications and AES-256 for stored data.<br/>
    <br/>
    3. <b>Security Audit:</b> Complete comprehensive security audit by end of Q2 2026. 
    This will include penetration testing, vulnerability scanning, and compliance verification.<br/>
    <br/>
    4. <b>Access Control:</b> Implement role-based access control (RBAC) within 20 days, 
    ensuring principle of least privilege across all systems.
    """
    story.append(Paragraph(security_text, styles['BodyText']))
    story.append(Spacer(1, 15))
    
    # Compliance Section
    story.append(Paragraph("<b>Compliance and Documentation</b>", styles['Heading2']))
    compliance_text = """
    <b>Compliance Requirements:</b><br/>
    <br/>
    1. <b>FedRAMP Compliance:</b> Achieve FedRAMP Moderate authorization within 6 months. 
    This is a critical milestone for federal deployment.<br/>
    <br/>
    2. <b>Documentation:</b> Submit all technical documentation within 60 days, including 
    system architecture diagrams, security controls matrix, and operational procedures.<br/>
    <br/>
    3. <b>Training Materials:</b> Develop and deliver user training materials within 90 days, 
    covering system operation, security protocols, and best practices.
    """
    story.append(Paragraph(compliance_text, styles['BodyText']))
    story.append(Spacer(1, 15))
    
    # Timeline Summary
    story.append(Paragraph("<b>Implementation Timeline Summary</b>", styles['Heading2']))
    timeline_text = """
    <b>Phase 1 (0-30 days):</b><br/>
    - Implement MFA (high priority)<br/>
    - Set up development environment<br/>
    - Deploy RBAC<br/>
    - Begin infrastructure setup<br/>
    <br/>
    <b>Phase 2 (31-60 days):</b><br/>
    - Complete infrastructure setup<br/>
    - Deploy encryption<br/>
    - Implement monitoring and logging<br/>
    - Submit technical documentation<br/>
    <br/>
    <b>Phase 3 (61-90 days):</b><br/>
    - Deliver training materials<br/>
    - Complete security audit<br/>
    - Performance optimization<br/>
    <br/>
    <b>Phase 4 (91-180 days):</b><br/>
    - Achieve FedRAMP authorization<br/>
    - Final compliance verification<br/>
    - Production deployment readiness
    """
    story.append(Paragraph(timeline_text, styles['BodyText']))
    story.append(Spacer(1, 15))
    
    # Conclusion
    story.append(Paragraph("<b>Conclusion</b>", styles['Heading2']))
    conclusion_text = """
    Our proposed solution addresses all requirements outlined in the RFI with a focus on 
    security, compliance, and timely delivery. We are committed to meeting all deadlines 
    and maintaining the highest standards of quality throughout the implementation process.
    """
    story.append(Paragraph(conclusion_text, styles['BodyText']))
    
    # Build PDF
    doc.build(story)
    print(f"Sample RFI response PDF created: {filename}")
    return filename


if __name__ == "__main__":
    create_sample_rfi_pdf()
