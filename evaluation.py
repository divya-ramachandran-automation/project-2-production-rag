def evaluate_retrieval(retrieved_chunks, expected_source):

    retrieved_sources = [
        chunk["metadata"].get("source")
        for chunk in retrieved_chunks
    ]

    return expected_source in retrieved_sources

def evaluate_answer(answer, expected_keywords):
    answer_lower = answer.lower()
    for keyword in expected_keywords:
        if keyword.lower() not in answer_lower:
            return False
    return True

def evaluate_faithfulness(answer, context, required_facts):
    answer_lower = answer.lower()
    context_lower = context.lower()
    for fact in required_facts:
        fact_lower = fact.lower()
        if fact_lower in answer_lower and fact_lower not in context_lower:
            return False
    return True

if __name__ == "__main__":

    sample_chunks = [
        {
            "text": "Employees can carry forward up to 10 unused vacation days.",
            "metadata": {
                "source": "leave_policy.txt"
            }
        }
    ]

    sample_answer = (
        "Employees can carry forward up to 10 unused vacation days."
    )

    sample_context = sample_chunks[0]["text"]

    print(
        "Retrieval test:",
        evaluate_retrieval(
            sample_chunks,
            "leave_policy.txt"
        )
    )

    print(
        "Answer quality test:",
        evaluate_answer(
            sample_answer,
            ["10", "vacation days"]
        )
    )

    print(
        "Faithfulness test:",
        evaluate_faithfulness(
            sample_answer,
            sample_context,
            ["10 vacation days"]
        )
    )

def evaluate_rag_case(
    retrieved_chunks,
    expected_source,
    answer,
    expected_keywords,
    context,
    required_facts
):
    retrieval_passed = evaluate_retrieval(
        retrieved_chunks,
        expected_source
    )

    answer_passed = evaluate_answer(
        answer,
        expected_keywords
    )

    faithfulness_passed = evaluate_faithfulness(
        answer,
        context,
        required_facts
    )

    return {
        "retrieval": retrieval_passed,
        "answer_quality": answer_passed,
        "faithfulness": faithfulness_passed,
        "overall": (
            retrieval_passed
            and answer_passed
            and faithfulness_passed
        )
    }

result = evaluate_rag_case(
    retrieved_chunks=sample_chunks,
    expected_source="leave_policy.txt",
    answer=sample_answer,
    expected_keywords=["10", "vacation days"],
    context=sample_context,
    required_facts=["10 vacation days"]
)

print("\nCombined Evaluation:")
print(result)