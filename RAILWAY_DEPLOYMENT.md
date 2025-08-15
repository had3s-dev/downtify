# Railway Deployment Guide

This guide will help you deploy Downtify to Railway and set up your custom domain `music.nexusremains.online`.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your custom domain `music.nexusremains.online` ready to configure
3. Git repository with this code

## Deployment Steps

### 1. Deploy to Railway

#### Option A: Using Railway CLI (Recommended)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize and deploy:
   ```bash
   railway init
   railway up
   ```

#### Option B: Using Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select this repository
5. Railway will automatically detect the configuration and deploy

### 2. Set Up Railway Storage

1. In your Railway project dashboard, go to the "Storage" tab
2. Click "Add Storage"
3. Name it "downloads"
4. Set the mount path to `/data/downloads`
5. Click "Add Storage"

### 3. Configure Environment Variables

In your Railway project dashboard, add these environment variables:

```
DOWNLOAD_DIR=/data/downloads
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
```

**Note:** The default Spotify credentials are included in the code, but for production use, you should create your own Spotify app and use those credentials.

### 4. Set Up Custom Domain

1. In your Railway project dashboard, go to the "Settings" tab
2. Scroll down to "Domains" section
3. Click "Add Domain"
4. Enter your custom domain: `music.nexusremains.online`
5. Railway will provide you with DNS records to configure

### 5. Configure DNS

You'll need to configure your DNS provider with the records Railway provides. Typically this involves:

1. Adding a CNAME record:
   - Name: `music` (or subdomain of your choice)
   - Value: The Railway-provided domain (e.g., `your-app.railway.app`)

2. Or adding an A record if Railway provides an IP address

### 6. SSL Certificate

Railway automatically provisions SSL certificates for custom domains, so your site will be accessible via HTTPS.

## Important Notes

### File Storage
- Railway provides persistent storage through their storage service
- Downloaded files are stored in `/data/downloads` and persist across deployments
- The storage is automatically mounted and managed by Railway

### Rate Limits
- Be aware of Railway's resource limits and Spotify's API rate limits
- Monitor your usage in the Railway dashboard

### Environment Variables
- `PORT`: Automatically set by Railway and properly handled by the startup script
- `DOWNLOAD_DIR`: Set to `/data/downloads` for Railway's persistent storage
- `CLIENT_ID` and `CLIENT_SECRET`: Your Spotify app credentials

## Troubleshooting

### Common Issues

1. **Build fails**: Check that all dependencies are in `requirements-app.txt`
2. **Port issues**: Railway automatically sets the `PORT` environment variable
3. **File downloads not working**: Check that Railway storage is properly configured
4. **Domain not working**: Ensure DNS records are properly configured and propagated

### Logs
- View logs in the Railway dashboard under the "Deployments" tab
- Use `railway logs` if using the CLI

## Security Considerations

1. **Spotify Credentials**: Use your own Spotify app credentials for production
2. **Environment Variables**: Never commit sensitive data to your repository
3. **Rate Limiting**: Implement proper rate limiting for production use
4. **File Access**: Downloaded files are publicly accessible via the `/downloads` endpoint

## Monitoring

- Use Railway's built-in monitoring dashboard
- Set up alerts for resource usage
- Monitor application logs for errors

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Downtify Issues: [GitHub Issues](https://github.com/henriquesebastiao/downtify/issues)
