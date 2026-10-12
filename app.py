from ingestion import ingest_documents
from chunking import chunk_documents
from embeddings import create_embeddings, create_embedding
from vector_store import create_collection, store_chunks
from retrieval import retrieve_relevant_chunks
from context_builder import build_context
from prompts import build_answer_prompt, build_standalone_question_prompt
from llm import generate_answer
from citations import get_source_citations
from memory import add_message, get_conversation_history


def main():

    # 1. Load documents
    documents = ingest_documents("knowledge")

    # 2. Split documents into chunks
    chunks = chunk_documents(
        documents,
        chunk_size=300,
        overlap=50
    )

    # 3. Generate embeddings
    embedded_chunks = create_embeddings(chunks)

    # 4. Create the vector database collection
    collection = create_collection()

    # 5. Store chunks in the collection
    store_chunks(embedded_chunks, collection)

    # 6. Ask multiple questions in one session
    while True:
        question = input(
            "\nAsk a company policy question (or type 'exit'): "
        ).strip()

        if question.lower() == "exit":
            print("Conversation ended.")
            break

        if not question:
            print("Please enter a question.")
            continue

        add_message("user", question)
        # 7. Rewrite the question using conversation history
        try:
            rewrite_prompt = build_standalone_question_prompt(
                question=question,
                conversation_history=get_conversation_history()[:-1]
            )

            standalone_question = generate_answer(rewrite_prompt)

        except Exception as error:
            print("Sorry, question rewriting failed. Please try again.")
            print(f"Technical details: {error}")
            continue

        print("Search question:", standalone_question)

        # 8. Create embedding from the rewritten question
        question_embedding = create_embedding(standalone_question)

        # 9. Retrieve relevant chunks
        try:
            relevant_chunks = retrieve_relevant_chunks(
                collection=collection,
                question=standalone_question,
                question_embedding=question_embedding,
                metadata_filter=None,
                n_results=5,
                distance_threshold=1.0
            )

        except Exception as error:
            print("Sorry, retrieval failed. Please try again later.")
            print(f"Technical details: {error}")
            continue

        # 10. Build context
        context = build_context(relevant_chunks)

        # 11. Generate an answer
        if not relevant_chunks:
            answer = (
                "I don't have enough relevant information "
                "in the available documents to answer this question."
            )

            print("\nGenerated Answer:")
            print(answer)
            print("\nSources: None")

        else:
            prompt = build_answer_prompt(
                context=context,
                question=question,
                conversation_history=get_conversation_history()
            )

            try:
                answer = generate_answer(prompt)

            except Exception as error:
                print(
                    "Sorry, answer generation failed. "
                    "Please try again later."
                )
                print(f"Technical details: {error}")
                continue

            # Display source citations
            sources = get_source_citations(relevant_chunks)

            print("\nGenerated Answer:")
            print(answer)

            if sources:
                print("\nSources:")
                for source in sources:
                    print(f"- {source}")
            else:
                print("\nSources: None")

        # 11. Save the assistant's answer
        add_message("assistant", answer)

        # 12. Display retrieval diagnostics
        print("\nQuestion:", question)
        print("Relevant chunks found:", len(relevant_chunks))

        for index, chunk in enumerate(relevant_chunks, start=1):
            print(f"\nResult {index}:")
            print("Text:", chunk["text"])
            print("Metadata:", chunk["metadata"])
            print("Distance:", chunk["distance"])


if __name__ == "__main__":
    main()