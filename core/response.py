def socket_response(
        is_success: bool,
        data: dict | None = None,
        error: str | None = None
) -> dict:
    dictionary = dict()
    if is_success:
        return {
            "is_success": is_success,
            "data": data
        }
    return {
        "is_success": is_success,
        "error": error
    }
