# Ansible Host Provisioning

### Ansible Setup

This is simply used to create a user on the host that ansible can use.
```bash
ansible-playbook ansible-setup.yaml --user=root
```

### Invoicer

This is used to provision docker, nginx, sqlite, and the users used for these components.
```bash
ansible-playbook invoicer.yaml --user=ansible
```

