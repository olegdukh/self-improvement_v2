#cloud-config

package_update: true
package_upgrade: true

packages:
  - docker.io
  - git
  - curl
  - jq
  - python3
  - python3-pip
  - libicu-dev
  - libssl-dev

runcmd:
  - curl -fsSL https://tailscale.com/install.sh | sh

  - systemctl enable tailscaled
  - systemctl start tailscaled

  - tailscale up --authkey=TAILSCALE_AUTH_KEY

  - ufw default deny incoming
  - ufw allow out 443/tcp
  - ufw allow out 80/tcp
  - ufw --force enable

  - mkdir -p /actions-runner

  - cd /actions-runner

  - curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.317.0/actions-runner-linux-x64-2.317.0.tar.gz

  - tar xzf actions-runner.tar.gz

  - ./config.sh       --url https://github.com/GITHUB_OWNER/GITHUB_REPO       --token RUNNER_TOKEN       --ephemeral       --unattended       --labels hetzner-ephemeral

  - ./run.sh
