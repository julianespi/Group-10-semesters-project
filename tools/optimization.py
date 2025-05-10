# Using Dynamic Programming since we are using a small data set
def dp_select(files, time_limit):
    n = len(files)
    dp = [[0] * (time_limit + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        t = files[i-1]['scan_time']
        s = files[i-1]['risk_score']
        for j in range(time_limit + 1):
            if j >= t:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j - t] + s)
            else:
                dp[i][j] = dp[i-1][j]

    # Backtrack to find selected files
    selected = []
    j = time_limit
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i-1][j]:
            selected.append(files[i-1]['name'])
            j -= files[i-1]['scan_time']

    return dp[n][time_limit], selected[::-1]  # Reverse to keep original order


