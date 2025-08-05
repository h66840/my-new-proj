# Package Tracker Configuration

## Todoist Integration Setup

### Prerequisites
1. Todoist account with API access
2. Python 3.7+ with requests library
3. Valid Todoist API token

### Configuration

#### Environment Variables
```bash
export TODOIST_API_TOKEN="your_todoist_api_token_here"
```

#### Package Types and Their Handling

| Package Type | Priority Level | Due Date | Use Case |
|-------------|---------------|----------|----------|
| `urgent` | 4 (Highest) | 2 hours | Medical supplies, critical documents |
| `perishable` | 4 (Highest) | 1 hour | Food deliveries, temperature-sensitive items |
| `important` | 3 (High) | 4 hours | Business documents, valuable items |
| `standard` | 2 (Normal) | 1 day | Regular packages, non-urgent items |

#### Task Creation Features

✅ **Automatic Due Date Assignment**
- Based on package type and urgency
- Helps prioritize package processing

✅ **Priority Levels**
- 1-4 scale (1=lowest, 4=highest)
- Visual indicators in Todoist

✅ **Rich Task Descriptions**
- Tracking ID
- Sender information
- Delivery timestamp
- Package type classification
- Action items

✅ **Enhanced Formatting**
- Emoji indicators for quick recognition
- Structured information layout
- Priority and due date summaries

### Usage Examples

#### Basic Usage
```python
from package_tracker import PackageTracker

# Initialize with your Todoist token
tracker = PackageTracker("your_todoist_token")

# Handle a standard package delivery
package_info = {
    "tracking_id": "PKG123456789",
    "sender": "Amazon",
    "delivery_time": "2024-01-15T14:30:00Z",
    "type": "standard"
}

tracker.handle_package_delivery(package_info)
```

#### Urgent Package Handling
```python
urgent_package = {
    "tracking_id": "URGENT987654321",
    "sender": "Medical Supply Co",
    "delivery_time": "2024-01-15T15:00:00Z",
    "type": "urgent"
}

tracker.handle_package_delivery(urgent_package)
```

### Integration with Delivery Services

This tracker can be integrated with various delivery notification systems:

- **Email parsing**: Parse delivery confirmation emails
- **SMS webhooks**: Handle SMS delivery notifications
- **API integrations**: Connect with shipping company APIs
- **IoT sensors**: Smart mailbox or doorbell integrations

### Customization Options

#### Custom Due Date Calculation
Modify the `calculate_due_date()` method to adjust timing based on your needs.

#### Custom Priority Mapping
Update the `determine_priority()` method to change priority assignments.

#### Task Content Formatting
Customize the task content and description templates in `handle_package_delivery()`.

### Troubleshooting

#### Common Issues
1. **Invalid API Token**: Ensure your Todoist API token is valid and has proper permissions
2. **Network Errors**: Check internet connectivity and Todoist API status
3. **Rate Limiting**: Todoist API has rate limits; implement appropriate delays for bulk operations

#### Error Handling
The tracker includes comprehensive error handling:
- API connection failures
- Invalid package data
- Todoist service unavailability

### Future Enhancements

🔮 **Planned Features**
- [ ] Integration with multiple task management platforms
- [ ] Machine learning for automatic package type detection
- [ ] Photo attachment support for package documentation
- [ ] Delivery location tracking
- [ ] Package value-based priority adjustment
- [ ] Recurring delivery pattern recognition

### Security Considerations

⚠️ **Important Security Notes**
- Never commit API tokens to version control
- Use environment variables for sensitive configuration
- Implement proper access controls for production deployments
- Consider encryption for stored package information

### Support

For issues or feature requests, please create an issue in the repository.