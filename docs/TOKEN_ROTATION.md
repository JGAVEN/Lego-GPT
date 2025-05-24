# JWT Token Rotation

To rotate authentication tokens:

1. **Generate a new secret**
   ```bash
   openssl rand -hex 32 > new_secret.txt
   ```
2. **Update environment**
   Set `JWT_SECRET` to the new secret for the API server and workers. Restart the processes or containers so they pick up the value.
3. **Invalidate old tokens**
   Tokens issued with the previous secret become invalid once the server restarts. Issue new tokens using:
   ```bash
   lego-gpt-token --secret $(cat new_secret.txt) --sub <user> > token.txt
   ```
4. **Redeploy clients**
   Distribute the new tokens to authorised users or update the `.env` files if automation uses them.

Rotating secrets periodically reduces the window of opportunity if a token or secret leaks.
