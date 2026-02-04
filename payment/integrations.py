
import httpx
import asyncio

async def async_payment_gateway(amount):
    # Simulate external payment gateway delay
    await asyncio.sleep(3)

    # Example real HTTP call (fake URL)
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "https://payment-gateway.example/pay",
    #         json={"amount": str(amount)}
    #     )
    #     return response.json()

    return {"status": "success"}
