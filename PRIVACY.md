## Privacy

**Last Updated:** June 19, 2025
**Version:** 0.0.1

## Overview

This privacy policy describes how the Salesforce Dify Plugin ("the Plugin") collects, uses, stores, and protects your
information when you use it to connect to and query Salesforce data through the Dify platform.

## Information We Collect

### 1. Authentication Credentials

The Plugin collects and processes the following authentication information:

- **Salesforce Login URL**: Your Salesforce instance URL (e.g., https://login.salesforce.com
  or https://test.salesforce.com)
- **Salesforce Username**: Your Salesforce account username/email
- **Salesforce Password + Security Token**: Your Salesforce password concatenated with your security token

### 2. Session Data

During operation, the Plugin temporarily stores:

- **Session Tokens**: OAuth session tokens obtained from Salesforce for API access
- **Instance URLs**: Your specific Salesforce instance URL for API calls
- **Session Expiry Information**: Timestamps for session management

## How We Use Your Information

### Authentication and Access

- Credentials are used exclusively to authenticate with your Salesforce instance via SOAP API
- Session tokens are used to make authorized API calls to retrieve data you request
- No credentials are transmitted to any third parties other than your specified Salesforce instance

### Data Retrieval

- SOQL queries are executed against your Salesforce instance to retrieve the specific data you request
- Query results are returned to you through the Dify platform interface
- The Plugin only accesses data that your Salesforce user account has permission to view

## Data Storage and Security

### Local Storage

- **Session Tokens**: Temporarily stored in Dify's secure key-value storage system for up to 23 hours
- **Credentials**: Stored securely within Dify's credential management system
- **No Persistent Data**: The Plugin does not permanently store your Salesforce data

### Security Measures

- All communications with Salesforce use HTTPS encryption
- Session tokens are automatically refreshed when expired
- Stored sessions are cleared when they expire
- Credentials are handled through Dify's secure credential management system

### Data Retention

- Session tokens are automatically deleted after 23 hours or when they expire
- No query results are permanently stored by the Plugin
- Credentials are retained only as long as you keep the Plugin configured in your Dify workspace

## Data Sharing and Third Parties

### No Third-Party Sharing

- Your Salesforce credentials and data are never shared with third parties
- The Plugin only communicates with your specified Salesforce instance and the Dify platform
- No analytics, tracking, or data collection services are used

### Salesforce Integration

- The Plugin connects directly to your Salesforce instance using official Salesforce APIs
- All data access is subject to your Salesforce organization's security policies and permissions
- The Plugin respects all Salesforce data access controls and user permissions

## Your Rights and Controls

### Access Control

- You control which Salesforce data the Plugin can access through your SOQL queries
- The Plugin can only access data that your Salesforce user account has permission to view
- You can revoke access at any time by removing the Plugin configuration from Dify

### Data Deletion

- You can delete stored credentials by removing the Plugin configuration
- Session data is automatically purged when sessions expire
- No permanent copies of your Salesforce data are retained

## Compliance and Standards

### Security Standards

- The Plugin follows secure coding practices for credential handling
- All API communications use industry-standard encryption (HTTPS/TLS)
- Session management follows OAuth and SOAP API best practices

### Salesforce Compliance

- The Plugin uses official Salesforce APIs and follows Salesforce security guidelines
- All data access respects Salesforce field-level security and sharing rules
- The Plugin operates within Salesforce API rate limits and usage policies

## Logging and Monitoring

### Operational Logs

The Plugin generates logs for:

- Authentication attempts (without storing actual credentials)
- API request status and errors
- Session management activities

### Log Security

- Logs do not contain sensitive credential information
- Only operational metadata is logged for troubleshooting purposes
- Logs are managed according to Dify platform policies

## Changes to This Privacy Policy

We may update this privacy policy from time to time. When we do:

- The "Last Updated" date at the top of this policy will be revised
- Significant changes will be communicated through appropriate channels
- Continued use of the Plugin after changes constitutes acceptance of the updated policy

## Contact Information

For questions about this privacy policy or the Plugin's data practices:

- **Plugin Author**: eric-2369
- **Repository**: https://github.com/Eric-2369/salesforce-dify-plugin
- **Issues**: Please report privacy concerns through the GitHub repository issues

## Disclaimer

This Plugin is provided "as is" without warranties. Users are responsible for:

- Ensuring compliance with their organization's data policies
- Managing their Salesforce credentials securely
- Understanding their Salesforce organization's data access permissions
- Complying with applicable data protection regulations (GDPR, CCPA, etc.)

By using this Plugin, you acknowledge that you have read and understood this privacy policy and agree to its terms.
