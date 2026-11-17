def inr(amount: float) -> str:
    """Indian number format: 186499 -> ₹1,86,499"""
    sign = "-" if amount < 0 else ""
    s = str(int(round(abs(amount))))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return f"{sign}₹{s}"
