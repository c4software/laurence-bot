commands = {}

def register_as_command(command_name, description):
    def wrap(f):
        commands[command_name] = f
        def wrapped_f(*args):
            f(*args)
        return wrapped_f
    return wrap
