from subprocess import check_output


def make_conf(config, filename, username):
    with open(config, 'r') as f:
        template = f.read()
    config = template.replace('FIRMWARE_PATH', f'../firmwares/{filename}')
    with open(f'configs/{username}.cfg', 'w') as f:
        f.write(config)
    return f'configs/{username}.cfg'


def flasher(conf):
    return check_output(['openocd', '-f', f'{conf}'], shell=False)
