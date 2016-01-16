import os
import json
from fabric.api import local, task

VAULT_PASSWD_FILE = os.path.join(os.environ['HOME'], '.ansible_vault_passwd')
VERBOSE_LEVEL = int(os.environ.get('ANSIBLE_VERBOSE_LEVEL', 0))

def ansible_playbook(playbook, inventory, tags=None, limit=None, extra_vars=None, var_file=None, require_vault=False):
    command = 'ansible-playbook'
    args = [
        '-i {}'.format(inventory),
    ]

    if VERBOSE_LEVEL:
        args.append('-' + 'v' * VERBOSE_LEVEL)

    if limit:
        args.append('--limit {}'.format(limit))

    if require_vault:
        if os.path.exists(VAULT_PASSWD_FILE):
            args.append('--vault-password-file={}'.format(VAULT_PASSWD_FILE))
        else:
            args.append('--ask-vault-pass')

    if extra_vars:
        args.append("--extra-vars='{}'".format(json.dumps(extra_vars)))

    if var_file:
        args.append("--extra-vars='@{}'".format(var_file))

    if tags:
        args.append('--tags={}'.format(tags))

    command = 'ansible-playbook {args} {playbook}'.format(
            args = ' '.join(args),
            playbook = playbook
    )
    return local(command)

@task
def provision(limit=None, tags=None, **extra_vars):
    '''Provision instances, including installing libraries and softwares and configure them properly

    Args:
        limit: limit provision to specific hosts (comma-separated)
        tags: only execute tasks matching specific tags (comma-separated)
        extra_vars: passed in as extra_vars
    '''
    ansible_playbook('provision.yml', 'inventory/perf.yml',
                        tags=tags, limit=limit, extra_vars=extra_vars)

@task
def aws_setup(tags=None):
    '''Setup infrastructure on AWS including secruity group, ec2 instances etc.

    Args:
        tags: only execute tasks matching specific tags (comma-separated)
    '''
    ansible_playbook('aws_setup.yml', 'localhost,',tags=tags)
