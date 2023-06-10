from pyngrok import ngrok


def init_tunnel(PORT):
    ssh_tunnel = ngrok.connect(f'{PORT}', "http", bind_tls=True)
