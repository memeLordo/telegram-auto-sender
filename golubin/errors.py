from loguru import logger


def form_error_list(error_list, err_sec):
    logger.warning(f"Flood wait for {err_sec}")
    with open("./golubin/error.txt", "w+") as f:
        for i, value in enumerate(error_list, start=1):
            username, message = value
            f.write(f"{i}: {username}\n")
            f.write(message + "\n")
        logger.success("Error file formed")
