# -*- coding: utf-8 -*-
import os


def env(key, conv=str):
    try:
        result = conv(os.environ[key])
    except Exception as e:
        print(f"{key} not found in env, setting it to 0.")
        result = conv(0)
    return result


token = env("token")
