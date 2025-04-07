---
title: Unified SSH Key-Based Authentication Setup (Linux & Windows Clients)
description: A consolidated guide to setting up SSH key-based (passwordless) authentication for Linux servers, showing commands for both Linux and Windows 10 (OpenSSH) clients side-by-side.
updated: 2025-04-07
date: 2025-02-13
authors:
  - devsanghani
categories:
  - Guide
  - Tutorial
tags:
  - SSH
  - Linux
  - Windows
comments: true
comment_id: '114156406676318218'
---

# How to Set Up SSH Key-Based Authentication for Passwordless Login (Linux & Windows Clients)

This guide walks you through setting up SSH key-based authentication to connect to a Linux server without a password. Instructions are provided for performing the steps from both Linux and Windows 10 (using its built-in OpenSSH client) client machines.

I think of this guide as my personal cheatsheet – a quick way to set up SSH keys in the future without wading through extensive documentation, regardless of whether you're on a Linux or Windows client at the time.

---

### Step 1: Generate an SSH Key Pair

The first step is to create a public/private key pair on your local (client) machine.

1.  **Open your terminal:**
    * **On Linux:** Open your standard terminal (e.g., Bash).
    * **On Windows:** Open **PowerShell**.

2.  **Check for existing keys:** Before generating, see if keys already exist:
    * **On Linux:**
        ```bash
        ls -al ~/.ssh/id_*.pub
        ```
    * **On Windows (PowerShell):**
        ```powershell
        Get-ChildItem -Path $env:USERPROFILE\.ssh\id_*.pub
        # Or use Test-Path to just check existence (returns True/False)
        Test-Path $env:USERPROFILE\.ssh\id_rsa.pub
        ```
    * If keys exist (like `id_rsa.pub`), you can use them or back them up before creating new ones.

3.  **Generate new keys (if needed):** Run the same command in your terminal/PowerShell:
    ```bash
    ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
    ```
    * `-t rsa`: Specifies the RSA algorithm.
    * `-b 4096`: Sets a strong key length.
    * `-C "your_email@domain.com"`: Adds an identifying comment.

4.  **Follow the prompts:**
    * **File Location:** Press **Enter** to accept the default.
        * Linux default: `~/.ssh/id_rsa`
        * Windows default: `%USERPROFILE%\.ssh\id_rsa`
    * **Passphrase:**
        * Enter a strong passphrase for security (recommended).
        * Press **Enter** twice (empty passphrase) for true passwordless login.

5.  **Verify creation:** Your key pair (`id_rsa` and `id_rsa.pub`) should now exist in the respective `.ssh` directory.

---

### Step 2: Copy Your Public Key to the Remote Linux Server

Now, you need to add the content of your *public* key (`id_rsa.pub`) to the `~/.ssh/authorized_keys` file on the *remote server* for the user you want to log in as.

* **On your Linux client machine:**

    * **Method A: Using `ssh-copy-id` (Recommended)**
        ```bash
        ssh-copy-id remote_username@server_ip_address
        ```
        *(You'll be prompted for the remote user's password once).*

    * **Method B: Manual Copy (If `ssh-copy-id` isn't available)**
        ```bash
        # Ensure directory exists with correct permissions on server
        ssh remote_username@server_ip_address "mkdir -p ~/.ssh && chmod 700 ~/.ssh"
        # Append public key and set permissions
        cat ~/.ssh/id_rsa.pub | ssh remote_username@server_ip_address "cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        ```
        *(You may be prompted for the password multiple times).*

* **On your Windows client machine (using PowerShell):**

    * Since `ssh-copy-id` is not available, use this PowerShell command:
        ```powershell
        # Read the public key, connect, ensure dir/perms, append key, set key file perms
        type $env:USERPROFILE\.ssh\id_rsa.pub | ssh remote_username@server_ip_address "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        ```
        *(You will be prompted for the remote user's password).*

**Replace `remote_username@server_ip_address` with your actual remote login details in all commands.**

---

### Step 3: Test Passwordless Login

From your client machine (Linux terminal or Windows PowerShell/Command Prompt), try connecting to the server:

```bash
ssh remote_username@server_ip_address
```

If successful, you should be logged in without entering the server password. If you set a passphrase for your key in Step 1, you will be prompted to enter *that* passphrase now.

---

### Step 4: Optional - Enhance Security by Disabling Password Authentication on Server

**WARNING:** Only perform this step after confirming your SSH key login works perfectly from all necessary client machines. Disabling passwords incorrectly can lock you out. Ensure the key-based user has `sudo` privileges if administrative tasks are needed.

This step is performed **on the remote Linux server**.

1.  Log in to your remote server using your SSH key.
2.  Edit the SSH daemon's configuration file:
    ```bash
    sudo nano /etc/ssh/sshd_config
    ```
3.  Find and modify (or add) these lines. Ensure they are uncommented (no `#` at the beginning):
    ```ini
    PasswordAuthentication no
    ChallengeResponseAuthentication no
    # Consider UsePAM implications; start with PasswordAuthentication no first
    # UsePAM no
    ```
4.  Save the file (Ctrl+O, Enter in `nano`) and exit (Ctrl+X).
5.  Restart the SSH service:
    * **Ubuntu/Debian:** `sudo systemctl restart ssh`
    * **CentOS/Fedora/RHEL:** `sudo systemctl restart sshd`

Password logins are now disabled on the server.

---

## Conclusion

By following these integrated steps, you can generate SSH keys on either Linux or Windows, copy the public key to your Linux server using the appropriate method for your client OS, and establish secure, passwordless SSH connections. Optionally, you can further harden your server by disabling password authentication entirely.

Happy coding and secure connecting!

---

*References: Windows 10 OpenSSH steps adapted from Christopher Hart’s blog post (May 23, 2020).*