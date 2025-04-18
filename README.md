# Notice Screen

A simple Flask application that displays notices to users and requires acknowledgment before redirecting to another URL. Used for maintenance notices, system updates, or important announcements.

![image](https://github.com/user-attachments/assets/456ae2c7-8836-40f9-82bd-35beef6ea31d)

## Features

- **Notice Display**: Show important notices to users before they access your service
- **Local Network Detection**: Automatically detect if the request is coming from a local network
- **Cookie Management**: Comprehensive cookie consent system with granular control
- **Reverse Proxy Support**: Different UI for users accessing through a reverse proxy
- **Status Page Integration**: Optional link to your status page

## Cookie Types

The application uses the following cookies:

- **Notice Acknowledgment**: Stores when you last acknowledged the notice to prevent showing it again for a specified period
- **Cookie Preferences**: Stores your cookie preferences to remember your choices

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment (development/production) | development |
| `REDIRECT_URL` | URL to redirect to after acknowledgment | (empty)|
| `ACKNOWLEDGMENT_TIMEOUT_DAYS` | Number of days before notice reappears | 14 |
| `STATUS_PAGE` | URL to your status page | (empty) |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hollowpnt92/notice-screen.git
cd notice-screen
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

The application will be available at `http://localhost:5009`.

## Usage

### Local Network Access
When accessing from a local network:
- The notice text can be edited
- Changes can be saved
- The "Save Changes" button is visible

### Remote Access (via Reverse Proxy)
When accessing through a reverse proxy:
- The notice text is read-only
- The "Save Changes" button is hidden
- The text box appears non-editable

### Cookie Management
Users can:
- View and manage individual cookie preferences
- Accept all cookies with one click
- Reject all cookies with one click
- Save specific preferences
- Toggle individual cookie types on/off

## Development

### Building the Image
```bash
docker-compose build
```

### Running Tests
```bash
docker-compose run web python -m pytest
```

## Production Deployment

For production deployment:
1. Set `FLASK_ENV=production` in your environment variables
2. Ensure proper reverse proxy configuration
3. Set appropriate cookie timeout values
4. Configure your status page URL if applicable

## Security Considerations

- The application uses a non-root user in the container
- Debug mode is disabled in production
- Local network detection is implemented for security
- Cookie preferences are respected and stored securely

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
