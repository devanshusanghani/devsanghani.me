---
title: SSH Key-Based (Passwordless) Authentication for Linux and Windows 10
description: A comprehensive tutorial on setting up SSH key-based (passwordless) authentication for Linux and Windows 10 (using OpenSSH), incorporating steps for both Linux and Windows environments.
date: 2025-02-13
authors:
    - devsanghani
categories:
    - Guide
    - Tutorial
tags:
    - SSH

comments: true

comment_id: '114156406676318218'
---
# How to Set Up SSH Key-Based Authentication for Passwordless Login

This tutorial explains how to set up an SSH key-based authentication to connect to your Linux server without entering a password. It covers generating an SSH key pair, copying your public key to the server, and logging in. We also provide details on using Windows 10’s OpenSSH client, which lacks the `ssh-copy-id` command, to achieve passwordless login.

---

## 1. Setting Up SSH Passwordless Login on Linux

### 1.1. Generate an SSH Key Pair

First, check if you already have an existing SSH key pair. Open your terminal and run:

```bash
ls -al ~/.ssh/id_*.pub
```

- **If keys exist:** You can use them or back them up and create a new one.
- **If not:** Generate a new key pair by executing:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
```

- Press **Enter** to accept the default file location (`/home/yourusername/.ssh/id_rsa`).
- When prompted, enter a secure passphrase (or press **Enter** to skip for passwordless login).

After the key generation, list your keys to verify they are created:

```bash
ls ~/.ssh/id_*
```



Below is a complete tutorial on setting up SSH key-based (passwordless) login on Linux and the Windows 10 OpenSSH equivalent for using **ssh-copy-id**.

---

## 1. Setting Up SSH Passwordless Login on Linux

### Step 1: Check for Existing SSH Keys

Before generating a new SSH key pair, verify if you already have one:

```bash
ls -al ~/.ssh/id_*.pub
```

- **If keys exist:**  
  - You can either use an existing key or back it up and generate a new one.
- **If no keys are present:** Proceed to generate a new SSH key pair.

---

## 2. Generate a New SSH Key Pair

Open your terminal and run:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
```

- When prompted:
  - **File Location:** Press **Enter** to accept the default location (`/home/yourusername/.ssh/id_rsa`).
  - **Passphrase:** You can set a passphrase for extra security. If you prefer not to use one, simply press **Enter** when prompted.

After completion, verify your keys by listing them:

```bash
ls ~/.ssh/id_*
```

---

## 3. Copy Your Public Key to the Remote Linux Server

### Using `ssh-copy-id`

On your local machine, use the `ssh-copy-id` command to copy your public key to the remote server:

```bash
ssh-copy-id remote_username@server_ip_address
```

- You will be prompted to enter the remote user's password.
- After authentication, your public key is added to the remote server’s `~/.ssh/authorized_keys` file.

### Without `ssh-copy-id`

If you prefer, or if `ssh-copy-id` isn’t available, run:

```bash
ssh remote_username@server_ip_address "mkdir -p ~/.ssh && chmod 700 ~/.ssh"
cat ~/.ssh/id_rsa.pub | ssh remote_username@server_ip_address "cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

This command logs into your server, ensures the `.ssh` directory exists with the correct permissions, and appends your public key to the `authorized_keys` file.

---

## 4. Test the Passwordless SSH Login

After copying the key, test your login by connecting to your server:

```bash
ssh remote_username@server_ip_address
```

If everything is set up correctly, you should be able to log in without being prompted for a password.

---

## 4. Configuring Passwordless Login with Sudo Privileges

Before disabling password authentication completely, ensure:
- You can log in with SSH keys.
- The user has proper sudo privileges.

### Disable SSH Password Authentication

1. Log in to your remote server.
2. Open the SSH configuration file:

   ```bash
   sudo nano /etc/ssh/sshd_config
   ```

3. Find and update (or add) the following directives:

   ```ini
   PasswordAuthentication no
   ChallengeResponseAuthentication no
   UsePAM no
   ```

4. Save the file and restart the SSH service:

   - **Ubuntu/Debian:**

     ```bash
     sudo systemctl restart ssh
     ```

   - **CentOS/Fedora:**

     ```bash
     sudo systemctl restart sshd
     ```

---

## 5. Windows 10 OpenSSH Equivalent of `ssh-copy-id`

Windows 10’s built-in OpenSSH client does not include the `ssh-copy-id` command. However, you can achieve the same result using PowerShell.

### 5.1. Generate an SSH Key Pair on Windows

1. Open a new **PowerShell** window (do not use Command Prompt).
2. Generate a new key pair:

   ```powershell
   ssh-keygen
   ```

   - By default, your keys will be stored in `%USERPROFILE%\.ssh\`.
   - The public key will be in `%USERPROFILE%\.ssh\id_rsa.pub`.

### 5.2. Copy the Public Key to the Remote Linux Server

Use the following one-liner in PowerShell to copy your public key:

```powershell
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh remote_username@server_ip_address "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

- Replace `remote_username@server_ip_address` with your actual remote login details.
- You may be prompted to verify the remote host’s authenticity and to enter the remote user’s password.

### 5.3. Test the Passwordless Login

Finally, test your connection by running:

```powershell
ssh remote_username@server_ip_address
```

If the configuration is correct, you will connect to your Linux device without a password.

---

## Conclusion

In this tutorial, authored by **Dev**, you learned how to:

- **Generate and verify an SSH key pair** on your client machine.
- **Copy the public key** to a remote Linux server using both the `ssh-copy-id` command and a manual method.
- **Log in passwordlessly** to your Linux server.
- **Enhance security** by disabling password-based SSH authentication.
- **Set up Windows 10’s OpenSSH client** to mimic the `ssh-copy-id` command using PowerShell.

By following these steps, you can securely manage your remote servers and even automate processes without the hassle of entering a password every time.

Happy coding and secure connecting!

---

*References: Windows 10 OpenSSH guide adapted from Christopher Hart’s blog post (May 23, 2020).*