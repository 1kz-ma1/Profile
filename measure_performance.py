#!/usr/bin/env python
"""
Cloudflareパフォーマンス測定スクリプト
キャッシング効果を測定します
"""

import requests
import time
from datetime import datetime


def measure_performance(url, num_requests=5):
    """
    URLのパフォーマンスを測定
    
    Args:
        url (str): 測定対象のURL
        num_requests (int): 測定回数
    """
    
    print(f"\n{'='*60}")
    print(f"Cloudflareパフォーマンス測定")
    print(f"{'='*60}")
    print(f"測定URL: {url}")
    print(f"測定回数: {num_requests}")
    print(f"測定開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    times = []
    cache_statuses = []
    
    for i in range(num_requests):
        try:
            print(f"リクエスト {i+1}/{num_requests}...", end=" ", flush=True)
            
            start_time = time.time()
            response = requests.get(url, timeout=10)
            elapsed_time = (time.time() - start_time) * 1000  # ミリ秒
            
            # Cloudflareヘッダー取得
            cf_cache_status = response.headers.get('CF-Cache-Status', 'N/A')
            cf_ray = response.headers.get('CF-Ray', 'N/A')
            cf_connect_time = response.headers.get('CF-Connection-Time', 'N/A')
            
            times.append(elapsed_time)
            cache_statuses.append(cf_cache_status)
            
            print(f"✅ {elapsed_time:.0f}ms | Cache: {cf_cache_status}")
            print(f"   CF-Ray: {cf_ray}")
            
            # リクエスト間隔（サーバー負荷軽減）
            if i < num_requests - 1:
                time.sleep(1)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ エラー: {str(e)}")
            times.append(None)
            cache_statuses.append('ERROR')
    
    # 結果集計
    print(f"\n{'='*60}")
    print("測定結果")
    print(f"{'='*60}\n")
    
    valid_times = [t for t in times if t is not None]
    
    if valid_times:
        avg_time = sum(valid_times) / len(valid_times)
        min_time = min(valid_times)
        max_time = max(valid_times)
        
        print(f"平均応答時間: {avg_time:.1f} ms")
        print(f"最小応答時間: {min_time:.1f} ms")
        print(f"最大応答時間: {max_time:.1f} ms")
        
        # キャッシュ統計
        cache_hits = sum(1 for status in cache_statuses if status == 'HIT')
        cache_miss = sum(1 for status in cache_statuses if status == 'MISS')
        
        print(f"\nキャッシュ統計:")
        print(f"  HIT: {cache_hits}回")
        print(f"  MISS: {cache_miss}回")
        
        if cache_hits > 0:
            hit_rate = (cache_hits / len([s for s in cache_statuses if s in ['HIT', 'MISS']])) * 100
            print(f"  ヒット率: {hit_rate:.1f}%")
        
        # 改善率推定
        if len(valid_times) >= 2:
            first_request = valid_times[0]
            avg_cached = sum(valid_times[1:]) / len(valid_times[1:])
            improvement = ((first_request - avg_cached) / first_request) * 100
            print(f"\n改善率: {improvement:.1f}%")
            print(f"(1回目: {first_request:.1f}ms → キャッシュ平均: {avg_cached:.1f}ms)")
    
    print(f"\n{'='*60}\n")


def main():
    """メイン処理"""
    
    # 測定対象URL
    urls = [
        "https://1kzma1.pythonanywhere.com/",
        "https://1kzma1.pythonanywhere.com/about",
        "https://1kzma1.pythonanywhere.com/blog",
    ]
    
    print("\n🔍 Cloudflareキャッシング効果測定ツール\n")
    print("このスクリプトは以下のURLのパフォーマンスを測定します:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    input("\nEnterキーを押して測定を開始...")
    
    for url in urls:
        measure_performance(url, num_requests=5)
        time.sleep(2)


if __name__ == "__main__":
    main()
