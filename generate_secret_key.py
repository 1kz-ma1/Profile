#!/usr/bin/env python
"""
Django SECRET_KEY 生成スクリプト

実行: python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("Generated SECRET_KEY:")
    print(secret_key)
    print("\nこの値を .env.railway の SECRET_KEY に設定してください")
