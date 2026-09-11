async def generate_promt(message: str, rules: dict):
    return f"""
    <rules>
    {rules}
    </rules>

    <message>
    {message}
    </message>
    """
