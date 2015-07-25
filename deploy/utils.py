import subprocess


def local(cmd, shell=None):
    p = subprocess.Popen(
        cmd,
        stdout=None,
        stderr=subprocess.STDOUT,
        shell=True,
        executable=shell,
    )
    out, err = p.communicate()


def prompt(text, default=''):
    if default == '':
        prompt_text = text
    else:
        prompt_text = '{} [{}]'.format(text.strip(), default)

    value = None
    while value is None:
        value = input(prompt_text) or default

    return value


def confirm(question, default=True):
    if default:
        choices = "Y/n"
    else:
        choices = "y/N"

    while True:
        response = prompt("{} [{}] ".format(question, choices))

        if not response:
            return default

        if response.lower() in ['y', 'yes']:
            return True

        if response.lower() in ['n', 'no']:
            return False

        print("Выберите вариант: y(es) или (n)o")
