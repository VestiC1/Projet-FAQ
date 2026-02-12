def get_faq(sb):
    result = sb.table("documents").select("content").execute()
    return [row["content"] for row in result.data]


def get_document(sb, id):
    result = (
        sb.table("documents")
        .select("content")
        .eq("content->>id", id)
        .maybe_single()
        .execute()
    )
    return result.data["content"] if result.data else None