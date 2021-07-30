import subprocess


def get_codecs():
    cmd = "ffmpeg -codecs"
    x = subprocess.check_output(cmd, shell=True)
    x = x.split(b'\n')
    for e in x:
        print(e)


def get_formats():
    cmd = "ffmpeg -formats"
    x = subprocess.check_output(cmd, shell=True)
    x = x.split(b'\n')
    for e in x:
        print(e)


def conv_seq_to_mov():

    input = r".%04d.png"
    output = r""
    frame_rate = 25

    cmd = f'ffmpeg -framerate {frame_rate} -i "{input}" "{output}"'
    print (cmd)
    subprocess.check_output(cmd, shell=true)


def conv_mov_to_seq():
    input = r""
    output = r""

    cmd = f'ffmpeg -i "{input}" "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=true)