"""
慢程式範例：效能極差的 O(n^2) 版本

* 用來讓 AI 做效能最佳化的示範

重點：
- 程式可以跑很久，學員會「感受到痛點」
- 可以用 AI 做 profiling、重寫
"""

import time

def find_duplicates_slow(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j and numbers[i] == numbers[j]:
                if numbers[i] not in duplicates:
                    duplicates.append(numbers[i])
    return duplicates

def main():
    print("[INFO] generating large list...")
    data = list(range(5000)) + list(range(2000, 7000))  # 製造重複值

    print("[INFO] finding duplicates...")
    start = time.time()
    dups = find_duplicates_slow(data)
    end = time.time()

    print(f"[INFO] found {len(dups)} duplicates")
    print(f"[INFO] time used = {end - start:.4f} sec")

if __name__ == "__main__":
    main()