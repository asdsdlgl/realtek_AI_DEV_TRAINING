import time
def find_duplicates_fast(numbers):
    seen = set()
    duplicates = set()

    for number in numbers:
        if number in seen:
            duplicates.add(number)
        else:
            seen.add(number)

    return list(duplicates)

def main():
    print("[INFO] generating large list...")
    data = list(range(5000)) + list(range(2000, 7000))  # 製造重複值
    print("[INFO] finding duplicates...")
    start = time.time()
    dups = find_duplicates_fast(data)
    end = time.time()
    print(f"[INFO] found {len(dups)} duplicates")
    print(f"[INFO] time used = {end - start:.4f} sec")

if __name__ == "__main__":
    main()