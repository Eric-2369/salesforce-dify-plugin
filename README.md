# salesforce-dify-plugin

A comprehensive Dify plugin that enables seamless integration with Salesforce, providing powerful data access and
interaction capabilities for your AI workflows.

- **Author:** eric-2369
- **Version:** 0.0.1
- **Type:** tool

## Features

- **Secure Authentication**: Robust authentication with automatic credential management
- **Smart Session Management**: Intelligent session handling with automatic token storage and refresh
- **Auto Recovery**: Automatic error handling and session recovery for uninterrupted workflows
- **Comprehensive Logging**: Full logging integration with Dify's plugin logging system
- **Multi-language Support**: English, Chinese, and Portuguese interface support
- **High Performance**: Optimized for efficient Salesforce data operations

## Installation

1. Install the plugin in your Dify environment
2. Configure your Salesforce credentials in the plugin settings

## Configuration

### Required Credentials

1. **Salesforce Login URL**
    - Production: `https://login.salesforce.com`
    - Sandbox: `https://test.salesforce.com`

2. **Salesforce Username**
    - Your Salesforce account username

3. **Salesforce Password + Security Token**
    - Your password concatenated with your security token (no space between them)
    - Example: If password is `mypassword` and token is `ABC123`, enter `mypasswordABC123`

### Getting Your Security Token

1. Log in to Salesforce
2. Go to Setup → My Personal Information → Reset My Security Token
3. Click "Reset Security Token"
4. Check your email for the new security token

## Usage

### Data Retrieval

Retrieve account information:

```sql
SELECT Id, Name
FROM Account LIMIT 10
```

Query contacts with specific criteria:

```sql
SELECT Id, Email
FROM Contact
WHERE Name = 'John Doe'
```

Access related data across objects:

```sql
SELECT Id, Channel_Type__c
FROM Holistic_Engagement__c
WHERE Person__r.Contact__r.Name = 'John Doe' LIMIT 10
```

## API Response Format

The plugin returns results in the following JSON format:

```json
{
  "totalSize": 5,
  "done": true,
  "records": [
    {
      "attributes": {
        "type": "Account",
        "url": "/services/data/v63.0/sobjects/Account/001..."
      },
      "Id": "001...",
      "Name": "Sample Account"
    }
  ],
  "query": "SELECT Id, Name FROM Account LIMIT 10"
}
```

## Technical Architecture

### Session Management

- **Secure Authentication**: Robust authentication with Salesforce
- **Token Storage**: Persistent session storage using Dify's KV storage
- **Automatic Refresh**: Intelligent token lifecycle management
- **Error Recovery**: Automatic error handling and session recovery

### Security Features

- **Secure Credential Storage**: All credentials are securely stored in Dify
- **Session Management**: Proactive session management and renewal
- **Error Handling**: Comprehensive error handling with user-friendly messages

### Performance Optimization

- **Session Caching**: Efficient session reuse to minimize overhead
- **Optimized Requests**: High-performance API communication
- **Memory Management**: Efficient resource usage in serverless environment

## Error Handling

The plugin provides comprehensive error handling for common scenarios:

- **Invalid Credentials**: Clear messages for authentication failures
- **Network Issues**: Timeout and connection error handling
- **Query Syntax Errors**: Detailed error messages for invalid queries
- **API Limits**: Proper handling of Salesforce API limits
- **Session Expiry**: Automatic session refresh and retry

## Logging

The plugin uses Dify's logging system to record:

- Authentication attempts and results
- Data query executions
- Session refresh operations
- Error conditions and resolutions

## Troubleshooting

### Common Issues

1. **Authentication Failed**
    - Verify your username and password
    - Ensure security token is current and correctly concatenated
    - Check if your Salesforce org allows API access

2. **Invalid Query**
    - Verify query syntax is correct
    - Ensure you have permission to access the queried objects
    - Check field names and object names are correct

3. **Network Timeouts**
    - Check your network connection
    - Verify the Salesforce login URL is correct
    - Ensure firewall allows outbound HTTPS connections

## Development

### Project Structure

```
salesforce-dify-plugin/
├── manifest.yaml              # Plugin configuration
├── requirements.txt           # Python dependencies
├── provider/
│   ├── salesforce.yaml       # Provider configuration
│   └── salesforce.py         # Credential validation
├── tools/
│   ├── soql_query.yaml       # Tool configuration
│   └── soql_query.py         # SOQL query implementation
└── utils/
    └── session_manager.py     # Session management logic
```

### Key Components

- **SalesforceSessionManager**: Handles authentication and session management
- **SalesforceProvider**: Validates credentials during plugin configuration
- **SoqlQueryTool**: Executes data queries with automatic error handling

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review Salesforce API documentation
3. Contact the plugin author
