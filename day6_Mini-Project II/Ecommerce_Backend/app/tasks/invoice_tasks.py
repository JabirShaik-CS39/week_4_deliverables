def generate_invoice(
    order_id: int,
    total: float
):

    filename = f"invoice_{order_id}.txt"

    with open(filename, "w") as f:

        f.write(
            f"""
Order ID: {order_id}
Total: {total}
"""
        )

    print(f"Invoice created: {filename}")