from dotenv import dotenv_values

env_config = dotenv_values(".env")

print(env_config)

my_api_id = env_config["MY_IP_ID"]
my_api_hash = env_config["MY_IP_HASH"]

# 1st
api_id = env_config["CLIENT_IP_ID"]
api_hash = env_config["CLIENT_IP_HASH"]

# 2nd
api_id2 = env_config["CLIENT_IP_ID2"]
api_hash2 = env_config["CLIENT_IP_HASH2"]

# 3rd
api_id3 = env_config["CLIENT_IP_ID3"]
api_hash3 = env_config["CLIENT_IP_HASH3"]
