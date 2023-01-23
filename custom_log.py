def log(tag="",message=""):
    with open("log.txt","a") as f:
        f.write(f"{tag}:{message}\n")