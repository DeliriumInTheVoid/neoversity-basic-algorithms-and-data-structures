# Testing Results

### Test Data
- **Coin Denominations**: [50, 25, 10, 5, 2, 1]
- **Test Amounts**: 113, 500, 1000, 5000, 10000

### Measurement Results

| Amount | Greedy (s) | Dynamic (s) | Speedup  |
|--------|------------|-------------|----------|
| 113    | 0.00001850 | 0.00009340  | 5.05x    |
| 500    | 0.00000730 | 0.00047090  | 64.51x   |
| 1000   | 0.00000360 | 0.00089630  | 248.97x  |
| 5000   | 0.00000470 | 0.00330710  | 703.64x  |
| 10000  | 0.00000360 | 0.00494930  | 1374.81x |

## Analysis and Conclusions

### 1. Time Complexity (Big O)

#### Greedy Algorithm
- **Time Complexity**: O(n), where _n_ is the number of coin denominations
- **Space Complexity**: O(1) (excluding the result)
- The algorithm iterates through the coin list once, performing division and subtraction for each denomination

#### Dynamic Programming
- **Time Complexity**: O(n × m), where _n_ is the number of denominations, _m_ is the amount
- **Space Complexity**: O(m), where _m_ is the amount
- The algorithm builds a dp table for all values from 0 to the amount, checking all denominations for each value

### 2. Performance with Large Amounts

#### Greedy Algorithm
✅ **Advantages**:
- Extremely fast - execution time is practically independent of the amount size
- Constant space complexity
- For amount 10000, executes in ~0.000004 seconds

❌ **Disadvantages**:
- Does not always give optimal result for arbitrary coin sets
- Works optimally only for "canonical" coin systems

#### Dynamic Programming
✅ **Advantages**:
- Always finds the optimal solution
- Guarantees minimum number of coins

❌ **Disadvantages**:
- Execution time grows linearly with increasing amount
- Requires O(m) additional memory
- For amount 10000, executes in ~0.005 seconds

### 3. Efficiency Comparison

1. **For Small Amounts (< 200)**:
   - Speed difference is negligible (5-10x)
   - Both algorithms work instantly
   - Either approach can be used

2. **For Medium Amounts (200-2000)**:
   - Greedy algorithm is 50-250 times faster
   - Dynamic programming still works acceptably
   - The difference becomes noticeable

3. **For Large Amounts (> 2000)**:
   - Greedy algorithm is 300-1400+ times faster
   - The difference grows linearly with increasing amount
   - Critical advantage of the greedy algorithm

### 4. When to Use Each Algorithm

#### Use Greedy Algorithm when:
- The coin system is canonical (like Ukrainian shah(= 1, 2, 5, 10, 25, 50)
- Maximum speed is required
- Processing large amounts
- Low memory consumption is critical
- **Examples**: ATMs, cash registers, POS terminals

#### Use Dynamic Programming when:
- The coin system is arbitrary (non-canonical)
- Finding optimal solution is critical
- Amounts are relatively small (< 10000)
- Sufficient memory is available
- **Examples**: mathematical problems, optimization tasks, non-standard currency systems

### 5. Special Cases

For the coin set [50, 25, 10, 5, 2, 1]:
- Both algorithms give **the same number of coins** for all test cases
- This is because this coin system is canonical
- Greedy algorithm for canonical systems always finds the optimal solution

**Counter-example** (non-canonical system):
For coins [1, 3, 4] and amount 6:
- Greedy: 4 + 1 + 1 = **3 coins**
- Dynamic: 3 + 3 = **2 coins** ✓ (optimal)

## General Conclusion

1. **Greedy Algorithm** is the better choice for practical applications with canonical coin systems due to:
   - Speed O(n) vs O(n×m)
   - Minimal memory consumption
   - Simplicity of implementation
   - Scalability for large amounts

2. **Dynamic Programming** is indispensable for:
   - Theoretical problems
   - Arbitrary coin systems
   - Cases where optimality is more important than speed

3. **Algorithm Choice** depends on:
   - Type of coin system (canonical or not)
   - Size of amounts
   - Speed and memory requirements
   - Need for guaranteed optimality

For real financial systems (banks, ATMs, stores), the optimal choice is the **greedy algorithm** because:
- National currencies use canonical denomination systems
- High transaction processing speed is required
- Limited computing resources (especially in embedded systems)
- Response time is critical for user experience
