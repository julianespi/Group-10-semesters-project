from datetime import datetime

def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Compare using the key function
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def counting_sort(arr):
    if not arr:
        return arr

     # Group by year
    year_buckets = {}
    for item in arr:
        year = item["year"]
        if year not in year_buckets:
            year_buckets[year] = []
        year_buckets[year].append(item)

    # Sort years in ascending order
    sorted_arr = []
    for year in sorted(year_buckets.keys()):
        # Sort each bucket by full date (datetime object)
        sorted_group = sorted(year_buckets[year], key=lambda x: x['date'] or datetime.min)
        sorted_arr.extend(sorted_group)

    return sorted_arr
