# Publishing via LinkedIn's Official API

No browser automation. No cookies. No scraping. One documented endpoint.

## What we use

| | |
|---|---|
| Product | **Share on LinkedIn** — self-serve, added from the app's Products tab, **no review queue** |
| Scope | `w_member_social` — create a post on behalf of the authenticated member |
| OAuth scopes requested | `openid profile w_member_social` |
| Endpoint | `POST https://api.linkedin.com/v2/ugcPosts` |
| Required header | `X-Restli-Protocol-Version: 2.0.0` |
| Success | `201 Created`, new post id in the `X-RestLi-Id` response header |

Docs: <https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin>

## Setup

1. <https://www.linkedin.com/developers/apps> → create app, associate it with a Page you admin (LinkedIn
   requires this even for personal posting).
2. Products tab → add **Share on LinkedIn**. Granted immediately.
3. Auth tab → add redirect URL `http://localhost:8765/callback`.
4. Run `scripts/linkedin_auth_github.py --repo OWNER/REPO`. It opens the consent screen, catches the
   redirect, exchanges the code, and stores the token directly as a GitHub Actions secret.

**The token never goes in git or workflow logs.** The local helper sends it to `gh secret set` without
printing it. Do not add a fallback that writes it to a file.

## Token lifetime — the operational catch

- Access tokens are valid **~60 days**.
- Programmatic refresh tokens are gated behind LinkedIn approval and are **not** granted by the
  self-serve Share on LinkedIn product.
- So: **expect to re-run `linkedin_auth_github.py` roughly every two months.** It is a browser click-through,
  about 30 seconds.
- `src/content_engine/linkedin.py` checks expiry before posting and fails rather than publishing with
  an expired token.

The expiry timestamp is stored in `LINKEDIN_TOKEN_EXPIRES_AT`. The orchestration posts one Slack
warning when seven days or less remain. A private `system:token-warning` issue prevents repeat alerts
for the same token.

## Scope boundaries

What `w_member_social` **can** do:

- Post text, article/link, and image posts to the authenticated member's own profile.
- Comment and react on behalf of that member — *if you already hold the target post's URN*.

What it **cannot** do, and why that closes off the "find posts to comment on" idea:

- Read the feed, search posts, or list anyone's activity. That needs `r_member_social`, which is
  **closed to new applicants**.
- So there is no legitimate way to *discover* posts to comment on. The only route is driving a
  logged-in browser session, which violates the User Agreement. This pipeline does not do it, and no
  amount of queue redesign changes that.

Company Page posting needs the Community Management API and partner approval — separate track, not
wired up here.

## Payload shapes

Text-only:

```json
{
  "author": "urn:li:person:<id>",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": { "text": "..." },
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" }
}
```

With a link, set `shareMediaCategory: "ARTICLE"` and add `media[].originalUrl`. With an image, register
the upload at `POST /v2/assets?action=registerUpload`, PUT the binary to the returned `uploadUrl`, then
reference the returned asset URN with `shareMediaCategory: "IMAGE"`.

## Formatting notes

- LinkedIn renders no markdown. `**bold**` publishes literally as asterisks. Draft in plain text.
- Line breaks survive. Use them; they are the only structural tool available.
- The first ~140 characters show before "see more". Front-load.
- Links in the body suppress reach somewhat. Put the link in the first comment if it matters — but that
  is a manual action here, since auto-commenting is out of scope.
