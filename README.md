# Firstmate Project Tracker

This repository publishes the application shell on GitHub Pages. Project records,
assistant messages and artifacts are supplied by a separately authenticated laptop
gateway after pairing. No project archive, pairing key or private attachment belongs
in this repository.

Open the deployed site, then enter the pairing key from the laptop's Firstmate
Project Tracker controls. The connection address can change when the temporary
HTTPS tunnel restarts. `connection.json` contains only its public address.

The laptop must be awake, connected and signed in. Unavailable connections leave
an explicit offline state. Private content stays in browser memory, and the pairing
key lasts only for the browser tab's session. Closing the tab requires pairing again.

The active Pages publishing source is the `main` branch with `.nojekyll`. The local
export checks a fixed repository allowlist before pushing. Its thirteen public files
contain only the application and deployment documentation. Local developer notes,
screenshots and test fixtures are excluded. A manual Actions workflow can also
build an artifact from the six named application files and four reviewed font
assets when Actions is available. Sora and Manrope are self-hosted with their
Open Font Licenses; no external font request is needed.
The public address carries an HMAC proof. The app verifies it with the pairing key
before sending credentials to an automatically discovered address.
