import random
import time

# ----------------- Merge Sort -----------------
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively apply merge sort on both halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Merge the two sorted halves
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# ----------------- Radix Sort -----------------
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Count occurrences of each digit in the current place value
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    # Update count[i] so that it contains the actual position in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # Copy the output array to arr[]
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr:
        return arr
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

# ----------------- Main -----------------
if __name__ == "__main__":
    num_elements = int(input("Enter the number of elements to generate: "))
    arr = [random.randint(1, 1000) for _ in range(num_elements)]
    print(f"\nGenerated array:\n{arr}")

    # Merge Sort
    merge_input = arr.copy()
    print("\nRunning Merge Sort...")
    start = time.time()
    merge_sort(merge_input)
    end = time.time()
    print(f"Sorted with Merge Sort:\n{merge_input}")
    print(f"Execution time: {end - start:.6f} seconds")

    # Radix Sort
    radix_input = arr.copy()
    print("\nRunning Radix Sort...")
    start = time.time()
    radix_sort(radix_input)
    end = time.time()
    print(f"Sorted with Radix Sort:\n{radix_input}")
    print(f"Execution time: {end - start:.6f} seconds")

